import os
import sys
import time
import random
import logging
from yt_dlp import YoutubeDL
from tqdm import tqdm

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
def build_ydl_opts(download_path, resolution, audio_only):
    """
    Build yt-dlp options dictionary.
    """
    os.makedirs(download_path, exist_ok=True)

    if audio_only:
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
        if resolution == "highest":
            fmt = "bestvideo+bestaudio/best"
        elif resolution == "lowest":
            fmt = "worstvideo+worstaudio/worst"
        else:
            # Try custom resolution
            fmt = f"bestvideo[height={resolution[:-1]}]+bestaudio/best" if resolution.endswith("p") else "best"

        ydl_opts = {
            "format": fmt,
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook]
        }

    return ydl_opts


def progress_hook(d):
    """
    tqdm-compatible progress bar updates.
    """
    if d["status"] == "downloading":
        if "total_bytes" in d:
            total = d["total_bytes"]
        elif "total_bytes_estimate" in d:
            total = d["total_bytes_estimate"]
        else:
            total = None

        if total:
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()
            sys.stdout.write(f"\r⬇️  {percent} | {speed} | ETA {eta}")
            sys.stdout.flush()

    elif d["status"] == "finished":
        logging.info("\n✅ Download completed successfully!")


# ---------------------- Core ----------------------
def download_video(youtube_link, download_path="downloads", resolution="highest", audio_only=False):
    """
    Download a single YouTube video with yt-dlp.
    """
    try:
        ydl_opts = build_ydl_opts(download_path, resolution, audio_only)
        with YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Fetching video: {youtube_link}")
            ydl.download([youtube_link])
    except Exception as e:
        logging.error(f"Unexpected error while downloading video: {e}")


def download_playlist(playlist_link, download_path="downloads", resolution="highest", audio_only=False):
    """
    Download all videos from a playlist with yt-dlp.
    """
    try:
        ydl_opts = build_ydl_opts(download_path, resolution, audio_only)
        with YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Fetching playlist: {playlist_link}")
            ydl.download([playlist_link])
    except Exception as e:
        logging.error(f"Failed to download playlist: {e}")


# ---------------------- CLI ----------------------
def main():
    link = input("Enter YouTube video or playlist link: ").strip()
    if not link:
        logging.error("No link provided. Exiting.")
        return

    # Decide if link is playlist or video
    is_playlist = "playlist" in link.lower()

    choice = input("\nDownload options:\n"
                   "1. Highest resolution video\n"
                   "2. Lowest resolution video\n"
                   "3. Audio only (mp3)\n"
                   "4. Custom resolution (e.g., 720p)\n"
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
        logging.warning("Invalid choice. Defaulting to highest resolution.")
        res, audio = "highest", True

    # Ask where to save
    custom_path = input("Enter download folder (leave blank for 'downloads'): ").strip()
    download_path = custom_path if custom_path else "downloads"

    # Download video or playlist
    if is_playlist:
        download_playlist(link, download_path, resolution=res, audio_only=audio)
    else:
        download_video(link, download_path, resolution=res, audio_only=audio)


# ---------------------- Entry ----------------------
if __name__ == "__main__":
    main()



# https://www.youtube.com/watch?v=xD1tmNm9u_I