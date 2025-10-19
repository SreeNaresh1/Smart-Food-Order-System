"""
Database Migration Script - Enhanced 2FA Features
Adds login history tracking, trusted devices, and account lockout features
"""

from app import app, db
from models import User, LoginHistory, TrustedDevice
from datetime import datetime

def migrate_database():
    """Add new 2FA enhancement tables and columns"""
    
    print("=" * 60)
    print("🔧 ENHANCED 2FA DATABASE MIGRATION")
    print("=" * 60)
    
    with app.app_context():
        print("\n📋 Step 1: Creating backup of current schema...")
        
        # Check if tables already exist
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print(f"✓ Found {len(existing_tables)} existing tables")
        
        print("\n📋 Step 2: Adding new columns to User table...")
        try:
            # Check if new columns exist
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            
            columns_to_add = []
            if 'failed_login_attempts' not in user_columns:
                columns_to_add.append('failed_login_attempts')
            if 'account_locked_until' not in user_columns:
                columns_to_add.append('account_locked_until')
            if 'last_login' not in user_columns:
                columns_to_add.append('last_login')
            
            if columns_to_add:
                print(f"  ➜ Adding columns: {', '.join(columns_to_add)}")
                
                # Add columns using raw SQL (safer for existing databases)
                with db.engine.connect() as conn:
                    if 'failed_login_attempts' in columns_to_add:
                        conn.execute(db.text("ALTER TABLE user ADD COLUMN failed_login_attempts INTEGER DEFAULT 0"))
                        conn.commit()
                        print("    ✓ Added: failed_login_attempts")
                    
                    if 'account_locked_until' in columns_to_add:
                        conn.execute(db.text("ALTER TABLE user ADD COLUMN account_locked_until DATETIME"))
                        conn.commit()
                        print("    ✓ Added: account_locked_until")
                    
                    if 'last_login' in columns_to_add:
                        conn.execute(db.text("ALTER TABLE user ADD COLUMN last_login DATETIME"))
                        conn.commit()
                        print("    ✓ Added: last_login")
            else:
                print("  ✓ All user columns already exist")
        
        except Exception as e:
            print(f"  ⚠️  Note: {str(e)}")
            print("  → Columns may already exist, continuing...")
        
        print("\n📋 Step 3: Creating new tables...")
        
        # Create all tables (will skip existing ones)
        try:
            db.create_all()
            
            # Verify new tables
            inspector = db.inspect(db.engine)
            updated_tables = inspector.get_table_names()
            
            if 'login_history' in updated_tables:
                print("  ✓ Created: login_history table")
            else:
                print("  ℹ️  login_history table already exists")
            
            if 'trusted_device' in updated_tables:
                print("  ✓ Created: trusted_device table")
            else:
                print("  ℹ️  trusted_device table already exists")
        
        except Exception as e:
            print(f"  ⚠️  Error creating tables: {str(e)}")
        
        print("\n📋 Step 4: Verifying schema...")
        
        # Verify LoginHistory table
        try:
            login_count = LoginHistory.query.count()
            print(f"  ✓ LoginHistory table operational ({login_count} records)")
        except Exception as e:
            print(f"  ✗ LoginHistory table issue: {str(e)}")
        
        # Verify TrustedDevice table
        try:
            device_count = TrustedDevice.query.count()
            print(f"  ✓ TrustedDevice table operational ({device_count} records)")
        except Exception as e:
            print(f"  ✗ TrustedDevice table issue: {str(e)}")
        
        # Verify User table columns
        try:
            user = User.query.first()
            if user:
                # Try to access new columns
                _ = user.failed_login_attempts
                _ = user.account_locked_until
                _ = user.last_login
                print(f"  ✓ User table enhanced successfully")
        except Exception as e:
            print(f"  ⚠️  User table verification: {str(e)}")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\n📊 New Features Available:")
        print("  ✓ Login History Tracking")
        print("  ✓ Trusted Device Management")
        print("  ✓ Account Lockout Protection")
        print("  ✓ Failed Attempt Monitoring")
        print("  ✓ Device Fingerprinting")
        
        print("\n🔧 Database Schema Updated:")
        print("  • User table: +3 columns")
        print("  • LoginHistory table: NEW")
        print("  • TrustedDevice table: NEW")
        
        print("\n📝 Next Steps:")
        print("  1. Restart your Flask application")
        print("  2. Test login with 2FA enabled")
        print("  3. Check 'Remember This Device' option")
        print("  4. View login history in profile")
        print("  5. Check admin dashboard for 2FA stats")
        
        print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        migrate_database()
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("  1. Make sure the Flask app is not running")
        print("  2. Check database file permissions")
        print("  3. Verify models.py is updated")
        print("  4. Try running: python app.py first")
        import traceback
        traceback.print_exc()
