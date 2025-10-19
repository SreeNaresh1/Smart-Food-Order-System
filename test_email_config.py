"""
Test Email Configuration
Run this to verify your email settings are correct before using 2FA
"""

from app import app, mail
from flask_mail import Message
import sys

def test_email_config():
    """Test if email configuration is working"""
    
    print("\n" + "="*60)
    print("🔧 Testing Email Configuration for 2FA")
    print("="*60 + "\n")
    
    # Check configuration
    print("📋 Current Configuration:")
    print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"   MAIL_PASSWORD: {'*' * len(app.config.get('MAIL_PASSWORD', '')) if app.config.get('MAIL_PASSWORD') else 'NOT SET'}")
    print()
    
    # Validate configuration
    if not app.config.get('MAIL_USERNAME') or app.config['MAIL_USERNAME'] == 'your-email@gmail.com':
        print("❌ ERROR: MAIL_USERNAME not configured!")
        print("   Please set your email in app.py or environment variables")
        return False
    
    if not app.config.get('MAIL_PASSWORD') or app.config['MAIL_PASSWORD'] == 'your-app-password':
        print("❌ ERROR: MAIL_PASSWORD not configured!")
        print("   Please set your app password in app.py or environment variables")
        return False
    
    # Get test recipient
    test_email = input("📧 Enter email address to send test to (or press Enter to use sender): ").strip()
    if not test_email:
        test_email = app.config['MAIL_USERNAME']
    
    print(f"\n📤 Sending test email to: {test_email}")
    print("⏳ Please wait...\n")
    
    # Send test email
    with app.app_context():
        try:
            msg = Message(
                subject='✅ Test Email - 2FA Configuration',
                recipients=[test_email]
            )
            
            msg.html = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .success { background: #d4edda; border: 2px solid #28a745; padding: 20px; border-radius: 8px; }
                    .code { font-size: 32px; font-weight: bold; color: #28a745; letter-spacing: 5px; }
                </style>
            </head>
            <body>
                <div class="success">
                    <h2>✅ Email Configuration Test Successful!</h2>
                    <p>Your Food Order System email settings are working correctly.</p>
                    <p>This means you can now use Two-Factor Authentication (2FA).</p>
                    <br>
                    <p>Sample OTP Code (for display test):</p>
                    <div class="code">123456</div>
                    <br>
                    <p><small>This is a test email sent from Flask-Mail</small></p>
                </div>
            </body>
            </html>
            """
            
            msg.body = """
            ✅ Email Configuration Test Successful!
            
            Your Food Order System email settings are working correctly.
            This means you can now use Two-Factor Authentication (2FA).
            
            Sample OTP Code (for display test): 123456
            
            This is a test email sent from Flask-Mail
            """
            
            mail.send(msg)
            
            print("✅ SUCCESS! Test email sent successfully!")
            print(f"   Check your inbox at: {test_email}")
            print("   (Don't forget to check spam folder)")
            print()
            print("🎉 Your 2FA email configuration is working!")
            print("   You can now enable Two-Factor Authentication in your profile.")
            print()
            return True
            
        except Exception as e:
            print("❌ FAILED! Error sending email:")
            print(f"   {str(e)}")
            print()
            print("🔧 Troubleshooting Steps:")
            print("   1. Check your email and app password are correct")
            print("   2. Make sure 2-Step Verification is enabled (for Gmail)")
            print("   3. Use App Password, not regular password (for Gmail)")
            print("   4. Check your internet connection")
            print("   5. Try disabling firewall/antivirus temporarily")
            print("   6. Review EMAIL_SETUP_GUIDE.md for detailed instructions")
            print()
            return False

if __name__ == '__main__':
    success = test_email_config()
    
    print("="*60)
    if success:
        print("✅ All tests passed! 2FA is ready to use.")
    else:
        print("❌ Configuration needs fixing. Review errors above.")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)
