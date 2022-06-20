#!/usr/bin/env python3
import time

import typer

from reddit.subreddit import get_subreddit_threads, collect_subreddit_threads
from utils.console import print_markdown
from utils.db import create_db_and_tables, get_db_threads, get_db_comments, save_object
from video_creation.background import download_background, chop_background_video, Background
from video_creation.final_video import make_final_video
from video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation.voices import save_text_to_mp3

app = typer.Typer()


def _process_thread(thread, comments, _background: Background) -> str:
    print_markdown("Processing thread: {}".format(thread.title))
    chosen_comments, length = save_text_to_mp3(thread, comments)
    download_screenshots_of_reddit_posts(thread, chosen_comments)
    download_background(_background)
    chop_background_video(_background, length)
    filename = make_final_video(thread, chosen_comments, length)
    return filename


@app.command()
def run():
    print_markdown(
        "### Thanks for using this tool! [Feel free to contribute to this project on GitHub!](https://lewismenelaws.com)"
        " If you have any questions, feel free to reach out to me on Twitter or submit a GitHub issue."
    )

    time.sleep(3)

    thread, comments = get_subreddit_threads()
    _background = Background.choose()
    filename = _process_thread(thread, comments, _background)
    print_markdown(f"Video saved to: {filename}")


@app.command()
def collect():
    print_markdown('### Collecting data from reddit...')
    collect_subreddit_threads()


@app.command()
def process():
    print_markdown('### Processing collected data...')
    threads = get_db_threads()
    for thread in threads:
        comments = get_db_comments(thread.id)
        _background = Background.random()
        try:
            filename = _process_thread(thread, comments, _background)
        except Exception as e:
            print_markdown(f"Error processing thread {thread.title}: {e}")
        else:
            print_markdown(f'### Video created: {filename}')
            thread.tiktok = filename
            thread.is_processed = True
            save_object(thread)

    print_markdown('### Done!')


if __name__ == "__main__":
    create_db_and_tables()
    app()
