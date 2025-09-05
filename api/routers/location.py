import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from models.geofence import DeviceLocationModel
from services.geofence_service import GeofenceService


router = APIRouter(prefix="/api/v1", tags=["location"])
logger = logging.getLogger(__name__)


@router.post("/location-check", response_model=Dict[str, Any])
async def check_location(
    location: DeviceLocationModel,
    service: GeofenceService = Depends() 
) -> Dict[str, Any]:
    """Check if device location is within any geofence."""
    try:
        result = await service.check_device_location(location)
        logger.info(f"Location check completed for device {location.device_id}")
        return result
    except Exception as e:
        logger.error(f"Error checking location for device {location.device_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")