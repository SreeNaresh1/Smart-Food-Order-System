from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Database instance will be set by app.py
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin, Supervisor, Employee, Customer
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    
    # Two-Factor Authentication fields
    two_factor_enabled = db.Column(db.Boolean, default=False)
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    backup_codes = db.Column(db.Text, nullable=True)  # Comma-separated encrypted codes
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='user', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    login_history = db.relationship('LoginHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    trusted_devices = db.relationship('TrustedDevice', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Role checking helper methods
    def has_role(self, *roles):
        """Check if user has any of the specified roles (case-insensitive)"""
        return self.role.lower() in [role.lower() for role in roles]
    
    def is_admin(self):
        """Check if user is an admin"""
        return self.role.lower() == 'admin'
    
    def is_supervisor(self):
        """Check if user is a supervisor"""
        return self.role.lower() == 'supervisor'
    
    def is_employee(self):
        """Check if user is an employee"""
        return self.role.lower() == 'employee'
    
    def is_customer(self):
        """Check if user is a customer"""
        return self.role.lower() == 'customer'
    
    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.is_admin() or self.is_supervisor()
    
    def can_edit_menu(self):
        """Check if user can fully edit menu items"""
        return self.is_admin()
    
    def can_view_all_orders(self):
        """Check if user can view all orders"""
        return self.is_admin() or self.is_supervisor()
    
    def can_access(self, feature):
        """Check if user can access a specific feature"""
        permissions = {
            'admin': ['*'],  # All features
            'supervisor': [
                'view_orders', 'manage_employees', 'update_menu_availability',
                'assign_deliveries', 'view_reports_limited', 'manage_feedback',
                'view_kitchen', 'assign_staff', 'view_payments_limited'
            ],
            'employee': [
                'view_assigned_orders', 'update_order_status', 'view_menu',
                'update_delivery_status', 'mark_payment_received', 'view_own_tasks'
            ],
            'customer': [
                'browse_menu', 'place_order', 'view_own_orders',
                'track_delivery', 'submit_feedback', 'view_profile', 'make_payment'
            ]
        }
        
        role_permissions = permissions.get(self.role.lower(), [])
        return '*' in role_permissions or feature in role_permissions
    
    def __repr__(self):
        return f'<User {self.name}>'

class MenuItem(db.Model):
    __tablename__ = 'menuitem'
    
    menu_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.Boolean, default=True, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    
    # Filter attributes
    is_vegetarian = db.Column(db.Boolean, default=False, nullable=False)
    is_spicy = db.Column(db.Boolean, default=False, nullable=False)
    is_popular = db.Column(db.Boolean, default=False, nullable=False)
    is_new = db.Column(db.Boolean, default=False, nullable=False)
    discount = db.Column(db.Numeric(5, 2), default=0, nullable=False)
    
    # Relationships
    order_details = db.relationship('OrderDetails', backref='menu_item', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='menu_item', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'

class Order(db.Model):
    __tablename__ = 'order'
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Confirmed, Preparing, Ready, Delivered, Cancelled
    delivery_address = db.Column(db.Text, nullable=True)
    order_time = db.Column(db.Time, nullable=True)
    estimated_time = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    order_details = db.relationship('OrderDetails', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='order', lazy=True, cascade='all, delete-orphan')
    delivery = db.relationship('Delivery', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_id}>'

class OrderDetails(db.Model):
    __tablename__ = 'orderdetails'
    
    order_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.menu_item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    sub_total = db.Column(db.Numeric(10, 2), nullable=False)
    special_instructions = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<OrderDetails {self.order_detail_id}>'

class Payment(db.Model):
    __tablename__ = 'payment'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # Cash, Card, Online, UPI
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    transaction_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Completed, Failed, Refunded
    
    def __repr__(self):
        return f'<Payment {self.payment_id}>'

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 scale
    comments = db.Column(db.Text, nullable=True)
    feedback_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    feedback_type = db.Column(db.String(50), nullable=False)  # Food, Service, Delivery, App
    
    def __repr__(self):
        return f'<Feedback {self.feedback_id}>'

class KitchenStaff(db.Model):
    __tablename__ = 'kitchenstaff'
    
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Chef, Assistant, Manager
    phone = db.Column(db.String(20), nullable=False)
    shift_time = db.Column(db.String(50), nullable=False)  # Morning, Evening, Night
    department = db.Column(db.String(50), nullable=False)  # Kitchen, Preparation, Cleaning
    status = db.Column(db.String(20), default='Active', nullable=False)  # Active, Inactive, On Leave
    
    # Relationships
    deliveries = db.relationship('Delivery', backref='staff', lazy=True)
    
    def __repr__(self):
        return f'<KitchenStaff {self.staff_name}>'

class Delivery(db.Model):
    __tablename__ = 'delivery'
    
    delivery_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('kitchenstaff.staff_id'), nullable=True)
    estimated_time = db.Column(db.DateTime, nullable=True)
    actual_time = db.Column(db.DateTime, nullable=True)
    delivery_status = db.Column(db.String(20), default='Assigned', nullable=False)  # Assigned, In Transit, Delivered, Failed
    tracking_code = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f'<Delivery {self.delivery_id}>'

class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    
    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.menu_item_id'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # Popular, Personal, Similar, Seasonal
    score = db.Column(db.Float, nullable=False)  # Recommendation confidence score
    created_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    ai_model = db.Column(db.String(50), default='Content-Based', nullable=False)
    
    def __repr__(self):
        return f'<Recommendation {self.recommendation_id}>'

class LoginHistory(db.Model):
    """Track all login attempts for security monitoring"""
    __tablename__ = 'login_history'
    
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # Supports IPv4 and IPv6
    user_agent = db.Column(db.String(255), nullable=True)  # Browser info
    location = db.Column(db.String(100), nullable=True)  # City/Country
    login_method = db.Column(db.String(50), nullable=False)  # password, otp, backup_code
    status = db.Column(db.String(20), nullable=False)  # success, failed, locked
    failure_reason = db.Column(db.String(100), nullable=True)  # wrong_password, wrong_otp, account_locked
    device_fingerprint = db.Column(db.String(255), nullable=True)  # Unique device identifier
    
    def __repr__(self):
        return f'<LoginHistory {self.history_id} - {self.status}>'

class TrustedDevice(db.Model):
    """Store trusted devices to skip 2FA"""
    __tablename__ = 'trusted_device'
    
    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    device_fingerprint = db.Column(db.String(255), unique=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=True)  # e.g., "Chrome on Windows"
    trusted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_used = db.Column(db.DateTime, default=datetime.now, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)  # Trust expires after 30 days
    ip_address = db.Column(db.String(45), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<TrustedDevice {self.device_name}>'
