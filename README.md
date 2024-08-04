
# Image Generation, Blending, and Video Creation Scripts

This repository contains Python scripts to generate random versions of a portrait picture using OpenAI DALLE-2, blend multiple images using a radial pattern, and combine them into short video clips.

## Scripts Overview

1. **generate.py**: Creates random versions of your portrait picture using OpenAI DALLE-2.
2. **blend.py**: Blends multiple images into a single image using a radial pattern.
3. **movie.py**: Combines the generated and blended images into short video clips.

## Third-Party Libraries

This project uses the following third-party libraries:

- `openai`: For interacting with OpenAI DALLE-2 API.
- `Pillow`: For image processing.
- `moviepy`: For creating video clips.
- `numpy`: For numerical operations.

## Getting Started

To manage dependencies and environment, this project uses [Poetry](https://python-poetry.org/). Follow the steps below to set up your environment.

### Prerequisites

- Python 3.7 or higher
- Poetry

### Installation

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. **Install dependencies using Poetry:**

```sh
poetry install
```

3. **Activate the virtual environment:**

```sh
poetry shell
```

### Usage

These scripts aren't expected to be reusable and are just me playing around - so you'll porbably have to tweak a few bits here and there to get started.

### Configuration

Make sure to set your OpenAI API key as an environment variable before running the scripts:

```sh
export OPENAI_API_KEY='your-api-key'
export OPENAI_ORG='your-org'
```

You can also put these values in a `.env` file.

## License

### Python Scripts

The Python scripts in this repository are licensed under the MIT License. See the LICENSE file for details.

### Image Files

All image files in this repository are under an All Rights Reserved license. See the LICENSE file for details.
