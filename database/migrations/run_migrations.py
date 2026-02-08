"""
Database migration runner for Phase III AI Chatbot integration.

This script runs SQL migration files in order to set up the database schema.
It can be used as an alternative to SQLModel's create_all for explicit migration control.

Usage:
    python run_migrations.py
    python run_migrations.py --migration 003
"""

import os
import sys
from pathlib import Path
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    return database_url

def run_migration(cursor, migration_file: Path):
    """Run a single migration file."""
    print(f"Running migration: {migration_file.name}")
    with open(migration_file, 'r') as f:
        sql = f.read()
    cursor.execute(sql)
    print(f"✓ Migration {migration_file.name} completed successfully")

def main():
    """Run all pending migrations."""
    # Get migrations directory
    migrations_dir = Path(__file__).parent

    # Get all SQL migration files in order
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        print("No migration files found")
        return

    # Connect to database
    database_url = get_database_url()

    try:
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cursor:
                # Run each migration
                for migration_file in migration_files:
                    run_migration(cursor, migration_file)

                # Commit all migrations
                conn.commit()
                print(f"\n✓ All {len(migration_files)} migrations completed successfully")

    except Exception as e:
        print(f"\n✗ Migration failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
