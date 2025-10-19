from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from datetime import datetime, timedelta
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.otp_handler import (
    generate_otp, 
    send_otp_email, 
    is_otp_valid,
    generate_backup_codes,
    hash_backup_codes,
    verify_backup_code
)
from utils.security_utils import (
    log_login_attempt,
    is_device_trusted,
    add_trusted_device,
    check_account_lockout,
    handle_failed_login,
    reset_failed_attempts,
    get_user_login_history,
    get_user_trusted_devices
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        remember_device = request.form.get('remember_device') == 'on'
        
        # Check if input is email (contains @) or username
        if '@' in username_or_email:
            # Login with email
            user = User.query.filter_by(email=username_or_email).first()
        else:
            # Login with username (name field)
            user = User.query.filter_by(name=username_or_email).first()
        
        if user:
            # Check account lockout
            is_locked, remaining_time = check_account_lockout(user)
            if is_locked:
                flash(f'Account locked due to too many failed attempts. Try again in {remaining_time}.', 'danger')
                log_login_attempt(user.user_id, 'locked', 'password', 'account_locked')
                return render_template('auth/login.html')
            
            # Verify password
            if check_password_hash(user.password, password):
                # Check if 2FA is enabled for this user
                if user.two_factor_enabled:
                    # Check if device is trusted
                    if is_device_trusted(user.user_id):
                        # Skip 2FA for trusted device
                        session['user_id'] = user.user_id
                        session['user_name'] = user.name
                        session['user_role'] = user.role
                        
                        # Reset failed attempts and update last login
                        reset_failed_attempts(user)
                        log_login_attempt(user.user_id, 'success', 'password_trusted_device')
                        
                        flash(f'Welcome back, {user.name}! (Trusted Device)', 'success')
                        return redirect(url_for('dashboard'))
                    
                    # Generate OTP for 2FA
                    otp_code = generate_otp()
                    otp_expiry = datetime.now() + timedelta(minutes=5)
                    
                    # Save OTP to database
                    user.otp_code = otp_code
                    user.otp_expiry = otp_expiry
                    
                    try:
                        db.session.commit()
                        
                        # Send OTP via email
                        from app import mail
                        email_sent = send_otp_email(mail, user.email, user.name, otp_code)
                        
                        if email_sent:
                            # Store user_id temporarily for OTP verification
                            session['pending_user_id'] = user.user_id
                            session['otp_attempts'] = 0
                            session['remember_device'] = remember_device
                            flash(f'OTP sent to {user.email}. Please check your email.', 'info')
                            return redirect(url_for('auth.verify_otp'))
                        else:
                            flash('Failed to send OTP. Please try again or contact support.', 'danger')
                            
                    except Exception as e:
                        db.session.rollback()
                        flash('An error occurred. Please try again.', 'danger')
                        print(f"OTP Error: {str(e)}")
                else:
                    # 2FA not enabled, login directly
                    session['user_id'] = user.user_id
                    session['user_name'] = user.name
                    session['user_role'] = user.role
                    
                    # Reset failed attempts and update last login
                    reset_failed_attempts(user)
                    log_login_attempt(user.user_id, 'success', 'password')
                    
                    flash(f'Welcome back, {user.name}!', 'success')
                    return redirect(url_for('dashboard'))
            else:
                # Wrong password - handle failed attempt
                is_now_locked = handle_failed_login(user)
                log_login_attempt(user.user_id, 'failed', 'password', 'wrong_password')
                
                if is_now_locked:
                    flash('Too many failed attempts. Account locked for 30 minutes.', 'danger')
                else:
                    remaining = 5 - user.failed_login_attempts
                    flash(f'Invalid password. {remaining} attempts remaining.', 'danger')
        else:
            flash('Invalid username/email or password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        country_code = request.form.get('country_code', '+91')
        phone_number = request.form.get('phone_number', '')
        # Combine country code with phone number
        phone = country_code + phone_number
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = request.form['address']
        # Always set role to Customer for public registration
        role = 'Customer'
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            role=role,
            password=hashed_password,
            address=address
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """Verify OTP code for two-factor authentication"""
    if 'pending_user_id' not in session:
        flash('Session expired. Please login again.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['pending_user_id'])
    
    if not user:
        session.pop('pending_user_id', None)
        flash('Invalid session. Please login again.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        otp_input = request.form.get('otp_code', '').strip()
        use_backup = request.form.get('use_backup') == 'true'
        
        # Increment attempt counter
        session['otp_attempts'] = session.get('otp_attempts', 0) + 1
        
        # Check if too many attempts
        if session['otp_attempts'] > 5:
            session.pop('pending_user_id', None)
            session.pop('otp_attempts', None)
            flash('Too many failed attempts. Please login again.', 'danger')
            return redirect(url_for('auth.login'))
        
        if use_backup:
            # Verify backup code
            is_valid, remaining_codes = verify_backup_code(user.backup_codes, otp_input)
            
            if is_valid:
                # Update remaining backup codes
                user.backup_codes = remaining_codes
                db.session.commit()
                
                # Login successful
                session['user_id'] = user.user_id
                session['user_name'] = user.name
                session['user_role'] = user.role
                session.pop('pending_user_id', None)
                session.pop('otp_attempts', None)
                
                flash(f'Welcome back, {user.name}! (Backup code used)', 'success')
                
                # Warn if running low on backup codes
                if remaining_codes:
                    remaining_count = len(remaining_codes.split(','))
                    if remaining_count <= 3:
                        flash(f'Warning: You have {remaining_count} backup codes remaining. Generate new ones in your profile.', 'warning')
                else:
                    flash('Warning: No backup codes remaining. Generate new ones immediately in your profile.', 'warning')
                
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid backup code. Please try again.', 'danger')
        else:
            # Verify OTP code
            if not is_otp_valid(user.otp_expiry):
                flash('OTP has expired. Please request a new one.', 'danger')
                log_login_attempt(user.user_id, 'failed', 'otp', 'otp_expired')
            elif user.otp_code == otp_input:
                # OTP is correct
                session['user_id'] = user.user_id
                session['user_name'] = user.name
                session['user_role'] = user.role
                
                # Check if user wants to remember this device
                remember_device = session.get('remember_device', False)
                if remember_device:
                    add_trusted_device(user.user_id, trust_duration_days=30)
                    flash(f'Welcome back, {user.name}! (Device trusted for 30 days)', 'success')
                else:
                    flash(f'Welcome back, {user.name}!', 'success')
                
                # Clear OTP from database
                user.otp_code = None
                user.otp_expiry = None
                
                # Reset failed attempts and update last login
                reset_failed_attempts(user)
                log_login_attempt(user.user_id, 'success', 'otp')
                
                # Clean up session
                session.pop('pending_user_id', None)
                session.pop('otp_attempts', None)
                session.pop('remember_device', None)
                
                db.session.commit()
                
                return redirect(url_for('dashboard'))
            else:
                remaining_attempts = 5 - session['otp_attempts']
                flash(f'Invalid OTP code. {remaining_attempts} attempts remaining.', 'danger')
                log_login_attempt(user.user_id, 'failed', 'otp', 'wrong_otp')
    
    return render_template('auth/verify_otp.html', user=user)

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP code"""
    if 'pending_user_id' not in session:
        return jsonify({'success': False, 'message': 'Session expired. Please login again.'})
    
    user = User.query.get(session['pending_user_id'])
    
    if not user:
        return jsonify({'success': False, 'message': 'Invalid session.'})
    
    # Generate new OTP
    otp_code = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=5)
    
    user.otp_code = otp_code
    user.otp_expiry = otp_expiry
    
    try:
        db.session.commit()
        
        # Send OTP via email
        from app import mail
        email_sent = send_otp_email(mail, user.email, user.name, otp_code)
        
        if email_sent:
            return jsonify({'success': True, 'message': f'New OTP sent to {user.email}'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send OTP. Please try again.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred.'})


@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    return render_template('auth/profile.html', user=user)

@auth_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    user.name = request.form['name']
    user.phone = request.form['phone']
    user.address = request.form['address']
    
    # Update password if provided
    new_password = request.form.get('new_password')
    if new_password:
        current_password = request.form.get('current_password')
        if check_password_hash(user.password, current_password):
            user.password = generate_password_hash(new_password)
        else:
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('auth.profile'))
    
    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Update failed. Please try again.', 'danger')
    
    return redirect(url_for('auth.profile'))

@auth_bp.route('/toggle-2fa', methods=['POST'])
def toggle_2fa():
    """Enable or disable two-factor authentication"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    user = User.query.get(session['user_id'])
    password = request.form.get('password')
    enable = request.form.get('enable') == 'true'
    
    # Verify password
    if not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Incorrect password'})
    
    if enable:
        # Enable 2FA
        if user.two_factor_enabled:
            return jsonify({'success': False, 'message': '2FA is already enabled'})
        
        # Generate test OTP
        otp_code = generate_otp()
        otp_expiry = datetime.now() + timedelta(minutes=5)
        
        user.otp_code = otp_code
        user.otp_expiry = otp_expiry
        
        try:
            db.session.commit()
            
            # Send test OTP
            from app import mail
            email_sent = send_otp_email(mail, user.email, user.name, otp_code)
            
            if email_sent:
                # Store verification session
                session['2fa_setup_user_id'] = user.user_id
                return jsonify({
                    'success': True, 
                    'message': f'Verification code sent to {user.email}',
                    'verify_required': True
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to send verification email'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'An error occurred'})
    else:
        # Disable 2FA
        if not user.two_factor_enabled:
            return jsonify({'success': False, 'message': '2FA is already disabled'})
        
        user.two_factor_enabled = False
        user.otp_code = None
        user.otp_expiry = None
        user.backup_codes = None
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': '2FA has been disabled'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Failed to disable 2FA'})

@auth_bp.route('/verify-2fa-setup', methods=['POST'])
def verify_2fa_setup():
    """Verify OTP to complete 2FA setup"""
    try:
        if '2fa_setup_user_id' not in session:
            return jsonify({'success': False, 'message': 'Invalid setup session'}), 400
        
        user = User.query.get(session['2fa_setup_user_id'])
        otp_input = request.form.get('otp_code', '').strip()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Verify OTP
        if not is_otp_valid(user.otp_expiry):
            return jsonify({'success': False, 'message': 'OTP has expired. Please try again.'}), 400
        
        if user.otp_code == otp_input:
            # Enable 2FA
            user.two_factor_enabled = True
            user.otp_code = None
            user.otp_expiry = None
            
            # Generate backup codes
            backup_codes = generate_backup_codes(10)
            user.backup_codes = hash_backup_codes(backup_codes)
            
            try:
                db.session.commit()
                session.pop('2fa_setup_user_id', None)
                
                return jsonify({
                    'success': True, 
                    'message': '2FA enabled successfully',
                    'backup_codes': backup_codes
                }), 200
            except Exception as e:
                db.session.rollback()
                print(f"Database error: {e}")
                return jsonify({'success': False, 'message': 'Failed to enable 2FA'}), 500
        else:
            return jsonify({'success': False, 'message': f'Invalid OTP code. You entered: {otp_input}, Expected: {user.otp_code}'}), 400
    except Exception as e:
        print(f"Error in verify_2fa_setup: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@auth_bp.route('/regenerate-backup-codes', methods=['POST'])
def regenerate_backup_codes():
    """Generate new backup codes"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    user = User.query.get(session['user_id'])
    password = request.form.get('password')
    
    # Verify password
    if not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Incorrect password'})
    
    if not user.two_factor_enabled:
        return jsonify({'success': False, 'message': '2FA is not enabled'})
    
    # Generate new backup codes
    backup_codes = generate_backup_codes(10)
    user.backup_codes = hash_backup_codes(backup_codes)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'New backup codes generated',
            'backup_codes': backup_codes
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to generate backup codes'})