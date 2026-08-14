
import os
import sys
import yt_dlp
from moviepy.editor import VideoFileClip

def process_video(url):
    print(f"[*] Downloading video from: {url}")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': 'source_video.mp4',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("[*] Processing and cropping to 9:16 vertical format...")
    clip = VideoFileClip("source_video.mp4")
    
    # Crop center for 9:16 aspect ratio
    w, h = clip.size
    target_width = h * (9 / 16)
    x_center = w / 2
    x1 = x_center - (target_width / 2)
    x2 = x_center + (target_width / 2)
    
    cropped_clip = clip.crop(x1=x1, y1=0, x2=x2, y2=h)
    
    # Trim first 30 seconds as a sample Short
    short_clip = cropped_clip.subclipped(0, min(30, clip.duration))
    
    output_filename = "output_short.mp4"
    short_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    print(f"[*] Successfully generated: {output_filename}")

if __name__ == "__main__":
    # URL passed via environment variable from GitHub Actions
    target_url = os.environ.get("VIDEO_URL", "https://www.youtube.com/watch?v=BaW_jenozKc")
    process_video(target_url)
