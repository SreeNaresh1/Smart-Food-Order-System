"""
Enhanced Security Utilities for 2FA System
Handles login history, device trust, and account lockout
"""

import hashlib
from datetime import datetime, timedelta
from flask import request
from models import db, LoginHistory, TrustedDevice


def get_device_fingerprint():
    """
    Generate a unique device fingerprint based on user agent and other factors
    
    Returns:
        str: Hashed device fingerprint
    """
    user_agent = request.headers.get('User-Agent', '')
    # In production, you might want to add more factors like screen resolution, timezone, etc.
    fingerprint = f"{user_agent}"
    return hashlib.sha256(fingerprint.encode()).hexdigest()


def get_client_ip():
    """
    Get client's IP address considering proxies
    
    Returns:
        str: Client IP address
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr


def get_device_name():
    """
    Extract a friendly device name from user agent
    
    Returns:
        str: Readable device name
    """
    user_agent = request.headers.get('User-Agent', '')
    
    # Detect browser
    if 'Chrome' in user_agent and 'Edg' not in user_agent:
        browser = 'Chrome'
    elif 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edg' in user_agent:
        browser = 'Edge'
    else:
        browser = 'Unknown Browser'
    
    # Detect OS
    if 'Windows' in user_agent:
        os = 'Windows'
    elif 'Mac' in user_agent:
        os = 'macOS'
    elif 'Linux' in user_agent:
        os = 'Linux'
    elif 'Android' in user_agent:
        os = 'Android'
    elif 'iPhone' in user_agent or 'iPad' in user_agent:
        os = 'iOS'
    else:
        os = 'Unknown OS'
    
    return f"{browser} on {os}"


def log_login_attempt(user_id, status, login_method='password', failure_reason=None):
    """
    Log a login attempt to the database
    
    Args:
        user_id (int): User ID attempting login
        status (str): 'success', 'failed', or 'locked'
        login_method (str): 'password', 'otp', or 'backup_code'
        failure_reason (str): Reason for failure if applicable
    
    Returns:
        LoginHistory: The created login history record
    """
    history = LoginHistory(
        user_id=user_id,
        login_time=datetime.now(),
        ip_address=get_client_ip(),
        user_agent=request.headers.get('User-Agent', '')[:255],
        login_method=login_method,
        status=status,
        failure_reason=failure_reason,
        device_fingerprint=get_device_fingerprint()
    )
    
    db.session.add(history)
    db.session.commit()
    
    return history


def is_device_trusted(user_id):
    """
    Check if the current device is trusted for this user
    
    Args:
        user_id (int): User ID to check
    
    Returns:
        bool: True if device is trusted and not expired
    """
    fingerprint = get_device_fingerprint()
    
    device = TrustedDevice.query.filter_by(
        user_id=user_id,
        device_fingerprint=fingerprint,
        is_active=True
    ).first()
    
    if device:
        # Check if device trust has expired
        if device.expires_at > datetime.now():
            # Update last used time
            device.last_used = datetime.now()
            db.session.commit()
            return True
        else:
            # Trust has expired, deactivate it
            device.is_active = False
            db.session.commit()
    
    return False


def add_trusted_device(user_id, trust_duration_days=30):
    """
    Mark the current device as trusted
    
    Args:
        user_id (int): User ID
        trust_duration_days (int): Number of days to trust this device
    
    Returns:
        TrustedDevice: The created trusted device record
    """
    fingerprint = get_device_fingerprint()
    
    # Check if device already exists
    device = TrustedDevice.query.filter_by(
        user_id=user_id,
        device_fingerprint=fingerprint
    ).first()
    
    if device:
        # Update existing device
        device.is_active = True
        device.last_used = datetime.now()
        device.expires_at = datetime.now() + timedelta(days=trust_duration_days)
        device.device_name = get_device_name()
        device.ip_address = get_client_ip()
    else:
        # Create new trusted device
        device = TrustedDevice(
            user_id=user_id,
            device_fingerprint=fingerprint,
            device_name=get_device_name(),
            trusted_at=datetime.now(),
            last_used=datetime.now(),
            expires_at=datetime.now() + timedelta(days=trust_duration_days),
            ip_address=get_client_ip(),
            is_active=True
        )
        db.session.add(device)
    
    db.session.commit()
    return device


def remove_trusted_device(user_id, device_id):
    """
    Remove a trusted device
    
    Args:
        user_id (int): User ID
        device_id (int): Device ID to remove
    
    Returns:
        bool: True if device was removed
    """
    device = TrustedDevice.query.filter_by(
        device_id=device_id,
        user_id=user_id
    ).first()
    
    if device:
        db.session.delete(device)
        db.session.commit()
        return True
    
    return False


def check_account_lockout(user):
    """
    Check if account is locked due to failed attempts
    
    Args:
        user: User model instance
    
    Returns:
        tuple: (is_locked: bool, remaining_time: str or None)
    """
    if user.account_locked_until:
        if user.account_locked_until > datetime.now():
            remaining = user.account_locked_until - datetime.now()
            minutes = int(remaining.total_seconds() / 60)
            return True, f"{minutes} minutes"
        else:
            # Lockout expired, reset
            user.account_locked_until = None
            user.failed_login_attempts = 0
            db.session.commit()
    
    return False, None


def handle_failed_login(user, max_attempts=5, lockout_duration_minutes=30):
    """
    Handle a failed login attempt and potentially lock the account
    
    Args:
        user: User model instance
        max_attempts (int): Maximum failed attempts before lockout
        lockout_duration_minutes (int): Duration of lockout in minutes
    
    Returns:
        bool: True if account is now locked
    """
    user.failed_login_attempts += 1
    
    if user.failed_login_attempts >= max_attempts:
        user.account_locked_until = datetime.now() + timedelta(minutes=lockout_duration_minutes)
        db.session.commit()
        log_login_attempt(user.user_id, 'locked', failure_reason='too_many_attempts')
        return True
    
    db.session.commit()
    return False


def reset_failed_attempts(user):
    """
    Reset failed login attempts after successful login
    
    Args:
        user: User model instance
    """
    user.failed_login_attempts = 0
    user.account_locked_until = None
    user.last_login = datetime.now()
    db.session.commit()


def get_user_login_history(user_id, limit=10):
    """
    Get recent login history for a user
    
    Args:
        user_id (int): User ID
        limit (int): Number of recent logins to retrieve
    
    Returns:
        list: List of LoginHistory records
    """
    return LoginHistory.query.filter_by(
        user_id=user_id
    ).order_by(
        LoginHistory.login_time.desc()
    ).limit(limit).all()


def get_user_trusted_devices(user_id):
    """
    Get all active trusted devices for a user
    
    Args:
        user_id (int): User ID
    
    Returns:
        list: List of TrustedDevice records
    """
    return TrustedDevice.query.filter_by(
        user_id=user_id,
        is_active=True
    ).order_by(
        TrustedDevice.last_used.desc()
    ).all()


def get_2fa_statistics():
    """
    Get 2FA statistics for admin dashboard
    
    Returns:
        dict: Statistics about 2FA usage
    """
    from models import User
    
    total_users = User.query.count()
    users_with_2fa = User.query.filter_by(two_factor_enabled=True).count()
    
    # Recent login attempts (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    recent_logins = LoginHistory.query.filter(
        LoginHistory.login_time >= yesterday
    ).count()
    
    recent_failed = LoginHistory.query.filter(
        LoginHistory.login_time >= yesterday,
        LoginHistory.status == 'failed'
    ).count()
    
    active_devices = TrustedDevice.query.filter_by(is_active=True).count()
    
    # Lockout count (last 24 hours)
    locked_accounts = LoginHistory.query.filter(
        LoginHistory.login_time >= yesterday,
        LoginHistory.status == 'locked'
    ).distinct(LoginHistory.user_id).count()
    
    return {
        'total_users': total_users,
        'users_with_2fa': users_with_2fa,
        '2fa_adoption_rate': round((users_with_2fa / total_users * 100), 1) if total_users > 0 else 0,
        'recent_logins_24h': recent_logins,
        'recent_failed_24h': recent_failed,
        'active_trusted_devices': active_devices,
        'locked_accounts_24h': locked_accounts
    }
