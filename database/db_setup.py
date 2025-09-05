import asyncpg
from typing import Optional


class DatabaseManager:
    """Manages database connections and setup."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
    
    async def create_pool(self) -> asyncpg.Pool:
        """Create database connection pool."""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=1,
            max_size=10
        )
        return self.pool
    
    async def close_pool(self) -> None:
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()
    
    async def create_tables(self) -> None:
        """Create required database tables."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS geofences (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    center_lat DECIMAL(10, 8) NOT NULL,
                    center_lon DECIMAL(11, 8) NOT NULL,
                    radius_km DECIMAL(10, 3) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS device_states (
                    device_id VARCHAR(255) PRIMARY KEY,
                    last_lat DECIMAL(10, 8),
                    last_lon DECIMAL(11, 8),
                    is_inside_fence BOOLEAN DEFAULT FALSE,
                    last_geofence_id INTEGER REFERENCES geofences(id),
                    last_updated TIMESTAMP DEFAULT NOW()
                )
            """)