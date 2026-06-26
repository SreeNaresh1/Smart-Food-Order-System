from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.models import db, Feedback, Order, User
from datetime import datetime
from functools import wraps

feedback_bp = Blueprint('feedback', __name__)

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

@feedback_bp.route('/')
@login_required
def list_feedback():
    page = request.args.get('page', 1, type=int)
    feedback_type = request.args.get('type', '')
    rating_filter = request.args.get('rating', '', type=str)
    
    # Filter based on user role
    user_role = session.get('user_role', '').lower()
    user_id = session.get('user_id')
    
    if user_role == 'customer':
        # Customer can only see their own feedback
        query = Feedback.query.filter_by(user_id=user_id)
    elif user_role in ['admin', 'supervisor']:
        # Admin and Supervisor can see all feedback
        query = Feedback.query
    else:
        # Employee can see their own feedback if they're also customers
        query = Feedback.query.filter_by(user_id=user_id)
    
    if feedback_type:
        query = query.filter(Feedback.feedback_type == feedback_type)
    
    if rating_filter:
        query = query.filter(Feedback.rating == int(rating_filter))
    
    feedback_list = query.order_by(Feedback.feedback_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get unique feedback types and ratings for filters
    feedback_types = db.session.query(Feedback.feedback_type).distinct().all()
    feedback_types = [ft[0] for ft in feedback_types]
    
    return render_template('feedback/list.html', 
                         feedback_list=feedback_list,
                         feedback_types=feedback_types,
                         current_type=feedback_type,
                         current_rating=rating_filter,
                         user_role=user_role)

@feedback_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_feedback():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        rating = int(request.form['rating'])
        comments = request.form['comments']
        feedback_type = request.form['feedback_type']
        
        # Validate order belongs to user if order_id provided
        if order_id:
            order = Order.query.get(order_id)
            if not order or (session.get('user_role') == 'Customer' and order.user_id != session.get('user_id')):
                flash('Invalid order selected.', 'danger')
                return redirect(url_for('feedback.add_feedback'))
        
        # Check if feedback already exists for this order
        if order_id:
            existing_feedback = Feedback.query.filter_by(
                user_id=session.get('user_id'),
                order_id=order_id
            ).first()
            if existing_feedback:
                flash('Feedback already submitted for this order.', 'info')
                return redirect(url_for('feedback.view_feedback', feedback_id=existing_feedback.feedback_id))
        
        # Create feedback
        feedback = Feedback(
            user_id=session.get('user_id'),
            order_id=order_id if order_id else None,
            rating=rating,
            comments=comments,
            feedback_type=feedback_type
        )
        
        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback submitted successfully!', 'success')
            return redirect(url_for('feedback.view_feedback', feedback_id=feedback.feedback_id))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting feedback.', 'danger')
    
    # Get user's orders for feedback
    user_orders = []
    if session.get('user_role') == 'Customer':
        user_orders = Order.query.filter_by(
            user_id=session.get('user_id')
        ).filter(Order.status.in_(['Delivered', 'Completed'])).order_by(
            Order.order_date.desc()
        ).all()
    
    return render_template('feedback/add.html', user_orders=user_orders)

@feedback_bp.route('/add_for_order/<int:order_id>', methods=['GET', 'POST'])
@feedback_bp.route('/create/<int:order_id>', methods=['GET', 'POST'])
@login_required
def add_feedback_for_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permission
    if session.get('user_role') == 'Customer' and order.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('feedback.list_feedback'))
    
    # Check if feedback already exists
    existing_feedback = Feedback.query.filter_by(
        user_id=session.get('user_id'),
        order_id=order_id
    ).first()
    if existing_feedback:
        flash('Feedback already submitted for this order.', 'info')
        return redirect(url_for('feedback.view_feedback', feedback_id=existing_feedback.feedback_id))
    
    if request.method == 'POST':
        rating = int(request.form['rating'])
        comments = request.form['comments']
        feedback_type = request.form['feedback_type']
        
        feedback = Feedback(
            user_id=session.get('user_id'),
            order_id=order_id,
            rating=rating,
            comments=comments,
            feedback_type=feedback_type
        )
        
        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback submitted successfully!', 'success')
            return redirect(url_for('orders.view_order', order_id=order_id))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting feedback.', 'danger')
    
    return render_template('feedback/add_for_order.html', order=order)

# Alias for template compatibility
create_feedback = add_feedback_for_order

@feedback_bp.route('/view/<int:feedback_id>')
@login_required
def view_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    # Check permission
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and feedback.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('feedback.list_feedback'))
    
    return render_template('feedback/view.html', feedback=feedback)

@feedback_bp.route('/edit/<int:feedback_id>', methods=['GET', 'POST'])
@login_required
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    # Check permission - only feedback owner can edit
    if feedback.user_id != session.get('user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('feedback.list_feedback'))
    
    if request.method == 'POST':
        feedback.rating = int(request.form['rating'])
        feedback.comments = request.form['comments']
        feedback.feedback_type = request.form['feedback_type']
        
        try:
            db.session.commit()
            flash('Feedback updated successfully!', 'success')
            return redirect(url_for('feedback.view_feedback', feedback_id=feedback_id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating feedback.', 'danger')
    
    return render_template('feedback/edit.html', feedback=feedback)

@feedback_bp.route('/delete/<int:feedback_id>', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    # Check permission
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    if user_role == 'Customer' and feedback.user_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('feedback.list_feedback'))
    
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting feedback.', 'danger')
    
    return redirect(url_for('feedback.list_feedback'))

@feedback_bp.route('/analytics')
@login_required
def feedback_analytics():
    """Analytics view for feedback (Admin only)"""
    user_role = session.get('user_role', '').lower()
    if user_role not in ['admin', 'supervisor']:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Calculate feedback statistics
    total_feedback = Feedback.query.count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar()
    
    # Rating distribution
    rating_dist = db.session.query(
        Feedback.rating,
        db.func.count(Feedback.feedback_id)
    ).group_by(Feedback.rating).all()
    
    # Feedback by type
    type_dist = db.session.query(
        Feedback.feedback_type,
        db.func.count(Feedback.feedback_id)
    ).group_by(Feedback.feedback_type).all()
    
    # Recent low ratings (for attention)
    low_ratings = Feedback.query.filter(
        Feedback.rating <= 2
    ).order_by(Feedback.feedback_date.desc()).limit(10).all()
    
    # Monthly feedback trend (last 6 months)
    monthly_feedback = db.session.query(
        db.func.strftime('%Y-%m', Feedback.feedback_date).label('month'),
        db.func.count(Feedback.feedback_id).label('count'),
        db.func.avg(Feedback.rating).label('avg_rating')
    ).group_by(db.text('month')).order_by(db.text('month DESC')).limit(6).all()
    
    stats = {
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 2) if avg_rating else 0,
        'rating_distribution': dict(rating_dist),
        'type_distribution': dict(type_dist),
        'low_ratings': low_ratings,
        'monthly_trend': list(reversed(monthly_feedback))  # Reverse to show chronological order
    }
    
    return render_template('feedback/analytics.html', stats=stats)
