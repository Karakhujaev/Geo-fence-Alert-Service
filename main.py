import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from config.settings import settings
from database.db_setup import DatabaseManager
from api.dependencies import get_geofence_service
from api.routers import location, health
from services.geofence_service import GeofenceService

db_manager = DatabaseManager(settings.database_url)

logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await db_manager.create_pool()
    await db_manager.create_tables()
    logger.info("Database initialized successfully")
    
    yield
    
    await db_manager.close_pool()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.app_name,
        description="Service for monitoring device locations within geo-fenced areas",
        version=settings.app_version,
        lifespan=lifespan,
        debug=settings.debug
    )
    
    def get_service() -> GeofenceService:
        return get_geofence_service(db_manager.pool)
    
    location.router.dependencies = [Depends(get_service)]
    
    app.include_router(health.router)
    app.include_router(location.router)
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )