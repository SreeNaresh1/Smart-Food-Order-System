# Smart Food Ordering System

A comprehensive full-stack web application built with Flask that provides a complete food ordering experience with AI-powered recommendations.

## 🍽️ System Overview

This is a 3-tier architecture application featuring:

- **Frontend**: HTML, CSS, JavaScript with Bootstrap for responsive design
- **Backend**: Flask (Python) with SQLAlchemy ORM
- **Database**: SQLite with 9 normalized tables

## 🚀 Features

### Core Functionality
- ✅ **User Management**: Role-based access (Admin, Supervisor, Employee, Customer)
- ✅ **Menu Management**: Full CRUD operations with categories and search
- ✅ **Order Processing**: Shopping cart, order tracking, status management
- ✅ **Payment System**: Multiple payment methods with transaction tracking
- ✅ **Delivery Management**: Real-time tracking with staff assignment
- ✅ **Kitchen Staff**: Staff scheduling and performance tracking
- ✅ **Feedback System**: Customer reviews and rating analytics

### 🤖 AI-Powered Features
- **Smart Recommendations**: Content-based filtering algorithm
- **Personal Preferences**: Based on order history and ratings
- **Popular Items**: Trending menu items
- **Category Analysis**: Intelligent category suggestions

### 📊 Analytics & Reporting
- **Sales Reports**: Comprehensive sales analytics with filtering
- **Menu Performance**: Top-selling items and category analysis
- **Customer Analytics**: Customer behavior and retention metrics
- **Delivery Performance**: On-time delivery tracking and staff performance
- **Feedback Analytics**: Rating trends and sentiment analysis

### 🔐 Security Features
- **Password Hashing**: Werkzeug security for secure authentication
- **Two-Factor Authentication (2FA)**: Email-based OTP verification with backup codes
- **Session Management**: Secure user sessions
- **Role-Based Access**: Granular permission control
- **SQL Injection Prevention**: Parameterized queries

## 📋 Database Schema

### Tables (9 Normalized Tables)
1. **USER** - User accounts and profiles
2. **ORDER** - Order information and status
3. **ORDERDETAILS** - Individual order items
4. **MENUITEM** - Food items and pricing
5. **PAYMENT** - Payment transactions
6. **FEEDBACK** - Customer reviews and ratings
7. **DELIVERY** - Delivery tracking and assignment
8. **KITCHENSTAFF** - Staff management
9. **RECOMMENDATION** - AI recommendation data

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Clone/Download** the project to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd "food order system"
   ```

3. **Run the setup script**:
   ```bash
   python run.py
   ```

### Manual Setup (Alternative)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure email for 2FA** (optional but recommended):
   - See `EMAIL_SETUP_GUIDE.md` for detailed instructions
   - Set environment variables or edit `app.py` with your email credentials
   - Test configuration: `python test_email_config.py`

3. **Create sample data** (optional):
   ```bash
   python create_sample_data.py
   ```

4. **Start the application**:
   ```bash
   python app.py
   ```

## 🌐 Access Information

- **Application URL**: http://localhost:5000
- **Admin Login**: admin@foodsystem.com / admin123
- **Customer Registration**: Available at /auth/register

## 👥 User Roles & Capabilities

### Admin
- Full system access
- User management
- Menu item management  
- Order management
- Staff management
- Reports and analytics
- System configuration

### Supervisor
- Most admin capabilities
- Order supervision
- Staff scheduling
- Performance monitoring
- Report generation

### Employee
- Order processing
- Payment handling
- Feedback management
- Basic reporting

### Customer
- Browse menu with search/filter
- Shopping cart management
- Order placement and tracking
- AI-powered recommendations
- Feedback and reviews
- Order history

## 📊 Sample Data

The application includes comprehensive sample data:
- **350+ Orders** spanning different time periods
- **30+ Menu Items** across 6 categories (Appetizers, Main Course, Chinese, Continental, Desserts, Beverages)
- **10+ Users** with different roles
- **Kitchen Staff** with various shifts and departments
- **Realistic Transactions** with payments, feedback, and deliveries

## 🤖 AI Recommendation System

### Algorithm: Content-Based Filtering

The recommendation engine analyzes:
- **Order History**: Previous purchases and frequencies
- **Rating Patterns**: Highly rated items and categories
- **Popular Trends**: System-wide popular items
- **Category Preferences**: User's preferred food categories

### Recommendation Types:
- **Personal**: Based on individual user history
- **Popular**: Trending items across all users
- **Similar**: Items similar to highly-rated purchases
- **Seasonal**: Time-based recommendations

## 📈 Reports & Analytics

### Available Reports:
1. **Sales Dashboard**: Overview of key metrics
2. **Sales Report**: Detailed sales analysis with filters
3. **Menu Analysis**: Performance of individual items and categories
4. **Customer Analysis**: Customer behavior and segmentation
5. **Delivery Performance**: Delivery timing and staff efficiency
6. **Feedback Summary**: Customer satisfaction analytics

### Key Metrics:
- Total revenue and order counts
- Average order value
- Customer retention rates
- On-time delivery percentage
- Average customer ratings
- Menu item popularity scores

## 🔧 Technical Architecture

### Backend (Flask)
- **app.py**: Main application entry point
- **models.py**: SQLAlchemy database models
- **routes/**: Modular blueprint-based routing
- **Authentication**: Session-based with role checking
- **Database**: SQLite with automatic table creation

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Custom CSS**: Enhanced styling and animations
- **JavaScript**: Interactive features and AJAX calls

### File Structure:
```
food order system/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── run.py               # Setup and launch script
├── create_sample_data.py # Sample data generator
├── routes/              # Route blueprints
│   ├── auth.py          # Authentication routes
│   ├── menu.py          # Menu management
│   ├── orders.py        # Order processing
│   ├── users.py         # User management
│   ├── payments.py      # Payment handling
│   ├── feedback.py      # Feedback system
│   ├── delivery.py      # Delivery tracking
│   ├── kitchen.py       # Kitchen staff
│   ├── recommendations.py # AI recommendations
│   └── reports.py       # Analytics and reports
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── dashboard.html   # Main dashboard
│   ├── auth/           # Authentication pages
│   ├── menu/           # Menu pages
│   └── ...             # Other template directories
└── static/             # Static files
    ├── css/style.css   # Custom styles
    └── js/main.js      # JavaScript functionality
```

## 🧪 Testing Data

### Test Credentials:
- **Admin**: admin@foodsystem.com / admin123
- **Supervisor**: supervisor@foodsystem.com / supervisor123
- **Employee**: alice@foodsystem.com / employee123
- **Customer**: Register new account or use existing sample customers

### Test Scenarios:
1. **Customer Journey**: Browse menu → Add to cart → Place order → Track delivery → Provide feedback
2. **Admin Tasks**: Add menu items → Manage users → View reports → Monitor orders
3. **Order Management**: Process orders → Update status → Assign delivery → Handle payments

## 🚀 Performance Features

- **Optimized Queries**: Efficient database operations with proper indexing
- **Pagination**: Large datasets handled with pagination
- **Caching**: Session-based cart management
- **Responsive Design**: Mobile-friendly interface
- **Fast Search**: Real-time search and filtering

## 🔮 AI Implementation Details

The recommendation system uses a hybrid approach:

1. **Content-Based Analysis**:
   - User preference profiling
   - Category affinity scoring
   - Historical purchase analysis

2. **Popularity-Based Recommendations**:
   - Order frequency analysis
   - Rating-weighted popularity
   - Trending item detection

3. **Collaborative Patterns**:
   - Similar user behavior
   - Cross-category recommendations
   - Seasonal preference tracking

## 📞 Support

For technical support or questions about the implementation:
- Review the code comments and documentation
- Check the Flask and SQLAlchemy documentation
- Examine the sample data and test scenarios

## 📚 Additional Documentation

- **[TWO_FACTOR_AUTH_GUIDE.md](TWO_FACTOR_AUTH_GUIDE.md)** - Complete guide to Two-Factor Authentication setup and usage
- **[EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md)** - Quick email configuration for 2FA (Gmail, Outlook, etc.)
- **DOCUMENTATION/** - Comprehensive technical and user documentation

## 🏆 Key Achievements

✅ **Complete CRUD Operations** for all 9 database tables  
✅ **Role-Based Security** with proper access controls  
✅ **Two-Factor Authentication** with email OTP and backup codes  
✅ **AI-Powered Recommendations** with content-based filtering  
✅ **Comprehensive Reporting** with SQL joins and aggregations  
✅ **Responsive Design** with modern UI/UX  
✅ **Scalable Architecture** with modular blueprints  
✅ **Performance Optimized** for 500+ records  
✅ **Production-Ready** with proper error handling

---
**Built with ❤️ using Flask, SQLAlchemy, Bootstrap, and AI algorithms**