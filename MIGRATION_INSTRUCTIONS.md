# Database Migration Instructions

The error you're seeing is because the new columns don't exist in your database yet. You need to run the migration first.

## Option 1: Manual Database Migration (Recommended)

Connect to your PostgreSQL database and run these SQL commands:

```sql
-- Add the new columns
ALTER TABLE subscribed_users ADD COLUMN extra_analytics INTEGER DEFAULT 0;
ALTER TABLE subscribed_users ADD COLUMN extra_qr_codes INTEGER DEFAULT 0;
ALTER TABLE subscribed_users ADD COLUMN extra_scans INTEGER DEFAULT 0;

-- Update any existing NULL values to 0
UPDATE subscribed_users SET extra_analytics = 0 WHERE extra_analytics IS NULL;
UPDATE subscribed_users SET extra_qr_codes = 0 WHERE extra_qr_codes IS NULL;
UPDATE subscribed_users SET extra_scans = 0 WHERE extra_scans IS NULL;

-- Verify the columns were added
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'subscribed_users'
AND column_name LIKE 'extra_%'
ORDER BY column_name;
```

## Option 2: Using psql Command Line

If you have psql installed, you can run:

```bash
psql "your-database-connection-string" -f add_extra_usage_columns.sql
```

## Option 3: Using Database Admin Tool

1. Open your database admin tool (pgAdmin, DBeaver, etc.)
2. Connect to your database
3. Execute the SQL commands from Option 1

## Verification

After running the migration, you should see output like:

```
 column_name   | data_type | column_default
---------------+-----------+----------------
 extra_analytics | integer   | 0
 extra_qr_codes  | integer   | 0
 extra_scans     | integer   | 0
```

## What These Columns Do

- `extra_analytics`: Stores additional analytics operations granted by admin
- `extra_qr_codes`: Stores additional QR code generation allowance granted by admin
- `extra_scans`: Stores additional scan allowance granted by admin

## After Migration

Once you've successfully added the columns:

1. Restart your Flask application
2. The error should be resolved
3. You can test the admin "Add Extra Usage" functionality

## Example Usage Flow

1. User has 10/100 analytics used
2. Admin grants 50 extra analytics
3. Database sets `extra_analytics = 50`
4. User now sees 10/150 analytics (100 base + 50 extra)
5. User has 140 analytics remaining to use

The system now shows increased limits instead of confusing reduced usage counts!