from typing import List

import sox
from moviepy.audio.fx.volumex import volumex
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    CompositeAudioClip,
    CompositeVideoClip,
)
from moviepy.video.io import ffmpeg_tools

from settings import settings
from utils.console import print_step
from utils.db import Thread

W, H = 1080, 1920


def get_background_audio(duration: int) -> AudioFileClip:
    bg_audio_clip = AudioFileClip("assets/mp3/background.mp3")
    bg_audio_clip = bg_audio_clip.set_duration(duration)
    bg_audio_clip = bg_audio_clip.fx(volumex, 0.4)
    return bg_audio_clip


def generate_image_clip(filename: str, duration: int):
    img_clip = (
        ImageClip(filename)
        .set_duration(duration)
        .set_position("center")
        .resize(width=W - 100)
        .set_opacity(settings.OPACITY)
    )
    return img_clip


def my_concatenate_audioclips(clips: List[AudioFileClip]) -> AudioFileClip:
    cbn = sox.Combiner()
    cbn.set_input_format(["mp3"] * len(clips), rate=[44100] * len(clips), channels=[2] * len(clips))
    cbn.convert(samplerate=44100, n_channels=2, bitdepth=64)
    filenames = [clip.filename for clip in clips]
    cbn.build(filenames, "assets/mp3/final.mp3", "concatenate", input_volumes=[0.8] * len(clips))
    return AudioFileClip("assets/mp3/final.mp3")


def make_final_video(thread: Thread, chosen_comments: list, length: int):
    print_step("Creating the final video...")
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)

    background_clip = (
        VideoFileClip("assets/mp4/clip.mp4")
        .without_audio()
        .resize(height=H)
        .crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    )
    # Gather all audio clips
    audio_clips = [AudioFileClip(f"assets/mp3/title.mp3")]
    for i in range(0, len(chosen_comments)):
        audio_clips.append(AudioFileClip(f"assets/mp3/{i}.mp3"))
    audio_concat = my_concatenate_audioclips(audio_clips)
    bg_audio_clip = get_background_audio(audio_concat.duration)
    audio_composite = CompositeAudioClip([audio_concat, bg_audio_clip])

    # Gather all images
    image_clips = []
    for i in range(0, len(chosen_comments)):
        image_clips.append(
            ImageClip(f"assets/png/comment_{i}.png")
            .set_duration(audio_clips[i + 1].duration)
            .set_position("center")
            .resize(width=W - 100),
        )

    # add title to video
    image_clips = [generate_image_clip("assets/png/title.png", audio_clips[0].duration)]
    for i in range(0, len(chosen_comments)):
        filename = f"assets/png/comment_{i}.png"
        image_clips.append(generate_image_clip(filename, audio_clips[i+1].duration))

    image_concat = concatenate_videoclips(image_clips).set_position(("center", "center"))
    image_concat.audio = audio_composite
    final = CompositeVideoClip([background_clip, image_concat])
    filename = thread.filename
    final.write_videofile(
        "assets/mp4/temp.mp4", fps=30, audio_codec="aac", audio_bitrate="192k"
    )
    ffmpeg_tools.ffmpeg_extract_subclip(
        "assets/mp4/temp.mp4", 0, length, targetname=filename
    )

    return filename
