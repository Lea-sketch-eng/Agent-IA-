"""Applique les migrations SQL de db/migrations/ sur la base DATABASE_URL.

Chaque fichier *.sql est appliqué une seule fois, dans l'ordre alphabétique,
dans sa propre transaction. Les migrations déjà appliquées sont enregistrées
dans la table schema_migrations. Un verrou consultatif empêche deux
déploiements simultanés d'appliquer les mêmes migrations.

Usage : DATABASE_URL=postgresql://... python scripts/migrate.py
"""
import os
import sys
from pathlib import Path

import psycopg

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "db" / "migrations"
LOCK_ID = 727274  # identifiant arbitraire du verrou consultatif


def pending_migrations(conn, directory):
    applied = {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}
    return [path for path in sorted(directory.glob("*.sql")) if path.name not in applied]


def migrate(database_url, directory=MIGRATIONS_DIR):
    """Applique les migrations en attente et retourne la liste des fichiers appliqués."""
    applied = []
    with psycopg.connect(database_url, autocommit=True) as conn:
        conn.execute("SELECT pg_advisory_lock(%s)", (LOCK_ID,))
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                " version text PRIMARY KEY,"
                " applied_at timestamptz NOT NULL DEFAULT now())"
            )
            for path in pending_migrations(conn, directory):
                with conn.transaction():
                    conn.execute(path.read_text(encoding="utf-8"))
                    conn.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s)", (path.name,)
                    )
                applied.append(path.name)
                print(f"✅ {path.name}")
        finally:
            conn.execute("SELECT pg_advisory_unlock(%s)", (LOCK_ID,))
    return applied


def main():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ Variable DATABASE_URL absente")
        sys.exit(1)
    applied = migrate(database_url)
    print(f"Migrations appliquées : {len(applied)}" if applied else "Base déjà à jour")


if __name__ == "__main__":
    main()
