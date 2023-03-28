import random
import proglog
from moviepy.video.io import ffmpeg_writer
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter


list_of_clips = []
time_stamps = []


def firestore_percent(tt):
    print(str(int((tt/video.duration)*100)) + " %")


def new_ffmpeg_write_video(clip, filename, fps, codec="libx264", bitrate=None,
                           preset="medium", withmask=False, write_logfile=False,
                           audiofile=None, verbose=True, threads=None, ffmpeg_params=None,
                           logger='bar'):
    """ Write the clip to a videofile. See VideoClip.write_videofile for details
    on the parameters.
    """
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

        for t,frame in clip.iter_frames(logger=logger, with_times=True,
                                        fps=fps, dtype="uint8"):
            if withmask:
                mask = (255*clip.mask.get_frame(t))
                if mask.dtype != "uint8":
                    mask = mask.astype("uint8")
                frame = np.dstack([frame,mask])

            firestore_percent(t)
            writer.write_frame(frame)

    if write_logfile:
        logfile.close()
    logger(message='Moviepy - Done !')


ffmpeg_writer.ffmpeg_write_video = new_ffmpeg_write_video


from moviepy.editor import *


def text_time_stamps(duration_of_video):
    local_time_stamps = []
    if 3 <= duration_of_video <= 6:
        local_time_stamps.append(0)
        local_time_stamps.append(1)
        local_time_stamps.append(2)
    elif 6 < duration_of_video <= 60:
        choice_maker = duration_of_video/3
        local_time_stamps.append(random.randint(0, 1))
        local_time_stamps.append(choice_maker + 1)
        local_time_stamps.append((choice_maker * 2) + 1)
    else:
        choice_maker = int(duration_of_video / 5)
        local_time_stamps.append(random.randint(0, choice_maker - 5))
        for i in range(1, 5):
            local_time_stamps.append(random.randint(i * choice_maker, ((i + 1) * choice_maker) - 5))
        if local_time_stamps[0] >= 10:
            local_time_stamps.pop(0)
            local_time_stamps.insert(0, random.randint(0, 9))
    for i in local_time_stamps:
        time_stamps.append(i)


def helper_text(local_time_stamps, duration_of_video):
    if 3 <= duration_of_video <= 10:
        text_duration = 2
    else:
        text_duration = 5
    txt_clip = TextClip("Text to show on the video", font='Liberation-Mono',
                        fontsize=15, color='white', bg_color=TextClip.list('color')[583])
    txt_clip = txt_clip.set_position((130, 20)).set_start(local_time_stamps[0]).set_end(local_time_stamps[0] + text_duration)
    list_of_clips.append(txt_clip)


def text_clip_show(local_time_stamps, local_list_of_letters, duration_of_video):
    text_duration = 0
    if duration_of_video < 3:
        text_duration = 0.5
    elif 3 <= duration_of_video <= 6:
        text_duration = 1
    elif 6 < duration_of_video <= 60:
        text_duration = 2
    elif 60 < duration_of_video:
        text_duration = 5
    for i in range(0, len(local_list_of_letters)):
        txt_clip = TextClip(local_list_of_letters[i], fontsize=120, color='white', stroke_color=TextClip.list('color')[583],
                            stroke_width=4, font='Liberation-Mono')
        txt_clip = txt_clip.set_position((50, 20)).set_start(local_time_stamps[i]).set_end(local_time_stamps[i] + text_duration)
        list_of_clips.append(txt_clip)


def moviepy(upload_file_name_with_path, edited_file_name_with_path):
    clip = VideoFileClip(upload_file_name_with_path)
    list_of_clips.append(clip)
    duration = clip.duration
    list_of_words = firestore.words_array_return(duration)
    word = random.choice(list_of_words)
    list_of_letters = list(word)

    text_time_stamps(duration)
    helper_text(time_stamps, duration)
    text_clip_show(time_stamps, list_of_letters, duration)

    video = CompositeVideoClip(list_of_clips)
    video.write_videofile(edited_file_name_with_path)
    return list_of_words, word