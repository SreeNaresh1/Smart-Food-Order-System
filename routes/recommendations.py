from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, MenuItem, User, Order, OrderDetails, Recommendation, Feedback
from datetime import datetime
from functools import wraps
import random

recommendations_bp = Blueprint('recommendations', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_recommendations(user_id, limit=10):
    """
    AI-based recommendation system using content-based filtering
    """
    user = User.query.get(user_id)
    if not user:
        return []
    
    # Get user's order history
    user_orders = db.session.query(OrderDetails, MenuItem).join(
        Order, OrderDetails.order_id == Order.order_id
    ).join(
        MenuItem, OrderDetails.menu_item_id == MenuItem.menu_item_id
    ).filter(Order.user_id == user_id).all()
    
    # Get user's preferred categories and items
    preferred_categories = {}
    ordered_items = set()
    
    for order_detail, menu_item in user_orders:
        ordered_items.add(menu_item.menu_item_id)
        category = menu_item.category
        if category in preferred_categories:
            preferred_categories[category] += order_detail.quantity
        else:
            preferred_categories[category] = order_detail.quantity
    
    # Get user's feedback to understand preferences
    user_feedback = db.session.query(Feedback, OrderDetails, MenuItem).join(
        Order, Feedback.order_id == Order.order_id
    ).join(
        OrderDetails, Order.order_id == OrderDetails.order_id
    ).join(
        MenuItem, OrderDetails.menu_item_id == MenuItem.menu_item_id
    ).filter(Feedback.user_id == user_id).all()
    
    highly_rated_categories = {}
    for feedback, order_detail, menu_item in user_feedback:
        if feedback.rating >= 4:  # High rating
            category = menu_item.category
            if category in highly_rated_categories:
                highly_rated_categories[category] += feedback.rating
            else:
                highly_rated_categories[category] = feedback.rating
    
    # Combine preferences with ratings
    for category, rating_sum in highly_rated_categories.items():
        if category in preferred_categories:
            preferred_categories[category] += rating_sum * 2  # Weight ratings higher
        else:
            preferred_categories[category] = rating_sum
    
    # Get popular items (ordered by many users)
    popular_items = db.session.query(
        MenuItem, 
        db.func.count(OrderDetails.order_detail_id).label('order_count')
    ).join(OrderDetails).group_by(MenuItem.menu_item_id).order_by(
        db.text('order_count DESC')
    ).limit(20).all()
    
    # Generate recommendations
    recommendations = []
    
    # 1. Items from preferred categories (not already ordered)
    if preferred_categories:
        top_categories = sorted(preferred_categories.items(), 
                              key=lambda x: x[1], reverse=True)[:3]
        
        for category, _ in top_categories:
            category_items = MenuItem.query.filter(
                MenuItem.category == category,
                MenuItem.availability == True,
                ~MenuItem.menu_item_id.in_(ordered_items)
            ).limit(3).all()
            
            for item in category_items:
                score = calculate_recommendation_score(
                    item, preferred_categories, highly_rated_categories
                )
                recommendations.append({
                    'menu_item': item,
                    'type': 'Personal',
                    'score': score,
                    'reason': f'Based on your preference for {category}'
                })
    
    # 2. Popular items (not already ordered)
    for menu_item, order_count in popular_items:
        if menu_item.menu_item_id not in ordered_items and menu_item.availability:
            score = min(order_count * 0.1, 5.0)  # Scale order count to score
            recommendations.append({
                'menu_item': menu_item,
                'type': 'Popular',
                'score': score,
                'reason': f'Popular choice - ordered {order_count} times'
            })
    
    # 3. Similar items to highly rated ones
    for feedback, order_detail, menu_item in user_feedback:
        if feedback.rating >= 4:
            similar_items = MenuItem.query.filter(
                MenuItem.category == menu_item.category,
                MenuItem.menu_item_id != menu_item.menu_item_id,
                MenuItem.availability == True,
                ~MenuItem.menu_item_id.in_(ordered_items)
            ).limit(2).all()
            
            for similar_item in similar_items:
                score = feedback.rating * 0.8  # Slightly lower than original rating
                recommendations.append({
                    'menu_item': similar_item,
                    'type': 'Similar',
                    'score': score,
                    'reason': f'Similar to {menu_item.name} (rated {feedback.rating}/5)'
                })
    
    # Remove duplicates and sort by score
    seen_items = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec['menu_item'].menu_item_id not in seen_items:
            seen_items.add(rec['menu_item'].menu_item_id)
            unique_recommendations.append(rec)
    
    # Sort by score and limit
    unique_recommendations.sort(key=lambda x: x['score'], reverse=True)
    return unique_recommendations[:limit]

def calculate_recommendation_score(menu_item, preferred_categories, highly_rated_categories):
    """Calculate recommendation score based on various factors"""
    score = 3.0  # Base score
    
    # Category preference bonus
    if menu_item.category in preferred_categories:
        category_score = preferred_categories[menu_item.category]
        score += min(category_score * 0.1, 2.0)
    
    # High rating bonus
    if menu_item.category in highly_rated_categories:
        rating_bonus = highly_rated_categories[menu_item.category] * 0.2
        score += min(rating_bonus, 1.5)
    
    # Price factor (slightly prefer mid-range items)
    if 10 <= float(menu_item.price) <= 25:
        score += 0.3
    
    return min(score, 5.0)  # Cap at 5.0

@recommendations_bp.route('/')
@login_required
def list_recommendations():
    user_id = session.get('user_id')
    
    # Get fresh recommendations
    recommendations = get_user_recommendations(user_id, limit=15)
    
    # Save recommendations to database for tracking
    for rec in recommendations[:10]:  # Save top 10
        existing_rec = Recommendation.query.filter_by(
            user_id=user_id,
            menu_item_id=rec['menu_item'].menu_item_id
        ).first()
        
        if not existing_rec:
            new_rec = Recommendation(
                user_id=user_id,
                menu_item_id=rec['menu_item'].menu_item_id,
                recommendation_type=rec['type'],
                score=rec['score'],
                ai_model='Content-Based'
            )
            db.session.add(new_rec)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    return render_template('recommendations/list.html', recommendations=recommendations)

@recommendations_bp.route('/api/recommendations')
@login_required
def api_recommendations():
    """API endpoint for getting recommendations"""
    user_id = session.get('user_id')
    limit = request.args.get('limit', 5, type=int)
    
    recommendations = get_user_recommendations(user_id, limit)
    
    result = []
    for rec in recommendations:
        result.append({
            'menu_item_id': rec['menu_item'].menu_item_id,
            'name': rec['menu_item'].name,
            'description': rec['menu_item'].description,
            'price': float(rec['menu_item'].price),
            'category': rec['menu_item'].category,
            'type': rec['type'],
            'score': rec['score'],
            'reason': rec['reason']
        })
    
    return jsonify(result)

@recommendations_bp.route('/refresh')
@login_required
def refresh_recommendations():
    """Refresh recommendations for current user"""
    user_id = session.get('user_id')
    
    # Delete old recommendations for this user
    Recommendation.query.filter_by(user_id=user_id).delete()
    
    # Generate new recommendations
    recommendations = get_user_recommendations(user_id, limit=10)
    
    # Save new recommendations
    for rec in recommendations:
        new_rec = Recommendation(
            user_id=user_id,
            menu_item_id=rec['menu_item'].menu_item_id,
            recommendation_type=rec['type'],
            score=rec['score'],
            ai_model='Content-Based'
        )
        db.session.add(new_rec)
    
    try:
        db.session.commit()
        flash('Recommendations refreshed!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error refreshing recommendations.', 'danger')
    
    return redirect(url_for('recommendations.list_recommendations'))

@recommendations_bp.route('/admin')
@login_required
def admin_recommendations():
    """Admin view of all recommendations"""
    user_role = session.get('user_role', '').lower()
    if user_role not in ['admin', 'supervisor']:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    recommendations = db.session.query(
        Recommendation, User, MenuItem
    ).join(User).join(MenuItem).order_by(
        Recommendation.created_date.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('recommendations/admin.html', recommendations=recommendations)