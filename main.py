"""
YouTube Downloader CLI
Downloads both video+audio AND mp3 audio-only (if video is selected).
"""

import os
import sys
from rich.progress import Progress
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
def build_ydl_opts(download_path, resolution, audio_only, progress_hooks, extract_mp3=False):
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
            "progress_hooks": progress_hooks,
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
            "progress_hooks": progress_hooks,
            "merge_output_format": "mp4",  # Ensures mp4 container
        }

    return ydl_opts


# ---------------------- Core ----------------------
def download(link, download_path="downloads", resolution="highest", audio_only=False):
    """
    Download video+audio, and also extract MP3 if video was chosen.
    """
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Starting...", total=None)

            def progress_hook(d):
                """
                CLI-friendly progress bar updates. Updates the task in the outer scope.
                """
                if d["status"] == "downloading":
                    if progress.tasks[task].total is None:
                        progress.update(task, total=d.get("total_bytes"))
                    progress.update(task, completed=d.get("downloaded_bytes", 0), description="[cyan]Downloading...")
                elif d["status"] == "finished":
                    progress.update(task, description=f"[green]Finished: {os.path.basename(d['filename'])}")
                    logging.info(f"Download finished: {d['filename']}")
                elif d["status"] == "error":
                    progress.update(task, description="[red]Error!")
                    logging.error(f"Error during download: {d.get('error', 'Unknown error')}")

            hooks = [progress_hook]

            if audio_only:
                # Only MP3
                progress.update(task, description="[cyan]Downloading audio...")
                ydl_opts = build_ydl_opts(download_path, None, True, hooks)
                with YoutubeDL(ydl_opts) as ydl:
                    logging.info(f"Fetching audio: {link}")
                    ydl.download([link])
            else:
                # Download video first
                progress.update(task, description="[cyan]Downloading video...")
                ydl_opts = build_ydl_opts(download_path, resolution, False, hooks)
                with YoutubeDL(ydl_opts) as ydl:
                    logging.info(f"Fetching video: {link}")
                    ydl.download([link])

                # Extract MP3 separately
                progress.update(task, description="[cyan]Extracting MP3...", completed=0, total=None)
                ydl_opts_mp3 = build_ydl_opts(download_path, None, True, hooks, extract_mp3=True)
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

    res = "highest"
    audio_only_flag = False

    match choice:
        case "1":
            res, audio_only_flag = "highest", False
        case "2":
            res, audio_only_flag = "lowest", False
        case "3":
            res, audio_only_flag = None, True
        case "4":
            res = input("Enter resolution (e.g., 360p, 720p, 1080p): ").strip()
            audio_only_flag = False
        case _:
            logging.warning("Invalid choice. Defaulting to highest resolution (+ mp3).")
            res, audio_only_flag = "highest", False

    # Ask where to save
    custom_path = input("Enter download folder (leave blank for 'downloads'): ").strip()
    download_path = custom_path if custom_path else "downloads"

    # Start download
    download(link, download_path, resolution=res, audio_only=audio_only_flag)



# ---------------------- Entry ----------------------
if __name__ == "__main__":
    main()
