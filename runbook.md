# Runbook: Backup Job Failure

## Purpose
Steps to follow when the daily backup job logs a FAILED status.

## 1. Detect
- Run the report: `python3 ~/backup-lab/scripts/backup_report.py`
- Or check the log: `tail -20 ~/backup-lab/logs/backup.log`
- A line containing `FAILED` means the job did not complete.

## 2. Investigate (check in this order)
1. Source path exists: `ls ~/backup-lab/source`
2. Disk space is available: `df -h` (Use% for `/` should not be near 100%)
3. Permissions allow reading the source and writing to backups: `ls -ld ~/backup-lab/source ~/backup-lab/backups`
4. Run tar by hand to see the real error message:
   `tar -czf /tmp/test.tar.gz -C ~/backup-lab/source .`
5. Check for a leftover tiny or empty archive from the failed run: `ls -lh ~/backup-lab/backups`

## 3. Fix
- Restore the missing source path, free disk space, or correct permissions.
- Delete any empty or partial archive left by the failed run.

## 4. Re-run and verify
- `~/backup-lab/scripts/backup.sh`
- `tail -3 ~/backup-lab/logs/backup.log` and confirm SUCCESS.
- Test the new backup with a restore (see SOP).

## 5. Escalate if unresolved
Escalate to the infrastructure/storage team with:
- The FAILED log lines
- Output of `df -h`
- What was checked and the result of each check

## 6. Record
Log the incident: date and time, cause, fix applied, and time to resolve.

## Incident log (example)
| Date | Time | Cause | Fix | Resolved |
|---|---|---|---|---|
| 2026-11-23 | 21:06 | Source folder missing (simulated) | Restored folder, re-ran job | Yes, 21:08 |
