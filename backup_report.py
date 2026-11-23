import pandas as pd
from pathlib import Path

LOG = Path.home() / "backup-lab/logs/backup.log"
OUT = Path.home() / "backup-lab/logs/daily_report.csv"

rows = []
for line in LOG.read_text().splitlines():
    p = [x.strip() for x in line.split("|")]
    if len(p) >= 3:
        rows.append({"timestamp": p[0], "status": p[1], "detail": p[2]})

df = pd.DataFrame(rows)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

jobs = df[df["status"].isin(["SUCCESS", "FAILED"])]
summary = jobs.groupby(["date", "status"]).size().unstack(fill_value=0)
for col in ["SUCCESS", "FAILED"]:
    if col not in summary.columns:
        summary[col] = 0
summary = summary[["SUCCESS", "FAILED"]]
summary["TOTAL"] = summary["SUCCESS"] + summary["FAILED"]
summary["SUCCESS_RATE_%"] = (summary["SUCCESS"] / summary["TOTAL"] * 100).round(1)

summary.to_csv(OUT)
print("=== Daily Backup Report ===")
print(summary.to_string())

failed = jobs[jobs["status"] == "FAILED"]
if not failed.empty:
    print("\nALERT: failed backup jobs")
    print(failed[["timestamp", "detail"]].to_string(index=False))
else:
    print("\nNo failed jobs.")
