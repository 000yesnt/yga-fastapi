import os

from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    app_mode: str = "DEBUG"
    db_url: str = "sqlite:///./sql_app.db"
    secret_key: str

    class Config:
        env_file = os.environ.get('envfile', '.env.debug')


settings = Settings()