"""
Create sample food images to demonstrate the system
These are better quality placeholders that look more like real food photos
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_food_sample(name, primary_color, secondary_color, filename):
    """Create a sample food image with realistic food-like appearance"""
    width, height = 400, 300
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        # Gradient from primary to secondary color
        r = int(primary_color[0] + (secondary_color[0] - primary_color[0]) * y / height)
        g = int(primary_color[1] + (secondary_color[1] - primary_color[1]) * y / height)
        b = int(primary_color[2] + (secondary_color[2] - primary_color[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add a plate-like circle in center
    center_x, center_y = width // 2, height // 2
    plate_radius = 110
    
    # Plate shadow
    draw.ellipse(
        [center_x - plate_radius + 5, center_y - plate_radius + 5,
         center_x + plate_radius + 5, center_y + plate_radius + 5],
        fill=(0, 0, 0, 30)
    )
    
    # Plate
    draw.ellipse(
        [center_x - plate_radius, center_y - plate_radius,
         center_x + plate_radius, center_y + plate_radius],
        fill=(250, 248, 245)
    )
    
    # Plate rim
    draw.ellipse(
        [center_x - plate_radius, center_y - plate_radius,
         center_x + plate_radius, center_y + plate_radius],
        outline=(220, 218, 215),
        width=3
    )
    
    # Inner plate circle
    inner_radius = 95
    draw.ellipse(
        [center_x - inner_radius, center_y - inner_radius,
         center_x + inner_radius, center_y + inner_radius],
        outline=(230, 228, 225),
        width=1
    )
    
    # Draw "food" on plate (abstract shapes representing food)
    # This makes it look more like an actual dish
    food_color = primary_color
    
    # Main food item (ellipse)
    draw.ellipse(
        [center_x - 60, center_y - 40,
         center_x + 60, center_y + 40],
        fill=food_color,
        outline=(food_color[0]-20, food_color[1]-20, food_color[2]-20),
        width=2
    )
    
    # Add some garnish/side items
    accent_color = secondary_color
    draw.ellipse(
        [center_x - 50, center_y + 20,
         center_x - 30, center_y + 35],
        fill=accent_color
    )
    draw.ellipse(
        [center_x + 30, center_y + 20,
         center_x + 50, center_y + 35],
        fill=accent_color
    )
    draw.ellipse(
        [center_x - 10, center_y - 45,
         center_x + 10, center_y - 30],
        fill=(100, 180, 100)  # Green garnish
    )
    
    # Add a label at bottom
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw name
    try:
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        
        # Text background
        padding = 10
        draw.rectangle(
            [text_x - padding, height - 60,
             text_x + text_width + padding, height - 30],
            fill=(255, 255, 255, 200)
        )
        draw.text((text_x, height - 55), name, fill=(60, 60, 60), font=font)
        
        # Small note
        note = "Sample Image - Replace with real photo"
        bbox2 = draw.textbbox((0, 0), note, font=small_font)
        note_width = bbox2[2] - bbox2[0]
        note_x = (width - note_width) // 2
        draw.text((note_x, height - 25), note, fill=(120, 120, 120), font=small_font)
    except:
        draw.text((width // 2, height - 40), name, fill=(60, 60, 60), font=font, anchor="mm")
    
    return img

def create_samples():
    """Create sample food images for demonstration"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'static', 'images', 'menu', 'samples')
    
    # Create samples directory
    os.makedirs(images_dir, exist_ok=True)
    
    # Define sample foods with realistic colors
    samples = {
        'roast-chicken.jpg': ('Roast Chicken', (210, 150, 90), (180, 130, 70)),
        'grilled-steak.jpg': ('Grilled Steak', (140, 80, 60), (100, 50, 40)),
        'caesar-salad.jpg': ('Caesar Salad', (140, 180, 100), (100, 140, 80)),
        'chocolate-cake.jpg': ('Chocolate Cake', (90, 60, 50), (120, 80, 65)),
        'pasta-carbonara.jpg': ('Pasta Carbonara', (245, 225, 180), (220, 200, 160)),
        'fish-and-chips.jpg': ('Fish & Chips', (200, 170, 120), (170, 140, 90)),
    }
    
    print("Creating sample food images for demonstration...")
    print("=" * 60)
    
    for filename, (name, primary, secondary) in samples.items():
        img = create_food_sample(name, primary, secondary, filename)
        filepath = os.path.join(images_dir, filename)
        img.save(filepath, 'JPEG', quality=90)
        print(f"✓ Created: {filename}")
    
    print("=" * 60)
    print(f"\n📍 Sample images saved to: {images_dir}")
    print("\n📝 These are EXAMPLE images to show how the system works.")
    print("   To use them:")
    print(f"   1. Copy from 'samples/' to 'menu/' folder")
    print("   2. Or create your own food photos")
    print("   3. Reference the filename when adding menu items")
    print("\n💡 Replace these with actual food photography for best results!")

if __name__ == '__main__':
    try:
        create_samples()
    except Exception as e:
        print(f"❌ Error: {e}")
