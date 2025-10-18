"""
Migration script to add filter columns to MenuItem table
Run this script once to update the database schema
"""
import sqlite3
import os

def migrate_database():
    # Database path
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Please ensure the app has been run at least once to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(menuitem)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print("Current MenuItem columns:", columns)
    
    # Add new columns if they don't exist
    new_columns = {
        'is_vegetarian': 'INTEGER DEFAULT 0 NOT NULL',
        'is_spicy': 'INTEGER DEFAULT 0 NOT NULL',
        'is_popular': 'INTEGER DEFAULT 0 NOT NULL',
        'is_new': 'INTEGER DEFAULT 0 NOT NULL',
        'discount': 'NUMERIC(5, 2) DEFAULT 0 NOT NULL'
    }
    
    for column_name, column_type in new_columns.items():
        if column_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE menuitem ADD COLUMN {column_name} {column_type}")
                print(f"✓ Added column: {column_name}")
            except sqlite3.OperationalError as e:
                print(f"⚠️  Warning for {column_name}: {e}")
        else:
            print(f"✓ Column {column_name} already exists")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("\n🎉 Database migration completed successfully!")
    print("You can now restart your Flask application.")

if __name__ == '__main__':
    migrate_database()
