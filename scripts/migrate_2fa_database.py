"""
Database Migration Script for 2FA
Adds 2FA columns to existing user table
"""

import sqlite3
import os

def migrate_database():
    """Add 2FA columns to existing user table"""
    
    # Try multiple possible database locations
    db_paths = [
        'instance/database.db',
        'database.db',
        'instance\\database.db'
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ database.db not found in any location!")
        print("   Searched: instance/database.db, database.db")
        print("   The database will be created when you run the app")
        return False
    
    print(f"📂 Found database: {db_path}\n")
    
    print("\n" + "="*60)
    print("🔄 Migrating Database for 2FA Support")
    print("="*60 + "\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print("📋 Current user table columns:")
        for col in columns:
            print(f"   • {col}")
        print()
        
        migrations_needed = []
        
        # Check each 2FA column
        if 'two_factor_enabled' not in columns:
            migrations_needed.append(('two_factor_enabled', 'BOOLEAN DEFAULT 0'))
        
        if 'otp_code' not in columns:
            migrations_needed.append(('otp_code', 'VARCHAR(6)'))
        
        if 'otp_expiry' not in columns:
            migrations_needed.append(('otp_expiry', 'DATETIME'))
        
        if 'backup_codes' not in columns:
            migrations_needed.append(('backup_codes', 'TEXT'))
        
        if not migrations_needed:
            print("✅ All 2FA columns already exist!")
            print("   No migration needed.")
            conn.close()
            return True
        
        print(f"🔧 Adding {len(migrations_needed)} new columns:\n")
        
        for column_name, column_type in migrations_needed:
            sql = f"ALTER TABLE user ADD COLUMN {column_name} {column_type}"
            print(f"   Adding: {column_name} ({column_type})")
            cursor.execute(sql)
        
        conn.commit()
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        print("\n📋 New user table structure:")
        
        # Show updated structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            marker = "🆕" if col_name in ['two_factor_enabled', 'otp_code', 'otp_expiry', 'backup_codes'] else "  "
            print(f"   {marker} {col_name} ({col_type})")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 2FA Database Migration Tool")
    print("="*60)
    
    success = migrate_database()
    
    if success:
        print("\n" + "="*60)
        print("✅ Database is ready for 2FA!")
        print("="*60)
        print("\nNext steps:")
        print("1. Run: python setup_2fa.py (to verify)")
        print("2. Configure email (see EMAIL_SETUP_GUIDE.md)")
        print("3. Start server: python app.py")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("❌ Migration incomplete")
        print("="*60 + "\n")
