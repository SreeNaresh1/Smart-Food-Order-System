from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, KitchenStaff, Delivery, User
from functools import wraps
from werkzeug.security import generate_password_hash

kitchen_bp = Blueprint('kitchen', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('user_role', '').lower()
        if 'user_id' not in session or user_role not in ['admin', 'supervisor']:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@kitchen_bp.route('/')
@login_required
def list_kitchen_staff():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    department_filter = request.args.get('department', '')
    shift_filter = request.args.get('shift', '')
    
    query = User.query.filter(User.role == 'Employee')
    
    staff_list = query.order_by(User.name.asc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Get filter options (simplified for now)
    statuses = ['Active', 'Inactive']
    departments = ['Kitchen', 'Preparation', 'Cleaning']
    shifts = ['Morning', 'Evening', 'Night']
    
    return render_template('kitchen/list.html',
                         staff=staff_list.items,
                         staff_list=staff_list,
                         statuses=statuses,
                         departments=departments,
                         shifts=shifts,
                         current_status=status_filter,
                         current_department=department_filter,
                         current_shift=shift_filter)

@kitchen_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_kitchen_staff():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form.get('address', '')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return render_template('kitchen/add.html')
        
        # Check if phone already exists
        if User.query.filter_by(phone=phone).first():
            flash('Phone number already exists.', 'danger')
            return render_template('kitchen/add.html')
        
        user = User(
            name=full_name,
            email=email,
            phone=phone,
            role='Employee',
            password=generate_password_hash(password),
            address=address
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Kitchen staff added successfully!', 'success')
            return redirect(url_for('kitchen.list_kitchen_staff'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding kitchen staff.', 'danger')
    
    return render_template('kitchen/add.html')

@kitchen_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_kitchen_staff(user_id):
    staff = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        staff.name = request.form['staff_name']
        staff.phone = request.form['phone']
        staff.address = request.form.get('address', '')
        
        try:
            db.session.commit()
            flash('Kitchen staff updated successfully!', 'success')
            return redirect(url_for('kitchen.list_kitchen_staff'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating kitchen staff.', 'danger')
    
    return render_template('kitchen/edit.html', staff=staff)

@kitchen_bp.route('/view/<int:user_id>')
@login_required
def view_kitchen_staff(user_id):
    staff = User.query.get_or_404(user_id)
    
    # Staff details for viewing
    return render_template('kitchen/view.html', staff=staff)

@kitchen_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_kitchen_staff(user_id):
    staff = User.query.get_or_404(user_id)
    
    # Only allow deleting Employee role users
    if staff.role != 'Employee':
        flash('Cannot delete non-employee users from this page.', 'danger')
        return redirect(url_for('kitchen.list_kitchen_staff'))
    
    try:
        db.session.delete(staff)
        db.session.commit()
        flash('Kitchen staff deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting kitchen staff.', 'danger')
    
    return redirect(url_for('kitchen.list_kitchen_staff'))

@kitchen_bp.route('/update_status/<int:user_id>', methods=['POST'])
@admin_required
def update_staff_status(user_id):
    staff = User.query.get_or_404(user_id)
    
    # User model doesn't have status field, redirect back
    flash('Status update is not applicable for employee users.', 'info')
    return redirect(url_for('kitchen.view_kitchen_staff', user_id=user_id))

@kitchen_bp.route('/schedule')
@login_required
def staff_schedule():
    """View staff schedule by shift and department"""
    
    # Get staff grouped by shift and department
    morning_staff = KitchenStaff.query.filter_by(
        shift_time='Morning', status='Active'
    ).order_by(KitchenStaff.department, KitchenStaff.staff_name).all()
    
    evening_staff = KitchenStaff.query.filter_by(
        shift_time='Evening', status='Active'
    ).order_by(KitchenStaff.department, KitchenStaff.staff_name).all()
    
    night_staff = KitchenStaff.query.filter_by(
        shift_time='Night', status='Active'
    ).order_by(KitchenStaff.department, KitchenStaff.staff_name).all()
    
    # Group by department for each shift
    def group_by_department(staff_list):
        groups = {}
        for staff in staff_list:
            if staff.department not in groups:
                groups[staff.department] = []
            groups[staff.department].append(staff)
        return groups
    
    schedule = {
        'Morning': group_by_department(morning_staff),
        'Evening': group_by_department(evening_staff),
        'Night': group_by_department(night_staff)
    }
    
    return render_template('kitchen/schedule.html', schedule=schedule)

@kitchen_bp.route('/performance')
@admin_required
def staff_performance():
    """Staff performance analytics"""
    
    # Overall statistics
    total_staff = KitchenStaff.query.count()
    active_staff = KitchenStaff.query.filter_by(status='Active').count()
    
    # Department distribution
    dept_distribution = db.session.query(
        KitchenStaff.department,
        db.func.count(KitchenStaff.staff_id)
    ).group_by(KitchenStaff.department).all()
    
    # Shift distribution
    shift_distribution = db.session.query(
        KitchenStaff.shift_time,
        db.func.count(KitchenStaff.staff_id)
    ).group_by(KitchenStaff.shift_time).all()
    
    # Status distribution
    status_distribution = db.session.query(
        KitchenStaff.status,
        db.func.count(KitchenStaff.staff_id)
    ).group_by(KitchenStaff.status).all()
    
    # Delivery performance by staff
    delivery_performance = db.session.query(
        KitchenStaff.staff_name,
        KitchenStaff.department,
        db.func.count(Delivery.delivery_id).label('total_deliveries'),
        db.func.count(
            db.case([(Delivery.delivery_status == 'Delivered', 1)])
        ).label('completed_deliveries')
    ).outerjoin(
        Delivery, KitchenStaff.staff_id == Delivery.staff_id
    ).group_by(KitchenStaff.staff_id).order_by(
        db.text('completed_deliveries DESC')
    ).limit(10).all()
    
    stats = {
        'total_staff': total_staff,
        'active_staff': active_staff,
        'department_distribution': dict(dept_distribution),
        'shift_distribution': dict(shift_distribution),
        'status_distribution': dict(status_distribution),
        'top_performers': delivery_performance
    }
    
    return render_template('kitchen/performance.html', stats=stats)