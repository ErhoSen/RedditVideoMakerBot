from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_USERNAME: str
    REDDIT_PASSWORD: str

    THEME: str = "dark"  # "light"
    OPACITY: Optional[float] = 0.85

    SUBREDDIT = "AskReddit"

    @property
    def theme_cookie_file(self):
        if self.THEME.casefold() == "dark":
            return "./video_creation/data/cookie-dark-mode.json"
        else:
            return "./video_creation/data/cookie-light-mode.json"

    class Config:
        env_file = ".env"


settings = Settings()
