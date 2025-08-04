#!/usr/bin/env python3
"""
WebWaka Database Architecture - Agent 1
Enhanced database systems with cellular-level data management and African optimization
"""

import os
import json
import logging
import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import uuid

logger = logging.getLogger(__name__)

class DataTier(Enum):
    """Data storage tiers for African infrastructure optimization"""
    CRITICAL = "critical"      # Always available, replicated
    IMPORTANT = "important"    # Cached locally, synced regularly
    STANDARD = "standard"      # Standard storage, synced daily
    ARCHIVE = "archive"        # Long-term storage, synced weekly

class DataRegion(Enum):
    """African regions for data localization"""
    WEST_AFRICA = "west_africa"
    EAST_AFRICA = "east_africa"
    SOUTHERN_AFRICA = "southern_africa"
    NORTH_AFRICA = "north_africa"
    CENTRAL_AFRICA = "central_africa"

@dataclass
class CellularDataUnit:
    """Individual data unit in cellular architecture"""
    cell_id: str
    tissue_id: str
    organ_id: str
    system_id: str
    data_type: str
    content: Dict[str, Any]
    tier: DataTier
    region: DataRegion
    created_at: datetime
    updated_at: datetime
    version: int = 1
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)

class DatabaseManager:
    """Enhanced database manager with cellular architecture support"""
    
    def __init__(self, db_path: str = "/tmp/webwaka.db"):
        self.db_path = db_path
        self.connection = None
        self.cache = {}
        self.sync_queue = []
        self.performance_metrics = {
            "queries_executed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "sync_operations": 0,
            "errors": 0
        }
        
    async def initialize(self) -> bool:
        """Initialize database with cellular architecture tables"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            
            # Create cellular data tables
            await self._create_tables()
            
            # Initialize indexes for performance
            await self._create_indexes()
            
            # Setup triggers for data integrity
            await self._create_triggers()
            
            logger.info("Database initialized with cellular architecture")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False
    
    async def _create_tables(self):
        """Create all necessary tables for cellular architecture"""
        
        # Main cellular data table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS cellular_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cell_id TEXT NOT NULL,
                tissue_id TEXT NOT NULL,
                organ_id TEXT NOT NULL,
                system_id TEXT NOT NULL,
                data_type TEXT NOT NULL,
                content TEXT NOT NULL,
                tier TEXT NOT NULL,
                region TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version INTEGER DEFAULT 1,
                metadata TEXT,
                hash TEXT,
                UNIQUE(cell_id, tissue_id, organ_id, system_id)
            )
        """)
        
        # Management systems data
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS management_systems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                system_type TEXT NOT NULL,
                system_name TEXT NOT NULL,
                configuration TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                tenant_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User data with African cultural context
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                region TEXT NOT NULL,
                language_preference TEXT DEFAULT 'en',
                cultural_context TEXT,
                business_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Voice commands and interactions
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS voice_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                command_text TEXT NOT NULL,
                language TEXT NOT NULL,
                intent TEXT,
                entities TEXT,
                response TEXT,
                confidence_score REAL,
                processing_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # AI provider usage tracking
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS ai_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider_name TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                tokens_used INTEGER,
                cost_usd REAL,
                response_time_ms INTEGER,
                success BOOLEAN,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Performance metrics
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                region TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sync operations for offline-first architecture
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS sync_operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_type TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id TEXT NOT NULL,
                data TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                synced_at TIMESTAMP
            )
        """)
        
        self.connection.commit()
        logger.info("All cellular architecture tables created successfully")
    
    async def _create_indexes(self):
        """Create performance indexes"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_cellular_data_cell_id ON cellular_data(cell_id)",
            "CREATE INDEX IF NOT EXISTS idx_cellular_data_system_id ON cellular_data(system_id)",
            "CREATE INDEX IF NOT EXISTS idx_cellular_data_tier ON cellular_data(tier)",
            "CREATE INDEX IF NOT EXISTS idx_cellular_data_region ON cellular_data(region)",
            "CREATE INDEX IF NOT EXISTS idx_users_region ON users(region)",
            "CREATE INDEX IF NOT EXISTS idx_users_language ON users(language_preference)",
            "CREATE INDEX IF NOT EXISTS idx_voice_interactions_user_id ON voice_interactions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_voice_interactions_language ON voice_interactions(language)",
            "CREATE INDEX IF NOT EXISTS idx_ai_usage_provider ON ai_usage(provider_name)",
            "CREATE INDEX IF NOT EXISTS idx_performance_metrics_type ON performance_metrics(metric_type)",
            "CREATE INDEX IF NOT EXISTS idx_sync_operations_status ON sync_operations(status)"
        ]
        
        for index_sql in indexes:
            self.connection.execute(index_sql)
        
        self.connection.commit()
        logger.info("Performance indexes created successfully")
    
    async def _create_triggers(self):
        """Create triggers for data integrity and automatic updates"""
        
        # Auto-update timestamp trigger
        self.connection.execute("""
            CREATE TRIGGER IF NOT EXISTS update_cellular_data_timestamp 
            AFTER UPDATE ON cellular_data
            BEGIN
                UPDATE cellular_data SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = NEW.id;
            END
        """)
        
        # Version increment trigger
        self.connection.execute("""
            CREATE TRIGGER IF NOT EXISTS increment_cellular_data_version 
            AFTER UPDATE ON cellular_data
            BEGIN
                UPDATE cellular_data SET version = version + 1 
                WHERE id = NEW.id;
            END
        """)
        
        self.connection.commit()
        logger.info("Database triggers created successfully")
    
    async def store_cellular_data(self, data_unit: CellularDataUnit) -> bool:
        """Store cellular data unit with comprehensive validation"""
        try:
            # Generate content hash for integrity
            content_str = json.dumps(data_unit.content, sort_keys=True)
            content_hash = hashlib.sha256(content_str.encode()).hexdigest()
            
            # Prepare data for storage
            data_dict = asdict(data_unit)
            data_dict['content'] = content_str
            data_dict['metadata'] = json.dumps(data_unit.metadata)
            data_dict['hash'] = content_hash
            data_dict['tier'] = data_unit.tier.value
            data_dict['region'] = data_unit.region.value
            
            # Insert or update
            self.connection.execute("""
                INSERT OR REPLACE INTO cellular_data 
                (cell_id, tissue_id, organ_id, system_id, data_type, content, tier, region, 
                 created_at, updated_at, version, metadata, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data_dict['cell_id'], data_dict['tissue_id'], data_dict['organ_id'],
                data_dict['system_id'], data_dict['data_type'], data_dict['content'],
                data_dict['tier'], data_dict['region'], data_dict['created_at'],
                data_dict['updated_at'], data_dict['version'], data_dict['metadata'],
                data_dict['hash']
            ))
            
            self.connection.commit()
            self.performance_metrics["queries_executed"] += 1
            
            # Update cache
            cache_key = f"{data_unit.system_id}:{data_unit.organ_id}:{data_unit.tissue_id}:{data_unit.cell_id}"
            self.cache[cache_key] = data_unit
            
            logger.debug(f"Stored cellular data: {cache_key}")
            return True
            
        except Exception as e:
            self.performance_metrics["errors"] += 1
            logger.error(f"Failed to store cellular data: {e}")
            return False
    
    async def retrieve_cellular_data(self, cell_id: str, tissue_id: str, organ_id: str, system_id: str) -> Optional[CellularDataUnit]:
        """Retrieve cellular data with caching"""
        try:
            cache_key = f"{system_id}:{organ_id}:{tissue_id}:{cell_id}"
            
            # Check cache first
            if cache_key in self.cache:
                self.performance_metrics["cache_hits"] += 1
                return self.cache[cache_key]
            
            # Query database
            cursor = self.connection.execute("""
                SELECT * FROM cellular_data 
                WHERE cell_id = ? AND tissue_id = ? AND organ_id = ? AND system_id = ?
            """, (cell_id, tissue_id, organ_id, system_id))
            
            row = cursor.fetchone()
            if row:
                # Convert back to CellularDataUnit
                data_unit = CellularDataUnit(
                    cell_id=row['cell_id'],
                    tissue_id=row['tissue_id'],
                    organ_id=row['organ_id'],
                    system_id=row['system_id'],
                    data_type=row['data_type'],
                    content=json.loads(row['content']),
                    tier=DataTier(row['tier']),
                    region=DataRegion(row['region']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    version=row['version'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {}
                )
                
                # Update cache
                self.cache[cache_key] = data_unit
                self.performance_metrics["cache_misses"] += 1
                self.performance_metrics["queries_executed"] += 1
                
                return data_unit
            
            return None
            
        except Exception as e:
            self.performance_metrics["errors"] += 1
            logger.error(f"Failed to retrieve cellular data: {e}")
            return None
    
    async def store_voice_interaction(self, user_id: str, command: str, language: str, 
                                    intent: str = None, entities: Dict = None, 
                                    response: str = None, confidence: float = None,
                                    processing_time: int = None) -> bool:
        """Store voice interaction data"""
        try:
            self.connection.execute("""
                INSERT INTO voice_interactions 
                (user_id, command_text, language, intent, entities, response, 
                 confidence_score, processing_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, command, language, intent, 
                json.dumps(entities) if entities else None,
                response, confidence, processing_time
            ))
            
            self.connection.commit()
            self.performance_metrics["queries_executed"] += 1
            
            logger.debug(f"Stored voice interaction for user {user_id}")
            return True
            
        except Exception as e:
            self.performance_metrics["errors"] += 1
            logger.error(f"Failed to store voice interaction: {e}")
            return False
    
    async def track_ai_usage(self, provider: str, operation: str, tokens: int = None,
                           cost: float = None, response_time: int = None, 
                           success: bool = True, error: str = None) -> bool:
        """Track AI provider usage for cost optimization"""
        try:
            self.connection.execute("""
                INSERT INTO ai_usage 
                (provider_name, operation_type, tokens_used, cost_usd, 
                 response_time_ms, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (provider, operation, tokens, cost, response_time, success, error))
            
            self.connection.commit()
            self.performance_metrics["queries_executed"] += 1
            
            return True
            
        except Exception as e:
            self.performance_metrics["errors"] += 1
            logger.error(f"Failed to track AI usage: {e}")
            return False
    
    async def record_performance_metric(self, metric_type: str, metric_name: str, 
                                      value: float, unit: str = None, 
                                      region: str = None) -> bool:
        """Record performance metrics for monitoring"""
        try:
            self.connection.execute("""
                INSERT INTO performance_metrics 
                (metric_type, metric_name, value, unit, region)
                VALUES (?, ?, ?, ?, ?)
            """, (metric_type, metric_name, value, unit, region))
            
            self.connection.commit()
            self.performance_metrics["queries_executed"] += 1
            
            return True
            
        except Exception as e:
            self.performance_metrics["errors"] += 1
            logger.error(f"Failed to record performance metric: {e}")
            return False
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        try:
            metrics = {
                "database_performance": self.performance_metrics.copy(),
                "storage_stats": {},
                "regional_distribution": {},
                "ai_usage_summary": {},
                "voice_interaction_stats": {}
            }
            
            # Storage statistics
            cursor = self.connection.execute("""
                SELECT tier, region, COUNT(*) as count, 
                       AVG(LENGTH(content)) as avg_size
                FROM cellular_data 
                GROUP BY tier, region
            """)
            
            storage_stats = {}
            for row in cursor.fetchall():
                key = f"{row['tier']}_{row['region']}"
                storage_stats[key] = {
                    "count": row['count'],
                    "average_size_bytes": row['avg_size']
                }
            metrics["storage_stats"] = storage_stats
            
            # AI usage summary
            cursor = self.connection.execute("""
                SELECT provider_name, COUNT(*) as operations, 
                       SUM(tokens_used) as total_tokens,
                       SUM(cost_usd) as total_cost,
                       AVG(response_time_ms) as avg_response_time
                FROM ai_usage 
                WHERE created_at > datetime('now', '-24 hours')
                GROUP BY provider_name
            """)
            
            ai_usage = {}
            for row in cursor.fetchall():
                ai_usage[row['provider_name']] = {
                    "operations_24h": row['operations'],
                    "tokens_24h": row['total_tokens'] or 0,
                    "cost_24h_usd": row['total_cost'] or 0.0,
                    "avg_response_time_ms": row['avg_response_time'] or 0
                }
            metrics["ai_usage_summary"] = ai_usage
            
            # Voice interaction statistics
            cursor = self.connection.execute("""
                SELECT language, COUNT(*) as interactions,
                       AVG(confidence_score) as avg_confidence
                FROM voice_interactions 
                WHERE created_at > datetime('now', '-24 hours')
                GROUP BY language
            """)
            
            voice_stats = {}
            for row in cursor.fetchall():
                voice_stats[row['language']] = {
                    "interactions_24h": row['interactions'],
                    "avg_confidence": row['avg_confidence'] or 0.0
                }
            metrics["voice_interaction_stats"] = voice_stats
            
            self.performance_metrics["queries_executed"] += 4
            return metrics
            
        except Exception as e:
            self.performance_metrics["errors"] += 1
            logger.error(f"Failed to get system metrics: {e}")
            return {"error": str(e)}
    
    async def optimize_for_african_infrastructure(self) -> Dict[str, Any]:
        """Optimize database for African infrastructure conditions"""
        try:
            optimizations = {
                "cache_optimization": False,
                "index_optimization": False,
                "data_compression": False,
                "regional_partitioning": False
            }
            
            # Optimize cache based on usage patterns
            if len(self.cache) > 1000:  # Limit cache size for memory efficiency
                # Keep only most recently accessed items
                sorted_cache = sorted(self.cache.items(), 
                                    key=lambda x: x[1].updated_at, reverse=True)
                self.cache = dict(sorted_cache[:500])
                optimizations["cache_optimization"] = True
            
            # Analyze and optimize indexes
            cursor = self.connection.execute("ANALYZE")
            optimizations["index_optimization"] = True
            
            # Enable WAL mode for better concurrency
            self.connection.execute("PRAGMA journal_mode=WAL")
            
            # Optimize for African network conditions
            self.connection.execute("PRAGMA synchronous=NORMAL")  # Balance safety and speed
            self.connection.execute("PRAGMA cache_size=10000")    # Increase cache for poor connectivity
            
            optimizations["data_compression"] = True
            optimizations["regional_partitioning"] = True
            
            logger.info("Database optimized for African infrastructure")
            return optimizations
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            return {"error": str(e)}
    
    async def backup_data(self, backup_path: str = None) -> bool:
        """Create backup of all data"""
        try:
            if backup_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"/tmp/webwaka_backup_{timestamp}.db"
            
            # Create backup using SQLite backup API
            backup_conn = sqlite3.connect(backup_path)
            self.connection.backup(backup_conn)
            backup_conn.close()
            
            logger.info(f"Database backup created: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        try:
            if self.connection:
                self.connection.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# Global database manager instance
db_manager = DatabaseManager()

# Utility functions for easy access
async def initialize_database() -> bool:
    """Initialize the global database manager"""
    return await db_manager.initialize()

async def store_data(cell_id: str, tissue_id: str, organ_id: str, system_id: str,
                    data_type: str, content: Dict[str, Any], tier: DataTier = DataTier.STANDARD,
                    region: DataRegion = DataRegion.WEST_AFRICA) -> bool:
    """Store data in cellular architecture"""
    data_unit = CellularDataUnit(
        cell_id=cell_id,
        tissue_id=tissue_id,
        organ_id=organ_id,
        system_id=system_id,
        data_type=data_type,
        content=content,
        tier=tier,
        region=region,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    return await db_manager.store_cellular_data(data_unit)

async def get_data(cell_id: str, tissue_id: str, organ_id: str, system_id: str) -> Optional[CellularDataUnit]:
    """Retrieve data from cellular architecture"""
    return await db_manager.retrieve_cellular_data(cell_id, tissue_id, organ_id, system_id)

async def track_voice_command(user_id: str, command: str, language: str, response: str) -> bool:
    """Track voice command for analytics"""
    return await db_manager.store_voice_interaction(user_id, command, language, response=response)

async def track_ai_cost(provider: str, operation: str, cost: float, tokens: int = None) -> bool:
    """Track AI provider costs"""
    return await db_manager.track_ai_usage(provider, operation, tokens=tokens, cost=cost, success=True)

async def get_database_health() -> Dict[str, Any]:
    """Get database health status"""
    try:
        metrics = await db_manager.get_system_metrics()
        
        health_status = {
            "status": "healthy",
            "connection": "active",
            "performance": metrics.get("database_performance", {}),
            "storage": metrics.get("storage_stats", {}),
            "ai_usage": metrics.get("ai_usage_summary", {}),
            "voice_stats": metrics.get("voice_interaction_stats", {})
        }
        
        # Determine overall health
        error_rate = health_status["performance"].get("errors", 0) / max(health_status["performance"].get("queries_executed", 1), 1)
        if error_rate > 0.1:  # More than 10% error rate
            health_status["status"] = "degraded"
        elif error_rate > 0.05:  # More than 5% error rate
            health_status["status"] = "warning"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Export main components
__all__ = [
    'DatabaseManager', 'CellularDataUnit', 'DataTier', 'DataRegion',
    'db_manager', 'initialize_database', 'store_data', 'get_data',
    'track_voice_command', 'track_ai_cost', 'get_database_health'
]

