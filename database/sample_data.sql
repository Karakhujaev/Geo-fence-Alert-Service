INSERT INTO geofences (name, center_lat, center_lon, radius_km) VALUES
('North Field', 40.7831, -73.9712, 2.5),
('South Field', 40.7489, -73.9857, 1.8),
('Equipment Yard', 40.7614, -73.9776, 0.5),
('Warehouse Area', 40.7505, -73.9934, 1.0),
('Maintenance Zone', 40.7580, -73.9855, 0.3);

INSERT INTO device_states (device_id, last_lat, last_lon, is_inside_fence, last_geofence_id) VALUES
('tractor_001', 40.7831, -73.9712, true, 1),
('plough_002', 40.7489, -73.9857, true, 2),
('harvester_003', 40.8000, -74.0000, false, null);