"""
Test script to verify payment email is working
Run this to test if payment@qrdada.com emails are being sent correctly
"""

from utils.email_service import email_service

print("Testing payment email configuration...")
print("=" * 80)

# Test payment email
result = email_service.send_payment_email(
    to="callincegoodsonmarialouis@gmail.com",  # Send to your personal email for testing
    subject="Test Payment Confirmation - QR Code Pro",
    body="""This is a test payment confirmation email.

If you receive this email, your payment email configuration is working correctly!

Test Details:
- From: payment@qrdada.com
- SMTP Server: smtp.gmail.com:587
- Authentication: App Password

This confirms that payment confirmation emails will be sent successfully.""",
    html="""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Payment Email</title>
</head>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <h1 style="color: #2c5282;">Test Payment Confirmation</h1>
    <p>This is a test payment confirmation email.</p>
    <p><strong>If you receive this email, your payment email configuration is working correctly!</strong></p>
    <div style="background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px;">
        <h3>Test Details:</h3>
        <ul>
            <li><strong>From:</strong> payment@qrdada.com</li>
            <li><strong>SMTP Server:</strong> smtp.gmail.com:587</li>
            <li><strong>Authentication:</strong> App Password</li>
        </ul>
    </div>
    <p>This confirms that payment confirmation emails will be sent successfully.</p>
</body>
</html>"""
)

if result:
    print("[SUCCESS] Payment test email sent successfully!")
    print("  Check callincegoodsonmarialouis@gmail.com for the test email")
else:
    print("[FAILED] Payment test email could not be sent")
    print("  Check the error messages above for details")

print("=" * 80)

# Test support email for comparison
print("\nTesting support email configuration (for comparison)...")
print("=" * 80)

result = email_service.send_support_email(
    to="callincegoodsonmarialouis@gmail.com",
    subject="Test Support Email - QR Code Pro",
    body="This is a test support email from support@qrdada.com"
)

if result:
    print("[SUCCESS] Support test email sent successfully!")
else:
    print("[FAILED] Support test email could not be sent")

print("=" * 80)
print("\nTest complete!")
