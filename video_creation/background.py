import random
from enum import Enum
from pathlib import Path
from random import randrange

from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from yt_dlp import YoutubeDL

from utils.console import print_step, print_substep


class Background(str, Enum):
    minecraft1 = "https://www.youtube.com/watch?v=n_Dv4JMiwK8"
    trackmania1 = "https://www.youtube.com/watch?v=c529EEYdDVg"
    trackmania2 = "https://www.youtube.com/watch?v=m7T6pRwxOk4"

    @property
    def filename(self):
        return f"assets/mp4/bg_{self.name}.mp4"

    @property
    def url(self):
        return self.value

    @classmethod
    def random(cls) -> 'Background':
        return random.choice(list(cls))

    @classmethod
    def choose(cls) -> 'Background':
        print_step("Choosing a background...")
        background_map = {}
        for i, background in enumerate(cls):
            background_map[i] = background
            print(f"{i} {background.name} - {background.url}")
        background_index = int(input("Choose a background: "))
        background = background_map[background_index]
        print_substep(f"Background chosen: {background.name} :thumbsup:", style="bold green")
        return background


def get_start_and_end_times(video_length, length_of_clip):
    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length


def download_background(background: Background):
    if not Path(background.filename).is_file():
        print_step(
            "We need to download the background video. This is fairly large but it's only done once."
        )

        print_substep("Downloading the background video... please be patient.")

        ydl_opts = {
            "outtmpl": background.filename,
            "merge_output_format": "mp4",
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(background.url)

        print_substep("Background video downloaded successfully!", style="bold green")
    else:
        print_substep(f"Background video {background.name} already downloaded.", style="bold green")


def chop_background_video(_background: Background, video_length):
    print_step("Finding a spot in the background video to chop...")
    background = VideoFileClip(_background.filename)

    start_time, end_time = get_start_and_end_times(video_length, background.duration)
    ffmpeg_extract_subclip(
        _background.filename,
        start_time,
        end_time,
        targetname="assets/mp4/clip.mp4",
    )
    print_substep("Background video chopped successfully!", style="bold green")
