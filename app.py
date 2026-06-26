from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import sqlite3
from functools import wraps

# Create Flask app
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'astrostarnaresh@gmail.com'
app.config['MAIL_PASSWORD'] = 'fjjytitmbavpfzkh'
app.config['MAIL_DEFAULT_SENDER'] = 'astrostarnaresh@gmail.com'

# Initialize extensions
mail = Mail(app)

# Import models first
from backend.models import db, User, Order, OrderDetails, MenuItem, Payment, Feedback, Delivery, KitchenStaff, Recommendation

# Initialize SQLAlchemy with app
db.init_app(app)

# Import blueprints after db initialization
from backend.routes.auth import auth_bp
from backend.routes.menu import menu_bp
from backend.routes.orders import orders_bp
from backend.routes.users import users_bp
from backend.routes.payments import payments_bp
from backend.routes.feedback import feedback_bp
from backend.routes.delivery import delivery_bp
from backend.routes.kitchen import kitchen_bp
from backend.routes.recommendations import recommendations_bp
from backend.routes.reports import reports_bp
from backend.routes.admin_security import admin_security_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(menu_bp, url_prefix='/menu')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(payments_bp, url_prefix='/payments')
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(delivery_bp, url_prefix='/delivery')
app.register_blueprint(kitchen_bp, url_prefix='/kitchen')
app.register_blueprint(recommendations_bp, url_prefix='/recommendations')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(admin_security_bp)

# Test route for 2FA modal
@app.route('/test-modal')
def test_modal():
    """Test page for 2FA modal input functionality"""
    return render_template('test_modal.html')

# Disable caching for development (helps with seeing CSS/JS changes immediately)
@app.after_request
def add_header(response):
    """Add headers to prevent aggressive browser caching during development"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Enhanced role required decorator with logging and security
def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Get user from database
            user = User.query.get(session['user_id'])
            if not user:
                flash('User not found. Please log in again.', 'danger')
                session.clear()
                return redirect(url_for('auth.login'))
            
            # Check if user role is allowed (case-insensitive)
            user_role = user.role.lower()
            allowed_roles_lower = [role.lower() for role in allowed_roles]
            
            if user_role not in allowed_roles_lower:
                flash(f'Access denied. This page requires {", ".join(allowed_roles)} privileges.', 'danger')
                # Log unauthorized access attempt
                print(f"⚠️ Unauthorized access attempt: User '{user.name}' ({user_role}) tried to access {request.endpoint}")
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    role = user.role.lower()
    
    # Get statistics based on role
    stats = {}
    
    if role in ['admin', 'supervisor']:
        stats['total_users'] = User.query.count()
        stats['total_orders'] = Order.query.count()
        stats['total_menu_items'] = MenuItem.query.count()
        stats['pending_orders'] = Order.query.filter_by(status='Pending').count()
        stats['confirmed_orders'] = Order.query.filter_by(status='Confirmed').count()
        stats['preparing_orders'] = Order.query.filter_by(status='Preparing').count()
        stats['ready_orders'] = Order.query.filter_by(status='Ready').count()
        stats['delivered_orders'] = Order.query.filter_by(status='Delivered').count()
        
        # Calculate total revenue
        delivered_orders = Order.query.filter_by(status='Delivered').all()
        stats['total_revenue'] = sum([float(order.total_amount) for order in delivered_orders])
        
        # Recent orders for management overview
        stats['recent_orders'] = Order.query.order_by(Order.order_date.desc()).limit(10).all()
        
        # Supervisor-specific data
        if role == 'supervisor':
            # Employee monitoring data
            stats['employees'] = User.query.filter(User.role.in_(['employee', 'staff'])).all()
            stats['total_employees'] = len(stats['employees'])
            
            # Add performance metrics to employees
            for employee in stats['employees']:
                employee.assigned_orders = Order.query.filter(
                    Order.status.in_(['Confirmed', 'Preparing']),
                    Order.assigned_to == employee.user_id if hasattr(Order, 'assigned_to') else True
                ).count()
                employee.performance_score = 85 + (employee.user_id % 15)  # Simulated performance
            
            # Performance metrics
            stats['completion_rate'] = 95
            stats['satisfaction_rate'] = 88
            stats['delivery_rate'] = 92
            stats['active_staff'] = stats['total_employees']
        
    elif role == 'employee':
        # Employee dashboard - focus on assigned orders and tasks
        stats['assigned_orders'] = Order.query.filter(Order.status.in_(['Confirmed', 'Preparing', 'Ready'])).count()
        stats['pending_tasks'] = Order.query.filter(Order.status.in_(['Confirmed', 'Preparing'])).count()
        stats['preparing_orders'] = Order.query.filter_by(status='Preparing').count()
        stats['ready_orders'] = Order.query.filter_by(status='Ready').count()
        
        # My assigned orders (show all active orders for employees to work on)
        stats['my_orders'] = Order.query.filter(
            Order.status.in_(['Confirmed', 'Preparing', 'Ready', 'Delivered'])
        ).order_by(Order.order_date.desc()).limit(15).all()
        
        # Today's performance
        from datetime import date
        today = date.today()
        stats['completed_today'] = Order.query.filter(
            Order.status == 'Delivered',
            Order.order_date >= datetime.combine(today, datetime.min.time())
        ).count()
        
        # Performance metrics (simulated for now)
        stats['performance_score'] = 88
        stats['completion_rate'] = 95
        stats['ontime_rate'] = 88
        stats['satisfaction_rate'] = 92
        
        # Recent activity
        stats['recent_activity'] = [
            {'time': 'Just now', 'description': 'Logged in to system'},
            {'time': '10 mins ago', 'description': f'Completed {stats["completed_today"]} orders today'}
        ]
        
    elif role == 'customer':
        # Total orders count
        stats['total_orders'] = Order.query.filter_by(user_id=user.user_id).count()
        stats['my_orders'] = stats['total_orders']  # Keep for backward compatibility
        
        # Pending orders count
        stats['pending_orders'] = Order.query.filter_by(
            user_id=user.user_id
        ).filter(
            Order.status.in_(['Pending', 'Confirmed', 'Preparing', 'Ready'])
        ).count()
        
        stats['recent_orders'] = Order.query.filter_by(user_id=user.user_id).order_by(Order.order_date.desc()).limit(5).all()
        
        # Calculate total spent by customer
        customer_orders = Order.query.filter_by(user_id=user.user_id, status='Delivered').all()
        stats['total_spent'] = sum([float(order.total_amount) for order in customer_orders])
        
        # Get recommendations for customer
        try:
            from backend.routes.recommendations import get_user_recommendations
            recommendations = get_user_recommendations(user.user_id)
            stats['recommendations'] = recommendations[:5]  # Top 5 recommendations
        except:
            stats['recommendations'] = []
        
        # Customer's favorite items (most ordered)
        from sqlalchemy import func
        favorite_items_query = db.session.query(
            MenuItem, func.sum(OrderDetails.quantity).label('total_ordered')
        ).join(OrderDetails).join(Order).filter(
            Order.user_id == user.user_id
        ).group_by(MenuItem.menu_item_id).order_by(
            func.sum(OrderDetails.quantity).desc()
        ).limit(5).all()
        
        stats['favorite_items'] = favorite_items_query
        stats['favorite_count'] = len(favorite_items_query)
        
        # Check if there are active orders for auto-refresh
        active_statuses = ['Confirmed', 'Preparing', 'Ready']
        stats['has_active_orders'] = any(
            order.status in active_statuses for order in stats.get('recent_orders', [])
        ) if stats.get('recent_orders') else False
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Return role-specific template
    if role == 'admin':
        return render_template('dashboard.html', user=user, stats=stats, current_time=current_time)
    elif role == 'supervisor':
        return render_template('dashboards/supervisor.html', user=user, stats=stats, current_time=current_time)
    elif role == 'employee':
        return render_template('dashboards/employee.html', user=user, stats=stats, current_time=current_time)
    else:  # customer
        # Prepare favorites for display
        favorites = [item[0] for item in stats.get('favorite_items', [])]
        recent_orders = stats.get('recent_orders', [])
        return render_template('dashboards/customer.html', 
                             user=user, 
                             stats=stats, 
                             favorites=favorites,
                             recent_orders=recent_orders,
                             current_time=current_time)

# Initialize database
def init_db():
    """Initialize database and create default admin and supervisor users"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin_user = User.query.filter_by(email='admin@foodsystem.com').first()
        if not admin_user:
            admin = User(
                name='System Administrator',
                email='admin@foodsystem.com',
                phone='1234567890',
                role='Admin',
                password=generate_password_hash('admin123'),
                address='System Address'
            )
            db.session.add(admin)
            print("✅ Default admin user created: admin@foodsystem.com / admin123")
        
        # Create default supervisor user if not exists
        supervisor_user = User.query.filter_by(email='supervisor@foodsystem.com').first()
        if not supervisor_user:
            supervisor = User(
                name='Branch Supervisor',
                email='supervisor@foodsystem.com',
                phone='9876543210',
                role='Supervisor',
                password=generate_password_hash('supervisor123'),
                address='Branch Office'
            )
            db.session.add(supervisor)
            print("✅ Default supervisor user created: supervisor@foodsystem.com / supervisor123")
        
        # Create default employee user if not exists
        employee_user = User.query.filter_by(email='employee@foodsystem.com').first()
        if not employee_user:
            employee = User(
                name='Staff Employee',
                email='employee@foodsystem.com',
                phone='5555555555',
                role='Employee',
                password=generate_password_hash('employee123'),
                address='Staff Quarters'
            )
            db.session.add(employee)
            print("✅ Default employee user created: employee@foodsystem.com / employee123")
        
        db.session.commit()

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    print("Smart Food Ordering System")
    print("=========================")
    print("Access the application at: http://localhost:5000")
    print("\n🔐 Default Login Credentials:")
    print("👤 Admin: admin@foodsystem.com / admin123")
    print("👤 Supervisor: supervisor@foodsystem.com / supervisor123")
    print("👤 Employee: employee@foodsystem.com / employee123")
    print("=========================")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
