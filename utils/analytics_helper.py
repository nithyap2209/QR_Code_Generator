# utils/analytics_helper.py
from datetime import datetime, UTC
from sqlalchemy import func

def get_real_time_analytics_data(user_id, subscription_obj):
    """
    Calculate real-time analytics data based on actual scans
    This can be imported anywhere in the application
    """
    try:
        # Import here to avoid circular imports
        from app import db, QRCode, Scan
        
        if not subscription_obj:
            return {
                'analytics_used': 0,
                'analytics_remaining': 0,
                'analytics_total': 0,
                'analytics_percent': 0,
                'dynamic_qr_count': 0,
                'todays_operations': 0
            }
        
        # Get subscription period
        start_date = subscription_obj.start_date
        end_date = subscription_obj.end_date
        analytics_limit = subscription_obj.effective_analytics_limit
        
        # Calculate total scans of dynamic QR codes during subscription period
        total_scans = (
            db.session.query(func.count(Scan.id))
            .join(QRCode, Scan.qr_code_id == QRCode.id)
            .filter(QRCode.user_id == user_id)
            .filter(QRCode.is_dynamic == True)
            .filter(Scan.timestamp >= start_date)
            .filter(Scan.timestamp <= end_date)
            .scalar()
        ) or 0
        
        # Calculate today's scans
        today = datetime.now(UTC).date()
        today_start = datetime.combine(today, datetime.min.time()).replace(tzinfo=UTC)
        today_end = datetime.combine(today, datetime.max.time()).replace(tzinfo=UTC)
        
        todays_scans = (
            db.session.query(func.count(Scan.id))
            .join(QRCode, Scan.qr_code_id == QRCode.id)
            .filter(QRCode.user_id == user_id)
            .filter(QRCode.is_dynamic == True)
            .filter(Scan.timestamp >= today_start)
            .filter(Scan.timestamp <= today_end)
            .scalar()
        ) or 0
        
        # Count dynamic QR codes
        dynamic_qr_count = (
            db.session.query(func.count(QRCode.id))
            .filter(QRCode.user_id == user_id)
            .filter(QRCode.is_dynamic == True)
            .scalar()
        ) or 0
        
        # Calculate remaining and percentage
        analytics_remaining = max(0, analytics_limit - total_scans)
        analytics_percent = min(100, (total_scans / analytics_limit * 100)) if analytics_limit > 0 else 0
        
        return {
            'analytics_used': total_scans,
            'analytics_remaining': analytics_remaining,
            'analytics_total': analytics_limit,
            'analytics_percent': analytics_percent,
            'dynamic_qr_count': dynamic_qr_count,
            'todays_operations': todays_scans
        }
        
    except Exception as e:
        print(f"Error calculating real-time analytics: {str(e)}")
        # Return fallback data
        return {
            'analytics_used': subscription_obj.analytics_used or 0,
            'analytics_remaining': 0,
            'analytics_total': subscription_obj.effective_analytics_limit,
            'analytics_percent': 0,
            'dynamic_qr_count': 0,
            'todays_operations': 0
        }

def update_subscription_with_real_analytics(subscribed_users_list):
    """
    Update a list of (SubscribedUser, Subscription) tuples with real-time analytics
    """
    updated_list = []
    
    for sub, plan in subscribed_users_list:
        # Get real-time analytics data
        analytics_data = get_real_time_analytics_data(sub.U_ID, sub)
        
        # Add real-time data as attributes to the subscription object
        sub.real_analytics_used = analytics_data['analytics_used']
        sub.real_analytics_remaining = analytics_data['analytics_remaining']
        sub.real_analytics_percent = analytics_data['analytics_percent']
        sub.real_todays_operations = analytics_data['todays_operations']
        sub.real_dynamic_qr_count = analytics_data['dynamic_qr_count']
        
        updated_list.append((sub, plan))
    
    return updated_list