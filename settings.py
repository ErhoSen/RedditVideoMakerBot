from pydantic import BaseSettings


class Settings(BaseSettings):
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_USERNAME: str
    REDDIT_PASSWORD: str

    THEME = "light"  # "dark"

    SUBREDDIT = "AskReddit"

    class Config:
        env_file = ".env"


settings = Settings()
