#!/usr/bin/env python3
"""
PostgreSQL Database Migration Script: Add User-Specific Limit Columns to subscribed_users table
Uses Flask app configuration for PostgreSQL database connection
"""

import sys
import os
from datetime import datetime, UTC
from sqlalchemy import create_engine, text, MetaData, inspect
from sqlalchemy.exc import OperationalError, IntegrityError, ProgrammingError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app_config():
    """Create Flask app configuration (same as your create_app function)"""
    config = {}

    # Configure the app using environment variables (same as your Flask app)
    
    config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY', 'generate-random-24-bytes-key-change-this')
    config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')
    config['FLASK_DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    config['FLASK_HOST'] = os.getenv('FLASK_HOST', '0.0.0.0')
    config['FLASK_PORT'] = int(os.getenv('FLASK_PORT', 5050))

    # PostgreSQL Database Configuration
    config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:Devi%401234@localhost:5432/qr')
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'

    # Upload folder configuration (from your create_app)
    upload_folder = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    config['UPLOAD_FOLDER'] = upload_folder

    # Create upload directories (from your create_app)
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'logos'), exist_ok=True)

    return config

def get_database_url():
    """Get PostgreSQL database URL using the same method as your Flask app"""
    # Use Flask app configuration method
    config = create_app_config()
    database_url = config['SQLALCHEMY_DATABASE_URI']

    if database_url:
        # Mask password for logging
        masked_url = database_url.replace('Devi%401234', '***')
        logger.info(f"Using PostgreSQL database URL from Flask config: {masked_url}")
        return database_url

    # Fallback to individual environment variables if SQLALCHEMY_DATABASE_URI is not set
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')  # PostgreSQL default port
    db_name = os.getenv('DB_NAME', 'qr')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'Devi@1234')

    # Construct PostgreSQL URL
    fallback_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    masked_fallback = fallback_url.replace(db_password, '***')
    logger.info(f"Using fallback PostgreSQL database URL: {masked_fallback}")
    return fallback_url

def check_table_exists(engine, table_name):
    """Check if a table exists in PostgreSQL"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return table_name in tables
    except Exception as e:
        logger.error(f"Error checking if table {table_name} exists: {e}")
        return False

def check_column_exists(engine, table_name, column_name):
    """Check if a column exists in a PostgreSQL table"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT COUNT(*) as count
                FROM information_schema.columns
                WHERE table_name = :table_name
                AND column_name = :column_name
                AND table_catalog = current_database()
            """), {'table_name': table_name, 'column_name': column_name})
            count = result.fetchone()[0]
            return count > 0
    except Exception as e:
        logger.error(f"Error checking column {column_name}: {e}")
        return False

def add_user_limit_columns():
    """Add user-specific limit columns to subscribed_users table"""
    try:
        # Get database connection using Flask app configuration
        database_url = get_database_url()

        # PostgreSQL engine configuration
        engine = create_engine(
            database_url,
            echo=False,  # Set to True for debugging
            pool_pre_ping=True,
            pool_recycle=300
        )

        logger.info("🚀 Starting PostgreSQL database migration...")
        logger.info("Connecting to PostgreSQL database...")

        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"✅ PostgreSQL connection successful: {version[:50]}...")

        # Check if subscribed_users table exists
        if not check_table_exists(engine, 'subscribed_users'):
            logger.error("❌ subscribed_users table does not exist!")
            logger.info("Available tables:")
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            for table in tables[:10]:  # Show first 10 tables
                logger.info(f"   - {table}")
            return False
        logger.info("✅ subscribed_users table found")

        # Define the columns to add (PostgreSQL syntax)
        columns_to_add = [
            {
                'name': 'user_analytics_limit',
                'definition': 'user_analytics_limit INTEGER DEFAULT NULL',
                'comment': 'User-specific analytics limit override'
            },
            {
                'name': 'user_qr_limit',
                'definition': 'user_qr_limit INTEGER DEFAULT NULL',
                'comment': 'User-specific QR code limit override'
            },
            {
                'name': 'user_scan_limit',
                'definition': 'user_scan_limit INTEGER DEFAULT NULL',
                'comment': 'User-specific scan limit override'
            }
        ]

        # Add each column if it doesn't exist
        with engine.connect() as connection:
            for column_info in columns_to_add:
                column_name = column_info['name']
                column_definition = column_info['definition']
                column_comment = column_info['comment']

                if check_column_exists(engine, 'subscribed_users', column_name):
                    logger.info(f"⚠️  Column {column_name} already exists, skipping...")
                    continue

                try:
                    # Add the column (PostgreSQL syntax)
                    alter_sql = f"ALTER TABLE subscribed_users ADD COLUMN {column_definition}"
                    logger.info(f"➕ Adding column: {column_name}")
                    logger.info(f"   SQL: {alter_sql}")

                    connection.execute(text(alter_sql))

                    # Add comment to column (PostgreSQL syntax)
                    comment_sql = f"COMMENT ON COLUMN subscribed_users.{column_name} IS '{column_comment}'"
                    connection.execute(text(comment_sql))

                    connection.commit()
                    logger.info(f"✅ Successfully added column: {column_name}")

                except Exception as e:
                    logger.error(f"❌ Error adding column {column_name}: {e}")
                    connection.rollback()
                    return False

        # Verify all columns were added
        logger.info("\n=== VERIFICATION ===")
        all_added = True
        for column_info in columns_to_add:
            column_name = column_info['name']
            if check_column_exists(engine, 'subscribed_users', column_name):
                logger.info(f"✅ Confirmed: {column_name} exists")
            else:
                logger.error(f"❌ Failed: {column_name} missing")
                all_added = False

        if all_added:
            logger.info("\n🎉 SUCCESS: All user limit columns added successfully!")
            # Show current table structure for the new columns (PostgreSQL)
            logger.info("\n=== NEW COLUMNS ADDED ===")
            with engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT
                        column_name,
                        data_type,
                        is_nullable,
                        column_default,
                        col_description(pgc.oid, ordinal_position) as column_comment
                    FROM information_schema.columns isc
                    LEFT JOIN pg_class pgc ON pgc.relname = isc.table_name
                    WHERE table_name = 'subscribed_users'
                    AND column_name IN ('user_analytics_limit', 'user_qr_limit', 'user_scan_limit')
                    ORDER BY column_name
                """))

                columns = result.fetchall()
                for i, col in enumerate(columns, 1):
                    logger.info(f"{i}. {col[0]:20} | {col[1]:15} | {'NULL' if col[2] == 'YES' else 'NOT NULL':8} | Default: {col[3] or 'NULL'}")

            # Show sample data
            logger.info("\n=== SAMPLE DATA ===")
            with engine.connect() as connection:
                try:
                    result = connection.execute(text("""
                        SELECT id, "U_ID", "S_ID", user_analytics_limit, user_qr_limit, user_scan_limit
                        FROM subscribed_users
                        LIMIT 3
                    """))
                    rows = result.fetchall()
                    if rows:
                        logger.info("ID | U_ID | S_ID | Analytics | QR | Scan")
                        logger.info("-" * 40)
                        for row in rows:
                            logger.info(f"{row[0]:2} | {row[1]:4} | {row[2]:4} | {row[3] or 'NULL':9} | {row[4] or 'NULL':2} | {row[5] or 'NULL':4}")
                    else:
                        logger.info("No existing records found (this is normal for new installations)")
                except Exception as e:
                    logger.info(f"Sample data query failed (this is normal): {e}")

            return True
        else:
            logger.error("\n❌ FAILED: Some columns were not added properly")
            return False
    except Exception as e:
        logger.error(f"❌ Migration failed with error: {e}")
        import traceback
        logger.error(f"Full error trace:\n{traceback.format_exc()}")
        return False

def rollback_migration():
    """Remove the added columns (rollback)"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url, echo=False, pool_pre_ping=True)

        columns_to_remove = ['user_analytics_limit', 'user_qr_limit', 'user_scan_limit']

        logger.info("🔄 Starting rollback migration...")

        with engine.connect() as connection:
            for column_name in columns_to_remove:
                if check_column_exists(engine, 'subscribed_users', column_name):
                    try:
                        # PostgreSQL DROP COLUMN syntax
                        alter_sql = f"ALTER TABLE subscribed_users DROP COLUMN {column_name}"
                        logger.info(f"🗑️  Removing column: {column_name}")
                        connection.execute(text(alter_sql))
                        connection.commit()
                        logger.info(f"✅ Removed column: {column_name}")
                    except Exception as e:
                        logger.error(f"❌ Error removing column {column_name}: {e}")
                        return False
                else:
                    logger.info(f"ℹ️  Column {column_name} doesn't exist, skipping...")

        logger.info("🔄 Rollback completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Rollback failed: {e}")
        return False

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("PostgreSQL Migration: Add User-Specific Limit Columns")
    logger.info("=" * 60)

    if len(sys.argv) > 1 and sys.argv[1] == '--rollback':
        logger.info("🔄 Starting rollback migration...")
        success = rollback_migration()
    else:
        logger.info("🚀 Starting forward migration...")
        logger.info("Adding user-specific limit columns to subscribed_users table:")
        logger.info("  • user_analytics_limit (INTEGER, DEFAULT NULL)")
        logger.info("  • user_qr_limit (INTEGER, DEFAULT NULL)")
        logger.info("  • user_scan_limit (INTEGER, DEFAULT NULL)")
        logger.info("")
        success = add_user_limit_columns()

    if success:
        logger.info("\n" + "=" * 60)
        logger.info("✅ POSTGRESQL MIGRATION COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info("The subscribed_users table now has the new user-specific limit columns.")
        logger.info("Your SubscribedUser model will work perfectly with these new columns.")
        sys.exit(0)
    else:
        logger.error("\n" + "=" * 60)
        logger.error("❌ POSTGRESQL MIGRATION FAILED!")
        logger.error("=" * 60)
        logger.error("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

