-- Migration script to add extra usage columns to subscribed_users table
-- Run this script to add the new columns for extra usage tracking

-- Add extra usage columns to subscribed_users table
ALTER TABLE subscribed_users
ADD COLUMN extra_analytics INTEGER DEFAULT 0,
ADD COLUMN extra_qr_codes INTEGER DEFAULT 0,
ADD COLUMN extra_scans INTEGER DEFAULT 0;

-- Update any existing NULL values to 0 for consistency
UPDATE subscribed_users
SET extra_analytics = 0
WHERE extra_analytics IS NULL;

UPDATE subscribed_users
SET extra_qr_codes = 0
WHERE extra_qr_codes IS NULL;

UPDATE subscribed_users
SET extra_scans = 0
WHERE extra_scans IS NULL;

-- Optional: Add comments to the columns for documentation
COMMENT ON COLUMN subscribed_users.extra_analytics IS 'Extra analytics operations granted by admin';
COMMENT ON COLUMN subscribed_users.extra_qr_codes IS 'Extra QR code generation allowance granted by admin';
COMMENT ON COLUMN subscribed_users.extra_scans IS 'Extra scan allowance granted by admin';

-- Show the updated table structure
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'subscribed_users'
ORDER BY ordinal_position;