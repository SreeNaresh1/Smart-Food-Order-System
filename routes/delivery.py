from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Delivery, Order, KitchenStaff, User
from datetime import datetime, timedelta
from functools import wraps
import uuid

delivery_bp = Blueprint('delivery', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_or_supervisor_required(f):
    """Decorator for routes that both admin and supervisor can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('user_role', '').lower()
        if 'user_id' not in session or user_role not in ['admin', 'supervisor']:
            flash('Access denied. Management privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('user_role', '').lower()
        if 'user_id' not in session or user_role not in ['admin', 'supervisor', 'employee']:
            flash('Access denied. Staff privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@delivery_bp.route('/')
@login_required
def list_deliveries():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    staff_filter = request.args.get('staff_id', '')
    
    # Query Delivery objects directly
    query = Delivery.query
    
    if status_filter:
        query = query.filter(Delivery.delivery_status == status_filter)
    
    if staff_filter:
        query = query.filter(Delivery.staff_id == staff_filter)
    
    deliveries = query.order_by(Delivery.estimated_time.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Get filters data
    statuses = db.session.query(Delivery.delivery_status).distinct().all()
    statuses = [status[0] for status in statuses]
    
    staff_list = KitchenStaff.query.filter_by(status='Active').all()
    
    return render_template('delivery/list.html',
                         deliveries=deliveries.items,
                         pagination=deliveries,
                         statuses=statuses,
                         staff_list=staff_list,
                         current_status=status_filter,
                         current_staff=staff_filter)

@delivery_bp.route('/create/<int:order_id>', methods=['GET', 'POST'])
@admin_or_supervisor_required
def create_delivery(order_id):
    """Admin and Supervisor can create deliveries"""
    order = Order.query.get_or_404(order_id)
    
    # Check if delivery already exists
    existing_delivery = Delivery.query.filter_by(order_id=order_id).first()
    if existing_delivery:
        flash('Delivery already exists for this order.', 'info')
        return redirect(url_for('delivery.view_delivery', delivery_id=existing_delivery.delivery_id))
    
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        estimated_time_str = request.form['estimated_time']
        
        # Parse estimated time
        estimated_time = datetime.strptime(estimated_time_str, '%Y-%m-%dT%H:%M')
        
        # Generate tracking code
        tracking_code = f"TRK{uuid.uuid4().hex[:8].upper()}"
        
        delivery = Delivery(
            order_id=order_id,
            staff_id=staff_id if staff_id else None,
            estimated_time=estimated_time,
            delivery_status='Assigned',
            tracking_code=tracking_code
        )
        
        try:
            db.session.add(delivery)
            
            # Update order status
            order.status = 'Preparing'
            
            db.session.commit()
            flash('Delivery created successfully!', 'success')
            return redirect(url_for('delivery.view_delivery', delivery_id=delivery.delivery_id))
        except Exception as e:
            db.session.rollback()
            flash('Error creating delivery.', 'danger')
    
    # Get available staff
    available_staff = KitchenStaff.query.filter_by(status='Active').all()
    
    # Default estimated time (1 hour from now)
    default_time = datetime.now() + timedelta(hours=1)
    
    return render_template('delivery/create.html', 
                         order=order, 
                         available_staff=available_staff,
                         default_time=default_time)

@delivery_bp.route('/view/<int:delivery_id>')
@login_required
def view_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    order = delivery.order
    
    # Check permission for customers
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and order.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('delivery.track'))
    
    return render_template('delivery/view.html', delivery=delivery, order=order)

@delivery_bp.route('/update_status/<int:delivery_id>', methods=['POST'])
@staff_required
def update_delivery_status(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    new_status = request.form['status']
    
    old_status = delivery.delivery_status
    delivery.delivery_status = new_status
    
    # Set actual delivery time when delivered
    if new_status == 'Delivered' and old_status != 'Delivered':
        delivery.actual_time = datetime.now()
        delivery.order.status = 'Delivered'
    elif new_status == 'In Transit' and old_status != 'In Transit':
        delivery.order.status = 'Out for Delivery'
    elif new_status == 'Failed':
        delivery.order.status = 'Delivery Failed'
    
    try:
        db.session.commit()
        flash('Delivery status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating delivery status.', 'danger')
    
    return redirect(url_for('delivery.view_delivery', delivery_id=delivery_id))

@delivery_bp.route('/assign_staff/<int:delivery_id>', methods=['POST'])
@staff_required
def assign_staff(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    staff_id = request.form['staff_id']
    
    # Validate staff
    staff = KitchenStaff.query.get(staff_id)
    if not staff or staff.status != 'Active':
        flash('Invalid or inactive staff selected.', 'danger')
        return redirect(url_for('delivery.view_delivery', delivery_id=delivery_id))
    
    delivery.staff_id = staff_id
    
    # Update status if currently unassigned
    if delivery.delivery_status == 'Assigned':
        delivery.delivery_status = 'Ready for Pickup'
    
    try:
        db.session.commit()
        flash(f'Staff {staff.staff_name} assigned to delivery.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error assigning staff.', 'danger')
    
    return redirect(url_for('delivery.view_delivery', delivery_id=delivery_id))

@delivery_bp.route('/track')
@login_required
def track():
    """Customer delivery tracking page"""
    user_id = session.get('user_id')
    
    # Get customer's active deliveries
    active_deliveries = db.session.query(Delivery, Order).join(
        Order, Delivery.order_id == Order.order_id
    ).filter(
        Order.user_id == user_id,
        Delivery.delivery_status.in_(['Assigned', 'Ready for Pickup', 'In Transit'])
    ).order_by(Delivery.estimated_time.asc()).all()
    
    # Get recent delivered orders
    recent_deliveries = db.session.query(Delivery, Order).join(
        Order, Delivery.order_id == Order.order_id
    ).filter(
        Order.user_id == user_id,
        Delivery.delivery_status == 'Delivered'
    ).order_by(Delivery.actual_time.desc()).limit(5).all()
    
    # Get the most recent order for the main tracking view
    order = None
    delivery = None
    if active_deliveries:
        delivery, order = active_deliveries[0]
    elif recent_deliveries:
        delivery, order = recent_deliveries[0]
    
    return render_template('delivery/track.html',
                         active_deliveries=active_deliveries,
                         recent_deliveries=recent_deliveries,
                         order=order,
                         delivery=delivery)

@delivery_bp.route('/track_by_code', methods=['POST'])
def track_by_code():
    """Track delivery by tracking code (public endpoint)"""
    tracking_code = request.form['tracking_code'].strip().upper()
    
    delivery = Delivery.query.filter_by(tracking_code=tracking_code).first()
    
    if not delivery:
        flash('Invalid tracking code.', 'danger')
        return render_template('delivery/track_public.html')
    
    return render_template('delivery/track_result.html', 
                         delivery=delivery, 
                         order=delivery.order)

@delivery_bp.route('/track_public')
def track_public():
    """Public tracking page (no login required)"""
    return render_template('delivery/track_public.html')

@delivery_bp.route('/performance')
@staff_required
def delivery_performance():
    """Delivery performance analytics"""
    # Average delivery time
    completed_deliveries = Delivery.query.filter(
        Delivery.delivery_status == 'Delivered',
        Delivery.actual_time.isnot(None),
        Delivery.estimated_time.isnot(None)
    ).all()
    
    on_time_count = 0
    total_delay_minutes = 0
    
    for delivery in completed_deliveries:
        time_diff = (delivery.actual_time - delivery.estimated_time).total_seconds() / 60
        if time_diff <= 0:  # On time or early
            on_time_count += 1
        else:
            total_delay_minutes += time_diff
    
    total_deliveries = len(completed_deliveries)
    on_time_percentage = (on_time_count / total_deliveries * 100) if total_deliveries > 0 else 0
    avg_delay = (total_delay_minutes / (total_deliveries - on_time_count)) if (total_deliveries - on_time_count) > 0 else 0
    
    # Staff performance
    staff_performance = db.session.query(
        KitchenStaff.staff_name,
        db.func.count(Delivery.delivery_id).label('total_deliveries'),
        db.func.count(
            db.case([(Delivery.delivery_status == 'Delivered', 1)])
        ).label('completed_deliveries')
    ).join(
        Delivery, KitchenStaff.staff_id == Delivery.staff_id
    ).group_by(KitchenStaff.staff_id).all()
    
    # Status distribution
    status_distribution = db.session.query(
        Delivery.delivery_status,
        db.func.count(Delivery.delivery_id)
    ).group_by(Delivery.delivery_status).all()
    
    stats = {
        'total_deliveries': total_deliveries,
        'on_time_percentage': round(on_time_percentage, 2),
        'average_delay_minutes': round(avg_delay, 2),
        'staff_performance': staff_performance,
        'status_distribution': dict(status_distribution)
    }
    
    return render_template('delivery/performance.html', stats=stats)

@delivery_bp.route('/track/<int:order_id>')
@login_required
def track_delivery(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permission - customers can only view their own orders
    if session.get('user_role') == 'customer' and order.user_id != session['user_id']:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get or create delivery record
    delivery = Delivery.query.filter_by(order_id=order_id).first()
    
    if not delivery and order.status in ['confirmed', 'preparing', 'ready', 'delivered']:
        # Create delivery record if order is confirmed but no delivery exists
        delivery = Delivery(
            order_id=order_id,
            delivery_status='assigned' if order.status == 'confirmed' else order.status,
            estimated_time=order.estimated_time or (order.order_date + timedelta(minutes=45)),
            tracking_code=f'TRK{order_id}{datetime.now().strftime("%Y%m%d")}'
        )
        db.session.add(delivery)
        db.session.commit()
    
    return render_template('delivery/track.html', order=order, delivery=delivery)

@delivery_bp.route('/auto-assign')
@login_required
def auto_assign_deliveries():
    """Auto-assign pending deliveries to available staff"""
    # Check if user is admin or staff
    user_role = session.get('user_role', '').lower()
    if user_role not in ['admin', 'supervisor', 'employee']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('delivery.list_deliveries'))
    
    # Get pending deliveries (not assigned to staff)
    pending_deliveries = Delivery.query.filter(
        Delivery.staff_id.is_(None),
        Delivery.delivery_status.in_(['Assigned', 'Pending'])
    ).all()
    
    if not pending_deliveries:
        flash('No pending deliveries to assign.', 'info')
        return redirect(url_for('delivery.list_deliveries'))
    
    # Get available staff
    available_staff = KitchenStaff.query.filter_by(status='Active').all()
    
    if not available_staff:
        flash('No available staff to assign deliveries.', 'warning')
        return redirect(url_for('delivery.list_deliveries'))
    
    # Simple round-robin assignment
    assigned_count = 0
    for i, delivery in enumerate(pending_deliveries):
        staff = available_staff[i % len(available_staff)]
        delivery.staff_id = staff.staff_id
        delivery.delivery_status = 'Assigned'
        assigned_count += 1
    
    try:
        db.session.commit()
        flash(f'Successfully auto-assigned {assigned_count} deliveries to {len(available_staff)} staff members.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error auto-assigning deliveries.', 'danger')
    
    return redirect(url_for('delivery.list_deliveries'))

@delivery_bp.route('/map')
@login_required
def delivery_map():
    """Display delivery map view"""
    # Check if user has permission
    user_role = session.get('user_role', '').lower()
    if user_role not in ['admin', 'supervisor', 'employee']:
        flash('Access denied.', 'danger')
        return redirect(url_for('delivery.list_deliveries'))
    
    # Get active deliveries
    active_deliveries = Delivery.query.filter(
        Delivery.delivery_status.in_(['Assigned', 'In Transit'])
    ).all()
    
    flash('Delivery map feature is under development. Showing list view.', 'info')
    return redirect(url_for('delivery.list_deliveries'))

@delivery_bp.route('/export')
@login_required
def export_deliveries():
    """Export delivery report as CSV"""
    # Check if user has permission
    user_role = session.get('user_role', '').lower()
    if user_role not in ['admin', 'supervisor']:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('delivery.list_deliveries'))
    
    from io import StringIO
    import csv
    from flask import make_response
    
    # Get all deliveries
    deliveries = Delivery.query.order_by(Delivery.estimated_time.desc()).all()
    
    # Create CSV
    si = StringIO()
    writer = csv.writer(si)
    
    # Write header
    writer.writerow(['Delivery ID', 'Order ID', 'Status', 'Staff', 'Customer', 'Estimated Time', 'Actual Time', 'Tracking Code'])
    
    # Write data
    for delivery in deliveries:
        writer.writerow([
            delivery.delivery_id,
            delivery.order_id,
            delivery.delivery_status,
            delivery.staff.staff_name if delivery.staff else 'Unassigned',
            delivery.order.customer.name if delivery.order and delivery.order.customer else 'N/A',
            delivery.estimated_time.strftime('%Y-%m-%d %H:%M') if delivery.estimated_time else 'N/A',
            delivery.actual_time.strftime('%Y-%m-%d %H:%M') if delivery.actual_time else 'N/A',
            delivery.tracking_code or 'N/A'
        ])
    
    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=deliveries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output