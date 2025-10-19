# 📧 Quick Email Setup for 2FA

## Gmail Setup (5 Minutes)

### Step 1: Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Find "2-Step Verification"
3. Click "Turn On"
4. Follow the setup wizard

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Windows Computer**
4. Click **Generate**
5. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 3: Configure in Project

**Option A: Environment Variables (Recommended)**

Open PowerShell and run:
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="abcd efgh ijkl mnop"
```

Then restart your Flask app.

**Option B: Direct Configuration**

Edit `app.py` (lines 19-22):
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'abcdefghijklmnop'  # Remove spaces
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
```

### Step 4: Test
1. Enable 2FA in your profile
2. Check if you receive the OTP email
3. ✅ Done!

---

## Current Configuration

Your `app.py` currently has:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
```

**To activate:**
- Replace `'your-email@gmail.com'` with your actual Gmail
- Replace `'your-app-password'` with your generated app password

---

## Troubleshooting

### "Failed to send OTP"
- ✅ Check spam folder
- ✅ Verify App Password (no spaces)
- ✅ Check internet connection
- ✅ Try disabling antivirus/firewall temporarily

### "SMTP Authentication Failed"
- ✅ Use App Password, NOT regular password
- ✅ Enable 2-Step Verification first
- ✅ Check for typos in email/password

### Still not working?
- Use a different Gmail account
- Try Outlook/Yahoo instead
- Check Python console for error messages

---

## Alternative: Outlook/Hotmail

Edit `app.py`:
```python
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@outlook.com'
app.config['MAIL_PASSWORD'] = 'your-password'
```

---

## Test Email Configuration

Create a test file `test_email.py`:
```python
from app import app, mail
from flask_mail import Message

with app.app_context():
    msg = Message(
        subject='Test Email',
        recipients=['your-email@gmail.com']
    )
    msg.body = 'This is a test email from Flask-Mail!'
    
    try:
        mail.send(msg)
        print('✅ Email sent successfully!')
    except Exception as e:
        print(f'❌ Error: {str(e)}')
```

Run:
```powershell
python test_email.py
```

---

## ✅ Once Configured

The 2FA system will:
- ✉️ Send OTP codes automatically on login
- 🔐 Send verification codes when enabling 2FA
- ⏰ Codes expire after 5 minutes
- 🔄 Allow resending codes
- 📧 Use beautiful HTML email templates

**Enjoy enhanced security! 🎉**
