from pathlib import Path

from mutagen.mp3 import MP3
from rich.progress import track

from utils.console import print_step, print_substep
from utils.db import Comment
from utils.text_to_speech import tts_client


def save_text_to_mp3(thread_title: str, comments: list[Comment]):
    print_step("Saving Text to MP3 files...")
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    audio_content = tts_client.get_audio(thread_title)
    with open("assets/mp3/title.mp3", "wb") as f:
        f.write(audio_content)
    length += MP3(f"assets/mp3/title.mp3").info.length

    chosen_comments = []
    for idx, comment in track(enumerate(comments), "Saving..."):
        # ! Stop creating mp3 files if the length is greater than 50 seconds.
        # This can be longer, but this is just a good starting point
        if length > 50:
            break
        audio_content = tts_client.get_audio(comment.body)
        with open(f"assets/mp3/{idx}.mp3", "wb") as f:
            f.write(audio_content)
        length += MP3(f"assets/mp3/{idx}.mp3").info.length
        chosen_comments.append(comment)

    print_substep("Saved Text to MP3 files successfully.", style="bold green")
    return chosen_comments, length
