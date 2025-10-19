"""
OTP Handler - Two-Factor Authentication Utilities
Handles OTP generation, validation, and email sending
"""

import random
import string
from datetime import datetime, timedelta
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash


def generate_otp(length=6):
    """
    Generate a random numeric OTP code
    
    Args:
        length (int): Length of OTP code (default: 6)
    
    Returns:
        str: Random numeric OTP code
    """
    return ''.join(random.choices(string.digits, k=length))


def generate_backup_codes(count=10):
    """
    Generate backup codes for account recovery
    
    Args:
        count (int): Number of backup codes to generate (default: 10)
    
    Returns:
        list: List of backup codes (8 characters each, alphanumeric)
    """
    codes = []
    for _ in range(count):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        codes.append(code)
    return codes


def hash_backup_codes(codes):
    """
    Hash backup codes for secure storage
    
    Args:
        codes (list): List of plain backup codes
    
    Returns:
        str: Comma-separated hashed codes
    """
    hashed = [generate_password_hash(code) for code in codes]
    return ','.join(hashed)


def verify_backup_code(stored_codes, input_code):
    """
    Verify a backup code against stored hashed codes
    
    Args:
        stored_codes (str): Comma-separated hashed backup codes
        input_code (str): Plain backup code to verify
    
    Returns:
        tuple: (bool: is_valid, str: remaining_codes or None)
    """
    if not stored_codes or not input_code:
        return False, None
    
    hashed_codes = stored_codes.split(',')
    
    for i, hashed_code in enumerate(hashed_codes):
        if check_password_hash(hashed_code, input_code.upper()):
            # Remove used code
            hashed_codes.pop(i)
            remaining = ','.join(hashed_codes) if hashed_codes else None
            return True, remaining
    
    return False, None


def send_otp_email(mail, recipient_email, recipient_name, otp_code, expiry_minutes=5):
    """
    Send OTP code via email
    
    Args:
        mail: Flask-Mail instance
        recipient_email (str): Email address to send OTP to
        recipient_name (str): Name of the recipient
        otp_code (str): OTP code to send
        expiry_minutes (int): OTP validity duration (default: 5 minutes)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject='Your Login OTP Code - Food Order System',
            recipients=[recipient_email]
        )
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f7fa;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .otp-box {{
                    background: #f8f9fa;
                    border: 2px dashed #667eea;
                    border-radius: 8px;
                    padding: 25px;
                    text-align: center;
                    margin: 25px 0;
                }}
                .otp-code {{
                    font-size: 42px;
                    font-weight: bold;
                    color: #667eea;
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                }}
                .warning {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                }}
                .icon {{
                    font-size: 48px;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="icon">🔐</div>
                    <h1>Two-Factor Authentication</h1>
                </div>
                <div class="content">
                    <h2 style="color: #333;">Hello {recipient_name},</h2>
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        You have requested to log in to your Food Order System account. 
                        Please use the following One-Time Password (OTP) to complete your login:
                    </p>
                    
                    <div class="otp-box">
                        <div style="color: #666; font-size: 14px; margin-bottom: 10px;">Your OTP Code</div>
                        <div class="otp-code">{otp_code}</div>
                        <div style="color: #666; font-size: 14px; margin-top: 10px;">
                            Valid for {expiry_minutes} minutes
                        </div>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>This code will expire in {expiry_minutes} minutes</li>
                            <li>Never share this code with anyone</li>
                            <li>Our team will never ask for your OTP code</li>
                            <li>If you didn't request this, please ignore this email</li>
                        </ul>
                    </div>
                    
                    <p style="font-size: 14px; color: #666; margin-top: 30px;">
                        If you're having trouble logging in, please contact our support team.
                    </p>
                </div>
                <div class="footer">
                    <p style="margin: 5px 0;">Food Order System</p>
                    <p style="margin: 5px 0;">This is an automated message, please do not reply.</p>
                    <p style="margin: 5px 0;">&copy; 2024 All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.body = f"""
        Hello {recipient_name},
        
        Your OTP code for login is: {otp_code}
        
        This code will expire in {expiry_minutes} minutes.
        
        Security Notice:
        - Never share this code with anyone
        - Our team will never ask for your OTP code
        - If you didn't request this, please ignore this email
        
        Food Order System
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return False


def is_otp_valid(otp_expiry):
    """
    Check if OTP is still valid (not expired)
    
    Args:
        otp_expiry (datetime): OTP expiration datetime
    
    Returns:
        bool: True if OTP is still valid, False otherwise
    """
    if not otp_expiry:
        return False
    
    current_time = datetime.now()
    
    # Debug logging
    print(f"🕒 OTP Validation Check:")
    print(f"   Current time: {current_time}")
    print(f"   OTP expiry:   {otp_expiry}")
    print(f"   Is valid:     {current_time < otp_expiry}")
    print(f"   Time remaining: {(otp_expiry - current_time).total_seconds()} seconds")
    
    return current_time < otp_expiry
