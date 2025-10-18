from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User
from werkzeug.security import generate_password_hash
from functools import wraps

users_bp = Blueprint('users', __name__)

def admin_or_supervisor_required(f):
    """Decorator for routes that both admin and supervisor can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('user_role', '').lower()
        if 'user_id' not in session or user_role not in ['admin', 'supervisor']:
            flash('Access denied. Admin or Supervisor privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that only admin can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('user_role', '').lower()
        if 'user_id' not in session or user_role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/')
@admin_or_supervisor_required
def list_users():
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    search = request.args.get('search', '')
    
    user_role = session.get('user_role', '').lower()
    
    query = User.query
    
    # Supervisor can only view Employee and Customer accounts
    if user_role == 'supervisor':
        query = query.filter(User.role.in_(['Employee', 'Customer']))
    
    if role_filter:
        query = query.filter(User.role == role_filter)
    
    if search:
        query = query.filter(User.name.contains(search) | 
                           User.email.contains(search))
    
    users = query.order_by(User.created_date.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Get unique roles for filter dropdown
    if user_role == 'supervisor':
        roles = ['Employee', 'Customer']
    else:
        roles = db.session.query(User.role).distinct().all()
        roles = [role[0] for role in roles]
    
    # Get role counts
    employee_count = User.query.filter(User.role.in_(['Employee', 'Supervisor'])).count()
    customer_count = User.query.filter_by(role='Customer').count()
    admin_count = User.query.filter_by(role='Admin').count()

    return render_template('users/list.html', 
                         users=users, 
                         roles=roles,
                         current_role=role_filter,
                         search_term=search,
                         employee_count=employee_count,
                         customer_count=customer_count,
                         admin_count=admin_count,
                         user_role=user_role)

@users_bp.route('/add', methods=['GET', 'POST'])
@admin_or_supervisor_required
def add_user():
    user_role = session.get('user_role', '').lower()
    
    if request.method == 'POST':
        # Get form data using the actual field names from the template
        name = request.form.get('full_name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        role = request.form.get('role', '')
        password = request.form.get('password', '')
        address = request.form.get('address', '')
        
        # Supervisor can only create Employee and Customer accounts
        if user_role == 'supervisor' and role not in ['Employee', 'Customer']:
            flash('Supervisors can only create Employee and Customer accounts.', 'danger')
            return render_template('users/add.html', user_role=user_role)
        
        # Validate required fields
        if not name or not email or not password or not role:
            flash('Please fill in all required fields.', 'danger')
            return render_template('users/add.html', user_role=user_role)
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return render_template('users/add.html', user_role=user_role)
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role,
            password=hashed_password,
            address=address
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'{role} added successfully!', 'success')
            return redirect(url_for('users.list_users'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding user.', 'danger')
    
    return render_template('users/add.html', user_role=user_role)

@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_or_supervisor_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user_role = session.get('user_role', '').lower()
    
    # Supervisor can only edit Employee and Customer accounts
    if user_role == 'supervisor' and user.role not in ['Employee', 'Customer']:
        flash('Supervisors can only edit Employee and Customer accounts.', 'danger')
        return redirect(url_for('users.list_users'))
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        
        # Only admin can change roles
        if user_role == 'admin':
            user.role = request.form['role']
        
        user.address = request.form['address']
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            user.password = generate_password_hash(new_password)
        
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('users.list_users'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating user.', 'danger')
    
    return render_template('users/edit.html', user=user, user_role=user_role)

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Only Admin can delete users"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting the current user
    if user_id == session.get('user_id'):
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('users.list_users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user. User may have associated orders.', 'danger')
    
    return redirect(url_for('users.list_users'))

@users_bp.route('/view/<int:user_id>')
@admin_or_supervisor_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    user_role = session.get('user_role', '').lower()
    
    # Supervisor can only view Employee and Customer accounts
    if user_role == 'supervisor' and user.role not in ['Employee', 'Customer']:
        flash('Supervisors can only view Employee and Customer accounts.', 'danger')
        return redirect(url_for('users.list_users'))
    
    # Get user statistics
    user_stats = {
        'total_orders': len(user.orders),
        'total_feedback': len(user.feedback),
        'recent_orders': user.orders[:5] if user.orders else []
    }
    
    return render_template('users/view.html', user=user, user_stats=user_stats, user_role=user_role)