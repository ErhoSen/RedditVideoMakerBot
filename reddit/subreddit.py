from sqlalchemy.exc import IntegrityError

from utils.console import print_substep
from utils.db import save_thread, Thread, Comment
from utils.reddit import reddit_client, choose_the_thread, choose_the_comments


def get_subreddit_threads():
    """
    Returns a list of threads from the AskReddit subreddit.
    """
    threads = reddit_client.get_subreddit_threads()
    submission = choose_the_thread(threads)

    print_substep(f"Video will be: {submission.title} :thumbsup:")
    thread = Thread(
        id=submission.id,
        title=submission.title,
        url=submission.url,
    )
    comments = []
    for top_level_comment in choose_the_comments(submission.comments):
        try:
            comments.append(
                Comment(id=top_level_comment.id, body=top_level_comment.body, permalink=top_level_comment.permalink)
            )
        except AttributeError:
            continue

    print_substep("Received AskReddit threads successfully.", style="bold green")

    return thread, comments


def collect_subreddit_threads():
    """
    Returns a list of threads from the AskReddit subreddit.
    """
    content = {}

    raw_threads = reddit_client.get_subreddit_threads()

    for raw_thread in raw_threads:
        try:
            thread = save_thread(raw_thread)
        except IntegrityError:
            print_substep(f"Thread {raw_thread.id} already exists.", style="bold red")
        else:
            print_substep(f"Thread saved into db: {thread.title}")

    print_substep("Received AskReddit threads successfully.", style="bold green")

    return content
