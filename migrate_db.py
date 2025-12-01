#!/usr/bin/env python3
"""
Database migration script to add extra usage columns
Run this with: python migrate_db.py
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.database import db
from app import app

def add_extra_usage_columns():
    """Add the extra usage columns to subscribed_users table"""

    with app.app_context():
        try:
            # Check if columns exist
            result = db.engine.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'subscribed_users'
                AND column_name IN ('extra_analytics', 'extra_qr_codes', 'extra_scans')
            """)

            existing_columns = [row[0] for row in result.fetchall()]

            if len(existing_columns) == 3:
                print("✅ All extra usage columns already exist!")
                return True

            print(f"Found {len(existing_columns)} existing columns: {existing_columns}")
            print("Adding missing columns...")

            # Add columns one by one
            if 'extra_analytics' not in existing_columns:
                db.engine.execute("ALTER TABLE subscribed_users ADD COLUMN extra_analytics INTEGER DEFAULT 0")
                print("✅ Added extra_analytics column")

            if 'extra_qr_codes' not in existing_columns:
                db.engine.execute("ALTER TABLE subscribed_users ADD COLUMN extra_qr_codes INTEGER DEFAULT 0")
                print("✅ Added extra_qr_codes column")

            if 'extra_scans' not in existing_columns:
                db.engine.execute("ALTER TABLE subscribed_users ADD COLUMN extra_scans INTEGER DEFAULT 0")
                print("✅ Added extra_scans column")

            # Update existing NULL values to 0
            db.engine.execute("UPDATE subscribed_users SET extra_analytics = 0 WHERE extra_analytics IS NULL")
            db.engine.execute("UPDATE subscribed_users SET extra_qr_codes = 0 WHERE extra_qr_codes IS NULL")
            db.engine.execute("UPDATE subscribed_users SET extra_scans = 0 WHERE extra_scans IS NULL")

            print("✅ Updated NULL values to 0")

            # Verify the migration
            result = db.engine.execute("""
                SELECT column_name, data_type, column_default
                FROM information_schema.columns
                WHERE table_name = 'subscribed_users'
                AND column_name LIKE 'extra_%'
                ORDER BY column_name
            """)

            print("\n📊 Extra usage columns created:")
            for row in result.fetchall():
                print(f"   • {row[0]}: {row[1]} (default: {row[2]})")

            print("\n🎉 Migration completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    success = add_extra_usage_columns()

    if success:
        print("\n✅ Migration successful! You can now restart your Flask application.")
    else:
        print("\n❌ Migration failed! Please check the errors above.")
        sys.exit(1)