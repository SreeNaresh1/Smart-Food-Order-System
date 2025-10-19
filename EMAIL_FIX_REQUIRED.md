# 📧 EMAIL CONFIGURATION REQUIRED - QUICK FIX

## 🚨 Issue: "Failed to send verification email"

**Root Cause:** Email credentials are not configured in the system.

**Status:** ✅ Easy to fix! Choose one of the options below.

---

## ⚡ **QUICK FIX OPTIONS**

### **Option 1: Use Mailtrap (EASIEST - No Real Email Needed)** ⭐ **RECOMMENDED**

Mailtrap is a fake SMTP server perfect for testing - no real email needed!

#### **Step 1: Get Free Mailtrap Account**
1. Go to: https://mailtrap.io/
2. Sign up for free account
3. Go to "Inboxes" → "My Inbox"
4. Copy the SMTP credentials shown

#### **Step 2: Configure in app.py**
Open `app.py` and change lines 18-24:

```python
# Flask-Mail Configuration (Mailtrap)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-mailtrap-username'  # From Mailtrap
app.config['MAIL_PASSWORD'] = 'your-mailtrap-password'  # From Mailtrap
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@foodsystem.com'
```

#### **Step 3: Restart Server & Test**
```powershell
# Restart server (Ctrl+C then run again)
python app.py
```

**Emails will appear in Mailtrap inbox (not real inbox)**

---

### **Option 2: Use Gmail (Real Emails)**

#### **Step 1: Enable 2-Step Verification**
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"

#### **Step 2: Generate App Password**
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Click "Generate"
4. Copy the 16-character password (example: `abcd efgh ijkl mnop`)

#### **Step 3: Configure in app.py**
Open `app.py` and change lines 18-24:

```python
# Flask-Mail Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Your Gmail
app.config['MAIL_PASSWORD'] = 'abcd efgh ijkl mnop'  # 16-char app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
```

#### **Step 4: Restart Server**
```powershell
python app.py
```

---

### **Option 3: Environment Variables (Production)**

#### **Windows PowerShell:**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
```

#### **Then restart server:**
```powershell
python app.py
```

---

## 🧪 **Test Email Configuration**

After configuring, test it:

```powershell
python test_email_config.py
```

**Should show:**
```
✅ Email sent successfully!
✅ Email configuration is working correctly!
```

---

## 🎯 **Then Test 2FA**

1. Go to: `http://localhost:5000/auth/profile`
2. Click "Enable" button
3. Enter your password
4. Click "Enable 2FA"
5. **Check Mailtrap inbox or Gmail** for OTP code
6. Enter the 6-digit code
7. Save backup codes!

---

## 📋 **Current Status**

✅ Password field is working (you entered password correctly)  
❌ Email not configured (this is why it failed)  
⏭️ **Next Step:** Configure email using Option 1 or 2 above  

---

## 🆘 **Quick Commands Reference**

### **Check Current Config:**
```powershell
python -c "from app import app; print('Username:', app.config.get('MAIL_USERNAME')); print('Password:', 'SET' if app.config.get('MAIL_PASSWORD') != 'your-app-password' else 'NOT SET')"
```

### **Test Email:**
```powershell
python test_email_config.py
```

---

## 💡 **My Recommendation**

**For Testing/Development:**
- ✅ Use **Mailtrap** (Option 1) - Free, easy, no real email needed

**For Production:**
- ✅ Use **Gmail with App Password** (Option 2)
- ✅ Or use **SendGrid/Mailgun/AWS SES**

---

## 🚀 **After Email Config**

Once email is configured:
1. ✅ 2FA will send OTP codes
2. ✅ Users will receive verification emails
3. ✅ Backup codes will be generated
4. ✅ Login history will be tracked
5. ✅ All 2FA features will work!

---

**Need Help?** Let me know which option you want to use and I can help configure it!

---

**Updated:** October 19, 2025  
**Issue:** Email not configured  
**Fix:** Configure using Option 1 (Mailtrap) or Option 2 (Gmail)  
**Time:** 5 minutes ⚡
