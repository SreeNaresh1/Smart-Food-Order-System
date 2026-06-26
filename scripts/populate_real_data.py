"""
Script to populate the Smart Food Ordering System database with real, comprehensive data.
This script will add 100-150 records across all tables with realistic food ordering data.
"""

import os
import sys
import datetime
from werkzeug.security import generate_password_hash
import random

# Add the current directory to sys.path to import our models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from backend.models import User, MenuItem, Order, OrderDetails, Payment, Feedback, Delivery, KitchenStaff, Recommendation

def create_comprehensive_data():
    """Create comprehensive realistic data for the food ordering system"""
    
    print("Creating comprehensive data for Smart Food Ordering System...")
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # 1. Create Users (20 users - mix of customers, staff, and admins)
        users_data = [
            # Admin Users
            {'name': 'System Admin', 'email': 'admin@foodsystem.com', 'password': 'admin123', 'phone': '9999999999', 'address': 'Admin Office, Food System HQ', 'role': 'admin'},
            {'name': 'Manager John', 'email': 'manager@foodsystem.com', 'password': 'manager123', 'phone': '9999999998', 'address': 'Manager Office, Food System', 'role': 'admin'},
            
            # Staff Users
            {'name': 'Kitchen Chef Ram', 'email': 'chef.ram@foodsystem.com', 'password': 'chef123', 'phone': '9999999997', 'address': 'Kitchen, Food System', 'role': 'staff'},
            {'name': 'Kitchen Chef Sita', 'email': 'chef.sita@foodsystem.com', 'password': 'chef123', 'phone': '9999999996', 'address': 'Kitchen, Food System', 'role': 'staff'},
            {'name': 'Delivery Boy Arjun', 'email': 'delivery.arjun@foodsystem.com', 'password': 'delivery123', 'phone': '9999999995', 'address': 'Delivery Hub, Food System', 'role': 'staff'},
            
            # Customer Users
            {'name': 'Priya Sharma', 'email': 'priya.sharma@gmail.com', 'password': 'priya123', 'phone': '9876543210', 'address': '123 MG Road, Bangalore, Karnataka 560001', 'role': 'customer'},
            {'name': 'Rahul Gupta', 'email': 'rahul.gupta@gmail.com', 'password': 'rahul123', 'phone': '9876543211', 'address': '456 Brigade Road, Bangalore, Karnataka 560025', 'role': 'customer'},
            {'name': 'Anjali Patel', 'email': 'anjali.patel@yahoo.com', 'password': 'anjali123', 'phone': '9876543212', 'address': '789 Koramangala, Bangalore, Karnataka 560034', 'role': 'customer'},
            {'name': 'Vikram Singh', 'email': 'vikram.singh@outlook.com', 'password': 'vikram123', 'phone': '9876543213', 'address': '321 Indiranagar, Bangalore, Karnataka 560038', 'role': 'customer'},
            {'name': 'Sneha Reddy', 'email': 'sneha.reddy@gmail.com', 'password': 'sneha123', 'phone': '9876543214', 'address': '654 Jayanagar, Bangalore, Karnataka 560011', 'role': 'customer'},
            {'name': 'Amit Kumar', 'email': 'amit.kumar@gmail.com', 'password': 'amit123', 'phone': '9876543215', 'address': '987 Whitefield, Bangalore, Karnataka 560066', 'role': 'customer'},
            {'name': 'Deepika Joshi', 'email': 'deepika.joshi@gmail.com', 'password': 'deepika123', 'phone': '9876543216', 'address': '147 Electronic City, Bangalore, Karnataka 560100', 'role': 'customer'},
            {'name': 'Rohit Agarwal', 'email': 'rohit.agarwal@gmail.com', 'password': 'rohit123', 'phone': '9876543217', 'address': '258 HSR Layout, Bangalore, Karnataka 560102', 'role': 'customer'},
            {'name': 'Kavya Nair', 'email': 'kavya.nair@gmail.com', 'password': 'kavya123', 'phone': '9876543218', 'address': '369 Marathahalli, Bangalore, Karnataka 560037', 'role': 'customer'},
            {'name': 'Aryan Mehta', 'email': 'aryan.mehta@gmail.com', 'password': 'aryan123', 'phone': '9876543219', 'address': '741 Sarjapur Road, Bangalore, Karnataka 560035', 'role': 'customer'},
            {'name': 'Pooja Iyer', 'email': 'pooja.iyer@gmail.com', 'password': 'pooja123', 'phone': '9876543220', 'address': '852 Bellandur, Bangalore, Karnataka 560103', 'role': 'customer'},
            {'name': 'Sanjay Verma', 'email': 'sanjay.verma@gmail.com', 'password': 'sanjay123', 'phone': '9876543221', 'address': '963 JP Nagar, Bangalore, Karnataka 560078', 'role': 'customer'},
            {'name': 'Ritu Bansal', 'email': 'ritu.bansal@gmail.com', 'password': 'ritu123', 'phone': '9876543222', 'address': '174 BTM Layout, Bangalore, Karnataka 560029', 'role': 'customer'},
            {'name': 'Karthik Raj', 'email': 'karthik.raj@gmail.com', 'password': 'karthik123', 'phone': '9876543223', 'address': '285 Malleshwaram, Bangalore, Karnataka 560003', 'role': 'customer'},
            {'name': 'Nisha Kapoor', 'email': 'nisha.kapoor@gmail.com', 'password': 'nisha123', 'phone': '9876543224', 'address': '396 Rajajinagar, Bangalore, Karnataka 560010', 'role': 'customer'}
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                phone=user_data['phone'],
                address=user_data['address'],
                role=user_data['role']
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        # 2. Create Menu Items (40+ items across different categories)
        menu_items_data = [
            # North Indian
            {'name': 'Butter Chicken', 'description': 'Tender chicken in rich tomato and butter gravy', 'price': 320.00, 'category': 'North Indian', 'availability': True, 'ingredients': 'Chicken, Tomato, Butter, Cream, Spices'},
            {'name': 'Dal Makhani', 'description': 'Creamy black lentils slow-cooked with butter and cream', 'price': 280.00, 'category': 'North Indian', 'availability': True, 'ingredients': 'Black Lentils, Butter, Cream, Tomato, Onions'},
            {'name': 'Paneer Tikka Masala', 'description': 'Grilled cottage cheese in spicy tomato gravy', 'price': 290.00, 'category': 'North Indian', 'availability': True, 'ingredients': 'Paneer, Tomato, Onions, Bell Peppers, Spices'},
            {'name': 'Kadai Chicken', 'description': 'Spicy chicken cooked in kadai with capsicum and onions', 'price': 340.00, 'category': 'North Indian', 'availability': True, 'ingredients': 'Chicken, Capsicum, Onions, Tomato, Kadai Masala'},
            {'name': 'Palak Paneer', 'description': 'Cottage cheese in creamy spinach gravy', 'price': 270.00, 'category': 'North Indian', 'availability': True, 'ingredients': 'Paneer, Spinach, Onions, Garlic, Cream'},
            {'name': 'Naan Bread', 'description': 'Soft and fluffy Indian bread baked in tandoor', 'price': 60.00, 'category': 'Breads', 'availability': True, 'ingredients': 'Flour, Yogurt, Oil, Salt, Baking Powder'},
            {'name': 'Garlic Naan', 'description': 'Naan bread topped with fresh garlic and herbs', 'price': 80.00, 'category': 'Breads', 'availability': True, 'ingredients': 'Flour, Garlic, Herbs, Yogurt, Oil'},
            {'name': 'Jeera Rice', 'description': 'Basmati rice flavored with cumin seeds', 'price': 180.00, 'category': 'Rice', 'availability': True, 'ingredients': 'Basmati Rice, Cumin Seeds, Ghee, Salt'},
            
            # South Indian
            {'name': 'Masala Dosa', 'description': 'Crispy rice crepe filled with spiced potato filling', 'price': 150.00, 'category': 'South Indian', 'availability': True, 'ingredients': 'Rice, Urad Dal, Potato, Onions, Spices'},
            {'name': 'Idli Sambar', 'description': 'Steamed rice cakes served with sambar and chutney', 'price': 120.00, 'category': 'South Indian', 'availability': True, 'ingredients': 'Rice, Urad Dal, Lentils, Vegetables, Spices'},
            {'name': 'Rava Upma', 'description': 'Semolina cooked with vegetables and spices', 'price': 100.00, 'category': 'South Indian', 'availability': True, 'ingredients': 'Semolina, Vegetables, Mustard Seeds, Curry Leaves'},
            {'name': 'Uttapam', 'description': 'Thick pancake topped with vegetables', 'price': 140.00, 'category': 'South Indian', 'availability': True, 'ingredients': 'Rice, Urad Dal, Onions, Tomato, Capsicum'},
            {'name': 'Vada Sambar', 'description': 'Deep-fried lentil donuts in sambar', 'price': 110.00, 'category': 'South Indian', 'availability': True, 'ingredients': 'Urad Dal, Lentils, Vegetables, Spices'},
            {'name': 'Coconut Rice', 'description': 'Rice cooked with fresh coconut and curry leaves', 'price': 160.00, 'category': 'South Indian', 'availability': True, 'ingredients': 'Rice, Coconut, Curry Leaves, Mustard Seeds'},
            
            # Chinese
            {'name': 'Chicken Hakka Noodles', 'description': 'Stir-fried noodles with chicken and vegetables', 'price': 250.00, 'category': 'Chinese', 'availability': True, 'ingredients': 'Noodles, Chicken, Vegetables, Soy Sauce, Spices'},
            {'name': 'Veg Manchurian', 'description': 'Mixed vegetable balls in spicy Manchurian sauce', 'price': 220.00, 'category': 'Chinese', 'availability': True, 'ingredients': 'Mixed Vegetables, Corn Flour, Soy Sauce, Garlic'},
            {'name': 'Chicken Fried Rice', 'description': 'Wok-tossed rice with chicken and vegetables', 'price': 240.00, 'category': 'Chinese', 'availability': True, 'ingredients': 'Rice, Chicken, Vegetables, Egg, Soy Sauce'},
            {'name': 'Chilli Chicken', 'description': 'Spicy chicken pieces in Indo-Chinese sauce', 'price': 280.00, 'category': 'Chinese', 'availability': True, 'ingredients': 'Chicken, Capsicum, Onions, Chilli Sauce, Soy Sauce'},
            {'name': 'Hot & Sour Soup', 'description': 'Spicy and tangy soup with vegetables', 'price': 120.00, 'category': 'Chinese', 'availability': True, 'ingredients': 'Vegetables, Mushrooms, Tofu, Vinegar, Spices'},
            
            # Italian
            {'name': 'Margherita Pizza', 'description': 'Classic pizza with tomato sauce, mozzarella, and basil', 'price': 350.00, 'category': 'Italian', 'availability': True, 'ingredients': 'Pizza Base, Tomato Sauce, Mozzarella, Basil, Olive Oil'},
            {'name': 'Chicken BBQ Pizza', 'description': 'Pizza topped with BBQ chicken and vegetables', 'price': 450.00, 'category': 'Italian', 'availability': True, 'ingredients': 'Pizza Base, BBQ Sauce, Chicken, Onions, Bell Peppers'},
            {'name': 'Pasta Arrabbiata', 'description': 'Penne pasta in spicy tomato sauce', 'price': 280.00, 'category': 'Italian', 'availability': True, 'ingredients': 'Penne Pasta, Tomato Sauce, Garlic, Red Chilli, Herbs'},
            {'name': 'Chicken Alfredo Pasta', 'description': 'Creamy pasta with grilled chicken', 'price': 320.00, 'category': 'Italian', 'availability': True, 'ingredients': 'Pasta, Chicken, Cream, Parmesan, Garlic, Herbs'},
            
            # Desserts
            {'name': 'Gulab Jamun', 'description': 'Soft milk dumplings in sugar syrup', 'price': 80.00, 'category': 'Desserts', 'availability': True, 'ingredients': 'Milk Powder, Sugar, Ghee, Rose Water, Cardamom'},
            {'name': 'Rasgulla', 'description': 'Spongy cottage cheese balls in sugar syrup', 'price': 70.00, 'category': 'Desserts', 'availability': True, 'ingredients': 'Cottage Cheese, Sugar, Water, Cardamom'},
            {'name': 'Chocolate Brownie', 'description': 'Rich chocolate brownie with vanilla ice cream', 'price': 150.00, 'category': 'Desserts', 'availability': True, 'ingredients': 'Chocolate, Butter, Sugar, Flour, Eggs, Vanilla Ice Cream'},
            {'name': 'Kulfi', 'description': 'Traditional Indian ice cream with nuts', 'price': 90.00, 'category': 'Desserts', 'availability': True, 'ingredients': 'Milk, Sugar, Cardamom, Pistachios, Almonds'},
            
            # Beverages
            {'name': 'Masala Chai', 'description': 'Traditional Indian spiced tea', 'price': 40.00, 'category': 'Beverages', 'availability': True, 'ingredients': 'Tea, Milk, Sugar, Ginger, Cardamom, Cloves'},
            {'name': 'Fresh Lime Soda', 'description': 'Refreshing lime drink with soda', 'price': 60.00, 'category': 'Beverages', 'availability': True, 'ingredients': 'Fresh Lime, Soda Water, Sugar, Salt, Mint'},
            {'name': 'Mango Lassi', 'description': 'Creamy yogurt drink with mango', 'price': 80.00, 'category': 'Beverages', 'availability': True, 'ingredients': 'Yogurt, Mango, Sugar, Cardamom, Ice'},
            {'name': 'Filter Coffee', 'description': 'South Indian style filter coffee', 'price': 50.00, 'category': 'Beverages', 'availability': True, 'ingredients': 'Coffee Powder, Milk, Sugar, Water'},
            
            # Fast Food
            {'name': 'Chicken Burger', 'description': 'Juicy grilled chicken burger with fries', 'price': 200.00, 'category': 'Fast Food', 'availability': True, 'ingredients': 'Chicken Patty, Burger Bun, Lettuce, Tomato, Cheese, Fries'},
            {'name': 'Veg Sandwich', 'description': 'Grilled sandwich with vegetables and cheese', 'price': 120.00, 'category': 'Fast Food', 'availability': True, 'ingredients': 'Bread, Vegetables, Cheese, Butter, Spices'},
            {'name': 'French Fries', 'description': 'Crispy golden potato fries', 'price': 80.00, 'category': 'Fast Food', 'availability': True, 'ingredients': 'Potatoes, Oil, Salt, Herbs'},
            {'name': 'Chicken Wings', 'description': 'Spicy chicken wings with dip', 'price': 180.00, 'category': 'Fast Food', 'availability': True, 'ingredients': 'Chicken Wings, Spicy Sauce, Herbs, Dip'},
            
            # Healthy Options
            {'name': 'Greek Salad', 'description': 'Fresh salad with feta cheese and olives', 'price': 180.00, 'category': 'Healthy', 'availability': True, 'ingredients': 'Lettuce, Tomato, Cucumber, Feta Cheese, Olives, Olive Oil'},
            {'name': 'Grilled Chicken Salad', 'description': 'Protein-rich salad with grilled chicken', 'price': 220.00, 'category': 'Healthy', 'availability': True, 'ingredients': 'Grilled Chicken, Mixed Greens, Tomato, Cucumber, Dressing'},
            {'name': 'Quinoa Bowl', 'description': 'Nutritious quinoa with vegetables', 'price': 200.00, 'category': 'Healthy', 'availability': True, 'ingredients': 'Quinoa, Vegetables, Nuts, Seeds, Dressing'},
            {'name': 'Fruit Salad', 'description': 'Fresh seasonal fruits with honey', 'price': 100.00, 'category': 'Healthy', 'availability': True, 'ingredients': 'Seasonal Fruits, Honey, Mint, Lime'},
            
            # Special Items (some unavailable for variety)
            {'name': 'Lobster Thermidor', 'description': 'Premium lobster in cream sauce', 'price': 1200.00, 'category': 'Special', 'availability': False, 'ingredients': 'Lobster, Cream, Cheese, Herbs, Wine'},
            {'name': 'Truffle Pasta', 'description': 'Luxury pasta with truffle oil', 'price': 800.00, 'category': 'Special', 'availability': False, 'ingredients': 'Pasta, Truffle Oil, Parmesan, Cream, Mushrooms'},
        ]
        
        menu_items = []
        for item_data in menu_items_data:
            menu_item = MenuItem(
                name=item_data['name'],
                description=item_data['description'],
                price=item_data['price'],
                category=item_data['category'],
                availability=item_data['availability'],
                ingredients=item_data['ingredients']
            )
            db.session.add(menu_item)
            menu_items.append(menu_item)
        
        db.session.commit()
        print(f"Created {len(menu_items)} menu items")
        
        # 3. Create Kitchen Staff (5 staff members)
        kitchen_staff_data = [
            {'user_id': 3, 'specialization': 'North Indian Cuisine', 'shift': 'morning', 'status': 'available'},
            {'user_id': 4, 'specialization': 'South Indian Cuisine', 'shift': 'evening', 'status': 'available'},
            {'user_id': 5, 'specialization': 'Chinese & Fast Food', 'shift': 'night', 'status': 'busy'},
        ]
        
        kitchen_staff = []
        for staff_data in kitchen_staff_data:
            staff = KitchenStaff(
                user_id=staff_data['user_id'],
                specialization=staff_data['specialization'],
                shift=staff_data['shift'],
                status=staff_data['status']
            )
            db.session.add(staff)
            kitchen_staff.append(staff)
        
        db.session.commit()
        print(f"Created {len(kitchen_staff)} kitchen staff members")
        
        # 4. Create Orders (30+ orders with different statuses and dates)
        order_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'delivered']
        customer_users = [u for u in users if u.role == 'customer']
        
        orders = []
        for i in range(35):
            # Generate random date within last 30 days
            days_ago = random.randint(0, 30)
            order_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            
            customer = random.choice(customer_users)
            status = random.choice(order_statuses)
            
            order = Order(
                user_id=customer.user_id,
                order_date=order_date,
                total_amount=0,  # Will be calculated after adding order details
                status=status,
                special_instructions=random.choice([
                    None, 'Extra spicy', 'Less oil', 'No onions', 'Extra cheese', 
                    'Mild spice level', 'Pack separately', 'Add extra sauce'
                ])
            )
            db.session.add(order)
            orders.append(order)
        
        db.session.commit()
        
        # 5. Create Order Details (2-5 items per order)
        order_details = []
        for order in orders:
            num_items = random.randint(2, 5)
            selected_items = random.sample([item for item in menu_items if item.availability], num_items)
            total_amount = 0
            
            for menu_item in selected_items:
                quantity = random.randint(1, 3)
                price = menu_item.price
                
                detail = OrderDetails(
                    order_id=order.order_id,
                    menu_item_id=menu_item.menu_item_id,
                    quantity=quantity,
                    price=price
                )
                db.session.add(detail)
                order_details.append(detail)
                total_amount += quantity * price
            
            # Update order total
            order.total_amount = total_amount
        
        db.session.commit()
        print(f"Created {len(order_details)} order details for {len(orders)} orders")
        
        # 6. Create Payments (for confirmed/delivered orders)
        payments = []
        for order in orders:
            if order.status in ['confirmed', 'preparing', 'ready', 'delivered']:
                payment = Payment(
                    order_id=order.order_id,
                    payment_method=random.choice(['credit_card', 'debit_card', 'upi', 'cash', 'net_banking']),
                    payment_status='completed',
                    transaction_id=f'TXN{random.randint(100000, 999999)}',
                    payment_date=order.order_date + datetime.timedelta(minutes=random.randint(1, 30))
                )
                db.session.add(payment)
                payments.append(payment)
        
        db.session.commit()
        print(f"Created {len(payments)} payments")
        
        # 7. Create Deliveries (for ready/delivered orders)
        delivery_persons = [
            'Raj Kumar - 9876543230', 'Suresh Yadav - 9876543231', 'Mohan Singh - 9876543232',
            'Ravi Sharma - 9876543233', 'Deepak Gupta - 9876543234'
        ]
        
        deliveries = []
        for order in orders:
            if order.status in ['ready', 'delivered']:
                delivery_person = random.choice(delivery_persons)
                name, phone = delivery_person.split(' - ')
                
                delivery_date = order.order_date + datetime.timedelta(minutes=random.randint(30, 90))
                estimated_delivery = delivery_date + datetime.timedelta(minutes=random.randint(15, 45))
                
                delivery = Delivery(
                    order_id=order.order_id,
                    delivery_address=order.user.address,
                    delivery_status='delivered' if order.status == 'delivered' else 'dispatched',
                    delivery_person_name=name,
                    delivery_person_phone=phone,
                    delivery_date=delivery_date if order.status == 'delivered' else None,
                    estimated_delivery_time=estimated_delivery
                )
                db.session.add(delivery)
                deliveries.append(delivery)
        
        db.session.commit()
        print(f"Created {len(deliveries)} deliveries")
        
        # 8. Create Feedback (for delivered orders)
        feedback_comments = [
            'Excellent food quality and fast delivery!', 'Food was delicious, will order again.',
            'Good taste but delivery was slightly delayed.', 'Amazing flavors, highly recommended!',
            'Great service and packaging.', 'Food was fresh and hot upon arrival.',
            'Loved the spice level, perfect!', 'Quick delivery and tasty food.',
            'Good portion size and value for money.', 'Exceptional quality and service.',
            'Food was okay, could be better.', 'Delivery was on time, food was great!',
            'Excellent presentation and taste.', 'Will definitely order again soon.',
            'Good experience overall.'
        ]
        
        feedbacks = []
        delivered_orders = [o for o in orders if o.status == 'delivered']
        
        for order in delivered_orders[:len(delivered_orders)//2]:  # Feedback for half of delivered orders
            feedback = Feedback(
                user_id=order.user_id,
                order_id=order.order_id,
                rating=random.randint(3, 5),  # Mostly positive ratings
                comment=random.choice(feedback_comments),
                feedback_date=order.order_date + datetime.timedelta(hours=random.randint(1, 24))
            )
            db.session.add(feedback)
            feedbacks.append(feedback)
        
        db.session.commit()
        print(f"Created {len(feedbacks)} feedback entries")
        
        # 9. Create Recommendations (AI-based recommendations for customers)
        recommendation_types = ['popular', 'similar', 'trending', 'personalized']
        recommendation_reasons = [
            'Based on your previous orders', 'Popular among customers',
            'Trending in your area', 'Similar to items you liked',
            'Highly rated by users', 'Perfect for the season',
            'Recommended by our chef', 'Great combination with your favorites'
        ]
        
        recommendations = []
        for customer in customer_users[:10]:  # Recommendations for 10 customers
            num_recommendations = random.randint(3, 8)
            recommended_items = random.sample(
                [item for item in menu_items if item.availability], 
                num_recommendations
            )
            
            for menu_item in recommended_items:
                recommendation = Recommendation(
                    user_id=customer.user_id,
                    menu_item_id=menu_item.menu_item_id,
                    score=random.uniform(3.5, 5.0),
                    type=random.choice(recommendation_types),
                    reason=random.choice(recommendation_reasons),
                    created_date=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 7))
                )
                db.session.add(recommendation)
                recommendations.append(recommendation)
        
        db.session.commit()
        print(f"Created {len(recommendations)} recommendations")
        
        # Print summary
        print("\n" + "="*50)
        print("DATABASE POPULATED SUCCESSFULLY!")
        print("="*50)
        print(f"Users: {len(users)} (Admin: 2, Staff: 3, Customers: 15)")
        print(f"Menu Items: {len(menu_items)} (Available: {len([i for i in menu_items if i.availability])})")
        print(f"Kitchen Staff: {len(kitchen_staff)}")
        print(f"Orders: {len(orders)}")
        print(f"Order Details: {len(order_details)}")
        print(f"Payments: {len(payments)}")
        print(f"Deliveries: {len(deliveries)}")
        print(f"Feedback: {len(feedbacks)}")
        print(f"Recommendations: {len(recommendations)}")
        print(f"\nTotal Records: {len(users) + len(menu_items) + len(kitchen_staff) + len(orders) + len(order_details) + len(payments) + len(deliveries) + len(feedbacks) + len(recommendations)}")
        print("="*50)

if __name__ == '__main__':
    create_comprehensive_data()
