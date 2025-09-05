# API Documentation

Base URL: `http://localhost:8000`

## Endpoints

### Check Device Location

**POST** `/api/v1/location-check`

```bash
curl -X POST "http://localhost:8000/api/v1/location-check" \
     -H "Content-Type: application/json" \
     -d '{"device_id": "tractor_001", "lat": 40.7831, "lon": -73.9712}'
```

**Request:**
```json
{
  "device_id": "tractor_001",
  "lat": 40.7831,
  "lon": -73.9712
}
```

**Response:**
```json
{
  "device_id": "tractor_001",
  "inside_geofence": true,
  "geofence_name": "North Field",
  "state_changed": false
}
```

### Health Check

**GET** `/health`
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "geofence-alert-service"
}
```

## Data Validation

- `device_id`: Required string (min length: 1)
- `lat`: Required number (-90 to 90)
- `lon`: Required number (-180 to 180)

## Error Responses

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "lat"],
      "msg": "ensure this value is greater than or equal to -90",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

**500 Server Error:**
```json
{
  "detail": "Internal server error"
}
```

## Events Published

When device exits geofence:
```json
{
  "event_type": "fence_exit",
  "device_id": "tractor_001",
  "latitude": 40.7831,
  "longitude": -73.9712,
  "geofence_name": "North Field",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Database Schema

**Geofences:**
```sql
CREATE TABLE geofences (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    center_lat DECIMAL(10, 8) NOT NULL,
    center_lon DECIMAL(11, 8) NOT NULL,
    radius_km DECIMAL(10, 3) NOT NULL
);
```

**Device States:**
```sql
CREATE TABLE device_states (
    device_id VARCHAR(255) PRIMARY KEY,
    last_lat DECIMAL(10, 8),
    last_lon DECIMAL(11, 8),
    is_inside_fence BOOLEAN DEFAULT FALSE,
    last_geofence_id INTEGER REFERENCES geofences(id)
);
```

## Sample Test Data

```sql
INSERT INTO geofences (name, center_lat, center_lon, radius_km) VALUES
('North Field', 40.7831, -73.9712, 2.5),
('South Field', 40.7489, -73.9857, 1.8),
('Equipment Yard', 40.7614, -73.9776, 0.5);
```

## Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Client Examples

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/location-check",
    json={"device_id": "tractor_001", "lat": 40.7831, "lon": -73.9712}
)
print(response.json())
```

**JavaScript:**
```javascript
fetch('http://localhost:8000/api/v1/location-check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        device_id: 'tractor_001',
        lat: 40.7831,
        lon: -73.9712
    })
}).then(r => r.json()).then(console.log);
```