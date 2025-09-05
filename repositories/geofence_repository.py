import asyncpg
from typing import List, Optional
from models.geofence import GeofenceModel, DeviceStateModel


class GeofenceRepository:
    """Repository for geofence and device state data access."""
    
    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool
    
    async def get_all_geofences(self) -> List[GeofenceModel]:
        """Retrieve all geofences from database."""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, name, center_lat, center_lon, radius_km FROM geofences"
            )
            return [GeofenceModel(**dict(row)) for row in rows]
    
    async def get_device_state(self, device_id: str) -> Optional[DeviceStateModel]:
        """Get the last known state of a device."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT device_id, last_lat, last_lon, is_inside_fence, 
                       last_geofence_id, last_updated
                FROM device_states 
                WHERE device_id = $1
                """,
                device_id
            )
            
            if row:
                return DeviceStateModel(**dict(row))
            return None
    
    async def update_device_state(
        self, 
        device_id: str, 
        lat: float, 
        lon: float, 
        is_inside_fence: bool,
        geofence_id: Optional[int] = None
    ) -> None:
        """Update or insert device state."""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO device_states 
                (device_id, last_lat, last_lon, is_inside_fence, last_geofence_id, last_updated)
                VALUES ($1, $2, $3, $4, $5, NOW())
                ON CONFLICT (device_id) DO UPDATE SET
                    last_lat = EXCLUDED.last_lat,
                    last_lon = EXCLUDED.last_lon,
                    is_inside_fence = EXCLUDED.is_inside_fence,
                    last_geofence_id = EXCLUDED.last_geofence_id,
                    last_updated = EXCLUDED.last_updated
                """,
                device_id, lat, lon, is_inside_fence, geofence_id
            )