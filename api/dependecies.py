from fastapi import HTTPException
from domain.geofence_calculator import GeofenceCalculator
from repositories.geofence_repository import GeofenceRepository
from services.geofence_service import GeofenceService
from services.event_publisher import MockEventPublisher


geofence_calculator = GeofenceCalculator()
event_publisher = MockEventPublisher()


def get_geofence_service(db_pool) -> GeofenceService:
    """Dependency injection for GeofenceService."""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    repository = GeofenceRepository(db_pool)
    return GeofenceService(repository, geofence_calculator, event_publisher)