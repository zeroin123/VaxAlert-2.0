import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def render_prophet_decomposition_panel(
    facility_id: str,
    antigen: str,
    facility_name: str,
    comp_df: pd.DataFrame,
):
    """Prophet component decomposition for Facility Drill-Down.

    Replaces the XGBoost feature importance panel.  Prophet carries 60% of
    the ensemble weight; showing its components is the honest explanation of
    what actually drives every alert.
    """
    if comp_df.empty:
        fac_comp = pd.DataFrame()
    else:
        _mask = (comp_df["facility_id"] == facility_id) & (comp_df["antigen"] == antigen)
        # Show only the 8-week forecast window in the per-facility panel
        if "is_forecast" in comp_df.columns:
            _mask = _mask & (comp_df["is_forecast"] == 1)
        fac_comp = comp_df[_mask].sort_values("forecast_week").reset_index(drop=True)

    if fac_comp.empty:
        st.info(
            "Prophet component analysis not yet available for this facility. "
            "Run `python forecast/generate_forecasts.py` to populate."
        )
        return

    st.subheader("🔍 Forecast Driver Analysis")
    st.markdown(
        f"This chart breaks the **Prophet forecast** for **{facility_name}** ({antigen}) into its three "
        "driving forces: the long-term **Trend**, the repeating **Seasonal cycle**, and any "
        "active **Event effects** (campaigns, conflicts, pandemic). "
        "Prophet carries **60% of the ensemble weight** — this is what's actually driving your alerts."
    )

    # Summary narrative — biggest driver over the 8-week window
    trend_avg  = fac_comp["trend"].mean()
    season_avg = fac_comp["seasonal"].mean()
    events_avg = fac_comp["events"].mean()

    drivers = {"Trend": abs(trend_avg), "Seasonality": abs(season_avg), "Events": abs(events_avg)}
    primary = max(drivers, key=drivers.get)

    trend_dir  = "rising ↑" if trend_avg > 1 else ("falling ↓" if trend_avg < -1 else "flat →")
    season_dir = "boosting demand ↑" if season_avg > 1 else ("suppressing demand ↓" if season_avg < -1 else "neutral")
    event_txt  = f"{events_avg:+.1f} doses/week from active events" if abs(events_avg) > 0.5 else "no active event effects"

    st.success(
        f"**Primary driver: {primary}.** "
        f"Trend is {trend_dir} ({trend_avg:+.1f} doses/wk) | "
        f"Season is {season_dir} ({season_avg:+.1f} doses/wk) | "
        f"Events: {event_txt}."
    )

    weeks = [f"Wk {i + 1}" for i in range(len(fac_comp))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Trend", x=weeks, y=fac_comp["trend"].values,
        marker_color="#1B4F72",
        hovertemplate="<b>Trend</b>: %{y:.1f} doses<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Seasonality", x=weeks, y=fac_comp["seasonal"].values,
        marker_color="#27AE60",
        hovertemplate="<b>Seasonality</b>: %{y:.1f} doses<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Events", x=weeks, y=fac_comp["events"].values,
        marker_color="#E74C3C",
        hovertemplate="<b>Events</b>: %{y:.1f} doses<extra></extra>",
    ))
    fig.update_layout(
        barmode="relative",   # stacked; negatives go downward
        height=300,
        margin=dict(l=20, r=20, t=20, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_title="Contribution (doses)",
        xaxis_title=None,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#1a202c"),
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 What do these components mean?"):
        st.markdown("""
| Component | What it means |
|---|---|
| **Trend** | The long-run direction of stock levels — population growth, policy changes, or facility expansion pushing demand up or down over months |
| **Seasonality** | Recurring annual patterns — Ethiopia's birth peaks, Kiremt rainy season delivery delays, post-SIA consumption rebounds |
| **Events** | Named disruptions — COVID pandemic, Tigray/Amhara conflict periods, measles SIA campaigns — captured as named events in the Prophet model |
        """)


def render_component_tier_heatmap(comp_df: pd.DataFrame):
    """Prophet component × access tier heatmap for the Model Performance tab.

    Replaces the XGBoost feature importance heatmap. Shows mean absolute
    contribution of Trend / Seasonality / Events per access tier across all
    non-ZI facilities.
    """
    st.markdown("#### 🔬 Forecast Driver Breakdown by Access Tier")
    n_weeks = len(comp_df) // max(comp_df["facility_id"].nunique() * comp_df["antigen"].nunique(), 1) if not comp_df.empty else 0
    st.caption(
        f"Each column shows the **share of the total forecast signal** coming from Trend, Seasonality, and Events "
        f"for that access tier — normalized to 100% so tiers with very different dose volumes are directly comparable. "
        f"Averaged over {n_weeks} weeks (7 years of history + 8-week forecast)."
    )

    if comp_df.empty or "access_tier" not in comp_df.columns:
        st.info(
            "Prophet component data not yet available. "
            "Run `python forecast/generate_forecasts.py` to populate."
        )
        return

    TIER_ORDER  = ["urban", "rural_road", "rural_remote", "pastoral"]
    TIER_LABELS = {
        "urban": "Urban",
        "rural_road": "Rural Road",
        "rural_remote": "Rural Remote",
        "pastoral": "Pastoral",
    }

    # Mean absolute contribution per component per tier, then normalize each
    # tier column to 100% so tiers with very different volumes are comparable.
    agg = (
        comp_df.groupby("access_tier")[["trend", "seasonal", "events"]]
        .apply(lambda g: g.abs().mean())
        .reindex(TIER_ORDER)
        .fillna(0)
    )
    col_sums = agg.sum(axis=1).replace(0, 1)          # avoid div-by-zero
    agg_pct = (agg.div(col_sums, axis=0) * 100).round(1)

    z = agg_pct.values.T          # shape (3, 4): rows=components, cols=tiers
    x = [TIER_LABELS.get(t, t) for t in TIER_ORDER]
    y = ["Trend", "Seasonality", "Events"]

    fig = go.Figure(go.Heatmap(
        z=z, x=x, y=y,
        colorscale="Viridis",
        zmin=0, zmax=100,
        text=[[f"{v:.1f}%" for v in row] for row in z],
        texttemplate="%{text}",
        colorbar=dict(title="Share of<br>total signal (%)", thickness=14),
        hovertemplate="<b>%{y}</b> in <b>%{x}</b>: %{z:.1f}% of total signal<extra></extra>",
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=80, r=20, t=10, b=40),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#1a202c", size=12),
        xaxis=dict(side="bottom"),
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📖 Reading this chart"):
        st.markdown("""
Each column sums to **100%**. A higher cell means that component explains a larger *share* of what Prophet is reacting to in that tier — regardless of how many doses those facilities handle in absolute terms.

| Component | What it captures |
|---|---|
| **Trend** | Long-run drift — population growth, policy, facility expansion |
| **Seasonality** | Annual cycle — Ethiopian birth peaks, Kiremt rainy-season delays |
| **Events** | Named disruptions — COVID, Tigray/Amhara conflict, measles SIA campaigns |

> **Example:** If pastoral shows Events = 55%, it means disruptions dominate the Prophet signal there — more so than in urban facilities — even though urban facilities handle 20× more doses.
        """)
