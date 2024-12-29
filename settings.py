from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    kafka_url: str
    stripe_api_key: str

    model_config = SettingsConfigDict(env_file=".env")