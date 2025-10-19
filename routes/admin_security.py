"""
Admin routes for security and 2FA management
"""
from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, User, LoginHistory
from datetime import datetime
from utils.security_utils import get_2fa_statistics

admin_security_bp = Blueprint('admin_security', __name__)


def require_admin():
    """Decorator to ensure user is admin"""
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    
    return None


@admin_security_bp.route('/admin/security-dashboard')
def security_dashboard():
    """Display 2FA and security statistics dashboard"""
    # Check admin access
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    # Get statistics
    stats = get_2fa_statistics()
    
    # Get recent login activity (last 50 logins)
    recent_logins = LoginHistory.query.order_by(
        LoginHistory.login_time.desc()
    ).limit(50).all()
    
    # Get all users for 2FA status overview
    users = User.query.order_by(User.name).all()
    
    return render_template(
        'admin/security_dashboard.html',
        stats=stats,
        recent_logins=recent_logins,
        users=users,
        now=datetime.now()
    )


@admin_security_bp.route('/admin/user-security/<int:user_id>')
def user_security_detail(user_id):
    """View detailed security info for a specific user"""
    # Check admin access
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response
    
    user = User.query.get_or_404(user_id)
    
    # Get user's login history
    login_history = LoginHistory.query.filter_by(
        user_id=user_id
    ).order_by(
        LoginHistory.login_time.desc()
    ).limit(20).all()
    
    # Get user's trusted devices
    from utils.security_utils import get_user_trusted_devices
    trusted_devices = get_user_trusted_devices(user_id)
    
    return render_template(
        'admin/user_security_detail.html',
        user=user,
        login_history=login_history,
        trusted_devices=trusted_devices,
        now=datetime.now()
    )
