# 📧 Gmail Setup Guide for 2FA

## ⚡ Quick Setup (5 Minutes)

### Step 1: Get Gmail App Password

1. **Go to your Google Account Security page:**
   - Visit: https://myaccount.google.com/security
   - Sign in with your Gmail account

2. **Enable 2-Step Verification** (if not already enabled):
   - Scroll to "How you sign in to Google"
   - Click "2-Step Verification"
   - Follow the prompts to enable it
   - **This is required** before you can create app passwords

3. **Create an App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - Or go to Security → 2-Step Verification → App passwords
   - Select app: **Mail**
   - Select device: **Windows Computer**
   - Click **Generate**
   - **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 2: Update app.py

Open `app.py` and find lines 18-24 (Flask-Mail Configuration section).

**Replace this:**
```python
# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
```

**With this (replace with YOUR email and app password):**
```python
# Flask-Mail Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-actual-email@gmail.com'  # ← Replace this
app.config['MAIL_PASSWORD'] = 'abcdefghijklmnop'  # ← Replace with 16-char app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-actual-email@gmail.com'  # ← Replace this
```

### Step 3: Restart Flask Server

1. **Stop the server:** Press `Ctrl+C` in the terminal running Flask
2. **Start it again:** `python app.py`

### Step 4: Test Email

Run the test script:
```powershell
python test_email_config.py
```

**Expected output:**
```
✅ Email configuration is set up correctly!
📧 Sending test email...
✅ Test email sent successfully!
Check your inbox at: your-actual-email@gmail.com
```

### Step 5: Try 2FA Again!

1. Login to your account
2. Go to Profile page
3. Click "Enable 2FA"
4. Enter your password
5. **Check your Gmail inbox** - you should receive the 6-digit OTP code!
6. Enter the code and save your backup codes

---

## 🔧 Example Configuration

If your Gmail is **john.doe@gmail.com** and app password is **abcd efgh ijkl mnop**:

```python
# Flask-Mail Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'john.doe@gmail.com'
app.config['MAIL_PASSWORD'] = 'abcdefghijklmnop'  # Remove spaces
app.config['MAIL_DEFAULT_SENDER'] = 'john.doe@gmail.com'
```

⚠️ **Important:** Remove spaces from the app password!

---

## ❓ Troubleshooting

### "App passwords" option not available?
- You must enable 2-Step Verification first
- Wait 5-10 minutes after enabling 2-Step Verification
- Make sure you're signed in to the correct Google account

### "Failed to send verification email" still appears?
1. Double-check the app password (no spaces)
2. Make sure you restarted the Flask server
3. Run `python test_email_config.py` to diagnose

### Test email not received?
1. Check spam/junk folder
2. Verify email address is correct in app.py
3. Try generating a new app password

---

## 🎯 What Happens Next?

Once configured:
- ✅ Users can enable 2FA on their profile
- ✅ OTP codes are sent to their registered email
- ✅ Login history is tracked
- ✅ Trusted devices remember users for 30 days
- ✅ Account lockout after 5 failed attempts
- ✅ Admin security dashboard shows statistics

---

## 🔒 Security Notes

1. **Never commit your app password to Git!**
   - Add `app.py` to `.gitignore` if it contains passwords
   - Or use environment variables for production

2. **The app password is NOT your Gmail password**
   - It's a special 16-character code
   - You can revoke it anytime from your Google Account

3. **Keep your app password secure**
   - Don't share it
   - Don't post it in screenshots
   - Regenerate if compromised

---

## 📝 Need Help?

If you're stuck, just let me know:
- "Can't find app passwords option"
- "Email test failed"
- "Still getting errors"

I'm here to help! 🚀
