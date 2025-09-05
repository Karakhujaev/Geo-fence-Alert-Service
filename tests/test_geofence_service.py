import pytest
from unittest.mock import AsyncMock, Mock
from services.geofence_service import GeofenceService
from models.geofence import DeviceLocationModel, GeofenceModel, DeviceStateModel


class TestGeofenceService:
    """Test cases for GeofenceService."""
    
    def setup_method(self):
        self.mock_repository = AsyncMock()
        self.mock_calculator = Mock()
        self.mock_event_publisher = AsyncMock()
        
        self.service = GeofenceService(
            self.mock_repository,
            self.mock_calculator,
            self.mock_event_publisher
        )
    
    @pytest.mark.asyncio
    async def test_device_enters_geofence_first_time(self):
        """Test device entering geofence for the first time."""
        location = DeviceLocationModel(
            device_id="test_device", lat=40.7831, lon=-73.9712
        )
        
        geofence = GeofenceModel(
            id=1, name="Test Field", 
            center_lat=40.7831, center_lon=-73.9712, 
            radius_km=2.0
        )
        
        self.mock_repository.get_all_geofences.return_value = [geofence]
        self.mock_repository.get_device_state.return_value = None  # First time
        self.mock_calculator.find_containing_geofence.return_value = geofence
        
        result = await self.service.check_device_location(location)
        
        assert result["device_id"] == "test_device"
        assert result["inside_geofence"] is True
        assert result["geofence_name"] == "Test Field"
        assert result["state_changed"] is True
        
        self.mock_repository.update_device_state.assert_called_once_with(
            "test_device", 40.7831, -73.9712, True, 1
        )
        
        self.mock_event_publisher.publish_geo_event.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_device_exits_geofence(self):
        """Test device exiting geofence triggers event."""
        location = DeviceLocationModel(
            device_id="test_device", lat=41.0, lon=-74.0  
        )
        
        previous_state = DeviceStateModel(
            device_id="test_device",
            last_lat=40.7831,
            last_lon=-73.9712,
            is_inside_fence=True,
            last_geofence_id=1,
            last_updated="2024-01-01T00:00:00Z"
        )
        
        geofence = GeofenceModel(
            id=1, name="Test Field", 
            center_lat=40.7831, center_lon=-73.9712, 
            radius_km=2.0
        )
        
        self.mock_repository.get_all_geofences.return_value = [geofence]
        self.mock_repository.get_device_state.return_value = previous_state
        self.mock_calculator.find_containing_geofence.return_value = None
        
        result = await self.service.check_device_location(location)
        
        assert result["device_id"] == "test_device"
        assert result["inside_geofence"] is False
        assert result["geofence_name"] is None
        assert result["state_changed"] is True
        
        self.mock_event_publisher.publish_geo_event.assert_called_once()
        
        self.mock_repository.update_device_state.assert_called_once_with(
            "test_device", 41.0, -74.0, False, None
        )
    
    @pytest.mark.asyncio
    async def test_device_stays_inside_geofence(self):
        """Test device staying inside same geofence doesn't trigger event."""
        location = DeviceLocationModel(
            device_id="test_device", lat=40.7831, lon=-73.9712
        )
        
        previous_state = DeviceStateModel(
            device_id="test_device",
            last_lat=40.7830,
            last_lon=-73.9710,
            is_inside_fence=True,
            last_geofence_id=1,
            last_updated="2024-01-01T00:00:00Z"
        )
        
        geofence = GeofenceModel(
            id=1, name="Test Field", 
            center_lat=40.7831, center_lon=-73.9712, 
            radius_km=2.0
        )
        
        self.mock_repository.get_all_geofences.return_value = [geofence]
        self.mock_repository.get_device_state.return_value = previous_state
        self.mock_calculator.find_containing_geofence.return_value = geofence
        
        result = await self.service.check_device_location(location)
        
        assert result["device_id"] == "test_device"
        assert result["inside_geofence"] is True
        assert result["geofence_name"] == "Test Field"
        assert result["state_changed"] is False 
        
        self.mock_event_publisher.publish_geo_event.assert_not_called()
        
        self.mock_repository.update_device_state.assert_called_once_with(
            "test_device", 40.7831, -73.9712, True, 1
        )