"""
Quick diagnostic: Check which users exist in Supabase and their email_verified status.
Run: python check_supabase_users.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or "postgres" not in DATABASE_URL:
    print("❌ DATABASE_URL not set or not a Postgres URL. Check your .env file.")
    exit(1)

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor

    print(f"Connecting to: {DATABASE_URL.split('@')[-1]}")
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    print("\n✅ Connected to Supabase!\n")

    # Check total user count
    cursor.execute("SELECT COUNT(*) as total FROM students")
    total = cursor.fetchone()
    print(f"📊 Total users in Supabase: {total['total']}")

    # Show all users with their key details
    cursor.execute("""
        SELECT id, name, role, email_verified, school_id
        FROM students
        ORDER BY role, id
        LIMIT 50
    """)
    users = cursor.fetchall()

    if not users:
        print("\n❌ NO USERS FOUND IN SUPABASE — Database needs to be seeded!")
        print("   → You need to run the migration script or create users manually.")
    else:
        print(f"\n{'ID':<40} {'Name':<25} {'Role':<20} {'Verified':<10}")
        print("-" * 100)
        for u in users:
            verified = "✅" if u['email_verified'] else "❌"
            print(f"{str(u['id']):<40} {str(u['name']):<25} {str(u['role']):<20} {verified}")

    # Check specifically for the teacher user
    cursor.execute("SELECT id, name, role, email_verified FROM students WHERE LOWER(id) = 'teacher'")
    teacher = cursor.fetchone()
    print(f"\n🔍 Teacher user (id='teacher'): {dict(teacher) if teacher else 'NOT FOUND'}")

    # Check for teachernoblenexus@gmail.com
    cursor.execute("SELECT id, name, role, email_verified FROM students WHERE LOWER(id) = LOWER('teachernoblenexus@gmail.com')")
    teacher_email = cursor.fetchone()
    print(f"🔍 Teacher email user: {dict(teacher_email) if teacher_email else 'NOT FOUND'}")

    # Check admin
    cursor.execute("SELECT id, name, role, email_verified FROM students WHERE id IN ('admin', 'rootadmin')")
    admins = cursor.fetchall()
    print(f"🔍 Admin users: {[dict(a) for a in admins] if admins else 'NOT FOUND'}")

    conn.close()

except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nPossible fixes:")
    print("  1. Check DATABASE_URL in .env uses Transaction Pooler (port 6543)")
    print("  2. Ensure Supabase project is active (not paused)")
    print("  3. URL-encode special chars in password (@ → %40)")
