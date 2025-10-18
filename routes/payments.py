from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from models import db, Payment, Order, User
from datetime import datetime
from functools import wraps
import uuid
import csv
from io import StringIO

payments_bp = Blueprint('payments', __name__)

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
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@payments_bp.route('/')
@login_required
def list_payments():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    # Filter based on user role
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer':
        # Customers can only see their own payments
        query = Payment.query.join(Order).filter(Order.user_id == user_id)
    else:
        # Admin/Supervisor can see all payments
        query = Payment.query
    
    if status_filter:
        query = query.filter(Payment.status == status_filter)
    
    payments = query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Get unique statuses for filter
    statuses = db.session.query(Payment.status).distinct().all()
    statuses = [status[0] for status in statuses]
    
    return render_template('payments/list.html', 
                         payments=payments, 
                         statuses=statuses,
                         current_status=status_filter)

@payments_bp.route('/process/<int:order_id>', methods=['GET', 'POST'])
@login_required
def process_payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user can process this payment
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and order.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('payments.list_payments'))
    
    # Check if payment already exists
    existing_payment = Payment.query.filter_by(order_id=order_id).first()
    if existing_payment:
        flash('Payment already processed for this order.', 'info')
        return redirect(url_for('payments.view_payment', payment_id=existing_payment.payment_id))
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        
        # Generate transaction ID
        transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"
        
        # Create payment record
        payment = Payment(
            order_id=order_id,
            payment_method=payment_method,
            amount=order.total_amount,
            transaction_id=transaction_id,
            status='Completed'  # In real app, this would be 'Pending' until confirmed
        )
        
        try:
            db.session.add(payment)
            
            # Update order status
            if order.status == 'Pending':
                order.status = 'Confirmed'
            
            db.session.commit()
            flash('Payment processed successfully!', 'success')
            return redirect(url_for('payments.view_payment', payment_id=payment.payment_id))
        except Exception as e:
            db.session.rollback()
            flash('Error processing payment.', 'danger')
    
    return render_template('payments/process.html', order=order)

@payments_bp.route('/view/<int:payment_id>')
@login_required
def view_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    order = payment.order
    
    # Check permission
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and order.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('payments.list_payments'))
    
    return render_template('payments/view.html', payment=payment, order=order)

@payments_bp.route('/update_status/<int:payment_id>', methods=['POST'])
@admin_required
def update_payment_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    new_status = request.form['status']
    
    old_status = payment.status
    payment.status = new_status
    
    # Update order status based on payment status
    if new_status == 'Completed' and old_status != 'Completed':
        if payment.order.status == 'Pending':
            payment.order.status = 'Confirmed'
    elif new_status == 'Failed' and old_status != 'Failed':
        if payment.order.status in ['Confirmed', 'Pending']:
            payment.order.status = 'Pending'
    elif new_status == 'Refunded':
        payment.order.status = 'Cancelled'
    
    try:
        db.session.commit()
        flash('Payment status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating payment status.', 'danger')
    
    return redirect(url_for('payments.view_payment', payment_id=payment_id))

@payments_bp.route('/refund/<int:payment_id>', methods=['POST'])
@admin_required
def refund_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    if payment.status != 'Completed':
        flash('Can only refund completed payments.', 'danger')
        return redirect(url_for('payments.view_payment', payment_id=payment_id))
    
    # Process refund
    payment.status = 'Refunded'
    payment.order.status = 'Cancelled'
    
    # Generate refund transaction ID
    refund_transaction_id = f"REF{uuid.uuid4().hex[:10].upper()}"
    payment.transaction_id = f"{payment.transaction_id} | {refund_transaction_id}"
    
    try:
        db.session.commit()
        flash('Payment refunded successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error processing refund.', 'danger')
    
    return redirect(url_for('payments.view_payment', payment_id=payment_id))

@payments_bp.route('/receipt/<int:payment_id>')
@login_required
def download_receipt(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    order = payment.order
    
    # Check permission
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and order.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('payments.list_payments'))
    
    # Get order details for receipt
    order_details = order.order_details
    
    return render_template('payments/receipt.html', 
                         payment=payment, 
                         order=order, 
                         order_details=order_details)

@payments_bp.route('/export')
@admin_required
def export_payments():
    # Get all payments
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    
    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    
    # Write headers
    writer.writerow([
        'Payment ID', 'Order ID', 'Customer Name', 'Customer Email',
        'Amount', 'Payment Method', 'Status', 'Transaction ID',
        'Payment Date', 'Order Date'
    ])
    
    # Write data
    for payment in payments:
        order = payment.order
        customer = order.customer if order else None
        
        writer.writerow([
            payment.payment_id,
            order.order_id if order else 'N/A',
            customer.name if customer else 'N/A',
            customer.email if customer else 'N/A',
            f"${payment.amount:.2f}",
            payment.payment_method if payment.payment_method else 'N/A',
            payment.status.title() if payment.status else 'Pending',
            payment.transaction_id if payment.transaction_id else 'N/A',
            payment.payment_date.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_date else 'N/A',
            order.order_date.strftime('%Y-%m-%d %H:%M:%S') if order and order.order_date else 'N/A'
        ])
    
    # Create response
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = f'attachment; filename=payments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    output.headers['Content-type'] = 'text/csv'
    
    return output
