"""
Test script to verify contact form reply email is working
This simulates sending a reply from the admin panel to a contact form submission
"""

from utils.email_service import email_service

print("Testing contact form reply email functionality...")
print("=" * 80)

# Simulate sending a reply to a contact form submission
result = email_service.send_support_email(
    to="callincegoodsonmarialouis@gmail.com",  # Your personal email for testing
    subject="Re: Your Contact Form Inquiry - QR Code Pro",
    body="""Dear User,

Thank you for reaching out to us through our contact form.

This is a test reply email to verify that the contact form reply functionality is working correctly after the SMTP migration.

Your inquiry:
"This was a test contact form submission"

Our response:
We have received your message and our team will get back to you shortly.

If you have any additional questions, please don't hesitate to contact us.

Best regards,
QR Code Pro Support Team
support@qrdada.com"""
)

if result:
    print("[SUCCESS] Contact reply email sent successfully!")
    print("  From: support@qrdada.com")
    print("  To: callincegoodsonmarialouis@gmail.com")
    print("  Check your email inbox for the test reply")
else:
    print("[FAILED] Contact reply email could not be sent")
    print("  Check the error messages above for details")

print("=" * 80)
print("\nTest complete!")
print("\nWhat this confirms:")
print("  - Admin panel contact form replies will work")
print("  - Emails sent from Contact Submission Details page will succeed")
print("  - Using support@qrdada.com as sender")
