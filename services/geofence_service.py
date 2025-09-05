from typing import Dict, Any
from models.geofence import DeviceLocationModel
from domain.geofence_calculator import GeofenceCalculator
from repositories.geofence_repository import GeofenceRepository
from services.event_publisher import EventPublisher, GeoEventData


class GeofenceService:
    """Main business logic for geofence operations."""
    
    def __init__(
        self, 
        repository: GeofenceRepository,
        calculator: GeofenceCalculator,
        event_publisher: EventPublisher
    ):
        self.repository = repository
        self.calculator = calculator
        self.event_publisher = event_publisher
    
    async def check_device_location(self, location: DeviceLocationModel) -> Dict[str, Any]:
        """Check if device location is within geofences and handle state changes."""
        
        geofences = await self.repository.get_all_geofences()
        device_state = await self.repository.get_device_state(location.device_id)
        
        containing_geofence = self.calculator.find_containing_geofence(location, geofences)
        is_inside = containing_geofence is not None
        
        state_changed = (
            device_state is None or 
            device_state.is_inside_fence != is_inside
        )
        
        if state_changed and device_state and device_state.is_inside_fence and not is_inside:
            await self._publish_fence_exit_event(location, device_state)
        
        geofence_id = containing_geofence.id if containing_geofence else None
        await self.repository.update_device_state(
            location.device_id, 
            location.lat, 
            location.lon, 
            is_inside,
            geofence_id
        )
        
        return {
            "device_id": location.device_id,
            "inside_geofence": is_inside,
            "geofence_name": containing_geofence.name if containing_geofence else None,
            "state_changed": state_changed
        }
    
    async def _publish_fence_exit_event(
        self, 
        location: DeviceLocationModel, 
        previous_state
    ) -> None:
        """Publish fence exit event."""
        geofences = await self.repository.get_all_geofences()
        geofence_name = None
        
        if previous_state.last_geofence_id:
            for gf in geofences:
                if gf.id == previous_state.last_geofence_id:
                    geofence_name = gf.name
                    break
        
        event_data = GeoEventData.create_fence_exit_event(
            location.device_id,
            location.lat,
            location.lon,
            geofence_name
        )
        
        await self.event_publisher.publish_geo_event(event_data)