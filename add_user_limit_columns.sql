-- Migration script to add user-specific limit columns to SubscribedUser table
-- This allows individual users to have custom limits without affecting the subscription plan.
--
-- Execute this script in your PostgreSQL database

BEGIN;

-- Add user-specific limit columns to subscribed_users table
-- NULL values mean the user uses the subscription plan default

-- Add analytics limit override column
ALTER TABLE subscribed_users
ADD COLUMN IF NOT EXISTS user_analytics_limit INTEGER;

-- Add QR code limit override column
ALTER TABLE subscribed_users
ADD COLUMN IF NOT EXISTS user_qr_limit INTEGER;

-- Add scan limit override column
ALTER TABLE subscribed_users
ADD COLUMN IF NOT EXISTS user_scan_limit INTEGER;

-- Add comments to document the purpose of these columns
COMMENT ON COLUMN subscribed_users.user_analytics_limit IS 'User-specific analytics limit override. NULL means use subscription plan default.';
COMMENT ON COLUMN subscribed_users.user_qr_limit IS 'User-specific QR code limit override. NULL means use subscription plan default.';
COMMENT ON COLUMN subscribed_users.user_scan_limit IS 'User-specific scan limit override. NULL means use subscription plan default.';

COMMIT;

-- Verify the columns were added
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'subscribed_users'
AND column_name IN ('user_analytics_limit', 'user_qr_limit', 'user_scan_limit')
ORDER BY column_name;