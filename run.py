"""
Startup script for Smart Food Ordering System
Run this script to start the application with sample data
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def create_sample_data():
    """Create sample data"""
    print("Creating sample data...")
    try:
        from create_sample_data import create_sample_data
        create_sample_data()
        print("Sample data created successfully!")
    except ImportError:
        print("Running sample data script...")
        subprocess.check_call([sys.executable, 'create_sample_data.py'])

def start_application():
    """Start the Flask application"""
    print("Starting Smart Food Ordering System...")
    print("=" * 50)
    print("🍽️  Smart Food Ordering System")
    print("=" * 50)
    print("📝 Features Included:")
    print("   ✅ User Management (Admin, Supervisor, Employee, Customer)")
    print("   ✅ Menu Management with Categories")
    print("   ✅ Order Processing & Cart System")
    print("   ✅ Payment Processing")
    print("   ✅ Delivery Tracking")
    print("   ✅ Kitchen Staff Management")
    print("   ✅ AI-Based Food Recommendations")
    print("   ✅ Feedback System")
    print("   ✅ Comprehensive Reports & Analytics")
    print("   ✅ Role-Based Access Control")
    print("   ✅ Responsive Web Design")
    print()
    print("🚀 Access URLs:")
    print("   🌐 Application: http://localhost:5000")
    print("   👤 Admin Login: admin@foodsystem.com / admin123")
    print("   👥 Customer: Register new account or use sample data")
    print()
    print("📊 Sample Data Includes:")
    print("   • 350+ Orders across different time periods")
    print("   • 30+ Menu items in 6 categories")
    print("   • 10+ Users with different roles")
    print("   • Kitchen staff and delivery personnel")
    print("   • Payments, feedback, and recommendations")
    print()
    print("💡 AI Recommendations:")
    print("   • Content-based filtering")
    print("   • Personal preferences analysis")
    print("   • Popular item suggestions")
    print("   • Category-based recommendations")
    print()
    print("=" * 50)
    
    # Start Flask app
    subprocess.check_call([sys.executable, 'app.py'])

def main():
    """Main function to set up and run the application"""
    print("Smart Food Ordering System - Setup & Launch")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        return
    
    try:
        # Step 1: Install requirements
        install_requirements()
        
        # Step 2: Create sample data (if requested)
        create_sample = input("\n🔄 Create sample data? (y/n) [y]: ").strip().lower()
        if create_sample in ['', 'y', 'yes']:
            create_sample_data()
        
        # Step 3: Start application
        print("\n🚀 Starting application...")
        time.sleep(2)
        start_application()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please check the error and try again.")

if __name__ == '__main__':
    main()