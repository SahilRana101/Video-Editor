from moviepy.editor import *
import random


clip = VideoFileClip(r"Video clip file destination")
aud = clip.audio
clip = clip.subclip(9, 20)
list_of_clips = []
duration = clip.duration

img = ImageClip(r"Image file destination")
img = img.set_start(0).set_end(9)
list_of_clips.append(img)
list_of_clips.append(clip)

video = CompositeVideoClip(list_of_clips)

video.write_videofile("Video_name.mp4")
