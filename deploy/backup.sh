#!/usr/bin/env bash
set -euo pipefail
umask 077
# Run as a dedicated backup account. Set PGSERVICE/PGPASSFILE securely.
: "${BACKUP_DIR:?Set an absolute backup directory}"
: "${PGDATABASE:?Set the database name}"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$BACKUP_DIR/$stamp"
pg_dump --format=custom --file="$BACKUP_DIR/$stamp/database.dump" "$PGDATABASE"
tar -czf "$BACKUP_DIR/$stamp/uploads.tar.gz" -C /srv/manarat uploads
sha256sum "$BACKUP_DIR/$stamp/database.dump" "$BACKUP_DIR/$stamp/uploads.tar.gz" > "$BACKUP_DIR/$stamp/SHA256SUMS"
echo "Backup completed: $stamp"
