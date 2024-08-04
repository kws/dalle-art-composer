import random
from pathlib import Path

import click
import cv2
import numpy as np
from moviepy.editor import *
from PIL import Image

image_folder = Path(__file__).parent / "photoshop"
session_folder = Path(__file__).parent / "sessions"


def circle_wipe(clip1, clip2, duration):
    def make_frame(t):
        img1 = clip1.get_frame(t)
        img2 = clip2.get_frame(t)
        height, width, _ = img1.shape
        mask = np.zeros((height, width), dtype=np.float32)
        # Calculate the diagonal length for the radius
        max_radius = int(np.sqrt(width**2 + height**2) / 2)
        radius = int((t / duration) * max_radius)
        cv2.circle(mask, (width // 2, height // 2), radius, 1, -1)
        return img1 * (1 - mask)[:, :, None] + img2 * mask[:, :, None]

    return VideoClip(make_frame, duration=duration)


def read_and_resize_image(path, w=1024, h=1024):
    image = Image.open(path).convert("RGB")
    return np.array(image.resize((w, h)))


def get_random_images(num_images=10):
    image_files = list(image_folder.glob("**/*.png")) + list(
        session_folder.glob("**/*.png")
    )
    random.shuffle(image_files)
    return image_files[:num_images]


def images_to_clips(image_files, durations=2):
    if isinstance(durations, int):
        durations = [durations] * len(image_files)

    # Load the images into clips
    return [
        ImageClip(read_and_resize_image(m)).set_duration(d)
        for m, d in zip(image_files, durations)
    ]


def create_transitions(clips, transition_duration=1):
    # Create transition clips
    transition_clips = []
    for i in range(len(clips) - 1):
        transition_clips.append(clips[i])
        transition_clips.append(
            circle_wipe(clips[i], clips[i + 1], transition_duration)
        )

    # Add the final clip
    transition_clips.append(clips[-1])

    # Concatenate all clips with transitions
    return concatenate_videoclips(transition_clips, method="compose")


def save_video_mp4(clip, filename, fps=24):
    clip.write_videofile(
        filename,
        codec="libx264",
        fps=fps,
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )


def save_video_gif(clip, filename, fps=24):
    clip.write_gif(filename, fps=fps)


def save_video(clip, filename, fps=24):
    if filename.endswith(".gif"):
        save_video_gif(clip, filename, fps)
    else:
        save_video_mp4(clip, filename, fps)


def composite_images(images, duration, transition_duration):
    clip = images_to_clips(images, duration)
    clip = create_transitions(clip, transition_duration)
    return clip


def random_images(num_images, filename, duration, transition_duration, fps):
    images = get_random_images(num_images)
    clip = composite_images(images, duration, transition_duration)
    save_video(clip, filename, fps)


def image_list(image_paths, filename, duration, transition_duration, fps):
    clip = composite_images(image_paths, duration, transition_duration)
    save_video(clip, filename, fps)


@click.group()
def cli():
    pass


@cli.command("random")
@click.option("--num-images", default=10, help="Number of random images to generate")
@click.option("--filename", default="output.mp4", help="Output filename")
@click.option("--duration", default=2, help="Duration of each image in seconds")
@click.option(
    "--transition-duration", default=1, help="Duration of the transition in seconds"
)
@click.option("--fps", default=24, help="Frames per second")
def random_images_command(num_images, filename, duration, transition_duration, fps):
    random_images(num_images, filename, duration, transition_duration, fps)


@cli.command("list")
@click.argument("image_paths", nargs=-1)
@click.option("--filename", default="output.mp4", help="Output filename")
@click.option("--duration", default=2, help="Duration of each image in seconds")
@click.option(
    "--transition-duration", default=1, help="Duration of the transition in seconds"
)
@click.option("--fps", default=24, help="Frames per second")
def image_list_command(image_paths, filename, duration, transition_duration, fps):
    image_list(image_paths, filename, duration, transition_duration, fps)


if __name__ == "__main__":
    cli()
