#!/bin/bash
set -e

BACKUP_DIR="./backups/mongo"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILE="$BACKUP_DIR/mongo_$DATE.archive.gz"

mkdir -p "$BACKUP_DIR"

docker exec mongo-db mongodump --db shop_db --archive --gzip > "$FILE"

echo "Backup created: $FILE ($(du -h "$FILE" | cut -f1))"

find "$BACKUP_DIR" -name "*.archive.gz" -mtime +7 -delete
echo "Old backups cleaned"