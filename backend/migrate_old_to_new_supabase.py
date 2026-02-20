"""
Migrate all data from OLD Supabase → NEW Supabase.
This copies all tables that exist in the old DB into the new one.

Run: python3 migrate_old_to_new_supabase.py
"""
import os
import sys

# ── Connection URLs ──────────────────────────────────────────────────────────
# Old Supabase — password was classbridge@2026 (@ encoded as %40 in URL)
OLD_URL_DECODED = "postgresql://postgres.btvojpsmuhkyukhacaxn:classbridge@2026@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
# psycopg2 DSN keywords avoid URL-parsing ambiguity with @ in the password
OLD_DSN = {
    "host": "aws-1-ap-south-1.pooler.supabase.com",
    "port": 6543,
    "dbname": "postgres",
    "user": "postgres.btvojpsmuhkyukhacaxn",
    "password": "classbridge@2026",
    "sslmode": "require",
    "connect_timeout": 15,
}

NEW_URL = "postgresql://postgres.mejirxyrvugqwplevzws:classbridge2026nexus@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require"


try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, execute_values
except ImportError:
    print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)

def connect(url_or_dsn, label):
    try:
        if isinstance(url_or_dsn, dict):
            conn = psycopg2.connect(**url_or_dsn)
        else:
            conn = psycopg2.connect(url_or_dsn, connect_timeout=15)
        conn.autocommit = False
        print(f"✅ Connected to {label}")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to {label}: {e}")
        sys.exit(1)

print("=" * 60)
print("ClassBridge: Old Supabase → New Supabase Migration")
print("=" * 60)

old_conn = connect(OLD_DSN, "OLD Supabase (ap-south-1)")
new_conn = connect(NEW_URL, "NEW Supabase (ap-northeast-1)")

old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
new_cur = new_conn.cursor(cursor_factory=RealDictCursor)

# ── Get all tables from OLD DB ───────────────────────────────────────────────
old_cur.execute("""
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public'
    ORDER BY tablename
""")
tables = [row['tablename'] for row in old_cur.fetchall()]
print(f"\n📋 Found {len(tables)} tables in OLD Supabase:")
for t in tables:
    print(f"   - {t}")

# ── Get all tables in NEW DB ─────────────────────────────────────────────────
new_cur.execute("""
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public'
    ORDER BY tablename
""")
new_tables = [row['tablename'] for row in new_cur.fetchall()]
print(f"\n📋 Found {len(new_tables)} tables in NEW Supabase:")
for t in new_tables:
    print(f"   - {t}")

if not new_tables:
    print("\n⚠️  NEW database has NO tables. The backend needs to run first to create the schema.")
    print("   Will now copy the DDL (table structure) from old DB and then copy data.\n")

# ── Copy table structures (DDL) if new DB is empty ───────────────────────────
# We use the backend's own init to create tables — but since we can't run the backend,
# let's get CREATE TABLE statements from old DB via information_schema

def get_column_defs(cur, table):
    cur.execute("""
        SELECT column_name, data_type, character_maximum_length,
               is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
    """, (table,))
    return cur.fetchall()

def pg_col_def(col):
    dtype = col['data_type']
    if dtype == 'character varying':
        length = col['character_maximum_length']
        dtype_str = f"VARCHAR({length})" if length else "TEXT"
    elif dtype == 'integer':
        dtype_str = "INTEGER"
    elif dtype == 'bigint':
        dtype_str = "BIGINT"
    elif dtype == 'boolean':
        dtype_str = "BOOLEAN"
    elif dtype == 'double precision':
        dtype_str = "DOUBLE PRECISION"
    elif dtype == 'real':
        dtype_str = "REAL"
    elif dtype == 'text':
        dtype_str = "TEXT"
    elif dtype == 'timestamp without time zone':
        dtype_str = "TIMESTAMP"
    elif dtype == 'timestamp with time zone':
        dtype_str = "TIMESTAMPTZ"
    elif dtype == 'date':
        dtype_str = "DATE"
    elif dtype == 'numeric':
        dtype_str = "NUMERIC"
    elif dtype == 'jsonb':
        dtype_str = "JSONB"
    elif dtype == 'json':
        dtype_str = "JSON"
    else:
        dtype_str = dtype.upper()

    nullable = "" if col['is_nullable'] == 'YES' else " NOT NULL"
    default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
    return f'"{col["column_name"]}" {dtype_str}{nullable}{default}'

migrated = 0
skipped = 0
errors = 0

for table in tables:
    print(f"\n{'─'*50}")
    print(f"📤 Migrating table: {table}")

    try:
        # Create table in new DB if it doesn't exist
        cols = get_column_defs(old_cur, table)
        if not cols:
            print(f"   ⚠️  No columns found, skipping.")
            skipped += 1
            continue

        col_defs = ", ".join(pg_col_def(c) for c in cols)
        create_sql = f'CREATE TABLE IF NOT EXISTS "{table}" ({col_defs});'

        try:
            new_cur.execute(create_sql)
            new_conn.commit()
            print(f"   ✅ Table created/verified in NEW DB")
        except Exception as e:
            new_conn.rollback()
            print(f"   ⚠️  Table create warning (may already exist): {e}")

        # Count rows in old DB
        old_cur.execute(f'SELECT COUNT(*) as cnt FROM "{table}"')
        count = old_cur.fetchone()['cnt']
        print(f"   📊 Rows in OLD DB: {count}")

        if count == 0:
            print(f"   ⏭️  Empty table, skipping data copy.")
            skipped += 1
            continue

        # Get column names
        col_names = [c['column_name'] for c in cols]
        col_names_quoted = ', '.join(f'"{c}"' for c in col_names)

        # Fetch all rows from old DB
        old_cur.execute(f'SELECT {col_names_quoted} FROM "{table}"')
        rows = old_cur.fetchall()

        # Convert RealDictRow to plain tuples
        row_tuples = [tuple(row[c] for c in col_names) for row in rows]

        # Insert into new DB
        placeholders = ', '.join(['%s'] * len(col_names))
        insert_sql = f'INSERT INTO "{table}" ({col_names_quoted}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'

        new_cur.executemany(insert_sql, row_tuples)
        new_conn.commit()
        print(f"   ✅ Copied {len(row_tuples)} rows")
        migrated += 1

    except Exception as e:
        new_conn.rollback()
        print(f"   ❌ Error migrating {table}: {e}")
        errors += 1

print(f"\n{'='*60}")
print(f"✅ Migration Complete!")
print(f"   Tables migrated: {migrated}")
print(f"   Tables skipped:  {skipped}")
print(f"   Errors:          {errors}")
print(f"{'='*60}")

# Verify
new_cur.execute("SELECT COUNT(*) as cnt FROM students")
final_count = new_cur.fetchone()['cnt']
print(f"\n🔍 Final check — Users in NEW Supabase: {final_count}")

old_conn.close()
new_conn.close()
