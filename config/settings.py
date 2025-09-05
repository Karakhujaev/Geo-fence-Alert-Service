import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/geofence_db")
    
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    app_name: str = "Geo-fence Alert Service"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"


settings = Settings()