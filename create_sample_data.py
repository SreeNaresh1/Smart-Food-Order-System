"""
Sample data generator for Smart Food Ordering System
Run this script to populate the database with test data
"""

import os
import sys
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, MenuItem, Order, OrderDetails, Payment, Feedback, Delivery, KitchenStaff, Recommendation

def create_sample_data():
    """Create sample data for the food ordering system"""
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        print("Creating sample users...")
        create_sample_users()
        
        print("Creating sample menu items...")
        create_sample_menu_items()
        
        print("Creating sample kitchen staff...")
        create_sample_kitchen_staff()
        
        print("Creating sample orders...")
        create_sample_orders()
        
        print("Creating sample payments...")
        create_sample_payments()
        
        print("Creating sample feedback...")
        create_sample_feedback()
        
        print("Creating sample deliveries...")
        create_sample_deliveries()
        
        print("Creating sample recommendations...")
        create_sample_recommendations()
        
        print("Sample data creation completed successfully!")

def create_sample_users():
    """Create sample users with different roles"""
    
    # Admin user
    if not User.query.filter_by(email='admin@foodsystem.com').first():
        admin = User(
            name='System Administrator',
            email='admin@foodsystem.com',
            phone='9876543210',
            role='Admin',
            password=generate_password_hash('admin123'),
            address='Admin Office, Food System HQ'
        )
        db.session.add(admin)
    
    # Supervisor
    supervisor = User(
        name='John Manager',
        email='supervisor@foodsystem.com',
        phone='9876543211',
        role='Supervisor',
        password=generate_password_hash('supervisor123'),
        address='Manager Office, Food System'
    )
    db.session.add(supervisor)
    
    # Employees
    employees = [
        ('Alice Employee', 'alice@foodsystem.com', '9876543212'),
        ('Bob Worker', 'bob@foodsystem.com', '9876543213'),
        ('Carol Staff', 'carol@foodsystem.com', '9876543214'),
    ]
    
    for name, email, phone in employees:
        employee = User(
            name=name,
            email=email,
            phone=phone,
            role='Employee',
            password=generate_password_hash('employee123'),
            address=f'{name} Address, City'
        )
        db.session.add(employee)
    
    # Customers
    customers = [
        ('Rajesh Kumar', 'rajesh@gmail.com', '9876543220', '123 MG Road, Bangalore'),
        ('Priya Sharma', 'priya@gmail.com', '9876543221', '456 Park Street, Mumbai'),
        ('Amit Singh', 'amit@gmail.com', '9876543222', '789 CP, Delhi'),
        ('Sunita Gupta', 'sunita@gmail.com', '9876543223', '321 Tank Bund, Hyderabad'),
        ('Vikram Reddy', 'vikram@gmail.com', '9876543224', '654 Brigade Road, Bangalore'),
        ('Meera Iyer', 'meera@gmail.com', '9876543225', '987 Marina Beach, Chennai'),
        ('Rohit Patel', 'rohit@gmail.com', '9876543226', '147 SG Highway, Ahmedabad'),
        ('Kavya Nair', 'kavya@gmail.com', '9876543227', '258 MG Road, Kochi'),
        ('Arjun Mehta', 'arjun@gmail.com', '9876543228', '369 FC Road, Pune'),
        ('Divya Joshi', 'divya@gmail.com', '9876543229', '741 Park Avenue, Kolkata'),
    ]
    
    for name, email, phone, address in customers:
        customer = User(
            name=name,
            email=email,
            phone=phone,
            role='Customer',
            password=generate_password_hash('customer123'),
            address=address,
            created_date=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        db.session.add(customer)
    
    db.session.commit()

def create_sample_menu_items():
    """Create sample menu items across different categories"""
    
    menu_items = [
        # Appetizers
        ('Vegetable Spring Rolls', 'Crispy rolls filled with fresh vegetables', 120, 'Appetizers', True, 'spring_rolls.jpg'),
        ('Chicken Wings', 'Spicy buffalo chicken wings with ranch dip', 180, 'Appetizers', True, 'chicken_wings.jpg'),
        ('Paneer Tikka', 'Grilled cottage cheese with spices', 160, 'Appetizers', True, 'paneer_tikka.jpg'),
        ('Fish Fingers', 'Crispy fish strips with tartar sauce', 200, 'Appetizers', True, 'fish_fingers.jpg'),
        ('Mushroom Soup', 'Creamy mushroom soup with herbs', 90, 'Appetizers', True, 'mushroom_soup.jpg'),
        
        # Main Course - North Indian
        ('Butter Chicken', 'Tender chicken in rich tomato-butter gravy', 280, 'Main Course', True, 'butter_chicken.jpg'),
        ('Dal Makhani', 'Creamy black lentils slow-cooked with spices', 180, 'Main Course', True, 'dal_makhani.jpg'),
        ('Palak Paneer', 'Cottage cheese in spinach gravy', 200, 'Main Course', True, 'palak_paneer.jpg'),
        ('Mutton Curry', 'Spicy mutton curry with traditional spices', 350, 'Main Course', True, 'mutton_curry.jpg'),
        ('Chole Bhature', 'Spicy chickpea curry with fried bread', 160, 'Main Course', True, 'chole_bhature.jpg'),
        
        # Main Course - South Indian
        ('Masala Dosa', 'Crispy crepe with spiced potato filling', 120, 'Main Course', True, 'masala_dosa.jpg'),
        ('Idli Sambhar', 'Steamed rice cakes with lentil curry', 80, 'Main Course', True, 'idli_sambhar.jpg'),
        ('Chicken Biryani', 'Fragrant basmati rice with spiced chicken', 250, 'Main Course', True, 'chicken_biryani.jpg'),
        ('Fish Curry', 'Traditional South Indian fish curry with coconut', 220, 'Main Course', True, 'fish_curry.jpg'),
        ('Veg Biryani', 'Aromatic vegetable biryani with raita', 180, 'Main Course', True, 'veg_biryani.jpg'),
        
        # Chinese
        ('Chicken Fried Rice', 'Wok-tossed rice with chicken and vegetables', 160, 'Chinese', True, 'chicken_fried_rice.jpg'),
        ('Veg Hakka Noodles', 'Stir-fried noodles with fresh vegetables', 140, 'Chinese', True, 'veg_hakka_noodles.jpg'),
        ('Manchurian Chicken', 'Indo-Chinese chicken balls in spicy sauce', 190, 'Chinese', True, 'manchurian_chicken.jpg'),
        ('Gobi Manchurian', 'Cauliflower fritters in tangy sauce', 130, 'Chinese', True, 'gobi_manchurian.jpg'),
        ('Sweet and Sour Pork', 'Crispy pork in sweet and sour sauce', 210, 'Chinese', False, 'sweet_sour_pork.jpg'),
        
        # Continental
        ('Margherita Pizza', 'Classic pizza with tomato, mozzarella, and basil', 220, 'Continental', True, 'margherita_pizza.jpg'),
        ('Chicken Burger', 'Grilled chicken burger with lettuce and mayo', 180, 'Continental', True, 'chicken_burger.jpg'),
        ('Caesar Salad', 'Fresh romaine lettuce with Caesar dressing', 150, 'Continental', True, 'caesar_salad.jpg'),
        ('Pasta Alfredo', 'Creamy white sauce pasta with herbs', 200, 'Continental', True, 'pasta_alfredo.jpg'),
        ('Grilled Sandwich', 'Toasted sandwich with vegetables and cheese', 120, 'Continental', True, 'grilled_sandwich.jpg'),
        
        # Desserts
        ('Gulab Jamun', 'Sweet milk dumplings in sugar syrup', 80, 'Desserts', True, 'gulab_jamun.jpg'),
        ('Chocolate Cake', 'Rich chocolate cake with chocolate ganache', 120, 'Desserts', True, 'chocolate_cake.jpg'),
        ('Ice Cream Sundae', 'Vanilla ice cream with chocolate sauce', 100, 'Desserts', True, 'ice_cream_sundae.jpg'),
        ('Ras Malai', 'Soft cottage cheese dumplings in milk', 90, 'Desserts', True, 'ras_malai.jpg'),
        ('Kulfi', 'Traditional Indian frozen dessert', 60, 'Desserts', True, 'kulfi.jpg'),
        
        # Beverages
        ('Masala Chai', 'Spiced Indian tea with milk', 30, 'Beverages', True, 'masala_chai.jpg'),
        ('Fresh Lime Soda', 'Refreshing lime drink with soda', 40, 'Beverages', True, 'lime_soda.jpg'),
        ('Mango Lassi', 'Creamy yogurt drink with mango', 70, 'Beverages', True, 'mango_lassi.jpg'),
        ('Filter Coffee', 'South Indian filter coffee', 35, 'Beverages', True, 'filter_coffee.jpg'),
        ('Fresh Orange Juice', 'Freshly squeezed orange juice', 60, 'Beverages', True, 'orange_juice.jpg'),
    ]
    
    for name, description, price, category, availability, image in menu_items:
        menu_item = MenuItem(
            name=name,
            description=description,
            price=price,
            category=category,
            availability=availability,
            image=image,
            created_date=datetime.now() - timedelta(days=random.randint(1, 90))
        )
        db.session.add(menu_item)
    
    db.session.commit()

def create_sample_kitchen_staff():
    """Create sample kitchen staff"""
    
    staff_data = [
        ('Raman Chef', 'Head Chef', '9876540001', 'Morning', 'Kitchen', 'Active'),
        ('Suresh Cook', 'Chef', '9876540002', 'Morning', 'Kitchen', 'Active'),
        ('Lakshmi Assistant', 'Assistant Chef', '9876540003', 'Evening', 'Kitchen', 'Active'),
        ('Kumar Delivery', 'Delivery Boy', '9876540004', 'Morning', 'Delivery', 'Active'),
        ('Ravi Delivery', 'Delivery Boy', '9876540005', 'Evening', 'Delivery', 'Active'),
        ('Deepak Manager', 'Kitchen Manager', '9876540006', 'Morning', 'Kitchen', 'Active'),
        ('Pradeep Cleaner', 'Cleaner', '9876540007', 'Night', 'Cleaning', 'Active'),
        ('Santosh Cook', 'Chef', '9876540008', 'Evening', 'Kitchen', 'Active'),
        ('Mahesh Assistant', 'Assistant Chef', '9876540009', 'Night', 'Kitchen', 'On Leave'),
        ('Rajesh Delivery', 'Delivery Boy', '9876540010', 'Night', 'Delivery', 'Active'),
    ]
    
    for name, role, phone, shift, dept, status in staff_data:
        staff = KitchenStaff(
            staff_name=name,
            role=role,
            phone=phone,
            shift_time=shift,
            department=dept,
            status=status
        )
        db.session.add(staff)
    
    db.session.commit()

def create_sample_orders():
    """Create sample orders with realistic data"""
    
    customers = User.query.filter_by(role='Customer').all()
    menu_items = MenuItem.query.all()
    
    # Create 300+ orders over the past year
    for _ in range(350):
        customer = random.choice(customers)
        order_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        # Create order
        order = Order(
            user_id=customer.user_id,
            order_date=order_date,
            total_amount=0,  # Will be calculated
            status=random.choice(['Pending', 'Confirmed', 'Preparing', 'Ready', 'Delivered', 'Cancelled']),
            delivery_address=customer.address,
            order_time=(order_date + timedelta(hours=random.randint(10, 22))).time(),
            estimated_time=order_date + timedelta(hours=1, minutes=random.randint(0, 30))
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order details (1-5 items per order)
        total_amount = 0
        num_items = random.randint(1, 5)
        selected_items = random.sample(menu_items, min(num_items, len(menu_items)))
        
        for menu_item in selected_items:
            quantity = random.randint(1, 3)
            unit_price = menu_item.price
            sub_total = unit_price * quantity
            total_amount += sub_total
            
            order_detail = OrderDetails(
                order_id=order.order_id,
                menu_item_id=menu_item.menu_item_id,
                quantity=quantity,
                unit_price=unit_price,
                sub_total=sub_total,
                special_instructions=random.choice(['', 'Less spicy', 'Extra sauce', 'No onions', 'Well done'])
            )
            db.session.add(order_detail)
        
        # Update order total
        order.total_amount = total_amount
    
    db.session.commit()

def create_sample_payments():
    """Create sample payments for orders"""
    
    orders = Order.query.all()
    
    for order in orders:
        # 90% of orders have payments
        if random.random() < 0.9:
            payment_method = random.choice(['Cash', 'Card', 'UPI', 'Net Banking'])
            status = 'Completed' if order.status != 'Cancelled' else 'Failed'
            
            payment = Payment(
                order_id=order.order_id,
                payment_method=payment_method,
                amount=order.total_amount,
                payment_date=order.order_date + timedelta(minutes=random.randint(1, 30)),
                transaction_id=f'TXN{random.randint(100000, 999999)}',
                status=status
            )
            db.session.add(payment)
    
    db.session.commit()

def create_sample_feedback():
    """Create sample feedback for orders"""
    
    orders = Order.query.filter_by(status='Delivered').all()
    customers = User.query.filter_by(role='Customer').all()
    
    # 60% of delivered orders have feedback
    for order in random.sample(orders, int(len(orders) * 0.6)):
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
        
        comments_pool = [
            'Great food and fast delivery!',
            'Delicious as always.',
            'Good taste but delivery was late.',
            'Excellent service and quality.',
            'Food was cold when delivered.',
            'Amazing flavors, will order again.',
            'Not satisfied with the quality.',
            'Perfect timing and hot food.',
            'Could be better.',
            'Outstanding experience!',
            'Food was too spicy.',
            'Fresh and tasty.',
            'Delivery person was very polite.',
            'Portion size was small.',
            'Exceeded expectations!'
        ]
        
        feedback = Feedback(
            user_id=order.user_id,
            order_id=order.order_id,
            rating=rating,
            comments=random.choice(comments_pool),
            feedback_date=order.order_date + timedelta(hours=random.randint(1, 48)),
            feedback_type=random.choice(['Food', 'Service', 'Delivery', 'App'])
        )
        db.session.add(feedback)
    
    # Add some general feedback (not order-specific)
    for _ in range(50):
        customer = random.choice(customers)
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
        
        feedback = Feedback(
            user_id=customer.user_id,
            order_id=None,
            rating=rating,
            comments=random.choice(comments_pool),
            feedback_date=datetime.now() - timedelta(days=random.randint(1, 180)),
            feedback_type=random.choice(['Food', 'Service', 'App', 'Overall'])
        )
        db.session.add(feedback)
    
    db.session.commit()

def create_sample_deliveries():
    """Create sample deliveries for orders"""
    
    orders = Order.query.filter(Order.status.in_(['Preparing', 'Ready', 'Delivered', 'Out for Delivery'])).all()
    staff = KitchenStaff.query.filter_by(department='Delivery', status='Active').all()
    
    for order in orders:
        # Skip if delivery already exists
        if Delivery.query.filter_by(order_id=order.order_id).first():
            continue
            
        assigned_staff = random.choice(staff) if staff and random.random() < 0.8 else None
        
        estimated_time = order.estimated_time or (order.order_date + timedelta(hours=1))
        actual_time = None
        delivery_status = 'Assigned'
        
        if order.status == 'Delivered':
            actual_time = estimated_time + timedelta(minutes=random.randint(-15, 45))
            delivery_status = 'Delivered'
        elif order.status == 'Out for Delivery':
            delivery_status = 'In Transit'
        elif order.status == 'Ready':
            delivery_status = 'Ready for Pickup'
        
        delivery = Delivery(
            order_id=order.order_id,
            staff_id=assigned_staff.staff_id if assigned_staff else None,
            estimated_time=estimated_time,
            actual_time=actual_time,
            delivery_status=delivery_status,
            tracking_code=f'TRK{random.randint(10000000, 99999999)}'
        )
        db.session.add(delivery)
    
    db.session.commit()

def create_sample_recommendations():
    """Create sample AI recommendations"""
    
    customers = User.query.filter_by(role='Customer').all()
    menu_items = MenuItem.query.all()
    
    for customer in customers:
        # Create 5-10 recommendations per customer
        num_recommendations = random.randint(5, 10)
        selected_items = random.sample(menu_items, min(num_recommendations, len(menu_items)))
        
        for menu_item in selected_items:
            recommendation_type = random.choice(['Popular', 'Personal', 'Similar', 'Seasonal'])
            score = random.uniform(3.0, 5.0)
            
            recommendation = Recommendation(
                user_id=customer.user_id,
                menu_item_id=menu_item.menu_item_id,
                recommendation_type=recommendation_type,
                score=score,
                created_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                ai_model='Content-Based'
            )
            db.session.add(recommendation)
    
    db.session.commit()

if __name__ == '__main__':
    create_sample_data()