Geo-fence Alert Service
A service for monitoring farm equipment locations within predefined geographical boundaries. Tracks device positions and publishes alerts when equipment exits designated areas.
Features

Real-time location monitoring for multiple devices
Circular geofence boundary detection
State tracking to prevent duplicate alerts
Event publishing for fence violations
PostgreSQL with async connection pooling
RESTful API with FastAPI

Quick Start
bashgit clone https://github.com/Karakhujaev/Geo-fence-Alert-Service
cd geofence-alert-service
docker-compose up -d
Service will be available at: http://localhost:8000
Check health: curl http://localhost:8000/health
Architecture
├── models/              # Data models
├── domain/              # Business logic
├── services/            # Service layer
├── repositories/        # Data access
├── database/           # DB management
├── config/             # Configuration
├── api/                # API routes
└── main.py             # Entry point
Documentation

Setup Guide - Installation and configuration
API Documentation - Complete API reference
Testing Guide - Testing and development

Configuration
Environment variables:
DATABASE_URL=postgresql://user:pass@localhost:5432/geofence_db
REDIS_URL=redis://localhost:6379
DEBUG=false
HOST=0.0.0.0
PORT=8000
Sample Usage
bashcurl -X POST "http://localhost:8000/api/v1/location-check" \
     -H "Content-Type: application/json" \
     -d '{"device_id": "tractor_001", "lat": 40.7831, "lon": -73.9712}'
Development Commands
bashmake help          # Show all commands
make setup         # Full development setup
make test          # Run tests with coverage
make docker-up     # Start with Docker