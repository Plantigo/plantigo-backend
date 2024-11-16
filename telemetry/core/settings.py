from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Telemetry Plantigo Service"
    database_url: str
    database_name: str
    jwt_secret_key: str = ''
    jwt_algorithm: str = "HS256"
    app_host: str = "[::]"
    app_port: int = 50051
    debug: bool = True
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
