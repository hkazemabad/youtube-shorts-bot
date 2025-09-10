import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, ImageClip

# ---------- تنظیمات ----------
YOUTUBE_URL = "YOUR_YOUTUBE_LINK_HERE"  # لینک ویدیو
VIDEO_PATH = "downloaded_video.mp4"
OUTPUT_PATH = "short_final.mp4"
COVER_PATH = "cover.png"                # مسیر تصویر کاور
CLIP_DURATION = 50                       # طول شورت در ثانیه
SH_WIDTH = 1080
SH_HEIGHT = 1920
FPS = 24                                 # فریم بر ثانیه

# ---------- دانلود ویدیو ----------
print("⬇️ دانلود ویدیو از یوتیوب...")
yt = YouTube(YOUTUBE_URL)
stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
stream.download(filename=VIDEO_PATH)
print(f"✅ دانلود شد: {VIDEO_PATH}")

# ---------- بارگذاری ویدیو ----------
video = VideoFileClip(VIDEO_PATH)

# ---------- برش ۵۰ ثانیه اول ----------
short_clip = video.subclip(0, min(CLIP_DURATION, video.duration))

# ---------- تبدیل به عمودی 9:16 ----------
video_resized = short_clip.resize(height=SH_HEIGHT)
video_vertical = video_resized.crop(
    x_center=video_resized.w/2,
    y_center=video_resized.h/2,
    width=SH_WIDTH,
    height=SH_HEIGHT
)

# ---------- اضافه کردن کاور تمام صفحه ----------
cover_clip = ImageClip(COVER_PATH, duration=video_vertical.duration)
cover_clip = cover_clip.resize(video_vertical.size)

# کاور جلو، صدا از ویدیو گرفته می‌شود
final_clip = cover_clip.set_audio(video_vertical.audio)

# ---------- ذخیره نهایی ----------
print("⬇️ در حال ساخت شورت با کاور تمام صفحه...")
final_clip.write_videofile(
    OUTPUT_PATH,
    codec="libx264",
    audio_codec="aac",
    fps=FPS
)

print(f"✅ شورت آماده شد: {OUTPUT_PATH}")
