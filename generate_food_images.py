"""
Generate default food images for menu items
Run this script to create placeholder images for different food categories
"""

from PIL import Image, ImageDraw, ImageFont
import os

"""
Generate default food images for menu items
Run this script to create placeholder images matching the reference style
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_food_image(category, emoji, color):
    """Create a placeholder image with reference style - gray background, two squares, text"""
    # Create image with gray background (like reference)
    bg_color = (128, 140, 152)  # Gray background
    img = Image.new('RGB', (400, 300), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw two small squares at the top (like reference image)
    square_size = 35
    square_gap = 15
    total_width = (square_size * 2) + square_gap
    start_x = (400 - total_width) // 2  # Center horizontally
    start_y = 45
    
    # Square color - lighter gray
    square_color = (169, 176, 184)
    outline_color = (100, 110, 120)
    
    # Draw first square
    draw.rectangle(
        [start_x, start_y, start_x + square_size, start_y + square_size],
        fill=square_color,
        outline=outline_color,
        width=2
    )
    
    # Draw second square
    draw.rectangle(
        [start_x + square_size + square_gap, start_y, 
         start_x + square_size + square_gap + square_size, start_y + square_size],
        fill=square_color,
        outline=outline_color,
        width=2
    )
    
    # Try to use a nice font, fallback to default
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
    except:
        try:
            font_large = ImageFont.truetype("Arial.ttf", 48)
        except:
            font_large = ImageFont.load_default()
    
    # Draw category name centered below squares (white text like reference)
    text_y = start_y + square_size + 55
    
    # Calculate text position for centering
    try:
        bbox = draw.textbbox((0, 0), category, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_x = (400 - text_width) // 2
        draw.text((text_x, text_y), category, fill='white', font=font_large)
    except:
        # Fallback for older PIL versions
        draw.text((200, text_y), category, fill='white', font=font_large, anchor='mm')
    
    return img

def generate_default_images():
    """Generate default images for all food categories"""
    
    # Define categories - all use gray background like reference image
    categories = {
        'default-food.jpg': ('Default Food', '#808c98'),
        'appetizers.jpg': ('Appetizers', '#808c98'),
        'main-course.jpg': ('Main Course', '#808c98'),
        'desserts.jpg': ('Desserts', '#808c98'),
        'beverages.jpg': ('Beverages', '#808c98'),
        'salads.jpg': ('Salads', '#808c98'),
        'soups.jpg': ('Soups', '#808c98'),
        'pizza.jpg': ('Pizza', '#808c98'),
        'burger.jpg': ('Burger', '#808c98'),
        'pasta.jpg': ('Pasta', '#808c98'),
        'chicken.jpg': ('Chicken', '#808c98'),
        'seafood.jpg': ('Seafood', '#808c98'),
        'vegetarian.jpg': ('Vegetarian', '#808c98'),
        'breakfast.jpg': ('Breakfast', '#808c98'),
        'sandwich.jpg': ('Sandwich', '#808c98'),
    }
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'static', 'images', 'menu')
    
    # Create directory if it doesn't exist
    os.makedirs(images_dir, exist_ok=True)
    
    print("Generating food placeholder images...")
    
    for filename, (category_name, color) in categories.items():
        filepath = os.path.join(images_dir, filename)
        
        # Create and save image (using category_name directly, not emoji)
        img = create_food_image(category_name, '', color)
        img.save(filepath, 'JPEG', quality=90)
        print(f"✓ Created: {filename}")
    
    print(f"\n🎉 Successfully generated {len(categories)} food images in {images_dir}")
    print("All images created with gray background and two squares (reference style)")
    print("\nYou can now replace these placeholder images with actual food photos.")

if __name__ == '__main__':
    try:
        generate_default_images()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: If PIL/Pillow is not installed, run: pip install Pillow")
