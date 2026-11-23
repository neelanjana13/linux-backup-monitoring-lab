# Linux Backup Monitoring & Restore Lab

A small lab that simulates a server backup process: scheduled backups, a retention policy, failure simulation, restore testing, and automated reporting from backup logs.

## Tools
Ubuntu (WSL2), Bash, cron, tar, Python (pandas), Excel

## Features
- Automated daily backup with timestamped, compressed archives (cron, 02:00)
- Retention policy: backups older than 7 days are removed automatically
- Every job writes a SUCCESS or FAILED line to a log
- Python script parses the log and produces a daily success/failure report (CSV) with an alert for failed jobs
- Tested a full restore, verified against the source with `diff`
- Tested a single-file restore of a deleted file
- Simulated a failed backup, investigated it, fixed it, and documented it in a runbook

## Project structure
    scripts/backup.sh          Backup and retention script
    scripts/backup_report.py   Log parser and daily report
    logs/backup.log            Sample log output
    logs/daily_report.csv      Sample daily report
    logs/backup_report_chart.xlsx   Excel chart of success vs failed jobs
    docs/runbook.md            Troubleshooting a failed backup
    docs/sop.md                Backup and restore procedures
    screenshots/               Evidence of each step

## How to run
1. Create the folders and add some sample files in `source/`.
2. Make the script executable: `chmod +x scripts/backup.sh`
3. Run a backup: `./scripts/backup.sh`
4. Schedule it with cron: `0 2 * * * /path/to/scripts/backup.sh`
5. Generate the report: `python3 scripts/backup_report.py`

## Sample result
On the test day, 12 backup jobs ran: 11 succeeded and 1 failed (a deliberate failure with the source folder renamed), giving a 91.7% success rate. The report flagged the failed job, and the runbook steps were used to recover.

## Concepts covered
Full backups, retention policies, restore validation, failure troubleshooting, log monitoring, backup reporting, documentation (SOP and runbook), escalation.

## Limitations and future improvements
- Full backups only. Incremental or differential backups would save space.
- Runs on WSL, where cron only works while Ubuntu is open. A real server runs cron continuously.
- Backups are stored on the same machine. A real setup keeps an offsite or cloud copy.
- The log records only "tar error" for failures. Capturing tar's actual error message would speed up diagnosis.
- Email alerts on failure could be added.
