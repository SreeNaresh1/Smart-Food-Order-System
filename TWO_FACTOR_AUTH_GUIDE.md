# Two-Factor Authentication (2FA) Implementation Guide

## 🔐 Overview

The Food Order System now includes **Two-Factor Authentication (2FA)** for enhanced account security. When enabled, users will need to enter a one-time code sent to their email in addition to their password when logging in.

---

## ✨ Features Implemented

### 1. **Email-Based OTP Authentication**
- 6-digit numeric OTP codes
- 5-minute validity period
- Beautiful HTML email templates
- Automatic expiry and resend functionality

### 2. **Backup Codes**
- 10 unique backup codes per user
- One-time use only
- Secure hashed storage
- Download and print functionality
- Regeneration capability

### 3. **User-Friendly Interface**
- Modern OTP verification page
- Real-time countdown timers
- Auto-submit when 6 digits entered
- Resend code functionality
- Backup code fallback option

### 4. **Security Features**
- Password confirmation for all 2FA changes
- Maximum 5 OTP attempts before lockout
- Secure OTP storage with expiry
- Encrypted backup code storage
- Session-based temporary authentication

---

## 📋 Database Changes

### New Fields Added to `User` Model:
```python
two_factor_enabled = db.Column(db.Boolean, default=False)  # 2FA on/off switch
otp_code = db.Column(db.String(6), nullable=True)          # Current OTP code
otp_expiry = db.Column(db.DateTime, nullable=True)         # OTP expiration time
backup_codes = db.Column(db.Text, nullable=True)           # Hashed backup codes (comma-separated)
```

---

## 🚀 How to Use 2FA

### **For Users:**

#### **Enabling 2FA:**
1. Login to your account
2. Go to **Profile** page
3. Find the **Two-Factor Authentication** section
4. Click **Enable** button
5. Enter your password
6. Check your email for verification code
7. Enter the 6-digit code
8. **Save your backup codes!** (Download or print them)
9. 2FA is now active ✅

#### **Logging In with 2FA:**
1. Enter username/email and password
2. Click **Login**
3. Check your email for OTP code
4. Enter the 6-digit code on verification page
5. Click **Verify & Login**
6. You're in! 🎉

#### **Using Backup Codes:**
- On OTP verification page, click **"Use Backup Code"**
- Enter one of your saved backup codes
- Each code can only be used **once**
- Generate new codes from your profile when running low

#### **Disabling 2FA:**
1. Go to **Profile** page
2. Find the **Two-Factor Authentication** section
3. Click **Disable** button
4. Enter your password
5. Confirm the action
6. 2FA is now disabled

#### **Regenerating Backup Codes:**
1. Go to **Profile** page
2. Click **"View/Regenerate Backup Codes"**
3. Enter your password
4. Click **"Generate New Codes"**
5. Download or print the new codes
6. Old backup codes are **invalidated**

---

## 📧 Email Configuration

### **Setup Instructions:**

#### **Option 1: Gmail (Recommended for Testing)**

1. **Enable 2-Step Verification** on your Google Account
2. **Generate an App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password

3. **Set Environment Variables:**

**Windows PowerShell:**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
```

**Windows Command Prompt:**
```cmd
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-app-password
```

**Or edit `app.py` directly (lines 19-22):**
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
```

#### **Option 2: Other Email Providers**

**Outlook/Hotmail:**
```python
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
```

**Yahoo:**
```python
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
```

**Custom SMTP:**
```python
app.config['MAIL_SERVER'] = 'your-smtp-server.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True  # or False
app.config['MAIL_USE_SSL'] = False  # or True for port 465
```

---

## 🔧 Technical Implementation

### **New Files Created:**

1. **`utils/otp_handler.py`** - OTP utility functions
   - `generate_otp()` - Generate 6-digit OTP
   - `send_otp_email()` - Send OTP via email
   - `is_otp_valid()` - Check OTP expiry
   - `generate_backup_codes()` - Create backup codes
   - `hash_backup_codes()` - Secure storage
   - `verify_backup_code()` - Validate backup codes

2. **`templates/auth/verify_otp.html`** - OTP verification page
   - Beautiful gradient design
   - Real-time countdown timers
   - Auto-submit functionality
   - Backup code fallback
   - Resend code button

### **Modified Files:**

1. **`models.py`**
   - Added 2FA fields to User model

2. **`app.py`**
   - Added Flask-Mail configuration
   - Imported Mail extension

3. **`routes/auth.py`**
   - Modified login route for 2FA check
   - Added OTP verification route
   - Added resend OTP route
   - Added 2FA toggle routes
   - Added backup code management

4. **`templates/auth/profile.html`**
   - Added 2FA management section
   - Added modals for enabling/disabling
   - Added backup code viewer
   - JavaScript for AJAX operations

5. **`requirements.txt`**
   - Added Flask-Mail==0.9.1

---

## 🎨 Email Template Design

The OTP email includes:
- **Beautiful gradient header** (purple theme)
- **Large, easy-to-read OTP code**
- **Expiry countdown** (5 minutes)
- **Security warnings and tips**
- **Professional footer**
- **Both HTML and plain text** versions

---

## 🔒 Security Features

### **Protection Mechanisms:**

1. **Password Verification** - All 2FA changes require password
2. **OTP Expiry** - Codes expire after 5 minutes
3. **Attempt Limiting** - Maximum 5 failed OTP attempts
4. **Secure Storage** - Backup codes hashed with Werkzeug
5. **One-Time Use** - Backup codes can't be reused
6. **Session Security** - Temporary session for pending logins
7. **Code Regeneration** - Invalidates old backup codes

### **Attack Prevention:**

- **Brute Force** - Limited attempts + expiry time
- **Code Reuse** - OTP cleared after successful login
- **Session Hijacking** - Separate pending session
- **Email Interception** - Time-limited codes
- **Backup Code Theft** - Hashed storage + one-time use

---

## 📊 User Experience Flow

```
┌─────────────────┐
│  Login Page     │
│  (Email/Pass)   │
└────────┬────────┘
         │
         ▼
    ┌────────────┐
    │ 2FA Check? │
    └──┬─────┬───┘
       │     │
    Yes│     │No
       │     │
       ▼     ▼
  ┌────────┐  ┌──────────┐
  │ Send   │  │ Dashboard│
  │ OTP    │  └──────────┘
  └───┬────┘
      │
      ▼
  ┌────────────────┐
  │ OTP Verify     │
  │ Page           │
  └───┬────┬───────┘
      │    │
   Valid│  │Backup
      │    │Code
      ▼    ▼
  ┌──────────────┐
  │  Dashboard   │
  └──────────────┘
```

---

## 🧪 Testing Checklist

### **Basic Functionality:**
- [ ] Enable 2FA from profile
- [ ] Receive OTP email
- [ ] Verify OTP code successfully
- [ ] Receive backup codes
- [ ] Login with OTP
- [ ] Login with backup code
- [ ] Resend OTP works
- [ ] Disable 2FA works

### **Security Tests:**
- [ ] Wrong password blocks 2FA toggle
- [ ] Invalid OTP shows error
- [ ] Expired OTP rejected
- [ ] Maximum attempts lockout works
- [ ] Backup code single-use enforced
- [ ] Regenerate backup codes works

### **Email Tests:**
- [ ] OTP email delivered
- [ ] Email formatting correct
- [ ] HTML version displays
- [ ] Plain text fallback works
- [ ] Sender address correct

### **Edge Cases:**
- [ ] User without 2FA can login normally
- [ ] Session expires properly
- [ ] Browser back button handled
- [ ] Multiple simultaneous OTPs
- [ ] Email failure handled gracefully

---

## 🐛 Troubleshooting

### **Problem: OTP email not received**
**Solutions:**
1. Check spam/junk folder
2. Verify email configuration in app.py
3. Check environment variables
4. Test SMTP connection
5. Enable "Less secure app access" (Gmail)
6. Use App Password instead of regular password

### **Problem: "Invalid OTP" error**
**Solutions:**
1. Check if code expired (5 minutes)
2. Verify exact digits (no spaces)
3. Request new code with resend button
4. Check system time is correct

### **Problem: Too many attempts lockout**
**Solutions:**
1. Wait 5 minutes for code expiry
2. Start new login session
3. Use backup code instead
4. Contact admin for assistance

### **Problem: Backup codes not working**
**Solutions:**
1. Enter uppercase letters
2. Remove any spaces
3. Verify code hasn't been used
4. Regenerate new backup codes

### **Problem: Email sending fails**
**Solutions:**
1. Check SMTP credentials
2. Verify network connection
3. Check firewall settings
4. Test with different email provider
5. Review app.py mail configuration

---

## 📝 Database Migration (If Needed)

If you have existing users and need to add 2FA fields:

```python
from app import app, db
from models import User

with app.app_context():
    # This will add new columns automatically
    db.create_all()
    
    # Or manually with SQLAlchemy-Migrate/Alembic
```

**Or manually via SQLite:**
```sql
ALTER TABLE user ADD COLUMN two_factor_enabled BOOLEAN DEFAULT 0;
ALTER TABLE user ADD COLUMN otp_code VARCHAR(6);
ALTER TABLE user ADD COLUMN otp_expiry DATETIME;
ALTER TABLE user ADD COLUMN backup_codes TEXT;
```

---

## 🎯 Future Enhancements

### **Planned Features:**
1. **SMS OTP** - Send codes via SMS (Twilio integration)
2. **Authenticator Apps** - Google Authenticator, Authy support
3. **Trusted Devices** - Remember devices for 30 days
4. **Email Alerts** - Notify on successful/failed login attempts
5. **Login History** - View recent login activity
6. **Recovery Email** - Alternative email for account recovery
7. **Biometric 2FA** - Fingerprint/Face ID support
8. **Admin Override** - Emergency 2FA bypass for admins

### **Security Improvements:**
1. **IP Whitelisting** - Allow specific IPs without 2FA
2. **Geographic Restrictions** - Block logins from unusual locations
3. **Device Fingerprinting** - Track and verify devices
4. **Rate Limiting** - Global login attempt limits
5. **CAPTCHA** - Add after failed attempts

---

## 📞 Support & Contact

### **For Users:**
- Check your spam folder first
- Use backup codes if email fails
- Contact system administrator for help
- Review this documentation

### **For Administrators:**
- Review email configuration
- Check user's 2FA status in database
- Can manually disable 2FA if needed
- Monitor failed login attempts

---

## 📄 License & Credits

**Implemented by:** GitHub Copilot AI Assistant  
**Date:** 2024  
**Version:** 1.0.0  

**Dependencies:**
- Flask-Mail 0.9.1
- Flask 3.0.0
- SQLAlchemy 2.0.23
- Werkzeug 3.0.1

---

## ✅ Summary

The Two-Factor Authentication system provides enterprise-grade security with minimal user friction. Users can enable/disable 2FA at will, use backup codes for recovery, and receive OTP codes via email with beautiful templates.

**Key Benefits:**
- ✅ Enhanced account security
- ✅ Protection against password theft
- ✅ User-controlled (optional)
- ✅ Multiple fallback options
- ✅ Beautiful user interface
- ✅ Professional email templates
- ✅ Comprehensive backup system

**Next Steps:**
1. Configure email settings
2. Test 2FA flow end-to-end
3. Educate users about 2FA
4. Monitor adoption rates
5. Collect user feedback

---

**🎉 2FA Implementation Complete!**
