# YouTube Downloader CLI

A powerful and user-friendly command-line tool for downloading YouTube videos, playlists, and audio. It offers format/resolution selection, automatic MP3 extraction, and subtitle support.

## Overview

This script provides an interactive command-line interface (CLI) to download content from YouTube. You can grab single videos or entire playlists, choose your desired video quality, or opt for an audio-only MP3 download. For maximum convenience, when you download a video, an MP3 version is also saved.

The tool is designed for ease of use, with clear prompts to guide you through the download process. It also includes Docker support for running in a containerized environment, simplifying dependency management.

## Features

- **Download Single Videos or Playlists:** Just provide the URL.
- **Flexible Resolution:** Choose from the highest, lowest, or a custom video resolution.
- **Audio-Only Mode:** Download directly to an MP3 file.
- **Automatic MP3 Extraction:** Get an MP3 audio file alongside every video download.
- **Subtitle Support:** Download subtitles for your chosen languages, with an option to include auto-generated captions.
- **Interactive CLI:** User-friendly prompts make it easy to configure your download.
- **Dockerized:** Run the application in a container with all dependencies, including FFmpeg, pre-installed.

## Prerequisites

This script relies on the powerful `yt-dlp` library, which requires the **FFmpeg** multimedia framework to be installed on your system for processing and merging video and audio streams.

### FFmpeg Installation

You must install FFmpeg on your system before using the script.

**On Windows (using [Winget](https://winstall.app/apps/Gyan.FFmpeg)):**
Open PowerShell or Command Prompt and run:
```sh
winget install -e --id Gyan.FFmpeg
```

**On Linux (Debian/Ubuntu):**
```sh
sudo apt update && sudo apt install ffmpeg
```

**On Linux (Fedora/CentOS):**
```sh
sudo dnf install ffmpeg
```

## Setup

Follow these steps to set up the project locally.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/NewGenesis04/youtube-downloader.git Youtube_Downloader
    cd Youtube_Downloader
    ```

2.  **Create and activate a virtual environment:**
    - On Windows:
      ```sh
      python -m venv .venv
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      python3 -m venv .venv
      source .venv/bin/activate
      ```

3.  **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the application, simply execute the main script:

```sh
python main.py
```

The script will then prompt you for:
1.  A YouTube video or playlist URL.
2.  Your desired download option (highest/lowest resolution, audio-only, etc.).
3.  A destination folder (defaults to the `downloads` directory).
4.  Whether you want to download subtitles.

## Docker Support

You can also run this application within a Docker container, which handles all dependencies for you.

1.  **Build the Docker image:**
    From the project root directory, run:
    ```sh
    docker build -t youtube-downloader .
    ```

2.  **Run the Docker container:**
    ```sh
    docker run --rm -it -v "$(pwd)/downloads:/app/downloads" youtube-downloader
    ```
    - `docker run --rm -it`: Runs the container in interactive mode and removes it once it exits.
    - `-v "$(pwd)/downloads:/app/downloads"`: This is crucial. It maps the `downloads` folder on your local machine to the `/app/downloads` folder inside the container. This ensures that your downloaded files are saved to your computer, not just inside the temporary container.

## Project Structure

```
.
├── Dockerfile              # Defines the Docker container environment.
├── main.py                 # Main script and CLI entry point.
├── requirements.txt        # Python dependencies.
├── downloads/              # Default output directory for downloads.
└── README.md               # This file.
```
