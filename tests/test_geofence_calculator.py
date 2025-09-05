import pytest
from domain.geofence_calculator import GeofenceCalculator
from models.geofence import GeofenceModel, DeviceLocationModel


class TestGeofenceCalculator:
    """Test cases for GeofenceCalculator."""
    
    def setup_method(self):
        self.calculator = GeofenceCalculator()
    
    def test_calculate_distance_same_point(self):
        """Test distance calculation for the same point."""
        distance = self.calculator.calculate_distance_km(
            40.7831, -73.9712, 40.7831, -73.9712
        )
        assert distance == 0.0
    
    def test_calculate_distance_known_points(self):
        """Test distance calculation for known points."""
        distance = self.calculator.calculate_distance_km(
            40.7128, -74.0060, 
            34.0522, -118.2437  
        )
        assert 3900 < distance < 4000
    
    def test_find_containing_geofence_inside(self):
        """Test finding geofence when device is inside."""
        geofences = [
            GeofenceModel(
                id=1, name="Test Field", 
                center_lat=40.7831, center_lon=-73.9712, 
                radius_km=2.0
            )
        ]
        
        location = DeviceLocationModel(
            device_id="test_device",
            lat=40.7831, lon=-73.9712  
        )
        
        result = self.calculator.find_containing_geofence(location, geofences)
        assert result is not None
        assert result.name == "Test Field"
    
    def test_find_containing_geofence_outside(self):
        """Test finding geofence when device is outside."""
        geofences = [
            GeofenceModel(
                id=1, name="Test Field", 
                center_lat=40.7831, center_lon=-73.9712, 
                radius_km=0.1  
            )
        ]
        
        location = DeviceLocationModel(
            device_id="test_device",
            lat=41.0, lon=-74.0  
        )
        
        result = self.calculator.find_containing_geofence(location, geofences)
        assert result is None
    
    def test_find_containing_geofence_multiple(self):
        """Test finding first matching geofence when multiple exist."""
        geofences = [
            GeofenceModel(
                id=1, name="First Field", 
                center_lat=40.7831, center_lon=-73.9712, 
                radius_km=5.0
            ),
            GeofenceModel(
                id=2, name="Second Field", 
                center_lat=40.7831, center_lon=-73.9712, 
                radius_km=10.0
            )
        ]
        
        location = DeviceLocationModel(
            device_id="test_device",
            lat=40.7831, lon=-73.9712
        )
        
        result = self.calculator.find_containing_geofence(location, geofences)
        assert result is not None
        assert result.name == "First Field" 