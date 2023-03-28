import proglog
import numpy as np
from moviepy.video.io import ffmpeg_writer
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter


list_of_video_clips = []
list_of_audio_clips = []
list_of_letters_and_time_stamps = [["A", "1", "2"], ["B", "3", "4"], ["C", "5", "6"], ["D", "7", "8"], ["E", "9", "10"]]


def edit_percent(timing, duration_of_clip):
    print(str(int((timing/duration_of_clip)*100)+1) + " %")


def new_ffmpeg_write_video(clip, filename, fps, codec="libx264", bitrate=None,
                           preset="medium", withmask=False, write_logfile=False,
                           audiofile=None, verbose=True, threads=None, ffmpeg_params=None,
                           logger='bar'):
    logger = proglog.default_bar_logger(logger)

    if write_logfile:
        logfile = open(filename + ".log", 'w+')
    else:
        logfile = None
    logger(message='Moviepy - Writing video %s\n' % filename)
    with FFMPEG_VideoWriter(filename, clip.size, fps, codec = codec,
                            preset=preset, bitrate=bitrate, logfile=logfile,
                            audiofile=audiofile, threads=threads,
                            ffmpeg_params=ffmpeg_params) as writer:

        nframes = int(clip.duration*fps)

        for t, frame in clip.iter_frames(logger=logger, with_times=True,
                                        fps=fps, dtype="uint8"):
            if withmask:
                mask = (255*clip.mask.get_frame(t))
                if mask.dtype != "uint8":
                    mask = mask.astype("uint8")
                frame = np.dstack([frame, mask])

            edit_percent(t, clip.duration)
            writer.write_frame(frame)

    if write_logfile:
        logfile.close()
    logger(message='Moviepy - Done !')


ffmpeg_writer.ffmpeg_write_video = new_ffmpeg_write_video


from moviepy.editor import *


def text_audio_show():
    for i in list_of_letters_and_time_stamps:
        txt_clip = TextClip(i[0], fontsize=80, color='white', stroke_color=TextClip.list('color')[583],
                            stroke_width=3, font='Liberation-Mono')
        txt_clip = txt_clip.set_position((20, 5)).set_start(float(i[1])).set_end(float(i[2]))
        list_of_video_clips.append(txt_clip)
        audio_clip = AudioFileClip("bellgang audio.mp3")
        audio_clip = audio_clip.volumex(0.015)
        audio_clip = audio_clip.set_start(float(i[1])).set_end(float(i[2]) + audio_clip.duration)
        list_of_audio_clips.append(audio_clip)


clip = VideoFileClip(r"Video clip file destination")
clip = clip.subclip(0, 12)
duration = clip.duration
list_of_video_clips.append(clip)
list_of_audio_clips.append(clip.audio)

text_audio_show()

audio_final = CompositeAudioClip(list_of_audio_clips)
video = CompositeVideoClip(list_of_video_clips)
video = video.set_audio(audio_final)
video.write_videofile("Video_clip_name.mp4")
