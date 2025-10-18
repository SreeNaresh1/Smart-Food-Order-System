from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Order, OrderDetails, MenuItem, User, Payment, Feedback, Delivery, KitchenStaff
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func, and_, or_, case, desc

reports_bp = Blueprint('reports', __name__)

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

def admin_required(f):
    """Decorator for admin-only routes (financial reports)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('user_role', '').lower()
        if 'user_id' not in session or user_role != 'admin':
            flash('Access denied. Admin privileges required for financial reports.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@reports_bp.route('/')
@admin_or_supervisor_required
def reports_dashboard():
    """Main reports dashboard with overview - accessible to admin and supervisor"""
    user_role = session.get('user_role', '').lower()
    
    # Calculate date ranges
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)
    month_ago = today - timedelta(days=30)
    
    # Quick stats
    total_orders = Order.query.count()
    
    # Supervisor can see revenue overview but not detailed financial reports
    if user_role == 'admin':
        total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    else:
        total_revenue = None  # Hide from supervisor
    
    total_customers = User.query.filter_by(role='Customer').count()
    total_menu_items = MenuItem.query.filter_by(availability=True).count()
    avg_rating = db.session.query(func.avg(Feedback.rating)).scalar() or 0
    
    # Today's stats
    today_orders = Order.query.filter(Order.order_date >= today_start).count()
    
    if user_role == 'admin':
        today_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.order_date >= today_start
        ).scalar() or 0
    else:
        today_revenue = None
    
    today_new_customers = User.query.filter(
        User.role == 'Customer',
        User.created_date >= today_start
    ).count()
    
    # This week's stats
    week_orders = Order.query.filter(Order.order_date >= week_ago).count()
    
    if user_role == 'admin':
        week_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.order_date >= week_ago
        ).scalar() or 0
        
        # Previous week's stats for growth calculation
        prev_week_orders = Order.query.filter(
            Order.order_date >= two_weeks_ago,
            Order.order_date < week_ago
        ).count()
        prev_week_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.order_date >= two_weeks_ago,
            Order.order_date < week_ago
        ).scalar() or 0
    else:
        week_revenue = None
        prev_week_orders = Order.query.filter(
            Order.order_date >= two_weeks_ago,
            Order.order_date < week_ago
        ).count()
    
    # Calculate growth rate
    if prev_week_orders > 0:
        growth_rate = ((week_orders - prev_week_orders) / prev_week_orders) * 100
    else:
        growth_rate = None
    
    # Recent activity
    recent_orders = Order.query.filter(
        Order.order_date >= week_ago
    ).count()
    
    if user_role == 'admin':
        recent_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.order_date >= week_ago
        ).scalar() or 0
    else:
        recent_revenue = None
    
    stats = {
        'total_orders': total_orders,
        'total_revenue': float(total_revenue) if total_revenue else None,
        'total_customers': total_customers,
        'total_menu_items': total_menu_items,
        'avg_rating': round(float(avg_rating), 2),
        'recent_orders': recent_orders,
        'recent_revenue': float(recent_revenue) if recent_revenue else None,
        # Today's performance
        'today_orders': today_orders,
        'today_revenue': float(today_revenue) if today_revenue else None,
        'today_new_customers': today_new_customers,
        'average_rating': round(float(avg_rating), 2),
        # This week's trends
        'week_orders': week_orders,
        'week_revenue': float(week_revenue) if week_revenue is not None else None,
        'growth_rate': round(growth_rate, 1) if growth_rate is not None else None
    }
    
    return render_template('reports/dashboard.html', stats=stats)

@reports_bp.route('/sales')
@admin_required
def sales_report():
    """Detailed sales report with filtering"""
    
    # Get filter parameters
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    status = request.args.get('status', '')
    
    # Build query
    query = db.session.query(
        Order.order_id,
        Order.order_date,
        Order.total_amount,
        Order.status,
        User.name.label('customer_name'),
        User.email.label('customer_email'),
        Payment.payment_method,
        Payment.status.label('payment_status')
    ).join(User, Order.user_id == User.user_id).outerjoin(
        Payment, Order.order_id == Payment.order_id
    )
    
    # Apply filters
    if start_date:
        query = query.filter(Order.order_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    
    if end_date:
        query = query.filter(Order.order_date <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    if status:
        query = query.filter(Order.status == status)
    
    # Execute query
    sales_data = query.order_by(Order.order_date.desc()).all()
    
    # Calculate totals
    total_amount = sum(sale.total_amount for sale in sales_data)
    completed_orders = [sale for sale in sales_data if sale.status in ['Delivered', 'Completed']]
    completed_amount = sum(sale.total_amount for sale in completed_orders)
    
    # Group by date for chart data
    daily_sales = {}
    for sale in sales_data:
        date_key = sale.order_date.strftime('%Y-%m-%d')
        if date_key not in daily_sales:
            daily_sales[date_key] = {'orders': 0, 'revenue': 0}
        daily_sales[date_key]['orders'] += 1
        daily_sales[date_key]['revenue'] += float(sale.total_amount)
    
    # Sort dates
    chart_data = []
    for date_key in sorted(daily_sales.keys()):
        chart_data.append({
            'date': date_key,
            'orders': daily_sales[date_key]['orders'],
            'revenue': daily_sales[date_key]['revenue']
        })
    
    # Get order statuses for filter
    order_statuses = db.session.query(Order.status).distinct().all()
    order_statuses = [status[0] for status in order_statuses]
    
    return render_template('reports/sales_report.html',
                         sales_data=sales_data,
                         total_amount=float(total_amount),
                         completed_amount=float(completed_amount),
                         chart_data=chart_data,
                         order_statuses=order_statuses,
                         filters={'start_date': start_date, 'end_date': end_date, 'status': status})

@reports_bp.route('/menu_analysis')
@admin_required
def menu_analysis():
    """Menu item performance analysis"""
    
    # Top selling items
    top_items = db.session.query(
        MenuItem.name,
        MenuItem.category,
        MenuItem.price,
        func.sum(OrderDetails.quantity).label('total_sold'),
        func.sum(OrderDetails.sub_total).label('total_revenue'),
        func.count(OrderDetails.order_detail_id).label('order_count')
    ).join(OrderDetails).group_by(MenuItem.menu_item_id).order_by(
        func.sum(OrderDetails.quantity).desc()
    ).limit(20).all()
    
    # Category performance
    category_performance = db.session.query(
        MenuItem.category,
        func.sum(OrderDetails.quantity).label('total_sold'),
        func.sum(OrderDetails.sub_total).label('total_revenue'),
        func.count(func.distinct(MenuItem.menu_item_id)).label('items_count')
    ).join(OrderDetails).group_by(MenuItem.category).order_by(
        func.sum(OrderDetails.sub_total).desc()
    ).all()
    
    # Items with low sales (need attention)
    low_performing = db.session.query(
        MenuItem.name,
        MenuItem.category,
        MenuItem.price,
        func.coalesce(func.sum(OrderDetails.quantity), 0).label('total_sold')
    ).outerjoin(OrderDetails).group_by(MenuItem.menu_item_id).having(
        func.coalesce(func.sum(OrderDetails.quantity), 0) <= 5
    ).order_by(func.coalesce(func.sum(OrderDetails.quantity), 0).asc()).all()
    
    # Price analysis
    price_analysis = db.session.query(
        case(
            (MenuItem.price < 10, 'Budget (< ₹10)'),
            (and_(MenuItem.price >= 10, MenuItem.price < 25), 'Mid-range (₹10-25)'),
            (MenuItem.price >= 25, 'Premium (₹25+)'),
            else_='Other'
        ).label('price_range'),
        func.sum(OrderDetails.quantity).label('total_sold'),
        func.sum(OrderDetails.sub_total).label('total_revenue')
    ).join(OrderDetails).group_by('price_range').all()
    
    return render_template('reports/menu_analysis.html',
                         top_items=top_items,
                         category_performance=category_performance,
                         low_performing=low_performing,
                         price_analysis=price_analysis)

@reports_bp.route('/customer_analysis')
@admin_required
def customer_analysis():
    """Customer behavior and analysis"""
    
    # Top customers by orders
    top_customers_orders = db.session.query(
        User.name,
        User.email,
        func.count(Order.order_id).label('total_orders'),
        func.sum(Order.total_amount).label('total_spent'),
        func.avg(Order.total_amount).label('avg_order_value')
    ).join(Order).group_by(User.user_id).order_by(
        func.count(Order.order_id).desc()
    ).limit(15).all()
    
    # Top customers by spending
    top_customers_spending = db.session.query(
        User.name,
        User.email,
        func.count(Order.order_id).label('total_orders'),
        func.sum(Order.total_amount).label('total_spent')
    ).join(Order).group_by(User.user_id).order_by(
        func.sum(Order.total_amount).desc()
    ).limit(15).all()
    
    # Customer registration trends (last 12 months)
    month_col = func.strftime('%Y-%m', User.created_date).label('month')
    registration_trends = db.session.query(
        month_col,
        func.count(User.user_id).label('new_customers')
    ).filter(User.role == 'Customer').group_by(month_col).order_by(desc(month_col)).limit(12).all()
    
    # Order frequency analysis - using subquery to avoid aggregate in GROUP BY
    from sqlalchemy import select
    
    # First, get order counts per customer
    order_counts_subq = db.session.query(
        User.user_id,
        func.count(Order.order_id).label('order_count')
    ).outerjoin(Order).filter(
        User.role == 'Customer'
    ).group_by(User.user_id).subquery()
    
    # Then categorize based on order count
    order_frequency = db.session.query(
        case(
            (order_counts_subq.c.order_count == 1, 'One-time (1 order)'),
            (and_(order_counts_subq.c.order_count >= 2, order_counts_subq.c.order_count <= 5), 'Regular (2-5 orders)'),
            (order_counts_subq.c.order_count > 5, 'Loyal (5+ orders)'),
            else_='Other'
        ).label('customer_type'),
        func.count(order_counts_subq.c.user_id).label('customer_count')
    ).select_from(order_counts_subq).group_by('customer_type').all()
    
    return render_template('reports/customer_analysis.html',
                         top_customers_orders=top_customers_orders,
                         top_customers_spending=top_customers_spending,
                         registration_trends=list(reversed(registration_trends)),
                         order_frequency=order_frequency)

@reports_bp.route('/delivery_performance')
@admin_required
def delivery_performance():
    """Delivery and kitchen performance report"""
    
    # Delivery statistics
    total_deliveries = Delivery.query.count()
    completed_deliveries = Delivery.query.filter_by(delivery_status='Delivered').count()
    
    # On-time delivery analysis
    on_time_deliveries = db.session.query(Delivery).filter(
        Delivery.delivery_status == 'Delivered',
        Delivery.actual_time <= Delivery.estimated_time
    ).count()
    
    on_time_percentage = (on_time_deliveries / completed_deliveries * 100) if completed_deliveries > 0 else 0
    
    # Average delivery time
    avg_delivery_time = db.session.query(
        func.avg(
            (func.julianday(Delivery.actual_time) - func.julianday(Delivery.estimated_time)) * 24 * 60
        )
    ).filter(
        Delivery.delivery_status == 'Delivered',
        Delivery.actual_time.isnot(None)
    ).scalar()
    
    # Staff performance
    staff_performance = db.session.query(
        KitchenStaff.staff_name,
        KitchenStaff.department,
        func.count(Delivery.delivery_id).label('total_assigned'),
        func.count(
            case((Delivery.delivery_status == 'Delivered', 1))
        ).label('completed'),
        func.avg(
            case(
                (Delivery.delivery_status == 'Delivered',
                 (func.julianday(Delivery.actual_time) - func.julianday(Delivery.estimated_time)) * 24 * 60)
            )
        ).label('avg_delay_minutes')
    ).join(Delivery).group_by(KitchenStaff.staff_id).order_by(
        func.count(Delivery.delivery_id).desc()
    ).all()
    
    # Delivery status distribution
    status_distribution = db.session.query(
        Delivery.delivery_status,
        func.count(Delivery.delivery_id)
    ).group_by(Delivery.delivery_status).all()
    
    # Monthly delivery trends
    month_col = func.strftime('%Y-%m', Delivery.estimated_time).label('month')
    monthly_trends = db.session.query(
        month_col,
        func.count(Delivery.delivery_id).label('total_deliveries'),
        func.count(
            case((Delivery.delivery_status == 'Delivered', 1))
        ).label('completed_deliveries')
    ).group_by(month_col).order_by(desc(month_col)).limit(12).all()
    
    stats = {
        'total_deliveries': total_deliveries,
        'completed_deliveries': completed_deliveries,
        'on_time_percentage': round(on_time_percentage, 2),
        'avg_delivery_delay': round(avg_delivery_time or 0, 2),
        'staff_performance': staff_performance,
        'status_distribution': dict(status_distribution),
        'monthly_trends': list(reversed(monthly_trends))
    }
    
    return render_template('reports/delivery_performance.html', stats=stats)

@reports_bp.route('/feedback_summary')
@admin_required
def feedback_summary():
    """Feedback analysis and summary report"""
    
    # Overall feedback statistics
    total_feedback = Feedback.query.count()
    avg_rating = db.session.query(func.avg(Feedback.rating)).scalar() or 0
    
    # Rating distribution
    rating_distribution = db.session.query(
        Feedback.rating,
        func.count(Feedback.feedback_id)
    ).group_by(Feedback.rating).all()
    
    # Feedback by type
    type_distribution = db.session.query(
        Feedback.feedback_type,
        func.count(Feedback.feedback_id),
        func.avg(Feedback.rating)
    ).group_by(Feedback.feedback_type).all()
    
    # Monthly feedback trends
    month_col = func.strftime('%Y-%m', Feedback.feedback_date).label('month')
    monthly_feedback = db.session.query(
        month_col,
        func.count(Feedback.feedback_id).label('feedback_count'),
        func.avg(Feedback.rating).label('avg_rating')
    ).group_by(month_col).order_by(desc(month_col)).limit(12).all()
    
    # Recent low ratings (need attention)
    low_ratings = db.session.query(
        Feedback, User, Order
    ).join(User, Feedback.user_id == User.user_id).outerjoin(
        Order, Feedback.order_id == Order.order_id
    ).filter(
        Feedback.rating <= 2
    ).order_by(Feedback.feedback_date.desc()).limit(10).all()
    
    # Best feedback (5-star ratings)
    high_ratings = db.session.query(
        Feedback, User
    ).join(User, Feedback.user_id == User.user_id).filter(
        Feedback.rating == 5
    ).order_by(Feedback.feedback_date.desc()).limit(5).all()
    
    return render_template('reports/feedback_summary.html',
                         total_feedback=total_feedback,
                         avg_rating=round(float(avg_rating), 2),
                         rating_distribution=dict(rating_distribution),
                         type_distribution=type_distribution,
                         monthly_trends=list(reversed(monthly_feedback)),
                         low_ratings=low_ratings,
                         high_ratings=high_ratings)

@reports_bp.route('/export/<report_type>')
@admin_required
def export_report(report_type):
    """Export reports as CSV (simplified implementation)"""
    
    # This is a simplified version - in production, you'd use proper CSV export
    flash(f'Export feature for {report_type} will be available soon!', 'info')
    return redirect(url_for('reports.reports_dashboard'))

@reports_bp.route('/api/chart_data/<chart_type>')
@admin_required
def chart_data_api(chart_type):
    """API endpoint for chart data"""
    
    if chart_type == 'daily_sales':
        # Last 30 days sales data
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        daily_data = db.session.query(
            func.date(Order.order_date).label('date'),
            func.count(Order.order_id).label('orders'),
            func.sum(Order.total_amount).label('revenue')
        ).filter(Order.order_date >= thirty_days_ago).group_by(
            func.date(Order.order_date)
        ).order_by('date').all()
        
        result = []
        for data in daily_data:
            result.append({
                'date': data.date.strftime('%Y-%m-%d'),
                'orders': data.orders,
                'revenue': float(data.revenue)
            })
        
        return jsonify(result)
    
    elif chart_type == 'category_sales':
        # Category wise sales
        category_data = db.session.query(
            MenuItem.category,
            func.sum(OrderDetails.quantity).label('quantity'),
            func.sum(OrderDetails.sub_total).label('revenue')
        ).join(OrderDetails).group_by(MenuItem.category).all()
        
        result = []
        for data in category_data:
            result.append({
                'category': data.category,
                'quantity': int(data.quantity),
                'revenue': float(data.revenue)
            })
        
        return jsonify(result)
    
    return jsonify({'error': 'Invalid chart type'}), 400

@reports_bp.route('/overview')
@admin_required
def overview():
    """System overview report"""
    
    # Overall system statistics
    total_users = User.query.count()
    total_customers = User.query.filter_by(role='Customer').count()
    total_staff = User.query.filter(User.role != 'Customer').count()
    
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    
    total_menu_items = MenuItem.query.count()
    active_menu_items = MenuItem.query.filter_by(availability=True).count()
    
    total_deliveries = Delivery.query.count()
    completed_deliveries = Delivery.query.filter_by(delivery_status='Delivered').count()
    
    total_feedback = Feedback.query.count()
    avg_rating = db.session.query(func.avg(Feedback.rating)).scalar() or 0
    
    total_payments = Payment.query.count()
    completed_payments = Payment.query.filter(
        or_(Payment.status == 'Completed', Payment.status == 'completed')
    ).count()
    
    # Recent activity (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    recent_orders = Order.query.filter(Order.order_date >= seven_days_ago).count()
    recent_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.order_date >= seven_days_ago
    ).scalar() or 0
    
    recent_customers = User.query.filter(
        User.role == 'Customer',
        User.created_date >= seven_days_ago
    ).count()
    
    recent_feedback = Feedback.query.filter(
        Feedback.feedback_date >= seven_days_ago
    ).count()
    
    # Order status breakdown
    order_status_breakdown = db.session.query(
        Order.status,
        func.count(Order.order_id)
    ).group_by(Order.status).all()
    
    # Payment method breakdown
    payment_method_breakdown = db.session.query(
        Payment.payment_method,
        func.count(Payment.payment_id),
        func.sum(Payment.amount)
    ).group_by(Payment.payment_method).all()
    
    # Top categories by revenue
    top_categories = db.session.query(
        MenuItem.category,
        func.sum(OrderDetails.sub_total).label('revenue'),
        func.sum(OrderDetails.quantity).label('items_sold')
    ).join(OrderDetails).group_by(MenuItem.category).order_by(
        func.sum(OrderDetails.sub_total).desc()
    ).limit(5).all()
    
    # System health metrics
    pending_orders = Order.query.filter(Order.status == 'Pending').count()
    in_transit_deliveries = Delivery.query.filter(Delivery.delivery_status == 'In Transit').count()
    pending_payments = Payment.query.filter(
        or_(Payment.status == 'Pending', Payment.status == 'pending')
    ).count()
    
    stats = {
        'total_users': total_users,
        'total_customers': total_customers,
        'total_staff': total_staff,
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'total_menu_items': total_menu_items,
        'active_menu_items': active_menu_items,
        'total_deliveries': total_deliveries,
        'completed_deliveries': completed_deliveries,
        'total_feedback': total_feedback,
        'avg_rating': round(float(avg_rating), 2),
        'total_payments': total_payments,
        'completed_payments': completed_payments,
        'recent_orders': recent_orders,
        'recent_revenue': float(recent_revenue),
        'recent_customers': recent_customers,
        'recent_feedback': recent_feedback,
        'order_status_breakdown': dict(order_status_breakdown),
        'payment_method_breakdown': payment_method_breakdown,
        'top_categories': top_categories,
        'pending_orders': pending_orders,
        'in_transit_deliveries': in_transit_deliveries,
        'pending_payments': pending_payments
    }
    
    return render_template('reports/overview.html', stats=stats)

@reports_bp.route('/daily/<date>')
@admin_required
def daily_report(date):
    """Generate daily report for a specific date"""
    try:
        report_date = datetime.strptime(date, '%Y-%m-%d').date()
        report_date_start = datetime.combine(report_date, datetime.min.time())
        report_date_end = datetime.combine(report_date, datetime.max.time())
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('reports.reports_dashboard'))
    
    # Daily statistics
    daily_orders = Order.query.filter(
        Order.order_date >= report_date_start,
        Order.order_date <= report_date_end
    ).all()
    
    total_orders = len(daily_orders)
    total_revenue = sum(order.total_amount for order in daily_orders)
    completed_orders = [o for o in daily_orders if o.status in ['Delivered', 'Completed']]
    
    daily_customers = User.query.filter(
        User.role == 'Customer',
        User.created_date >= report_date_start,
        User.created_date <= report_date_end
    ).count()
    
    daily_feedback = Feedback.query.filter(
        Feedback.feedback_date >= report_date_start,
        Feedback.feedback_date <= report_date_end
    ).all()
    
    avg_rating = db.session.query(func.avg(Feedback.rating)).filter(
        Feedback.feedback_date >= report_date_start,
        Feedback.feedback_date <= report_date_end
    ).scalar() or 0
    
    # Order status breakdown
    status_breakdown = {}
    for order in daily_orders:
        status = order.status
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
    
    stats = {
        'report_date': report_date.strftime('%Y-%m-%d'),
        'report_type': 'Daily',
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'completed_orders': len(completed_orders),
        'new_customers': daily_customers,
        'total_feedback': len(daily_feedback),
        'avg_rating': round(float(avg_rating), 2),
        'status_breakdown': status_breakdown,
        'orders': daily_orders,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('reports/period_report.html', stats=stats)

@reports_bp.route('/weekly/<start_date>')
@admin_required
def weekly_report(start_date):
    """Generate weekly report starting from a specific date"""
    try:
        week_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        week_start_dt = datetime.combine(week_start, datetime.min.time())
        week_end = week_start + timedelta(days=6)
        week_end_dt = datetime.combine(week_end, datetime.max.time())
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('reports.reports_dashboard'))
    
    # Weekly statistics
    weekly_orders = Order.query.filter(
        Order.order_date >= week_start_dt,
        Order.order_date <= week_end_dt
    ).all()
    
    total_orders = len(weekly_orders)
    total_revenue = sum(order.total_amount for order in weekly_orders)
    completed_orders = [o for o in weekly_orders if o.status in ['Delivered', 'Completed']]
    
    weekly_customers = User.query.filter(
        User.role == 'Customer',
        User.created_date >= week_start_dt,
        User.created_date <= week_end_dt
    ).count()
    
    weekly_feedback = Feedback.query.filter(
        Feedback.feedback_date >= week_start_dt,
        Feedback.feedback_date <= week_end_dt
    ).all()
    
    avg_rating = db.session.query(func.avg(Feedback.rating)).filter(
        Feedback.feedback_date >= week_start_dt,
        Feedback.feedback_date <= week_end_dt
    ).scalar() or 0
    
    # Order status breakdown
    status_breakdown = {}
    for order in weekly_orders:
        status = order.status
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
    
    # Daily breakdown
    daily_breakdown = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        day_orders = [o for o in weekly_orders if day_start <= o.order_date <= day_end]
        day_revenue = sum(o.total_amount for o in day_orders)
        daily_breakdown.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day.strftime('%A'),
            'orders': len(day_orders),
            'revenue': float(day_revenue)
        })
    
    stats = {
        'report_date': f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}",
        'report_type': 'Weekly',
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'completed_orders': len(completed_orders),
        'new_customers': weekly_customers,
        'total_feedback': len(weekly_feedback),
        'avg_rating': round(float(avg_rating), 2),
        'status_breakdown': status_breakdown,
        'daily_breakdown': daily_breakdown,
        'orders': weekly_orders,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('reports/period_report.html', stats=stats)

@reports_bp.route('/monthly/<start_date>')
@admin_required
def monthly_report(start_date):
    """Generate monthly report for a specific month"""
    try:
        month_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        month_start_dt = datetime.combine(month_start, datetime.min.time())
        # Get last day of month
        if month_start.month == 12:
            month_end = month_start.replace(day=31)
        else:
            next_month = month_start.replace(month=month_start.month + 1, day=1)
            month_end = next_month - timedelta(days=1)
        month_end_dt = datetime.combine(month_end, datetime.max.time())
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('reports.reports_dashboard'))
    
    # Monthly statistics
    monthly_orders = Order.query.filter(
        Order.order_date >= month_start_dt,
        Order.order_date <= month_end_dt
    ).all()
    
    total_orders = len(monthly_orders)
    total_revenue = sum(order.total_amount for order in monthly_orders)
    completed_orders = [o for o in monthly_orders if o.status in ['Delivered', 'Completed']]
    
    monthly_customers = User.query.filter(
        User.role == 'Customer',
        User.created_date >= month_start_dt,
        User.created_date <= month_end_dt
    ).count()
    
    monthly_feedback = Feedback.query.filter(
        Feedback.feedback_date >= month_start_dt,
        Feedback.feedback_date <= month_end_dt
    ).all()
    
    avg_rating = db.session.query(func.avg(Feedback.rating)).filter(
        Feedback.feedback_date >= month_start_dt,
        Feedback.feedback_date <= month_end_dt
    ).scalar() or 0
    
    # Order status breakdown
    status_breakdown = {}
    for order in monthly_orders:
        status = order.status
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
    
    # Weekly breakdown
    weekly_breakdown = []
    current_week_start = month_start
    week_num = 1
    while current_week_start <= month_end:
        week_end = min(current_week_start + timedelta(days=6), month_end)
        week_start_dt = datetime.combine(current_week_start, datetime.min.time())
        week_end_dt = datetime.combine(week_end, datetime.max.time())
        
        week_orders = [o for o in monthly_orders if week_start_dt <= o.order_date <= week_end_dt]
        week_revenue = sum(o.total_amount for o in week_orders)
        
        weekly_breakdown.append({
            'week': f"Week {week_num}",
            'date_range': f"{current_week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}",
            'orders': len(week_orders),
            'revenue': float(week_revenue)
        })
        
        current_week_start = week_end + timedelta(days=1)
        week_num += 1
    
    stats = {
        'report_date': month_start.strftime('%B %Y'),
        'report_type': 'Monthly',
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'completed_orders': len(completed_orders),
        'new_customers': monthly_customers,
        'total_feedback': len(monthly_feedback),
        'avg_rating': round(float(avg_rating), 2),
        'status_breakdown': status_breakdown,
        'weekly_breakdown': weekly_breakdown,
        'orders': monthly_orders,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('reports/period_report.html', stats=stats)

@reports_bp.route('/custom')
@admin_required
def custom_report():
    """Generate custom report based on parameters"""
    
    date_from = request.args.get('dateFrom', '')
    date_to = request.args.get('dateTo', '')
    include_orders = request.args.get('includeOrders', 'false') == 'true'
    include_revenue = request.args.get('includeRevenue', 'false') == 'true'
    include_customers = request.args.get('includeCustomers', 'false') == 'true'
    include_feedback = request.args.get('includeFeedback', 'false') == 'true'
    
    try:
        start_date = datetime.strptime(date_from, '%Y-%m-%d')
        end_date = datetime.strptime(date_to, '%Y-%m-%d')
        end_date = datetime.combine(end_date.date(), datetime.max.time())
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('reports.reports_dashboard'))
    
    stats = {
        'report_date': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'report_type': 'Custom',
        'include_orders': include_orders,
        'include_revenue': include_revenue,
        'include_customers': include_customers,
        'include_feedback': include_feedback
    }
    
    # Only calculate requested metrics
    if include_orders or include_revenue:
        orders = Order.query.filter(
            Order.order_date >= start_date,
            Order.order_date <= end_date
        ).all()
        
        if include_orders:
            stats['total_orders'] = len(orders)
            stats['completed_orders'] = len([o for o in orders if o.status in ['Delivered', 'Completed']])
            status_breakdown = {}
            for order in orders:
                status = order.status
                status_breakdown[status] = status_breakdown.get(status, 0) + 1
            stats['status_breakdown'] = status_breakdown
            stats['orders'] = orders
        
        if include_revenue:
            stats['total_revenue'] = float(sum(order.total_amount for order in orders))
    
    if include_customers:
        customers = User.query.filter(
            User.role == 'Customer',
            User.created_date >= start_date,
            User.created_date <= end_date
        ).count()
        stats['new_customers'] = customers
    
    if include_feedback:
        feedback = Feedback.query.filter(
            Feedback.feedback_date >= start_date,
            Feedback.feedback_date <= end_date
        ).all()
        
        avg_rating = db.session.query(func.avg(Feedback.rating)).filter(
            Feedback.feedback_date >= start_date,
            Feedback.feedback_date <= end_date
        ).scalar() or 0
        
        stats['total_feedback'] = len(feedback)
        stats['avg_rating'] = round(float(avg_rating), 2)
    
    return render_template('reports/period_report.html', stats=stats)