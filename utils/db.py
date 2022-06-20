from typing import List

from slugify import slugify
from sqlalchemy import create_engine, Column, TEXT
from sqlmodel import Field, SQLModel, Session, Relationship, select

from utils.reddit import choose_the_comments
from utils.voice import sanitize_text


class Thread(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str = Field(sa_column=Column(TEXT))
    url: str
    is_processed: bool = False
    is_published: bool = False
    tiktok: str = None

    comments: List["Comment"] = Relationship(back_populates="thread")

    @property
    def filename(self):
        slug = slugify(self.title, max_length=50, word_boundary=True)
        return f"assets/out/{slug}.mp4"

    @property
    def sanitized_text(self):
        return sanitize_text(self.title)


class Comment(SQLModel, table=True):
    id: str = Field(primary_key=True)
    body: str = Field(sa_column=Column(TEXT))
    permalink: str
    score: int

    thread_id: str = Field(foreign_key='thread.id')
    thread: Thread = Relationship(back_populates="comments")

    @property
    def sanitized_text(self):
        return sanitize_text(self.body)


engine = create_engine("sqlite:///video_creation/data/reddit.sqlite3")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def save_thread(raw_thread: dict) -> Thread:
    with Session(engine) as session:
        comments = []
        for comment in choose_the_comments(raw_thread.comments):
            try:
                comments.append(Comment(
                    id=comment.id,
                    body=comment.body,
                    permalink=comment.permalink,
                    score=comment.score,
                ))
            except AttributeError:
                pass

        thread = Thread(
            id=raw_thread.id,
            title=raw_thread.title,
            url=raw_thread.url,
            comments=comments
        )

        session.add(thread)
        session.commit()
        session.refresh(thread)

    return thread


def _get_collection(statement, limit=None, offset=None):
    with Session(engine) as session:
        results = session.exec(statement)
        return results.all()


def get_db_threads():
    statement = select(Thread).where(Thread.is_processed == False)
    return _get_collection(statement)


def get_db_comments(thread_id):
    statement = select(Comment).where(Comment.thread_id == thread_id).order_by(Comment.score.desc())
    return _get_collection(statement)


def save_object(obj):
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
