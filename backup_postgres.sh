#!/bin/bash
set -e

BACKUP_DIR="./backups/postgres"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILE="$BACKUP_DIR/postgres_$DATE.sql"

mkdir -p "$BACKUP_DIR"

docker exec postgres-db pg_dump -U postgres Test_base_python > "$FILE"

echo "Backup created: $FILE"

find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
echo "Old backups cleaned"