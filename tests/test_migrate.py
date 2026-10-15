import os
import uuid

import psycopg
import pytest
from migrate import migrate

DATABASE_URL = os.environ.get("DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DATABASE_URL non définie")


@pytest.fixture
def schema_url():
    """Isole chaque test dans un schéma Postgres temporaire."""
    schema = f"test_{uuid.uuid4().hex[:8]}"
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute(f"CREATE SCHEMA {schema}")
    sep = "&" if "?" in DATABASE_URL else "?"
    yield f"{DATABASE_URL}{sep}options=-csearch_path%3D{schema}"
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute(f"DROP SCHEMA {schema} CASCADE")


def write(directory, name, sql):
    (directory / name).write_text(sql, encoding="utf-8")


def test_applies_migrations_in_order_then_is_idempotent(schema_url, tmp_path):
    write(tmp_path, "0002_add.sql", "ALTER TABLE t ADD COLUMN b int;")
    write(tmp_path, "0001_create.sql", "CREATE TABLE t (a int);")

    assert migrate(schema_url, tmp_path) == ["0001_create.sql", "0002_add.sql"]
    assert migrate(schema_url, tmp_path) == []


def test_failed_migration_is_rolled_back_and_not_recorded(schema_url, tmp_path):
    write(tmp_path, "0001_ok.sql", "CREATE TABLE t (a int);")
    write(tmp_path, "0002_broken.sql", "CREATE TABLE u (a int); SELECT * FROM missing;")

    with pytest.raises(psycopg.errors.UndefinedTable):
        migrate(schema_url, tmp_path)

    with psycopg.connect(schema_url) as conn:
        versions = [r[0] for r in conn.execute("SELECT version FROM schema_migrations")]
        u_exists = conn.execute("SELECT to_regclass('u')").fetchone()[0]
    assert versions == ["0001_ok.sql"]
    assert u_exists is None


def test_real_migrations_apply_cleanly(schema_url):
    migrate(schema_url)
    with psycopg.connect(schema_url) as conn:
        assert conn.execute("SELECT to_regclass('app_settings')").fetchone()[0] is not None
