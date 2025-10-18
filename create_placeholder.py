"""
Create a single clean placeholder image for menu items without photos
This will be used as fallback when no specific food image is available
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image():
    """Create a clean, neutral placeholder image"""
    # Image dimensions
    width, height = 400, 300
    
    # Neutral gray background
    bg_color = (240, 242, 245)
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a centered icon/symbol
    # Draw a simple plate/dish icon
    center_x, center_y = width // 2, height // 2
    
    # Outer circle (plate)
    plate_radius = 60
    draw.ellipse(
        [center_x - plate_radius, center_y - plate_radius,
         center_x + plate_radius, center_y + plate_radius],
        outline=(180, 190, 200),
        width=4
    )
    
    # Inner circle
    inner_radius = 45
    draw.ellipse(
        [center_x - inner_radius, center_y - inner_radius,
         center_x + inner_radius, center_y + inner_radius],
        outline=(180, 190, 200),
        width=2
    )
    
    # Add utensils (fork and knife)
    # Fork on left
    fork_x = center_x - 90
    fork_y = center_y
    draw.line([fork_x, fork_y - 40, fork_x, fork_y + 40], fill=(150, 160, 170), width=3)
    for i in range(-2, 3):
        draw.line([fork_x + i*6, fork_y - 40, fork_x + i*6, fork_y - 25], fill=(150, 160, 170), width=2)
    
    # Knife on right
    knife_x = center_x + 90
    knife_y = center_y
    draw.line([knife_x, knife_y - 40, knife_x, knife_y + 40], fill=(150, 160, 170), width=3)
    draw.polygon([knife_x - 4, knife_y - 40, knife_x + 4, knife_y - 40, knife_x, knife_y - 50], 
                 fill=(150, 160, 170))
    
    # Add text at bottom
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = "No Image Available"
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, height - 50), text, fill=(150, 160, 170), font=font)
    except:
        draw.text((width // 2, height - 50), text, fill=(150, 160, 170), font=font, anchor="mm")
    
    return img

def main():
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'static', 'images', 'menu')
    
    # Create directory if it doesn't exist
    os.makedirs(images_dir, exist_ok=True)
    
    # Create and save the placeholder
    img = create_placeholder_image()
    filepath = os.path.join(images_dir, 'default-food.jpg')
    img.save(filepath, 'JPEG', quality=90)
    
    print("✓ Created: default-food.jpg (clean placeholder)")
    print(f"\n📍 Saved to: {images_dir}")
    print("\n📝 Instructions:")
    print("=" * 60)
    print("To add food images for your menu items:")
    print("1. Place your food images in: static/images/menu/")
    print("2. Name them descriptively (e.g., 'roast-chicken.jpg', 'burger-deluxe.jpg')")
    print("3. When adding/editing menu items, enter the image filename")
    print("   Example: 'roast-chicken.jpg' or 'images/menu/roast-chicken.jpg'")
    print("4. Supported formats: .jpg, .jpeg, .png, .webp")
    print("5. Recommended size: 400x300 pixels or similar ratio")
    print("\nThe 'default-food.jpg' will be used for items without specific images.")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: If PIL/Pillow is not installed, run: pip install Pillow")
