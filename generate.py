import random
import time
from pathlib import Path

import click
import requests
import yaml
from decouple import config
from openai import OpenAI
from ratelimit import limits, sleep_and_retry

# Create a unique session id based on the current timestamp
session_id = str(int(round(time.time() * 1000)))
session_path = Path(__file__).parent / "sessions" / session_id

client = OpenAI(organization=config("OPENAI_ORG"), api_key=config("OPENAI_API_KEY"))


@sleep_and_retry
@limits(calls=1, period=45)
def create_image(prompt):
    response = client.images.edit(
        image=open("kaj.png", "rb"),
        mask=open("kaj-transparent3.png", "rb"),
        prompt=prompt,
        n=2,
        size="1024x1024",
    )
    return response


def download_images(key, response):
    for ix, image in enumerate(response.data):
        response = requests.get(image.url)
        if response.status_code == 200:
            session_path.mkdir(parents=True, exist_ok=True)
            (session_path / f"{key}-{ix+1:02}.png").write_bytes(response.content)


@click.command()
@click.argument("prompts_file", type=click.Path(exists=True))
def main(prompts_file):
    with open(prompts_file, "rt") as FILE:
        data = yaml.safe_load(FILE)

    portraits = list(data["portraits"])
    random.shuffle(portraits)

    for prompt in portraits:
        key = prompt["key"]
        prompt = prompt["prompt"]
        response = create_image(prompt)
        download_images(key, response)


if __name__ == "__main__":
    main()
