# Setup Guide

## Docker Setup (Recommended)

```bash
git clone https://github.com/Karakhujaev/Geo-fence-Alert-Service .
make setup
docker-compose up -d
```

Verify: `curl http://localhost:8000/health`

## Manual Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis (optional)

### Installation

```bash
pip install -r requirements.txt

createdb geofence_db
createuser geofence_user --pwprompt

cp .env.example .env

python main.py
```

### Database Setup

```sql
CREATE DATABASE geofence_db;
CREATE USER geofence_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE geofence_db TO geofence_user;
```

Load sample data:
```bash
psql -U geofence_user -d geofence_db -f migrations/sample_data.sql
```

## Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/geofence_db
REDIS_URL=redis://localhost:6379
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

## Production Deployment

### Docker
```bash
docker build -t geofence-service .
docker run -d -p 8000:8000 -e DATABASE_URL=... geofence-service
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geofence-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: geofence-service
        image: geofence-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://..."
```

## Troubleshooting

**Database connection issues:**
```bash
psql -U geofence_user -d geofence_db -h localhost

sudo systemctl status postgresql
```

**Port conflicts:**
```bash
lsof -i :8000
```