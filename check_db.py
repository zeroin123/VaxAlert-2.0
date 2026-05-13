import sqlite3
db = r"C:\Users\PC\Desktop\Habtech Hackaton\VaxAlert\data\vaxalert.db"
con = sqlite3.connect(db)
cur = con.cursor()

print("=== model_metrics: models x folds ===")
cur.execute("""
    SELECT model, fold, COUNT(*) as n, ROUND(AVG(mae),3) as avg_mae,
           ROUND(AVG(stockout_detection_rate),3) as avg_sdr
    FROM model_metrics
    GROUP BY model, fold
    ORDER BY model, fold
""")
for r in cur.fetchall():
    print(f"  {r[0]:25s}  fold={r[1]:6s}  n={r[2]:4d}  mae={r[3]}  sdr={r[4]}")

print()
print("=== forecast_output: models ===")
cur.execute("SELECT model, COUNT(*) FROM forecast_output GROUP BY model")
for r in cur.fetchall():
    print(f"  {r[0]:15s}  {r[1]} rows")

con.close()
