"""
Scheduler for automated subscription expiry notifications
This module sets up APScheduler to run periodic tasks
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_scheduler(app):
    """
    Initialize and start the background scheduler

    Args:
        app: Flask application instance
    """
    scheduler = BackgroundScheduler(daemon=True)

    def check_and_send_expiry_notifications():
        """
        Job function to check and send expiry notifications
        Runs within app context
        """
        with app.app_context():
            try:
                from models.subscription import process_expiry_notifications
                logger.info("=== Running scheduled expiry notification check ===")
                result = process_expiry_notifications()
                if result:
                    logger.info("Expiry notifications processed successfully")
                else:
                    logger.error("Failed to process expiry notifications")
            except Exception as e:
                logger.error(f"Error in scheduled expiry notification job: {str(e)}")
                import traceback
                traceback.print_exc()

    # Schedule the job to run daily at 9:00 AM
    # You can adjust the time as needed
    scheduler.add_job(
        func=check_and_send_expiry_notifications,
        trigger=CronTrigger(hour=9, minute=0),  # Run at 9:00 AM every day
        id='expiry_notification_job',
        name='Send subscription expiry notifications',
        replace_existing=True
    )

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started - Expiry notifications will run daily at 9:00 AM")

    return scheduler
