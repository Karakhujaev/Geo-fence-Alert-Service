# Testing Guide

## Running Tests

```bash
pip install -r requirements-test.txt

make test
# or
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