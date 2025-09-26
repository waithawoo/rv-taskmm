from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import List

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class Settings(BaseSettings):
    REDIS_URL: str = 'redis://localhost:6379' # redis://:password@host:port
    
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    JWT_SECRET: str
    JWT_ALGORITHM: str
    
    CORS_ALLOWED_ORIGINS: str = "*"
    CORS_ALLOWED_METHODS: str = "*"
    CORS_ALLOWED_HEADERS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = True
    
    TRUSTED_HOSTS: str = "*"
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    @property
    def cors_allowed_origins(self) -> List[str]:
        if self.CORS_ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]
    
    @property
    def cors_allowed_methods(self) -> List[str]:
        if self.CORS_ALLOWED_METHODS == "*":
            return ["*"]
        return [method.strip() for method in self.CORS_ALLOWED_METHODS.split(",")]
    
    @property
    def cors_allowed_headers(self) -> List[str]:
        if self.CORS_ALLOWED_HEADERS == "*":
            return ["*"]
        return [header.strip() for header in self.CORS_ALLOWED_HEADERS.split(",")]
    
    @property
    def trusted_hosts(self) -> List[str]:
        if self.TRUSTED_HOSTS == "*":
            return ["*"]
        return [host.strip() for host in self.TRUSTED_HOSTS.split(",")]

Config = Settings()
