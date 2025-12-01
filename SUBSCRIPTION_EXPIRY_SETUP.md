# Subscription Expiry Notification Setup

## Overview
This system automatically sends email notifications to users 24 hours before their subscription expires.

## Files Updated

### 1. **models/subscription.py**
- **Changes:**
  - Removed local `mail = Mail()` initialization (line 38)
  - Updated `send_subscription_expiry_notification()` to import mail from app
  - Added `from flask import url_for, request` import for URL generation

### 2. **app.py**
- **Changes:**
  - Added scheduler initialization after mail and login_manager setup (lines 260-267)
  - Scheduler initializes automatically when the app starts

### 3. **scheduler.py** (NEW FILE)
- **Purpose:** Background scheduler for automated tasks
- **Functionality:**
  - Runs `process_expiry_notifications()` daily at 9:00 AM
  - Uses APScheduler with BackgroundScheduler
  - Runs within Flask app context
  - Includes error handling and logging

### 4. **requirements.txt**
- **Changes:**
  - Added `APScheduler==3.10.4` dependency

## Installation Steps

1. **Install the new dependency:**
   ```bash
   pip install APScheduler==3.10.4
   ```

   Or install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify email configuration in .env file:**
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

3. **Restart your Flask application:**
   ```bash
   python app.py
   ```

   You should see:
   ```
   ✓ Scheduler initialized - Subscription expiry notifications will run automatically
   ```

## How It Works

1. **Scheduler runs daily at 9:00 AM** (configurable in `scheduler.py`)
2. **Finds subscriptions expiring in 24 hours** using `find_expiring_subscriptions()`
3. **Checks each subscription:**
   - Verifies user has a valid email
   - Verifies email is confirmed
   - Calculates exact hours remaining
4. **Sends email notification** with:
   - Subscription details
   - Expiry date and time
   - Current usage stats
   - Renewal link
5. **Logs all emails** in the EmailLog table

## Manual Testing

### Option 1: Admin Route (requires login)
```bash
# Access via browser while logged in as admin
http://localhost:5000/subscription/admin/send-expiry-notifications
```

### Option 2: Cron Route (no authentication)
```bash
# Via curl
curl -X GET http://localhost:5000/subscription/cron/send-expiry-notifications

# Or via browser
http://localhost:5000/subscription/cron/send-expiry-notifications
```

### Option 3: Python Console
```python
from app import app, create_app
from models.subscription import process_expiry_notifications

create_app()
with app.app_context():
    result = process_expiry_notifications()
    print(f"Result: {result}")
```

## Customization

### Change Notification Time
Edit `scheduler.py`:
```python
scheduler.add_job(
    func=check_and_send_expiry_notifications,
    trigger=CronTrigger(hour=9, minute=0),  # Change hour/minute here
    ...
)
```

### Change Hours Before Expiry
Edit the call in `scheduler.py`:
```python
# Default is 24 hours
expiring_subscriptions = find_expiring_subscriptions(hours_before=24)

# Change to 48 hours
expiring_subscriptions = find_expiring_subscriptions(hours_before=48)
```

Or update the function call in `process_expiry_notifications()` in `models/subscription.py`.

## Troubleshooting

### Issue: Emails not sending
**Solution:**
1. Check email configuration in `.env`
2. For Gmail, use an App Password (not your regular password)
3. Check logs: `flask_app.log`
4. Test email configuration manually

### Issue: Scheduler not starting
**Solution:**
1. Check console output when app starts
2. Ensure APScheduler is installed: `pip install APScheduler==3.10.4`
3. Check for import errors in logs

### Issue: No subscriptions found
**Solution:**
1. Verify you have subscriptions in database expiring in 24 hours
2. Run manual test to see console output
3. Check subscription end_date and _is_active status

### Issue: Mail object not found
**Solution:**
1. Ensure app.py creates the mail object: `mail = Mail(app)`
2. Verify mail is imported at top of app.py: `from flask_mail import Mail, Message`

## Logs

Check these locations for logs:
- **Console output:** Shows real-time processing
- **flask_app.log:** Application logs
- **EmailLog table:** Database records of all emails sent

## Security Note

The cron endpoint (`/subscription/cron/send-expiry-notifications`) has no authentication for easy cron job access. To add security, uncomment the token check in `models/subscription.py`:

```python
# Add to .env
CRON_SECRET_TOKEN=your-secret-token-here

# Uncomment in subscription.py
token = request.args.get('token')
if token != current_app.config.get('CRON_SECRET_TOKEN'):
    return jsonify({'error': 'Invalid token'}), 403
```

Then call with:
```bash
curl -X GET "http://localhost:5000/subscription/cron/send-expiry-notifications?token=your-secret-token-here"
```

## Production Deployment

### Using Server Cron (Alternative to Scheduler)
If you prefer using server cron instead of the built-in scheduler:

1. **Disable scheduler** in `app.py` (comment out lines 260-267)

2. **Add to crontab:**
   ```bash
   # Run daily at 9:00 AM
   0 9 * * * curl -X GET https://yourdomain.com/subscription/cron/send-expiry-notifications
   ```

3. **Or use wget:**
   ```bash
   0 9 * * * wget -q -O /dev/null https://yourdomain.com/subscription/cron/send-expiry-notifications
   ```

The built-in scheduler is recommended as it's more reliable and doesn't require external cron access.
