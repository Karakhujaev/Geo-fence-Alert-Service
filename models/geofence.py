from typing import Optional
from pydantic import BaseModel, Field


class GeofenceModel(BaseModel):
    """Model representing a geofence boundary."""
    id: int
    name: str
    center_lat: float = Field(..., ge=-90, le=90)
    center_lon: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(..., gt=0)


class DeviceLocationModel(BaseModel):
    """Model for device location data."""
    device_id: str = Field(..., min_length=1)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class DeviceStateModel(BaseModel):
    """Model representing device's last known state."""
    device_id: str
    last_lat: Optional[float]
    last_lon: Optional[float]
    is_inside_fence: bool
    last_geofence_id: Optional[int]
    last_updated: Optional[str]