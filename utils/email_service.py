"""
Simple SMTP Email Service with App Passwords
Uses Gmail SMTP with app-specific passwords for two accounts:
- payment@qrdada.com: For payment-related emails
- support@qrdada.com: For all other emails (verification, password reset, contact, etc.)
"""

import os
import logging
from typing import Optional, List, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

logger = logging.getLogger(__name__)

class SMTPEmailService:
    """Service for sending emails using Gmail SMTP with App Passwords"""

    def __init__(self):
        # Email accounts
        self.payment_email = 'payment@qrdada.com'
        self.support_email = 'support@qrdada.com'

        # App passwords (from environment variables)
        self.payment_password = os.getenv('PAYMENT_EMAIL_PASSWORD', 'rjmg bphb pxdt imce')
        self.support_password = os.getenv('SUPPORT_EMAIL_PASSWORD', 'cxog owai wjlw wchw')

        # SMTP settings
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

    def _send_smtp_email(
        self,
        from_email: str,
        password: str,
        to_email: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        attachments: Optional[List[Tuple[bytes, str, str]]] = None
    ) -> bool:
        """
        Send email using SMTP

        Args:
            attachments: List of tuples (file_data, filename, mimetype)
                        Example: [(pdf_bytes, 'invoice.pdf', 'application/pdf')]
        """
        try:
            # Remove spaces from password (Gmail app passwords can have spaces for readability)
            clean_password = password.replace(' ', '')

            # Create message
            if html or attachments:
                msg = MIMEMultipart('mixed')
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = subject

                # Create alternative part for text and HTML
                if html:
                    alt_part = MIMEMultipart('alternative')
                    alt_part.attach(MIMEText(body, 'plain'))
                    alt_part.attach(MIMEText(html, 'html'))
                    msg.attach(alt_part)
                else:
                    msg.attach(MIMEText(body, 'plain'))

                # Attach files if provided
                if attachments:
                    for file_data, filename, mimetype in attachments:
                        attachment = MIMEApplication(file_data, _subtype=mimetype.split('/')[-1])
                        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(attachment)
            else:
                msg = MIMEText(body, 'plain')
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = subject

            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.set_debuglevel(0)  # Disable debug output
                server.starttls()  # Enable TLS
                server.login(from_email, clean_password)  # Use password without spaces
                server.send_message(msg)

            logger.info(f"Email sent successfully from {from_email} to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email from {from_email}: {e}", exc_info=True)
            return False

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        email_type: str = 'support',
        attachments: Optional[List[Tuple[bytes, str, str]]] = None
    ) -> bool:
        """
        Send an email using the appropriate Gmail account

        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text body
            html: HTML body (optional)
            email_type: Type of email - 'payment' or 'support' (default: 'support')
            attachments: List of tuples (file_data, filename, mimetype)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        # Determine sender and password
        if email_type == 'payment':
            from_email = self.payment_email
            password = self.payment_password
        else:
            from_email = self.support_email
            password = self.support_password

        return self._send_smtp_email(from_email, password, to, subject, body, html, attachments)

    def send_payment_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        attachments: Optional[List[Tuple[bytes, str, str]]] = None
    ) -> bool:
        """Send payment-related email using payment@qrdada.com"""
        return self.send_email(to, subject, body, html, email_type='payment', attachments=attachments)

    def send_support_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        attachments: Optional[List[Tuple[bytes, str, str]]] = None
    ) -> bool:
        """Send support-related email using support@qrdada.com"""
        return self.send_email(to, subject, body, html, email_type='support', attachments=attachments)


# Global instance
smtp_email_service = SMTPEmailService()

# Alias for compatibility with existing code
email_service = smtp_email_service


def init_smtp_email_service(app=None):
    """Initialize SMTP email service with Flask app"""
    if app:
        # Store email service in app config
        app.config['EMAIL_SERVICE'] = smtp_email_service
        logger.info("SMTP Email service initialized with App Passwords")
    return smtp_email_service

# Alias for compatibility
init_email_service = init_smtp_email_service
