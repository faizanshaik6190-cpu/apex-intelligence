#!/bin/bash

# Apex Intelligence - Backup script

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_FILE="apex_intelligence.db"
PG_CONTAINER="apex_intelligence-postgres-1"

mkdir -p $BACKUP_DIR

echo "📦 Backing up Apex Intelligence..."

# Backup SQLite database if using SQLite
if [ -f $DB_FILE ]; then
    cp $DB_FILE $BACKUP_DIR/apex_intelligence_$TIMESTAMP.db
    echo "✅ SQLite backup: $BACKUP_DIR/apex_intelligence_$TIMESTAMP.db"
fi

# Backup PostgreSQL if using Docker Compose
if docker ps | grep -q $PG_CONTAINER; then
    docker exec $PG_CONTAINER pg_dump -U apex_user apex_intelligence > $BACKUP_DIR/apex_intelligence_pg_$TIMESTAMP.sql
    echo "✅ PostgreSQL backup: $BACKUP_DIR/apex_intelligence_pg_$TIMESTAMP.sql"
fi

echo "✅ Backup complete"
