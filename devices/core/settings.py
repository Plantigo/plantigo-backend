from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Plantigo Devices Service"
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
