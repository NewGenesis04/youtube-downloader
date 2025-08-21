"""
YouTube Downloader CLI
Downloads both video+audio AND mp3 audio-only (if video is selected).
"""

import os
import sys
import logging
from yt_dlp import YoutubeDL

# ---------------------- Logging Setup ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("youtube_downloader.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# ---------------------- Helpers ----------------------
def build_ydl_opts(download_path, resolution, audio_only, extract_mp3=False):
    """
    Build yt-dlp options dictionary.
    extract_mp3=True ensures audio-only MP3 is extracted even if video was downloaded.
    """
    os.makedirs(download_path, exist_ok=True)

    if audio_only or extract_mp3:
        # Base options for audio extraction
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
    else:
        # Video download with audio merged
        if resolution == "highest":
            fmt = "bestvideo+bestaudio/best"
        elif resolution == "lowest":
            fmt = "worstvideo+worstaudio/worst"
        else:
            fmt = f"bestvideo[height={resolution[:-1]}]+bestaudio/best" if resolution and resolution.endswith("p") else "best"

        ydl_opts = {
            "format": fmt,
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
            "merge_output_format": "mp4",  # Ensures mp4 container
        }

    return ydl_opts


def progress_hook(d):
    """
    CLI-friendly progress bar updates.
    """
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        sys.stdout.write(f"\r⬇️  {percent} | {speed} | ETA {eta}")
        sys.stdout.flush()

    elif d["status"] == "finished":
        logging.info("\n✅ Download completed successfully!")


# ---------------------- Core ----------------------
def download(link, download_path="downloads", resolution="highest", audio_only=False):
    """
    Download video+audio, and also extract MP3 if video was chosen.
    """
    try:
        if audio_only:
            # Only MP3
            ydl_opts = build_ydl_opts(download_path, None, True)
            with YoutubeDL(ydl_opts) as ydl:
                logging.info(f"Fetching audio: {link}")
                ydl.download([link])
        else:
            # Download video first
            ydl_opts = build_ydl_opts(download_path, resolution, False)
            with YoutubeDL(ydl_opts) as ydl:
                logging.info(f"Fetching video: {link}")
                ydl.download([link])

            # Extract MP3 separately
            ydl_opts_mp3 = build_ydl_opts(download_path, None, True, extract_mp3=True)
            with YoutubeDL(ydl_opts_mp3) as ydl:
                logging.info(f"Extracting MP3 audio from: {link}")
                ydl.download([link])

    except Exception as e:
        logging.error(f"Failed to download: {e}")


# ---------------------- CLI ----------------------
def main():
    link = input("Enter YouTube video or playlist link: ").strip()
    if not link:
        logging.error("No link provided. Exiting.")
        return

    choice = input("\nDownload options:\n"
                   "1. Highest resolution video (+ mp3)\n"
                   "2. Lowest resolution video (+ mp3)\n"
                   "3. Audio only (mp3)\n"
                   "4. Custom resolution (+ mp3)\n"
                   "Enter choice (1-4): ")

    if choice == "1":
        res, audio = "highest", True
    elif choice == "2":
        res, audio = "lowest", True
    elif choice == "3":
        res, audio = None, True
    elif choice == "4":
        res = input("Enter resolution (e.g., 360p, 720p, 1080p): ").strip()
        audio = True
    else:
        logging.warning("Invalid choice. Defaulting to highest resolution (+ mp3).")
        res, audio = "highest", True

    # Ask where to save
    custom_path = input("Enter download folder (leave blank for 'downloads'): ").strip()
    download_path = custom_path if custom_path else "downloads"

    # Start download
    download(link, download_path, resolution=res, audio_only=audio)


# ---------------------- Entry ----------------------
if __name__ == "__main__":
    main()
