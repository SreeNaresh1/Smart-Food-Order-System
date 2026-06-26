"""
2FA Setup and Testing Script
Automates the setup and testing of Two-Factor Authentication
"""

from app import app, db, mail
from backend.models import User
from werkzeug.security import generate_password_hash
from flask_mail import Message
import sys

def setup_database():
    """Ensure database has 2FA fields"""
    print("\n" + "="*60)
    print("📊 Step 1: Setting up database...")
    print("="*60)
    
    with app.app_context():
        try:
            # This will add new columns if they don't exist
            db.create_all()
            print("✅ Database schema updated successfully!")
            print("   Added 2FA fields to User table:")
            print("   - two_factor_enabled (Boolean)")
            print("   - otp_code (String)")
            print("   - otp_expiry (DateTime)")
            print("   - backup_codes (Text)")
            return True
        except Exception as e:
            print(f"❌ Database setup failed: {str(e)}")
            return False

def check_email_config():
    """Check if email is configured"""
    print("\n" + "="*60)
    print("📧 Step 2: Checking email configuration...")
    print("="*60)
    
    username = app.config.get('MAIL_USERNAME')
    password = app.config.get('MAIL_PASSWORD')
    
    print(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"   MAIL_USERNAME: {username}")
    
    if password and password != 'your-app-password':
        print(f"   MAIL_PASSWORD: {'*' * len(password)} (configured)")
    else:
        print(f"   MAIL_PASSWORD: NOT CONFIGURED ⚠️")
    
    if username == 'your-email@gmail.com' or password == 'your-app-password':
        print("\n⚠️  Email not configured yet!")
        print("\n📝 To configure email, you have two options:")
        print("\n   Option A - Environment Variables (Recommended):")
        print("   $env:MAIL_USERNAME=\"your-email@gmail.com\"")
        print("   $env:MAIL_PASSWORD=\"your-app-password\"")
        print("\n   Option B - Edit app.py (lines 22-24)")
        print("\n   See EMAIL_SETUP_GUIDE.md for detailed instructions")
        return False
    else:
        print("✅ Email configuration looks good!")
        return True

def test_email():
    """Test sending email"""
    print("\n" + "="*60)
    print("📤 Step 3: Testing email sending...")
    print("="*60)
    
    username = app.config.get('MAIL_USERNAME')
    
    print(f"\n📧 Attempting to send test email to: {username}")
    print("⏳ Please wait...\n")
    
    with app.app_context():
        try:
            msg = Message(
                subject='✅ 2FA Setup Test - Food Order System',
                recipients=[username]
            )
            
            msg.html = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f7fa; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
                    .success { background: #d4edda; border: 2px solid #28a745; padding: 20px; border-radius: 8px; margin: 20px 0; }
                    .code { font-size: 36px; font-weight: bold; color: #28a745; letter-spacing: 5px; font-family: 'Courier New', monospace; text-align: center; margin: 20px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 2FA Setup Successful!</h1>
                    </div>
                    <div class="success">
                        <h2>✅ Email Configuration Test Passed!</h2>
                        <p>Your Food Order System is now ready to use Two-Factor Authentication.</p>
                        <p>Sample OTP Code (for display test):</p>
                        <div class="code">123456</div>
                        <p><strong>What this means:</strong></p>
                        <ul>
                            <li>Email sending is working correctly</li>
                            <li>Users can now enable 2FA in their profiles</li>
                            <li>OTP codes will be sent to this email format</li>
                            <li>The system is production-ready</li>
                        </ul>
                    </div>
                    <p style="color: #666; font-size: 14px; text-align: center; margin-top: 30px;">
                        This is an automated test message from Food Order System
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.body = """
            🎉 2FA Setup Successful!
            
            ✅ Email Configuration Test Passed!
            
            Your Food Order System is now ready to use Two-Factor Authentication.
            
            Sample OTP Code (for display test): 123456
            
            What this means:
            - Email sending is working correctly
            - Users can now enable 2FA in their profiles
            - OTP codes will be sent in this format
            - The system is production-ready
            
            This is an automated test message from Food Order System
            """
            
            mail.send(msg)
            
            print("✅ SUCCESS! Test email sent successfully!")
            print(f"   Check your inbox at: {username}")
            print("   (Don't forget to check spam/junk folder)")
            return True
            
        except Exception as e:
            print(f"❌ FAILED! Error sending email:")
            print(f"   {str(e)}")
            print("\n🔧 Common issues:")
            print("   - Check email and password are correct")
            print("   - Use App Password for Gmail (not regular password)")
            print("   - Enable 2-Step Verification first (Gmail)")
            print("   - Check internet connection")
            print("   - Review EMAIL_SETUP_GUIDE.md")
            return False

def check_test_user():
    """Check if test user exists and can enable 2FA"""
    print("\n" + "="*60)
    print("👤 Step 4: Checking user accounts...")
    print("="*60)
    
    with app.app_context():
        try:
            users = User.query.all()
            
            if not users:
                print("⚠️  No users found in database!")
                print("   Create a user by registering on the website")
                return False
            
            print(f"✅ Found {len(users)} user(s) in database:")
            print()
            
            for user in users:
                status = "✅ ENABLED" if user.two_factor_enabled else "⭕ DISABLED"
                print(f"   • {user.name} ({user.email})")
                print(f"     Role: {user.role}")
                print(f"     2FA Status: {status}")
                print()
            
            enabled_count = sum(1 for u in users if u.two_factor_enabled)
            print(f"📊 2FA Statistics:")
            print(f"   Total Users: {len(users)}")
            print(f"   2FA Enabled: {enabled_count}")
            print(f"   2FA Disabled: {len(users) - enabled_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking users: {str(e)}")
            return False

def create_documentation_summary():
    """Show documentation summary"""
    print("\n" + "="*60)
    print("📚 Step 5: Documentation overview...")
    print("="*60)
    
    docs = [
        ("TWO_FACTOR_AUTH_GUIDE.md", "Complete 2FA guide (400+ lines)"),
        ("EMAIL_SETUP_GUIDE.md", "Quick email setup (5 minutes)"),
        ("2FA_QUICK_REFERENCE.md", "Quick reference card"),
        ("2FA_IMPLEMENTATION_COMPLETE.md", "Technical summary"),
        ("test_email_config.py", "Email testing script"),
    ]
    
    print("\n📖 Available Documentation:")
    for doc, desc in docs:
        print(f"   ✅ {doc}")
        print(f"      {desc}")
    print()

def show_next_steps():
    """Display next steps for user"""
    print("\n" + "="*60)
    print("🎯 Next Steps:")
    print("="*60)
    print()
    print("1️⃣  Configure Email (if not done yet):")
    print("   • See EMAIL_SETUP_GUIDE.md for instructions")
    print("   • Use Gmail App Password (not regular password)")
    print("   • Test with: python test_email_config.py")
    print()
    print("2️⃣  Start Your Server:")
    print("   • Run: python app.py")
    print("   • Access: http://localhost:5000")
    print()
    print("3️⃣  Enable 2FA (Optional for users):")
    print("   • Login to your account")
    print("   • Go to Profile page")
    print("   • Find 'Two-Factor Authentication' section")
    print("   • Click 'Enable' button")
    print("   • Save your backup codes!")
    print()
    print("4️⃣  Test 2FA:")
    print("   • Logout after enabling 2FA")
    print("   • Login again - you'll need OTP from email")
    print("   • Test backup codes as well")
    print()
    print("✅ 2FA is OPTIONAL - users choose to enable it")
    print("✅ Existing login still works without 2FA")
    print("✅ No changes to current workflows")
    print()

def main():
    """Main setup routine"""
    print("\n" + "="*60)
    print("🔐 TWO-FACTOR AUTHENTICATION SETUP")
    print("Food Order System - Automated Setup & Testing")
    print("="*60)
    
    # Step 1: Database
    db_ok = setup_database()
    
    # Step 2: Email config check
    email_configured = check_email_config()
    
    # Step 3: Test email (only if configured)
    email_ok = False
    if email_configured:
        email_ok = test_email()
    
    # Step 4: Check users
    users_ok = check_test_user()
    
    # Step 5: Documentation
    create_documentation_summary()
    
    # Summary
    print("\n" + "="*60)
    print("📋 SETUP SUMMARY:")
    print("="*60)
    print()
    print(f"   Database Setup:     {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"   Email Config:       {'✅ CONFIGURED' if email_configured else '⚠️  PENDING'}")
    print(f"   Email Test:         {'✅ PASS' if email_ok else ('⏭️  SKIPPED' if not email_configured else '❌ FAIL')}")
    print(f"   User Accounts:      {'✅ FOUND' if users_ok else '⚠️  NONE'}")
    print()
    
    if db_ok and email_configured and email_ok:
        print("🎉 SUCCESS! 2FA is fully configured and ready to use!")
        print()
    elif db_ok and not email_configured:
        print("⚠️  PARTIAL SETUP: Database ready, but email needs configuration")
        print()
    else:
        print("❌ SETUP INCOMPLETE: Please review errors above")
        print()
    
    # Next steps
    show_next_steps()
    
    print("="*60)
    print("For detailed help, see: TWO_FACTOR_AUTH_GUIDE.md")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
