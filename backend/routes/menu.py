from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from backend.models import db, MenuItem
from functools import wraps

menu_bp = Blueprint('menu', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
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

@menu_bp.route('/')
@login_required
def list_menu():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = MenuItem.query
    
    if category:
        query = query.filter(MenuItem.category == category)
    
    if search:
        query = query.filter(MenuItem.name.contains(search) | 
                           MenuItem.description.contains(search))
    
    menu_items = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = db.session.query(MenuItem.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('menu/list.html', 
                         menu_items=menu_items, 
                         categories=categories,
                         current_category=category,
                         search_term=search)

@menu_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_menu_item():
    if request.method == 'POST':
        # Use correct form field names from the template
        name = request.form.get('item_name', '')
        description = request.form.get('description', '')
        price = request.form.get('price', 0)
        category = request.form.get('category', '')
        availability = request.form.get('availability', 'Available') == 'Available'
        image = request.form.get('image', '')
        
        # Additional attributes for filtering
        is_vegetarian = 'is_vegetarian' in request.form
        is_spicy = 'is_spicy' in request.form
        is_popular = 'is_popular' in request.form
        is_new = 'is_new' in request.form
        discount = float(request.form.get('discount', 0))
        
        # Validate required fields
        if not name or not price or not category:
            flash('Please fill in all required fields.', 'danger')
            return render_template('menu/add.html')
        
        try:
            price = float(price)
        except ValueError:
            flash('Invalid price value.', 'danger')
            return render_template('menu/add.html')
        
        menu_item = MenuItem(
            name=name,
            description=description,
            price=price,
            category=category,
            availability=availability,
            image=image,
            is_vegetarian=is_vegetarian,
            is_spicy=is_spicy,
            is_popular=is_popular,
            is_new=is_new,
            discount=discount
        )
        
        try:
            db.session.add(menu_item)
            db.session.commit()
            flash('Menu item added successfully!', 'success')
            return redirect(url_for('menu.list_menu'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding menu item.', 'danger')
    
    return render_template('menu/add.html')

@menu_bp.route('/edit/<int:menu_item_id>', methods=['GET', 'POST'])
@admin_or_supervisor_required
def edit_menu_item(menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    user_role = session.get('user_role', '').lower()
    
    if request.method == 'POST':
        # Admin can edit everything
        if user_role == 'admin':
            menu_item.name = request.form.get('item_name', menu_item.name)
            menu_item.description = request.form.get('description', menu_item.description)
            
            try:
                menu_item.price = float(request.form.get('price', menu_item.price))
            except ValueError:
                flash('Invalid price value.', 'danger')
                return render_template('menu/edit.html', menu_item=menu_item, user_role=user_role)
                
            menu_item.category = request.form.get('category', menu_item.category)
            menu_item.image = request.form.get('image', menu_item.image)
            
            # Update filter attributes
            menu_item.is_vegetarian = 'is_vegetarian' in request.form
            menu_item.is_spicy = 'is_spicy' in request.form
            menu_item.is_popular = 'is_popular' in request.form
            menu_item.is_new = 'is_new' in request.form
            menu_item.discount = float(request.form.get('discount', 0))
        
        # Supervisor can only edit availability
        menu_item.availability = request.form.get('availability', 'Available') == 'Available'
        
        try:
            db.session.commit()
            flash('Menu item updated successfully!', 'success')
            return redirect(url_for('menu.list_menu'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating menu item.', 'danger')
    
    return render_template('menu/edit.html', menu_item=menu_item, user_role=user_role)

@menu_bp.route('/toggle-availability/<int:menu_item_id>', methods=['POST'])
@admin_or_supervisor_required
def toggle_availability(menu_item_id):
    """Quick toggle for availability - accessible to both admin and supervisor"""
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    
    try:
        menu_item.availability = not menu_item.availability
        db.session.commit()
        status = "available" if menu_item.availability else "unavailable"
        flash(f'Menu item marked as {status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating menu item availability.', 'danger')
    
    return redirect(url_for('menu.list_menu'))

@menu_bp.route('/delete/<int:menu_item_id>', methods=['POST'])
@admin_required
def delete_menu_item(menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    
    try:
        db.session.delete(menu_item)
        db.session.commit()
        flash('Menu item deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting menu item.', 'danger')
    
    return redirect(url_for('menu.list_menu'))

@menu_bp.route('/view/<int:menu_item_id>')
@login_required
def view_menu_item(menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    return render_template('menu/view.html', menu_item=menu_item)

@menu_bp.route('/api/menu_items')
@login_required
def api_menu_items():
    """API endpoint for getting menu items (for AJAX calls)"""
    category = request.args.get('category', '')
    available_only = request.args.get('available_only', 'true') == 'true'
    
    query = MenuItem.query
    
    if category:
        query = query.filter(MenuItem.category == category)
    
    if available_only:
        query = query.filter(MenuItem.availability == True)
    
    menu_items = query.all()
    
    result = []
    for item in menu_items:
        result.append({
            'menu_item_id': item.menu_item_id,
            'name': item.name,
            'description': item.description,
            'price': float(item.price),
            'category': item.category,
            'availability': item.availability,
            'image': item.image
        })
    
    return jsonify(result)
