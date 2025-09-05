import math
from typing import List
from models.geofence import GeofenceModel, DeviceLocationModel


class GeofenceCalculator:
    """Handles geofence calculations using Haversine formula."""
    
    @staticmethod
    def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula."""
        earth_radius_km = 6371.0
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return earth_radius_km * c
    
    def find_containing_geofence(
        self, 
        location: DeviceLocationModel, 
        geofences: List[GeofenceModel]
    ) -> GeofenceModel | None:
        """Find the first geofence that contains the given location."""
        for geofence in geofences:
            distance = self.calculate_distance_km(
                location.lat, location.lon,
                geofence.center_lat, geofence.center_lon
            )
            
            if distance <= geofence.radius_km:
                return geofence
                
        return None