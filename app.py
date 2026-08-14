import os
import sys
import yt_dlp
from moviepy.editor import VideoFileClip

def process_video(url):
    # Convert standard youtube URL to a Piped/Invidious proxy stream if it fails direct
    print(f"[*] Fetching video stream for: {url}")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'source_video.mp4',
        'geo_bypass': True,
        'nocheckcertificate': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"[*] Direct download failed, trying alternative client workaround... {e}")
            # Fallback to embedded player client signature
            ydl_opts['extractor_args'] = {'youtube': {'player_client': ['mweb']}}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_fallback:
                ydl_fallback.download([url])

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
    target_url = os.environ.get("VIDEO_URL", "https://www.youtube.com/watch?v=jNQXAC9IVRw")
    process_video(target_url)
