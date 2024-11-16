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
    iot_collection_name: str = "telemetry"
    max_grpc_workers: int = 10
    use_tls: bool = False
    tls_cert_path: str = "server.crt"
    tls_key_path: str = "server.key"


settings = Settings()
