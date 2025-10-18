"""
Update existing menu items to use proper image paths or null values
This clears out the old category-based placeholder references
"""
import sqlite3
import os

def update_menu_images():
    """Update menu item images in database"""
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all menu items
    cursor.execute("SELECT menu_item_id, name, image FROM menuitem")
    items = cursor.fetchall()
    
    print("Current menu items:")
    print("=" * 70)
    
    updated = 0
    for item_id, name, image in items:
        # If image references old category placeholders, clear it
        old_placeholders = [
            'appetizers.jpg', 'main-course.jpg', 'desserts.jpg', 
            'beverages.jpg', 'salads.jpg', 'soups.jpg',
            'pizza.jpg', 'burger.jpg', 'pasta.jpg',
            'chicken.jpg', 'seafood.jpg', 'vegetarian.jpg',
            'breakfast.jpg', 'sandwich.jpg'
        ]
        
        if image in old_placeholders or image == 'default-food.jpg':
            # Clear the image so it uses the fallback
            cursor.execute("UPDATE menuitem SET image = NULL WHERE menu_item_id = ?", (item_id,))
            print(f"✓ Cleared: {name} (was using {image})")
            updated += 1
        else:
            print(f"  Kept: {name} (image: {image or 'None - will use default'})")
    
    conn.commit()
    conn.close()
    
    print("=" * 70)
    print(f"\n✅ Updated {updated} menu items")
    print(f"   Total items: {len(items)}")
    print("\n📝 Next steps:")
    print("   1. Add real food images to static/images/menu/")
    print("   2. Edit menu items through admin panel")
    print("   3. Set image filename for each item (e.g., 'roast-chicken.jpg')")
    print("   4. Items without images will show the default placeholder")

if __name__ == '__main__':
    try:
        update_menu_images()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
