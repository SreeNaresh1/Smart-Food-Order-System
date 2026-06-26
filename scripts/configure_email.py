"""
Quick Email Configuration Helper
Run this to quickly configure email for 2FA
"""

import os

print("\n" + "="*70)
print("📧 QUICK EMAIL CONFIGURATION FOR 2FA")
print("="*70 + "\n")

print("Choose your email service:\n")
print("1. ⭐ Mailtrap (RECOMMENDED for testing - no real email needed)")
print("2. 📧 Gmail (real emails)")
print("3. 🔧 Other SMTP server")
print("4. ❌ Skip (configure manually later)\n")

choice = input("Enter your choice (1-4): ").strip()

if choice == "1":
    print("\n" + "="*70)
    print("MAILTRAP CONFIGURATION")
    print("="*70 + "\n")
    print("📝 Steps:")
    print("1. Go to https://mailtrap.io/")
    print("2. Sign up for free account (takes 2 minutes)")
    print("3. Go to 'Inboxes' → 'My Inbox'")
    print("4. Find 'SMTP Settings' section")
    print("5. Copy the credentials below:\n")
    
    username = input("Enter Mailtrap Username: ").strip()
    password = input("Enter Mailtrap Password: ").strip()
    
    if username and password:
        config = f"""
# Flask-Mail Configuration (Mailtrap)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '{username}'
app.config['MAIL_PASSWORD'] = '{password}'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@foodsystem.com'
"""
        
        print("\n✅ Configuration generated!")
        print("\n📋 Copy this configuration to app.py (lines 18-24):\n")
        print(config)
        print("\n💡 Or I can update it automatically!")
        
        update = input("\nUpdate app.py automatically? (yes/no): ").strip().lower()
        if update in ['yes', 'y']:
            try:
                # Read current app.py
                with open('app.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace email configuration
                old_config = """# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'"""
                
                new_config = f"""# Flask-Mail Configuration (Mailtrap)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '{username}'
app.config['MAIL_PASSWORD'] = '{password}'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@foodsystem.com'"""
                
                content = content.replace(old_config, new_config)
                
                # Write back
                with open('app.py', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("\n✅ app.py updated successfully!")
                print("🔄 Please restart your Flask server (Ctrl+C then run 'python app.py')")
                print("\n📧 Emails will appear in your Mailtrap inbox!")
                
            except Exception as e:
                print(f"\n❌ Error updating file: {e}")
                print("Please update app.py manually with the configuration above.")

elif choice == "2":
    print("\n" + "="*70)
    print("GMAIL CONFIGURATION")
    print("="*70 + "\n")
    print("📝 Steps to get Gmail App Password:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Enable '2-Step Verification' if not enabled")
    print("3. Go to https://myaccount.google.com/apppasswords")
    print("4. Select 'Mail' and 'Windows Computer'")
    print("5. Click 'Generate'")
    print("6. Copy the 16-character password\n")
    
    email = input("Enter your Gmail address: ").strip()
    app_password = input("Enter Gmail App Password (16 chars): ").strip().replace(' ', '')
    
    if email and app_password:
        config = f"""
# Flask-Mail Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '{email}'
app.config['MAIL_PASSWORD'] = '{app_password}'
app.config['MAIL_DEFAULT_SENDER'] = '{email}'
"""
        
        print("\n✅ Configuration generated!")
        print("\n📋 Copy this configuration to app.py (lines 18-24):\n")
        print(config)
        
        print("\n💡 Or I can update it automatically!")
        
        update = input("\nUpdate app.py automatically? (yes/no): ").strip().lower()
        if update in ['yes', 'y']:
            try:
                with open('app.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_config = """# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'"""
                
                new_config = f"""# Flask-Mail Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '{email}'
app.config['MAIL_PASSWORD'] = '{app_password}'
app.config['MAIL_DEFAULT_SENDER'] = '{email}'"""
                
                content = content.replace(old_config, new_config)
                
                with open('app.py', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("\n✅ app.py updated successfully!")
                print("🔄 Please restart your Flask server (Ctrl+C then run 'python app.py')")
                print("\n📧 OTP codes will be sent to users' email addresses!")
                
            except Exception as e:
                print(f"\n❌ Error updating file: {e}")
                print("Please update app.py manually with the configuration above.")

elif choice == "3":
    print("\n" + "="*70)
    print("CUSTOM SMTP CONFIGURATION")
    print("="*70 + "\n")
    
    server = input("SMTP Server (e.g., smtp.office365.com): ").strip()
    port = input("SMTP Port (e.g., 587): ").strip()
    use_tls = input("Use TLS? (yes/no): ").strip().lower() in ['yes', 'y']
    username = input("SMTP Username: ").strip()
    password = input("SMTP Password: ").strip()
    sender = input("Default Sender Email: ").strip()
    
    if all([server, port, username, password, sender]):
        config = f"""
# Flask-Mail Configuration (Custom)
app.config['MAIL_SERVER'] = '{server}'
app.config['MAIL_PORT'] = {port}
app.config['MAIL_USE_TLS'] = {use_tls}
app.config['MAIL_USERNAME'] = '{username}'
app.config['MAIL_PASSWORD'] = '{password}'
app.config['MAIL_DEFAULT_SENDER'] = '{sender}'
"""
        
        print("\n✅ Configuration generated!")
        print("\n📋 Copy this to app.py (lines 18-24):\n")
        print(config)

else:
    print("\n⏭️ Skipped. Please configure email manually in app.py")
    print("See EMAIL_FIX_REQUIRED.md for instructions")

print("\n" + "="*70)
print("NEXT STEPS:")
print("="*70)
print("1. Restart Flask server: python app.py")
print("2. Test email: python test_email_config.py")
print("3. Try enabling 2FA again!")
print("\n")
