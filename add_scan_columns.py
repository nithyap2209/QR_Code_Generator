# add_scan_columns.py
import psycopg2
from app import app
import os

def get_db_connection():
    """Get PostgreSQL connection from Flask config"""
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    
    # Parse the DATABASE_URL
    # Format: postgresql://username:password@host:port/database
    if db_url.startswith('postgresql://'):
        return psycopg2.connect(db_url)
    else:
        # If using environment variables, construct manually
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'your_db_name'),
            user=os.getenv('DB_USER', 'your_username'),
            password=os.getenv('DB_PASSWORD', 'your_password'),
            port=os.getenv('DB_PORT', '5432')
        )

def add_scan_columns():
    """Add scan tracking columns to PostgreSQL database"""
    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("Connected to PostgreSQL database")
        
        # Add scan_limit column to subscriptions table
        try:
            cursor.execute('''
                ALTER TABLE subscriptions 
                ADD COLUMN scan_limit INTEGER DEFAULT 0
            ''')
            print("✓ Added scan_limit column to subscriptions table")
        except psycopg2.errors.DuplicateColumn:
            print("ℹ scan_limit column already exists in subscriptions table")
            conn.rollback()
        
        # Add scans_used column to subscribed_users table
        try:
            cursor.execute('''
                ALTER TABLE subscribed_users 
                ADD COLUMN scans_used INTEGER DEFAULT 0
            ''')
            print("✓ Added scans_used column to subscribed_users table")
        except psycopg2.errors.DuplicateColumn:
            print("ℹ scans_used column already exists in subscribed_users table")
            conn.rollback()
        
        # Commit changes
        conn.commit()
        
        # Verify columns were added
        cursor.execute("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'subscriptions' AND column_name = 'scan_limit'
        """)
        result = cursor.fetchone()
        if result:
            print(f"✓ Verified scan_limit column: {result}")
        
        cursor.execute("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'subscribed_users' AND column_name = 'scans_used'
        """)
        result = cursor.fetchone()
        if result:
            print(f"✓ Verified scans_used column: {result}")
        
        cursor.close()
        conn.close()
        
        print("✅ Manual migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Manual migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    with app.app_context():
        add_scan_columns()