import json
import logging
from datetime import datetime
from typing import Dict, Any
from abc import ABC, abstractmethod


class EventPublisher(ABC):
    """Abstract base class for event publishing."""
    
    @abstractmethod
    async def publish_geo_event(self, event_data: Dict[str, Any]) -> None:
        """Publish geo-fence event."""
        pass


class GeoEventData:
    """Factory for creating geo-fence event data."""
    
    @staticmethod
    def create_fence_exit_event(
        device_id: str, 
        lat: float, 
        lon: float, 
        geofence_name: str = None
    ) -> Dict[str, Any]:
        return {
            "event_type": "fence_exit",
            "device_id": device_id,
            "latitude": lat,
            "longitude": lon,
            "geofence_name": geofence_name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


class MockEventPublisher(EventPublisher):
    """Mock implementation for testing/development."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def publish_geo_event(self, event_data: Dict[str, Any]) -> None:
        self.logger.info(f"Publishing geo-event: {json.dumps(event_data)}")


class RedisEventPublisher(EventPublisher):
    """Redis-based event publisher implementation."""
    
    def __init__(self, redis_url: str, queue_name: str = "geo-events"):
        self.redis_url = redis_url
        self.queue_name = queue_name
        self.logger = logging.getLogger(__name__)
    
    async def publish_geo_event(self, event_data: Dict[str, Any]) -> None:
        self.logger.info(f"Publishing to Redis queue {self.queue_name}: {json.dumps(event_data)}")