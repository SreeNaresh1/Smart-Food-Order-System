# 🔐 Role-Based Access Control (RBAC) Guide
## Food Ordering System - Complete Access Control Documentation

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Role Hierarchy](#role-hierarchy)
3. [Detailed Access Matrix](#detailed-access-matrix)
4. [Implementation Guide](#implementation-guide)
5. [Security Best Practices](#security-best-practices)

---

## 🎯 Overview

The Food Ordering System implements a **4-tier role-based access control system**:
- **Admin** - Full system control
- **Supervisor** - Management oversight
- **Employee** - Operational tasks
- **Customer** - Order placement & tracking

Each role has specific permissions designed to maintain security and operational efficiency.

---

## 👥 Role Hierarchy

```
┌─────────────────────────────────────────────┐
│              ADMIN (Level 4)                │
│         ✓ Full System Access                │
└─────────────────┬───────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
┌────────▼──────────┐  ┌──▼──────────────────┐
│  SUPERVISOR       │  │  EMPLOYEE           │
│    (Level 3)      │  │    (Level 2)        │
│  ✓ Management     │  │  ✓ Operations       │
│  ✓ Oversight      │  │  ✓ Task Execution   │
└───────────────────┘  └─────────────────────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌──────────▼──────────┐
         │    CUSTOMER         │
         │     (Level 1)       │
         │  ✓ Order & Track    │
         └─────────────────────┘
```

---

## 📊 Detailed Access Matrix

### 🔴 ADMIN - Complete System Access

#### ✅ Can Access:
| Feature Area | Permissions |
|-------------|-------------|
| **Dashboard** | • Full system statistics<br>• All user metrics<br>• Revenue analytics<br>• Global performance reports |
| **User Management** | • View all users (Admin, Supervisor, Employee, Customer)<br>• Create new users (all roles)<br>• Edit user details<br>• Delete users (except own account)<br>• Reset passwords<br>• Assign/change roles |
| **Menu Management** | • Add new menu items<br>• Edit menu items (name, price, category)<br>• Delete menu items<br>• Set availability<br>• Upload/change images<br>• Set discounts & promotions<br>• Manage categories |
| **Order Management** | • View ALL orders (system-wide)<br>• Modify order status<br>• Cancel any order<br>• Refund orders<br>• Assign orders to staff<br>• View order history<br>• Export order data |
| **Delivery Management** | • View all deliveries<br>• Assign delivery personnel<br>• Track all deliveries<br>• Update delivery status<br>• Manage delivery zones |
| **Payment Management** | • View all payments<br>• Process refunds<br>• View transaction details<br>• Generate payment reports |
| **Kitchen Management** | • View kitchen staff<br>• Manage kitchen assignments<br>• Monitor preparation times<br>• Access kitchen dashboard |
| **Feedback Management** | • View all customer feedback<br>• Respond to feedback<br>• Delete inappropriate feedback<br>• Generate satisfaction reports |
| **Reports & Analytics** | • Financial reports<br>• Sales analytics<br>• Customer analytics<br>• Staff performance reports<br>• Revenue trends<br>• Export all reports |
| **System Settings** | • Configure system settings<br>• Manage integrations<br>• Database management<br>• Backup/restore |

#### ❌ Cannot Access:
- Nothing - Admin has full access to all features

---

### 🟡 SUPERVISOR - Management & Oversight

#### ✅ Can Access:
| Feature Area | Permissions |
|-------------|-------------|
| **Dashboard** | • Department/branch statistics<br>• Team performance metrics<br>• Order overview (assigned area)<br>• Revenue for assigned area |
| **User Management** | • View Employees & Customers<br>• Create Employee accounts<br>• Edit Employee details<br>• View Supervisor list (read-only)<br>• **Cannot create/edit Admins** |
| **Menu Management** | • View all menu items<br>• Edit availability status<br>• Update stock levels<br>• Suggest menu changes<br>• **Cannot add/delete items**<br>• **Cannot modify prices** (requires admin approval) |
| **Order Management** | • View orders in assigned area/branch<br>• Update order status (Confirmed → Preparing → Ready)<br>• Assign orders to employees<br>• **Cannot cancel confirmed orders without approval**<br>• View order history (assigned area) |
| **Delivery Management** | • View deliveries in assigned area<br>• Assign delivery personnel<br>• Track deliveries (assigned area)<br>• Update delivery status |
| **Payment Management** | • View payments (assigned area)<br>• Generate payment reports (limited)<br>• **Cannot process refunds** |
| **Kitchen Management** | • Monitor kitchen staff performance<br>• Assign kitchen tasks<br>• View preparation times<br>• Manage kitchen workflow |
| **Feedback Management** | • View feedback (assigned area)<br>• Respond to customer feedback<br>• Escalate issues to admin |
| **Reports & Analytics** | • Branch/area performance reports<br>• Employee performance metrics<br>• Daily sales reports<br>• **Cannot access financial analytics**<br>• **Cannot export system-wide data** |

#### ❌ Cannot Access:
- ❌ Create/edit Admin or Supervisor accounts
- ❌ Delete users (any role)
- ❌ Add/delete menu items
- ❌ Modify menu prices without approval
- ❌ View/manage other branches' data
- ❌ Access system-wide financial reports
- ❌ System settings & configuration
- ❌ Database management
- ❌ Process refunds
- ❌ Cancel confirmed orders without admin approval
- ❌ Access global analytics

---

### 🟢 EMPLOYEE - Operational Tasks

#### ✅ Can Access:
| Feature Area | Permissions |
|-------------|-------------|
| **Dashboard** | • Personal task dashboard<br>• Assigned orders count<br>• Today's performance<br>• Shift information |
| **User Management** | • View own profile<br>• Edit own profile (limited fields)<br>• **Cannot view other users** |
| **Menu Management** | • View menu items (read-only)<br>• Check item availability<br>• **Cannot make any changes** |
| **Order Management** | • View assigned orders ONLY<br>• Update status of assigned orders (Preparing → Ready)<br>• View order details<br>• **Cannot cancel orders**<br>• **Cannot assign orders** |
| **Delivery Management** | • View assigned deliveries<br>• Update delivery status (Picked Up → In Transit → Delivered)<br>• Mark orders as delivered<br>• **Cannot assign deliveries** |
| **Payment Management** | • Mark cash payments as received<br>• **Cannot view payment history**<br>• **Cannot process refunds** |
| **Kitchen Management** | • View assigned kitchen tasks<br>• Update preparation status<br>• Mark dishes as ready<br>• **Cannot manage other staff** |
| **Feedback Management** | • **Cannot access feedback system** (unless customer) |
| **Reports & Analytics** | • View personal performance metrics<br>• Today's completed tasks<br>• **Cannot access team reports** |

#### ❌ Cannot Access:
- ❌ Create/edit/delete users
- ❌ Add/edit/delete menu items
- ❌ View orders not assigned to them
- ❌ Cancel or refund orders
- ❌ Assign tasks to other employees
- ❌ Access financial data
- ❌ View other employees' performance
- ❌ System settings
- ❌ Customer management
- ❌ Payment processing (except cash collection)
- ❌ Feedback management
- ❌ Reports & analytics (except personal)
- ❌ Delivery assignment

---

### 🔵 CUSTOMER - Order & Track

#### ✅ Can Access:
| Feature Area | Permissions |
|-------------|-------------|
| **Dashboard** | • Personal order statistics<br>• Total spent<br>• Favorite items<br>• Recommendations<br>• Active order tracking |
| **User Management** | • View own profile<br>• Edit own profile (name, phone, address, password)<br>• **Cannot view other users** |
| **Menu Management** | • View all available menu items<br>• Browse by category<br>• Filter (vegetarian, spicy, new, popular)<br>• View prices & descriptions<br>• **Cannot make any changes** |
| **Order Management** | • Place new orders<br>• View own orders ONLY<br>• Track order status<br>• Cancel pending orders (before confirmation)<br>• Re-order previous items<br>• **Cannot view others' orders** |
| **Delivery Management** | • Track own deliveries<br>• View delivery status<br>• Update delivery address (before dispatch)<br>• **Cannot manage deliveries** |
| **Payment Management** | • Select payment method<br>• Make payments<br>• View own payment history<br>• **Cannot process refunds** (must contact admin) |
| **Feedback Management** | • Submit feedback for completed orders<br>• View own feedback history<br>• Rate orders & items<br>• **Cannot view others' feedback** |
| **Reports & Analytics** | • View personal order history<br>• Total spending summary<br>• Favorite items list<br>• **Cannot access system analytics** |

#### ❌ Cannot Access:
- ❌ Any user management features
- ❌ Add/edit/delete menu items
- ❌ View other customers' orders
- ❌ Assign or manage deliveries
- ❌ Access kitchen system
- ❌ View financial data
- ❌ System settings
- ❌ Employee management
- ❌ Reports & analytics (system-wide)
- ❌ Cancel confirmed/preparing orders
- ❌ Process own refunds (must request)

---

## 💻 Implementation Guide

### 1. Enhanced Role Decorator (app.py)

The current decorator needs enhancement. Here's the improved version:

```python
# Enhanced role required decorator with logging
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
            
            # Check if user role is allowed
            user_role = user.role.lower()
            allowed_roles_lower = [role.lower() for role in allowed_roles]
            
            if user_role not in allowed_roles_lower:
                flash(f'Access denied. This page requires {", ".join(allowed_roles)} privileges.', 'danger')
                # Log unauthorized access attempt
                print(f"Unauthorized access attempt: User {user.name} ({user_role}) tried to access {request.endpoint}")
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 2. Route Protection Examples

#### Admin-Only Routes
```python
# routes/users.py
@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    # Only admins can delete users
    pass

# routes/menu.py
@menu_bp.route('/add', methods=['GET', 'POST'])
@role_required('admin')
def add_menu_item():
    # Only admins can add menu items
    pass
```

#### Admin + Supervisor Routes
```python
# routes/orders.py
@orders_bp.route('/list')
@role_required('admin', 'supervisor')
def list_orders():
    user = User.query.get(session['user_id'])
    
    if user.role.lower() == 'admin':
        # Show all orders
        orders = Order.query.all()
    else:  # supervisor
        # Show only orders in assigned area
        orders = Order.query.filter_by(branch_id=user.branch_id).all()
    
    return render_template('orders/list.html', orders=orders)
```

#### Employee Routes
```python
# routes/orders.py
@orders_bp.route('/my-tasks')
@role_required('employee')
def my_tasks():
    user_id = session['user_id']
    # Show only assigned orders
    orders = Order.query.filter_by(assigned_to=user_id).all()
    return render_template('orders/my_tasks.html', orders=orders)
```

#### Customer Routes
```python
# routes/orders.py
@orders_bp.route('/my-orders')
@role_required('customer')
def my_orders():
    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('orders/my_orders.html', orders=orders)
```

### 3. Template-Level Access Control

Add role checks in templates to hide/show features:

```html
<!-- base.html or dashboard -->
{% if user.role|lower == 'admin' %}
    <!-- Admin-only features -->
    <li><a href="{{ url_for('users.list_users') }}">User Management</a></li>
    <li><a href="{{ url_for('menu.add_menu_item') }}">Add Menu Item</a></li>
    <li><a href="{{ url_for('reports.financial') }}">Financial Reports</a></li>
{% endif %}

{% if user.role|lower in ['admin', 'supervisor'] %}
    <!-- Admin & Supervisor features -->
    <li><a href="{{ url_for('orders.list_orders') }}">Order Management</a></li>
    <li><a href="{{ url_for('delivery.track_all') }}">Track Deliveries</a></li>
{% endif %}

{% if user.role|lower == 'employee' %}
    <!-- Employee features -->
    <li><a href="{{ url_for('orders.my_tasks') }}">My Tasks</a></li>
    <li><a href="{{ url_for('kitchen.my_assignments') }}">Kitchen Tasks</a></li>
{% endif %}

{% if user.role|lower == 'customer' %}
    <!-- Customer features -->
    <li><a href="{{ url_for('menu.browse') }}">Browse Menu</a></li>
    <li><a href="{{ url_for('orders.my_orders') }}">My Orders</a></li>
    <li><a href="{{ url_for('feedback.submit') }}">Feedback</a></li>
{% endif %}
```

### 4. Database Model Updates

Ensure your User model supports role-based queries:

```python
# models.py - User model enhancements
class User(db.Model):
    # ... existing fields ...
    
    def has_role(self, *roles):
        """Check if user has any of the specified roles"""
        return self.role.lower() in [role.lower() for role in roles]
    
    def can_access(self, feature):
        """Check if user can access a specific feature"""
        permissions = {
            'admin': ['*'],  # All features
            'supervisor': [
                'view_orders', 'manage_employees', 'update_menu_availability',
                'assign_deliveries', 'view_reports_limited', 'manage_feedback'
            ],
            'employee': [
                'view_assigned_orders', 'update_order_status', 'view_menu',
                'update_delivery_status', 'mark_payment_received'
            ],
            'customer': [
                'browse_menu', 'place_order', 'view_own_orders',
                'track_delivery', 'submit_feedback', 'view_profile'
            ]
        }
        
        role_permissions = permissions.get(self.role.lower(), [])
        return '*' in role_permissions or feature in role_permissions
    
    def is_admin(self):
        return self.role.lower() == 'admin'
    
    def is_supervisor(self):
        return self.role.lower() == 'supervisor'
    
    def is_employee(self):
        return self.role.lower() == 'employee'
    
    def is_customer(self):
        return self.role.lower() == 'customer'
```

---

## 🔒 Security Best Practices

### 1. **Always Verify on Server Side**
- Never rely solely on template-level hiding
- Always use `@role_required` decorator on routes
- Double-check permissions in route handlers

### 2. **Principle of Least Privilege**
- Give users minimum access needed for their role
- Don't grant "just in case" permissions
- Regularly audit user roles

### 3. **Session Security**
```python
# app.py configuration
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Auto logout
```

### 4. **Logging & Monitoring**
```python
import logging

def log_access_attempt(user, endpoint, allowed):
    status = "ALLOWED" if allowed else "DENIED"
    logging.info(f"Access {status}: User {user.name} ({user.role}) -> {endpoint}")
```

### 5. **Password Security**
```python
# Enforce strong passwords
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a number"
    return True, "Password is valid"
```

### 6. **Rate Limiting**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: session.get('user_id'))

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Prevent brute force attacks
    pass
```

---

## 🧪 Testing Access Control

### Test Cases

1. **Admin Tests**
   - ✓ Can access all routes
   - ✓ Can create/edit/delete users
   - ✓ Can manage menu items

2. **Supervisor Tests**
   - ✓ Can view orders in assigned area
   - ✗ Cannot access system-wide financial reports
   - ✗ Cannot delete users

3. **Employee Tests**
   - ✓ Can view assigned orders
   - ✗ Cannot view all orders
   - ✗ Cannot access user management

4. **Customer Tests**
   - ✓ Can browse menu and place orders
   - ✗ Cannot access kitchen or delivery management
   - ✗ Cannot view other customers' data

---

## 📝 Quick Reference Table

| Feature | Admin | Supervisor | Employee | Customer |
|---------|-------|------------|----------|----------|
| **Dashboard Access** | ✅ Full | ✅ Limited | ✅ Personal | ✅ Personal |
| **User Management** | ✅ All | ⚠️ Employees Only | ❌ | ❌ |
| **Add/Delete Menu Items** | ✅ | ❌ | ❌ | ❌ |
| **Edit Menu Availability** | ✅ | ✅ | ❌ | ❌ |
| **View All Orders** | ✅ | ⚠️ Area Only | ❌ | ❌ |
| **Cancel Orders** | ✅ | ⚠️ Limited | ❌ | ⚠️ Pending Only |
| **Assign Deliveries** | ✅ | ✅ | ❌ | ❌ |
| **Update Order Status** | ✅ | ✅ | ⚠️ Assigned Only | ❌ |
| **Process Refunds** | ✅ | ❌ | ❌ | ❌ |
| **Financial Reports** | ✅ | ⚠️ Limited | ❌ | ❌ |
| **System Settings** | ✅ | ❌ | ❌ | ❌ |
| **Submit Feedback** | ✅ | ✅ | ✅ | ✅ |
| **View Feedback** | ✅ All | ⚠️ Area Only | ❌ | ⚠️ Own Only |

**Legend:**
- ✅ Full Access
- ⚠️ Limited/Conditional Access
- ❌ No Access

---

## 📞 Support & Questions

For implementation questions or access control issues:
1. Review this documentation
2. Check route decorators are correctly applied
3. Verify user role in database
4. Check session data
5. Review application logs

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-18  
**Author:** Food Ordering System Development Team
