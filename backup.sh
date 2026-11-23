#!/bin/bash
SOURCE="$HOME/backup-lab/source"
DEST="$HOME/backup-lab/backups"
LOG="$HOME/backup-lab/logs/backup.log"
TS=$(date +%Y-%m-%d_%H-%M-%S)
FILE="$DEST/backup_$TS.tar.gz"

if tar -czf "$FILE" -C "$SOURCE" . 2>/dev/null; then
    SIZE=$(du -h "$FILE" | cut -f1)
    echo "$(date '+%Y-%m-%d %H:%M:%S') | SUCCESS | $FILE | $SIZE" >> "$LOG"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') | FAILED | $FILE | tar error" >> "$LOG"
fi

# Retention: delete backups older than 7 days
DELETED=$(find "$DEST" -name "backup_*.tar.gz" -mtime +7 -print -delete | wc -l)
echo "$(date '+%Y-%m-%d %H:%M:%S') | RETENTION | removed $DELETED old backup(s) | -" >> "$LOG"
