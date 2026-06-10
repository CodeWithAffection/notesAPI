from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_database_url : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    allowed_origins : list[str]

    class Config():
        env_file = ".env"

settings = Settings()
