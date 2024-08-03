from pathlib import Path
from blend import blend_images_radial
from PIL import Image

# Load your images
if __name__ == "__main__":
    image_folder = Path(__file__).parent / "photoshop"

    num_to_use = 6

    files = [
        image_folder / "astronomer.png",
        image_folder / "futuristic.png",
        image_folder / "lightman.png",
        image_folder / "norwegian.png",
        image_folder / "steampunk.png",
        # image_folder / "weird.png",
    ]

    num_to_use = len(files)

    images = [Image.open(path).convert("RGBA") for path in files[:num_to_use]]

    # Blend the images
    blended_image = blend_images_radial(images, offset=-90, blur_radius=0)

    # Save the result
    blended_image.save("blended_image.png")
