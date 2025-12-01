from .database import db
from datetime import datetime, UTC
import logging
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import pytz
from flask import request, has_request_context  # FIXED: Added has_request_context

# Models
class User(UserMixin, db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)
    company_email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirm_token = db.Column(db.String(500), nullable=True)  # Increased length to safely store token
    email_token_created_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))  
    qr_codes = db.relationship('QRCode', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Updated Token Generation
    def get_reset_token(self, expires_sec=1800):
        """Generate a secure token for password reset (30 minute expiry)"""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id, 'email': self.company_email, 'purpose': 'reset_password'}, 
                      salt='password-reset-salt')

    # Updated Token Verification
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """Verify a password reset token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='password-reset-salt', max_age=expires_sec)
            user_id = data.get('user_id')
            purpose = data.get('purpose')
            if user_id and purpose == 'reset_password':
                return User.query.get(user_id)
            return None
        except Exception as e:
            logging.error(f"Token verification error: {str(e)}")
            return None
        
    # Updated Email Confirmation Token
    def get_email_confirm_token(self):
        """Generate a secure token for email confirmation"""
        try:
            s = Serializer(current_app.config['SECRET_KEY'])
            token = s.dumps({
                'user_id': self.id, 
                'email': self.company_email, 
                'purpose': 'email_confirm',
                'timestamp': datetime.now(UTC).timestamp()  # Add timestamp for uniqueness
            }, salt='email-confirm-salt')
            
            # Store token in the user model
            self.email_confirm_token = token
            self.email_token_created_at = datetime.now(UTC)
            
            # Return the token - committing will be done by calling function
            return token
        except Exception as e:
            logging.error(f"Error generating token: {str(e)}")
            return None
        
    # Updated Email Token Verification
    @staticmethod
    def verify_email_token(token, expires_sec=86400):  # 24 hours
        """Verify an email confirmation token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='email-confirm-salt', max_age=expires_sec)
            user_id = data.get('user_id')
            purpose = data.get('purpose')
            
            logging.info(f"Verifying email token: user_id={user_id}, purpose={purpose}")
            
            if user_id and purpose == 'email_confirm':
                user = User.query.get(user_id)
                
                # Additional check to make sure token matches stored token
                if user and user.email_confirm_token == token:
                    return user
                elif user:
                    logging.warning(f"Token mismatch for user {user_id}: Stored token doesn't match provided token")
                else:
                    logging.warning(f"User {user_id} not found")
                    
                return user
            return None
        except Exception as e:
            logging.error(f"Email token verification error: {str(e)}")
            return None
        
class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(255), nullable=False, index=True)
    recipient_name = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    
    # Email details
    email_type = db.Column(db.String(50), nullable=False, index=True)  # 'verification', 'password_reset', 'payment_confirmation', etc.
    subject = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='sent', nullable=False)  # 'sent', 'failed', 'bounced'
    
    # Additional data (JSON format)
    email_metadata = db.Column(db.Text, nullable=True)  # Store additional info like payment_id, order_id, etc.
    
    # Tracking info
    sent_at = db.Column(db.DateTime, default=datetime.now(UTC), nullable=False)
    error_message = db.Column(db.Text, nullable=True)  # Store error if email failed
    
    # System info
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    
    # Relationship
    user = db.relationship('User', backref='email_logs')
    
    def __repr__(self):
        return f"<EmailLog {self.email_type} to {self.recipient_email}>"
    
    @property
    def formatted_sent_time(self):
        """Format sent time for display"""
        if self.sent_at:
            if self.sent_at.tzinfo is None:
                return pytz.UTC.localize(self.sent_at).astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d %b %Y, %H:%M %p IST')
            return self.sent_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d %b %Y, %H:%M %p IST')
        return 'N/A'
    
    @staticmethod
    def log_email(recipient_email, recipient_name, email_type, subject, user_id=None, 
                  status='sent', metadata=None, error_message=None):
        """
        Log an email sending attempt with proper request context handling
        
        Args:
            recipient_email (str): Email address of recipient
            recipient_name (str): Name of recipient
            email_type (str): Type of email (verification, password_reset, etc.)
            subject (str): Email subject
            user_id (int, optional): User ID if applicable
            status (str): Status of email (sent, failed)
            metadata (dict, optional): Additional data to store
            error_message (str, optional): Error message if failed
        """
        try:
            # FIXED: Safely get request context
            ip_address = None
            user_agent = None
            
            # Check if we're in a request context before accessing request
            if has_request_context():
                try:
                    ip_address = request.remote_addr
                    user_agent = request.headers.get('User-Agent', '')
                except RuntimeError:
                    # Request context might not be available
                    pass
            
            # Convert metadata to JSON string if provided
            metadata_json = None
            if metadata:
                import json
                metadata_json = json.dumps(metadata)
            
            email_log = EmailLog(
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                user_id=user_id,
                email_type=email_type,
                subject=subject,
                status=status,
                email_metadata=metadata_json,
                error_message=error_message,
                ip_address=ip_address,
                user_agent=user_agent,
                sent_at=datetime.now(UTC)
            )
            
            db.session.add(email_log)
            db.session.commit()
            
            current_app.logger.info(f"Email log created: {email_type} to {recipient_email} - {status}")
            return True
            
        except Exception as e:
            try:
                db.session.rollback()
            except:
                pass
            current_app.logger.error(f"Failed to log email: {str(e)}")
            # Don't raise the exception to prevent breaking the email flow
            return False
