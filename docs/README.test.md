# Testing Guide

## Running Tests

```bash
pip install -r requirements-test.txt

make test
pytest tests/ -v

pytest tests/ -v --cov=. --cov-report=html
```

## Test Files

```
tests/
├── test_geofence_calculator.py  # Distance calculations
├── test_geofence_service.py     # Business logic
└── test_api.py                  # API endpoints
```

## Example Tests

**Unit Test:**
```python
def test_distance_calculation():
    calculator = GeofenceCalculator()
    distance = calculator.calculate_distance_km(
        40.7831, -73.9712,  
        40.7831, -73.9712   
    )
    assert distance == 0.0
```

**API Test:**
```python
@pytest.mark.asyncio
async def test_location_check():
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "/api/v1/location-check",
            json={"device_id": "test", "lat": 40.7831, "lon": -73.9712}
        )
    assert response.status_code == 200
```

## Test Database

```bash
createdb geofence_test_db

export TEST_DATABASE_URL=postgresql://user:pass@localhost:5432/geofence_test_db

pytest tests/
```

## Docker Testing

```bash
docker-compose -f docker-compose.test.yml up -d

pytest tests/ -v

docker-compose -f docker-compose.test.yml down
```

## Test Commands

```bash
pytest tests/test_geofence_calculator.py -v

pytest tests/test_api.py::test_location_check -v

pytest tests/ -k "geofence" -v

pytest tests/ --cov=. --cov-report=term-missing
```

## Writing Tests

**Test Structure:**
```python
import pytest
from unittest.mock import AsyncMock

class TestGeofenceService:
    def setup_method(self):
        self.mock_repository = AsyncMock()
        self.service = GeofenceService(self.mock_repository, ...)
    
    @pytest.mark.asyncio
    async def test_something(self):
```

**Required Packages:**
- pytest
- pytest-asyncio
- httpx
- pytest-mock
- coverage