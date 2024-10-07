from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_USER: str  
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    MAIL_USERNAME : str
    MAIL_PASSWORD : str
    MAIL_FROM : str
    MAIL_SERVER : str
    EMAIL_PORT : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    model_config = SettingsConfigDict(env_file=".env")