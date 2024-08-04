import math
import random
from pathlib import Path

import click
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

image_folder = Path(__file__).parent / "photoshop"
session_folder = Path(__file__).parent / "sessions"


def create_sector_mask_polygon(size, start_angle, end_angle):
    width, height = size
    cx, cy = width // 2, height // 2

    # Create a blank mask
    mask = Image.new("L", (width, height), 0)
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


def blend_images_radial(image_paths, offset=0, blur_radius=0, w=1024, h=1024):
    if not image_paths:
        raise ValueError("No images provided for blending")

    images = [Image.open(path).convert("RGBA").resize((w, h)) for path in image_paths]

    # Assuming all images are the same size
    width, height = images[0].size
    result = Image.new("RGBA", (width, height))

    num_images = len(images)
    angle_per_image = 360 / num_images

    for i, img in enumerate(images):
        start_angle = i * angle_per_image + offset
        end_angle = (i + 1) * angle_per_image + offset

        mask = create_sector_mask_polygon((width, height), start_angle, end_angle)
        if blur_radius:
            mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result.paste(img, (0, 0), mask)

    return result


def get_random_images(num_images=10):
    image_files = list(image_folder.glob("**/*.png")) + list(
        session_folder.glob("**/*.png")
    )
    random.shuffle(image_files)
    return image_files[:num_images]


@click.group()
def cli():
    pass


@cli.command("random")
@click.option("--num-images", default=5, help="Number of random images to use")
@click.option("--filename", default="output-blended.png", help="Output filename")
@click.option("--offset", default=-90, help="Degrees to start rendering at")
@click.option("--blur_radius", default=0, help="Blur radius of blend")
def random_command(num_images, filename, offset, blur_radius):
    images = get_random_images(num_images)
    blended_image = blend_images_radial(images, offset=offset, blur_radius=blur_radius)
    blended_image.save(filename)


@cli.command("list")
@click.argument("image_paths", nargs=-1)
@click.option("--filename", default="output-blended.png", help="Output filename")
@click.option("--offset", default=-90, help="Degrees to start rendering at")
@click.option("--blur_radius", default=0, help="Blur radius of blend")
def image_list_command(image_paths, filename, offset, blur_radius):
    blended_image = blend_images_radial(
        image_paths, offset=offset, blur_radius=blur_radius
    )
    blended_image.save(filename)


@cli.command("from-file")
@click.argument(
    "file_list", nargs=1, type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("--filename", default="output-blended.png", help="Output filename")
@click.option("--offset", default=-90, help="Degrees to start rendering at")
@click.option("--blur_radius", default=0, help="Blur radius of blend")
def from_file_command(file_list, filename, offset, blur_radius):
    lines = Path(file_list).read_text().splitlines()
    image_paths = []
    for line in lines:
        if line and not line.startswith("#"):
            image_paths.append(line)

    blended_image = blend_images_radial(
        image_paths, offset=offset, blur_radius=blur_radius
    )
    blended_image.save(filename)


if __name__ == "__main__":
    cli()
