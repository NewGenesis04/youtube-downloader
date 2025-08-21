# YouTube Downloader

This repository provides a simple command-line interface (CLI) to download YouTube videos and playlists.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Files](#files)
5. [License](#license)

## Requirements

The following Python packages are required to run the script:

- tqdm: A fast, extensible progress bar for Python and CLI.
- yt-dlp: A fork of youtube-dl with additional features and fixes.

## Installation

To install the required packages, navigate to the project directory and run:

```
pip install -r requirements.txt
```

## Usage

To use the YouTube Downloader, run the provided `main.py` script. The script will guide you through the process of selecting the download options (highest/lowest resolution, audio-only, or custom resolution) and the download path.

## Files

### main.py

This script provides a CLI to download YouTube videos and playlists. It handles user input for selecting download options and the download path.

### playlist_downloader.py

This script contains the core functionality to download YouTube playlists using the `yt-dlp` library. It provides a function `download_playlist()` that takes the playlist link, download path, resolution, and audio-only options as input.

### video_downloader.py

This script contains the core functionality to download YouTube videos using the `yt-dlp` library. It provides a function `download_video()` that takes the video link, download path, resolution, and audio-only options as input.

### requirements.txt

This file lists the required Python packages for the project.

## License

This project is licensed under the [MIT License](LICENSE).