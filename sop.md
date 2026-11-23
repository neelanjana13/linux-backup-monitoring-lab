# SOP: Backup and Restore

## Configuration
| Item | Value |
|---|---|
| Source | ~/backup-lab/source |
| Destination | ~/backup-lab/backups |
| Method | tar + gzip (full backup) |
| Schedule | Daily at 02:00 (cron: `0 2 * * *`) |
| Retention | Backups older than 7 days are deleted |
| Log file | ~/backup-lab/logs/backup.log |
| Log format | timestamp / status / detail / size |

## Daily monitoring
1. Run `python3 ~/backup-lab/scripts/backup_report.py`.
2. Confirm each day shows SUCCESS and no FAILED entries.
3. If there is a FAILED entry, follow runbook.md.

## Full restore
1. Pick the backup: `LATEST=$(ls -t ~/backup-lab/backups/*.tar.gz | head -1)`
2. List its contents: `tar -tzf "$LATEST"`
3. Extract to a separate location: `tar -xzf "$LATEST" -C ~/backup-lab/restore_test`
4. Verify: `diff -r ~/backup-lab/source ~/backup-lab/restore_test`

## Single-file restore
1. Confirm the file is in the backup: `tar -tzf "$LATEST" | grep filename`
2. Extract only that file: `tar -xzf "$LATEST" -C ~/backup-lab/source ./filename`

## Validation
- Run a restore test after any change to the backup configuration.
- Run a restore test at least once a week.
