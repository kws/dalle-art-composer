from pathlib import Path

from PIL import Image

from blend import blend_images_radial


def read_and_resize_image(path, w=1024, h=1024):
    image = Image.open(path).convert("RGBA")
    return image.resize((w, h))


# Load your images
if __name__ == "__main__":
    image_folder = Path(__file__).parent / "photoshop"
    session_folder = Path(__file__).parent / "sessions"

    num_to_use = 6

    files = [
        image_folder / "astronomer.png",
        image_folder / "futuristic.png",
        image_folder / "lightman.png",
        image_folder / "norwegian.png",
        # image_folder / "steampunk.png",
        session_folder / "1722722312347" / "charming_spy-02.png",
        # session_folder / "1722722986442" / "the_hay_wain_style-01.png",
        # image_folder / "weird.png",
    ]

    num_to_use = len(files)

    images = [read_and_resize_image(path) for path in files[:num_to_use]]

    # Blend the images
    blended_image = blend_images_radial(images, offset=-90, blur_radius=0)

    # Save the result
    blended_image.save("blended_image.png")
