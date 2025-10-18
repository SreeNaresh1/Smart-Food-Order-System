from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Order, OrderDetails, MenuItem, User, Payment
from datetime import datetime, timedelta
from functools import wraps

orders_bp = Blueprint('orders', __name__)

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

@orders_bp.route('/')
@login_required
def list_orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    # Filter orders based on user role
    user_role = session.get('user_role', '').lower()
    user_id = session.get('user_id')
    
    if user_role == 'customer':
        query = Order.query.filter_by(user_id=user_id)
    elif user_role in ['admin', 'supervisor']:
        # Both admin and supervisor can view all orders
        # In a real system, supervisor would be limited to their branch
        query = Order.query
    elif user_role == 'employee':
        # Employee can only see assigned orders (if you implement assignment)
        query = Order.query
    else:
        query = Order.query.filter_by(user_id=user_id)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.order_by(Order.order_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get unique statuses for filter dropdown
    statuses = db.session.query(Order.status).distinct().all()
    statuses = [status[0] for status in statuses]
    
    return render_template('orders/list.html', 
                         orders=orders, 
                         statuses=statuses,
                         current_status=status_filter,
                         user_role=user_role)

@orders_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_order():
    if request.method == 'POST':
        delivery_address = request.form['delivery_address']
        order_time = request.form.get('order_time')
        
        # Create new order
        order = Order(
            user_id=session['user_id'],
            total_amount=0,  # Will be calculated after adding items
            status='Pending',
            delivery_address=delivery_address,
            order_time=datetime.strptime(order_time, '%H:%M').time() if order_time else None
        )
        
        try:
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Add order details from cart (assuming cart is stored in session)
            cart_items = session.get('cart', [])
            total_amount = 0
            
            for item in cart_items:
                menu_item = MenuItem.query.get(item['menu_item_id'])
                if menu_item:
                    sub_total = menu_item.price * item['quantity']
                    total_amount += sub_total
                    
                    order_detail = OrderDetails(
                        order_id=order.order_id,
                        menu_item_id=menu_item.menu_item_id,
                        quantity=item['quantity'],
                        unit_price=menu_item.price,
                        sub_total=sub_total,
                        special_instructions=item.get('special_instructions', '')
                    )
                    db.session.add(order_detail)
            
            # Update order total
            order.total_amount = total_amount
            
            db.session.commit()
            
            # Clear cart
            session.pop('cart', None)
            
            flash('Order created successfully!', 'success')
            return redirect(url_for('orders.view_order', order_id=order.order_id))
        except Exception as e:
            db.session.rollback()
            flash('Error creating order.', 'danger')
    
    # Get cart items for checkout display
    cart_items = []
    total_amount = 0
    cart = session.get('cart', [])
    
    for item in cart:
        menu_item = MenuItem.query.get(item['menu_item_id'])
        if menu_item:
            sub_total = menu_item.price * item['quantity']
            total_amount += sub_total
            
            cart_items.append({
                'menu_item': menu_item,
                'quantity': item['quantity'],
                'special_instructions': item.get('special_instructions', ''),
                'sub_total': sub_total
            })
    
    user = User.query.get(session['user_id'])
    return render_template('orders/create.html', 
                         cart_items=cart_items, 
                         total_amount=total_amount,
                         user=user)

@orders_bp.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    payment_method = request.form['payment_method']
    total_amount = float(request.form['total_amount'])
    special_instructions = request.form.get('special_instructions', '')
    
    # Get cart items
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('menu.list_menu'))
    
    try:
        # Create new order
        user = User.query.get(session['user_id'])
        order = Order(
            user_id=session['user_id'],
            total_amount=total_amount,
            status='confirmed',  # Set to confirmed after payment
            delivery_address=user.address,
            estimated_time=datetime.now() + timedelta(minutes=45)  # 45 min estimate
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Add order details from cart
        for item in cart:
            menu_item = MenuItem.query.get(item['menu_item_id'])
            if menu_item:
                sub_total = menu_item.price * item['quantity']
                
                order_detail = OrderDetails(
                    order_id=order.order_id,
                    menu_item_id=menu_item.menu_item_id,
                    quantity=item['quantity'],
                    unit_price=menu_item.price,
                    sub_total=sub_total,
                    special_instructions=item.get('special_instructions', '') or special_instructions
                )
                db.session.add(order_detail)
        
        # Create payment record
        payment = Payment(
            order_id=order.order_id,
            payment_method=payment_method.upper(),
            amount=total_amount,
            payment_date=datetime.now(),
            transaction_id=f'TXN{order.order_id}{datetime.now().strftime("%Y%m%d%H%M%S")}',
            status='Completed'
        )
        db.session.add(payment)
        
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        # Show success message
        flash('Order placed successfully! Your order is being prepared.', 'success')
        return redirect(url_for('orders.order_success', order_id=order.order_id))
        
    except Exception as e:
        db.session.rollback()
        flash('Payment processing failed. Please try again.', 'danger')
        return redirect(url_for('orders.create_order'))

@orders_bp.route('/success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permission
    if order.user_id != session['user_id']:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('orders/success.html', order=order)

@orders_bp.route('/view/<int:order_id>')
@login_required
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permission
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and order.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('orders.list_orders'))
    
    order_details = OrderDetails.query.filter_by(order_id=order_id).all()
    
    return render_template('orders/view.html', 
                         order=order, 
                         order_details=order_details)

@orders_bp.route('/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    """Admin, Supervisor, and Employee can update order status"""
    user_role = session.get('user_role', '').lower()
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status', '')
    
    # Validate status transitions
    if user_role == 'employee':
        # Employees can only move orders forward through the workflow
        valid_statuses = ['Confirmed', 'Preparing', 'Ready', 'Delivered']
        allowed_transitions = {
            'Confirmed': 'Preparing',
            'Preparing': 'Ready', 
            'Ready': 'Delivered'
        }
        # Check if this is a valid transition for employee
        if new_status not in valid_statuses:
            flash('Invalid status for employee.', 'danger')
            return redirect(url_for('orders.view_order', order_id=order_id))
    else:
        # Admin and Supervisor have full control
        valid_statuses = ['Pending', 'Confirmed', 'Preparing', 'Ready', 'Delivered', 'Cancelled']
    
    if new_status not in valid_statuses:
        flash('Invalid status.', 'danger')
        return redirect(url_for('orders.view_order', order_id=order_id))
    
    order.status = new_status
    
    # Update estimated time if status is changed to preparing
    if new_status == 'Preparing' and not order.estimated_time:
        order.estimated_time = datetime.now() + timedelta(minutes=30)
    
    try:
        db.session.commit()
        flash(f'Order status updated to {new_status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating order status.', 'danger')
    
    return redirect(url_for('orders.view_order', order_id=order_id))

@orders_bp.route('/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permission
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and order.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('orders.list_orders'))
    
    # Can only cancel pending orders
    if order.status not in ['Pending', 'Confirmed']:
        flash('Cannot cancel order in current status.', 'danger')
        return redirect(url_for('orders.view_order', order_id=order_id))
    
    order.status = 'Cancelled'
    
    try:
        db.session.commit()
        flash('Order cancelled successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error cancelling order.', 'danger')
    
    return redirect(url_for('orders.view_order', order_id=order_id))

# Cart management routes
@orders_bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    menu_item_id = int(request.form['menu_item_id'])
    quantity = int(request.form['quantity'])
    special_instructions = request.form.get('special_instructions', '')
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    
    # Check if item already in cart
    existing_item = None
    for item in cart:
        if item['menu_item_id'] == menu_item_id:
            existing_item = item
            break
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        cart.append({
            'menu_item_id': menu_item_id,
            'quantity': quantity,
            'special_instructions': special_instructions
        })
    
    session['cart'] = cart
    session.modified = True
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Item added to cart!', 'cart_count': len(cart)})
    
    flash('Item added to cart!', 'success')
    return redirect(url_for('menu.list_menu'))

@orders_bp.route('/view_cart')
@login_required
def view_cart():
    cart = session.get('cart', [])
    cart_items = []
    total_amount = 0
    
    for item in cart:
        menu_item = MenuItem.query.get(item['menu_item_id'])
        if menu_item:
            sub_total = menu_item.price * item['quantity']
            total_amount += sub_total
            
            cart_items.append({
                'menu_item': menu_item,
                'quantity': item['quantity'],
                'special_instructions': item['special_instructions'],
                'sub_total': sub_total
            })
    
    return render_template('orders/cart.html', 
                         cart_items=cart_items, 
                         total_amount=total_amount)

@orders_bp.route('/remove_from_cart/<int:menu_item_id>', methods=['POST'])
@login_required
def remove_from_cart(menu_item_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['menu_item_id'] != menu_item_id]
    session['cart'] = cart
    session.modified = True
    
    flash('Item removed from cart.', 'info')
    return redirect(url_for('orders.view_cart'))

@orders_bp.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared.', 'info')
    return redirect(url_for('orders.view_cart'))