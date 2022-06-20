import praw
from praw.models.comment_forest import CommentForest

from settings import settings


class RedditClient:
    def __init__(self, subreddit: str = "AskReddit"):
        self.reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent="Accessing AskReddit threads",
            username=settings.REDDIT_USERNAME,
            password=settings.REDDIT_PASSWORD
        )
        self.subreddit = self.reddit.subreddit(subreddit)

    def get_subreddit_threads(self):
        return self.subreddit.top(time_filter='month', limit=25)


reddit_client = RedditClient(subreddit=settings.SUBREDDIT)


def choose_the_thread(threads: list) -> dict:
    """Choose a thread from the list of threads."""
    threads_map = {}
    for i, thread in enumerate(threads):
        threads_map[i] = thread
        print(i, thread.title)
    chosen_thread = input("Choose a thread: ")
    return threads_map[int(chosen_thread)]


def choose_the_comments(comments: CommentForest, limit: int = 15) -> dict:
    # filter out MoreComments objects
    comments = filter(lambda x: isinstance(x, praw.models.Comment), comments)
    # sort by score
    sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)
    for i, comment in enumerate(sorted_comments):
        # check if comment is deleted by author
        if comment.author is None:
            continue
        # check if comment is removed by hand
        if comment.body in ('[removed]', '[deleted]'):
            continue
        # check if comment is too long
        if comment.body.count(" ") > 50:
            continue
        # check if we have reached the limit
        if i < limit:
            yield comment
