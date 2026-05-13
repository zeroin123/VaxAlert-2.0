"""
Global stacking meta-learner — dual-path constrained weighted blend.

Instead of a black-box XGBoost meta-model, we learn explicit linear weights
via SLSQP constrained optimisation on the pooled OOF (out-of-fold) rows:

  Non-zero-inflated series (≤60% zero weeks):
    All 5 base models blend with floors: naive_last_value ≥ 20%, holt_winters ≥ 20%.
    Remaining weight is freely allocated to whichever models reduce MSE.

  Zero-inflated series (>60% zero weeks):
    Only the 3 simple models blend: naive_last_value, naive_seasonal, holt_winters.
    XGBoost and Prophet receive hard-zero weight (they produce meaningless smooth
    curves on near-zero data).

Conformal prediction intervals remain per-tier calibrated (same as before).
Weights are learned once from OOF data during CV and saved to disk.
A JSON sidecar is written so the dashboard can display the named weights.
"""

import json
import logging
import os

import joblib
import numpy as np
import pandas as pd
from scipy.optimize import minimize

logger = logging.getLogger(__name__)

META_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".cache", "meta_model.pkl"
)
os.makedirs(os.path.dirname(META_MODEL_PATH), exist_ok=True)

BASE_MODELS = ["naive_last_value", "naive_seasonal", "holt_winters", "xgboost", "prophet"]
TIER_ENCODE = {"urban": 0, "rural_road": 1, "rural_remote": 2, "pastoral": 3}

# Higher percentile for tiers with more volatile / zero-inflated residuals
TIER_PERCENTILES = {0: 80, 1: 83, 2: 87, 3: 93}  # urban → pastoral

# ── Weight optimisation constants ────────────────────────────────────────────

# Non-ZI: all 5 models, floors on naive+HW
_BOUNDS_NORMAL = [
    (0.20, 1.0),  # naive_last_value  ≥ 20%
    (0.00, 1.0),  # naive_seasonal    unconstrained
    (0.20, 1.0),  # holt_winters      ≥ 20%
    (0.00, 1.0),  # xgboost           unconstrained
    (0.00, 1.0),  # prophet           unconstrained
]
_INIT_NORMAL = np.array([0.25, 0.05, 0.25, 0.25, 0.20])

# ZI: only first 3 models (xgb + prophet get hard 0 after optimisation)
_BOUNDS_ZI = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]  # [nv_last, nv_seasonal, hw]
_INIT_ZI   = np.array([0.40, 0.10, 0.50])

_SUM1 = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
_BASE_COLS = [f"pred_{m}" for m in BASE_MODELS]


def build_meta_features(
    base_predictions: dict,        # {model_name: array of h predictions}
    current_stock: float,
    weekly_consumption: float,
    access_tier: str,
    horizon_steps: list,           # e.g. [1,2,...,h]
    zero_inf: bool = False,        # True for zero-inflated series
) -> pd.DataFrame:
    """Build a feature matrix where each row is one (series, week) pair."""
    h = len(horizon_steps)
    rows = []
    for i in range(h):
        row = {f"pred_{m}": float(base_predictions.get(m, [0]*h)[i]) for m in BASE_MODELS}
        row["current_stock"]      = float(current_stock)
        row["weekly_consumption"] = float(weekly_consumption or 1.0)
        row["tier"]               = float(TIER_ENCODE.get(access_tier, 1))
        row["horizon"]            = int(horizon_steps[i])
        row["zero_inf"]           = float(zero_inf)   # 0.0 or 1.0
        # Diversity statistics (kept for compatibility; not used in the linear blend)
        preds_arr = np.array([row[f"pred_{m}"] for m in BASE_MODELS])
        row["pred_mean"] = float(preds_arr.mean())
        row["pred_std"]  = float(preds_arr.std())
        row["pred_min"]  = float(preds_arr.min())
        row["pred_max"]  = float(preds_arr.max())
        rows.append(row)
    return pd.DataFrame(rows)


class StackingEnsemble:
    """Dual-path constrained weighted blend (replaces the XGBoost meta-learner)."""

    def __init__(self):
        self._weights_normal = None   # np.ndarray (5,) — non-ZI series
        self._weights_zi     = None   # np.ndarray (5,) — ZI series (xgb=prophet=0)
        self._conformal_widths = None # {tier_int: float}

    # ── Persistence ──────────────────────────────────────────────────────────

    @classmethod
    def load(cls) -> "StackingEnsemble":
        if not os.path.exists(META_MODEL_PATH):
            return None
        try:
            obj = joblib.load(META_MODEL_PATH)
            inst = cls()
            inst._weights_normal   = obj["weights_normal"]
            inst._weights_zi       = obj["weights_zi"]
            inst._conformal_widths = obj.get("conformal_widths",
                                             {t: 5.0 for t in TIER_PERCENTILES})
            return inst
        except Exception as e:
            logger.warning("Failed to load meta-model: %s", e)
            return None

    def save(self):
        joblib.dump({
            "weights_normal":   self._weights_normal,
            "weights_zi":       self._weights_zi,
            "conformal_widths": self._conformal_widths,
        }, META_MODEL_PATH)

        # Human-readable JSON sidecar for the dashboard
        json_path = META_MODEL_PATH.replace(".pkl", "_weights.json")
        with open(json_path, "w") as f:
            json.dump({
                "normal": {
                    m: round(float(w), 6)
                    for m, w in zip(BASE_MODELS, self._weights_normal)
                },
                "zero_inflated": {
                    m: round(float(w), 6)
                    for m, w in zip(BASE_MODELS, self._weights_zi)
                },
            }, f, indent=2)

    # ── Training ─────────────────────────────────────────────────────────────

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> "StackingEnsemble":
        """
        X: pooled OOF meta-features (must include 'zero_inf' column).
        y: actual closing-stock targets, same row order as X.
        """
        n = len(X)
        split = int(n * 0.85)
        X_tr, X_val = X.iloc[:split].copy(), X.iloc[split:].copy()
        y_tr = y[:split]
        y_val = y[split:]

        zi_tr  = X_tr["zero_inf"].astype(bool).values
        zi_val = X_val["zero_inf"].astype(bool).values

        # ── Non-ZI weights (5 models, floors on naive+HW) ────────────────
        Xn_tr  = X_tr[_BASE_COLS].values[~zi_tr]
        yn_tr  = y_tr[~zi_tr]
        Xn_val = X_val[_BASE_COLS].values[~zi_val]
        yn_val = y_val[~zi_val]

        def mse_n(w):
            return float(np.mean((Xn_tr @ w - yn_tr) ** 2))

        res_n = minimize(
            mse_n, _INIT_NORMAL.copy(), method="SLSQP",
            bounds=_BOUNDS_NORMAL, constraints=_SUM1,
            options={"ftol": 1e-10, "maxiter": 2000},
        )
        self._weights_normal = res_n.x / res_n.x.sum()

        # ── ZI weights (3 simple models, xgb+prophet = 0) ────────────────
        Xzi_tr = X_tr[_BASE_COLS[:3]].values[zi_tr]   # [nv_last, nv_sn, hw]
        yzi_tr = y_tr[zi_tr]

        if len(Xzi_tr) >= 10:
            def mse_zi(w):
                return float(np.mean((Xzi_tr @ w - yzi_tr) ** 2))
            res_zi = minimize(
                mse_zi, _INIT_ZI.copy(), method="SLSQP",
                bounds=_BOUNDS_ZI, constraints=_SUM1,
                options={"ftol": 1e-10, "maxiter": 2000},
            )
            w3 = res_zi.x / res_zi.x.sum()
        else:
            logger.warning("Too few ZI OOF rows (%d) — using fallback 40/10/50 split", len(Xzi_tr))
            w3 = _INIT_ZI / _INIT_ZI.sum()

        # Pad to 5: xgboost=0, prophet=0
        self._weights_zi = np.array([w3[0], w3[1], w3[2], 0.0, 0.0])

        # ── Per-tier conformal widths (on non-ZI validation rows) ────────
        val_pred  = Xn_val @ self._weights_normal
        residuals = np.abs(yn_val - val_pred)
        tier_vals = X_val["tier"].astype(int).values[~zi_val]

        self._conformal_widths = {}
        for tier_int, pct in TIER_PERCENTILES.items():
            mask = tier_vals == tier_int
            tier_resid = residuals[mask]
            self._conformal_widths[tier_int] = (
                float(np.percentile(tier_resid, pct))
                if len(tier_resid) > 5
                else float(np.percentile(residuals, pct))
            )

        return self

    # ── Inference ────────────────────────────────────────────────────────────

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if self._weights_normal is None:
            return np.zeros(len(X))
        is_zi = bool(X["zero_inf"].iloc[0]) if "zero_inf" in X.columns else False
        w = self._weights_zi if is_zi else self._weights_normal
        return np.maximum(0, X[_BASE_COLS].values @ w)

    def predict_interval(self, X: pd.DataFrame) -> pd.DataFrame:
        yhat     = self.predict(X)
        tier_int = int(X["tier"].iloc[0]) if "tier" in X.columns else 1
        widths   = self._conformal_widths or {t: 5.0 for t in TIER_PERCENTILES}
        w        = widths.get(tier_int, widths.get(1, 5.0))
        lower    = np.maximum(0, yhat - w)
        upper    = yhat + w
        return pd.DataFrame({"yhat": yhat, "yhat_lower": lower, "yhat_upper": upper})

    # ── Interpretability ─────────────────────────────────────────────────────

    def feature_importance(self) -> pd.Series:
        """Return normal-series weights as a named Series (for CV print + feature panel)."""
        if self._weights_normal is None:
            return pd.Series(dtype=float)
        return pd.Series(self._weights_normal, index=BASE_MODELS).sort_values(ascending=False)
