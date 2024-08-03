from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
from pathlib import Path
import random

def create_sector_mask_pieslice(size, start_angle, end_angle):
    # Create a blank mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = size
    radius = min(width, height) // 2

    # Draw the sector
    draw.pieslice([0, 0, width, height], start_angle, end_angle, fill=255)

    return mask

def create_sector_mask_polygon(size, start_angle, end_angle):
    width, height = size
    cx, cy = width // 2, height // 2
    radius = min(width, height) // 2

    # Create a blank mask
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Convert angles to radians
    start_angle_rad = math.radians(start_angle)
    end_angle_rad = math.radians(end_angle)

    # Calculate the coordinates of the sector vertices
    start_x = cx + radius * math.cos(start_angle_rad)
    start_y = cy - radius * math.sin(start_angle_rad)
    end_x = cx + radius * math.cos(end_angle_rad)
    end_y = cy - radius * math.sin(end_angle_rad)

    # Define the polygon points
    polygon = [(cx, cy), (start_x, start_y), (end_x, end_y)]

    # Draw the sector polygon
    draw.polygon(polygon, fill=255)

    return mask

def create_sector_mask_polygon_big(size, start_angle, end_angle):
    width, height = size
    cx, cy = width // 2, height // 2

    # Create a blank mask
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Convert angles to radians
    start_angle_rad = math.radians(start_angle)
    end_angle_rad = math.radians(end_angle)

    # Calculate the coordinates of the sector vertices, extended beyond the image boundaries
    start_x = cx + 2 * width * math.cos(start_angle_rad)
    start_y = cy - 2 * height * math.sin(start_angle_rad)
    end_x = cx + 2 * width * math.cos(end_angle_rad)
    end_y = cy - 2 * height * math.sin(end_angle_rad)

    # Define the polygon points, ensuring it extends beyond the image
    polygon = [(cx, cy), (start_x, start_y), (end_x, end_y)]

    # Draw the sector polygon
    draw.polygon(polygon, fill=255)

    return mask

def blend_images_radial(images, offset=0, blur_radius=0):
    if not images:
        raise ValueError("No images provided for blending")
    
    # Assuming all images are the same size
    width, height = images[0].size
    result = Image.new('RGBA', (width, height))
    
    num_images = len(images)
    angle_per_image = 360 / num_images
    
    for i, img in enumerate(images):
        start_angle = i * angle_per_image + offset
        end_angle = (i + 1) * angle_per_image + offset

        mask = create_sector_mask_polygon_big((width, height), start_angle, end_angle)
        if blur_radius:
            mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
        
        result.paste(img, (0, 0), mask)
    
    return result

# Load your images
if __name__ == "__main__":
    sessions = Path(__file__).parent / "photoshop"
    files = list(sessions.glob("**/*.png"))
    random.shuffle(files)

    num_to_use = 6


    num_to_use = min(num_to_use, len(files))

    images = [Image.open(path).convert("RGBA") for path in files[:num_to_use]]

    # Blend the images
    blended_image = blend_images_radial(images, offset=-90, blur_radius=0)

    # Save the result
    blended_image.save("blended_image.png")
