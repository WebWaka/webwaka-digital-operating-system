"""
WebWaka Enhanced Cellular Architecture Core System
Biological-inspired modular architecture with standardized interfaces
"""

import json
import uuid
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable, TypeVar, Generic
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type definitions
T = TypeVar('T')
CellData = Dict[str, Any]
TissueData = Dict[str, Any]
OrganData = Dict[str, Any]

class CellularStatus(Enum):
    """Cellular component status types"""
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PROCESSING = "processing"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    DEGRADED = "degraded"

class ConnectionType(Enum):
    """Connection types between cellular components"""
    TISSUE_INTERNAL = "tissue_internal"
    CROSS_TISSUE = "cross_tissue"
    ORGAN_INTERNAL = "organ_internal"
    CROSS_ORGAN = "cross_organ"
    SYSTEM_EXTERNAL = "system_external"

class CellularPriority(Enum):
    """Priority levels for cellular operations"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class CellularMetrics:
    """Metrics for cellular component performance"""
    cell_id: str
    status: CellularStatus
    last_activity: datetime
    processing_time_avg: float
    error_count: int
    success_count: int
    memory_usage: float
    cpu_usage: float
    connection_count: int
    data_throughput: float
    uptime_percentage: float
    
    def calculate_health_score(self) -> float:
        """Calculate overall health score (0-100)"""
        if self.success_count + self.error_count == 0:
            return 100.0
        
        success_rate = self.success_count / (self.success_count + self.error_count)
        performance_score = min(100.0, (1000.0 / max(self.processing_time_avg, 1.0)))
        resource_score = max(0.0, 100.0 - (self.memory_usage + self.cpu_usage))
        
        return (success_rate * 40 + performance_score * 30 + resource_score * 20 + self.uptime_percentage * 10)

@dataclass
class CellularConnection:
    """Connection between cellular components"""
    source_cell: str
    target_cell: str
    connection_type: ConnectionType
    strength: float  # 0.0 to 1.0
    bandwidth: float
    latency: float
    is_bidirectional: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_used: datetime = field(default_factory=datetime.now)

class CellularInterface(ABC):
    """Abstract base class for all cellular components"""
    
    def __init__(self, cell_id: str, cell_type: str, config: Dict[str, Any] = None):
        self.cell_id = cell_id
        self.cell_type = cell_type
        self.config = config or {}
        self.status = CellularStatus.INACTIVE
        self.metrics = CellularMetrics(
            cell_id=cell_id,
            status=self.status,
            last_activity=datetime.now(),
            processing_time_avg=0.0,
            error_count=0,
            success_count=0,
            memory_usage=0.0,
            cpu_usage=0.0,
            connection_count=0,
            data_throughput=0.0,
            uptime_percentage=100.0
        )
        self.connections: Dict[str, CellularConnection] = {}
        self.data_store: Dict[str, Any] = {}
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.created_at = datetime.now()
        self.last_error: Optional[Exception] = None
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the cellular component"""
        pass
    
    @abstractmethod
    async def process(self, data: CellData) -> CellData:
        """Process data through the cellular component"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the cellular component gracefully"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities this cell provides"""
        pass
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Get list of dependencies this cell requires"""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the cellular component"""
        try:
            health_score = self.metrics.calculate_health_score()
            return {
                "cell_id": self.cell_id,
                "status": self.status.value,
                "health_score": health_score,
                "last_activity": self.metrics.last_activity.isoformat(),
                "uptime": (datetime.now() - self.created_at).total_seconds(),
                "error_count": self.metrics.error_count,
                "success_count": self.metrics.success_count,
                "connection_count": len(self.connections),
                "is_healthy": health_score > 70.0 and self.status == CellularStatus.ACTIVE
            }
        except Exception as e:
            logger.error(f"Health check failed for cell {self.cell_id}: {e}")
            return {
                "cell_id": self.cell_id,
                "status": "error",
                "health_score": 0.0,
                "is_healthy": False,
                "error": str(e)
            }
    
    def add_connection(self, connection: CellularConnection):
        """Add connection to another cellular component"""
        self.connections[connection.target_cell] = connection
        self.metrics.connection_count = len(self.connections)
        self.emit_event("connection_added", {"connection": connection})
    
    def remove_connection(self, target_cell_id: str):
        """Remove connection to another cellular component"""
        if target_cell_id in self.connections:
            connection = self.connections.pop(target_cell_id)
            self.metrics.connection_count = len(self.connections)
            self.emit_event("connection_removed", {"connection": connection})
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to registered handlers"""
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(self.cell_id, event_type, data)
            except Exception as e:
                logger.error(f"Event handler error in cell {self.cell_id}: {e}")
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register event handler"""
        self.event_handlers[event_type].append(handler)
    
    def update_metrics(self, processing_time: float = None, success: bool = True):
        """Update cellular metrics"""
        self.metrics.last_activity = datetime.now()
        
        if processing_time is not None:
            # Update average processing time
            total_operations = self.metrics.success_count + self.metrics.error_count
            if total_operations > 0:
                self.metrics.processing_time_avg = (
                    (self.metrics.processing_time_avg * total_operations + processing_time) / 
                    (total_operations + 1)
                )
            else:
                self.metrics.processing_time_avg = processing_time
        
        if success:
            self.metrics.success_count += 1
        else:
            self.metrics.error_count += 1
        
        # Calculate uptime percentage
        total_time = (datetime.now() - self.created_at).total_seconds()
        if total_time > 0:
            active_time = total_time - (self.metrics.error_count * 60)  # Assume 1 minute downtime per error
            self.metrics.uptime_percentage = max(0.0, min(100.0, (active_time / total_time) * 100))

class TissueInterface(ABC):
    """Abstract base class for tissue-level components"""
    
    def __init__(self, tissue_id: str, tissue_type: str, config: Dict[str, Any] = None):
        self.tissue_id = tissue_id
        self.tissue_type = tissue_type
        self.config = config or {}
        self.cells: Dict[str, CellularInterface] = {}
        self.status = CellularStatus.INACTIVE
        self.created_at = datetime.now()
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the tissue component"""
        pass
    
    @abstractmethod
    async def coordinate_cells(self, operation: str, data: TissueData) -> TissueData:
        """Coordinate operations across cells in the tissue"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the tissue component gracefully"""
        pass
    
    def add_cell(self, cell: CellularInterface):
        """Add cell to tissue"""
        self.cells[cell.cell_id] = cell
        cell.register_event_handler("status_change", self._handle_cell_status_change)
        self.emit_event("cell_added", {"cell_id": cell.cell_id})
    
    def remove_cell(self, cell_id: str):
        """Remove cell from tissue"""
        if cell_id in self.cells:
            cell = self.cells.pop(cell_id)
            self.emit_event("cell_removed", {"cell_id": cell_id})
    
    def get_cell(self, cell_id: str) -> Optional[CellularInterface]:
        """Get cell by ID"""
        return self.cells.get(cell_id)
    
    def _handle_cell_status_change(self, cell_id: str, event_type: str, data: Dict[str, Any]):
        """Handle cell status changes"""
        self.emit_event("cell_status_change", {"cell_id": cell_id, "data": data})
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to registered handlers"""
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(self.tissue_id, event_type, data)
            except Exception as e:
                logger.error(f"Event handler error in tissue {self.tissue_id}: {e}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on tissue and all cells"""
        cell_health = {}
        healthy_cells = 0
        total_cells = len(self.cells)
        
        for cell_id, cell in self.cells.items():
            health = await cell.health_check()
            cell_health[cell_id] = health
            if health.get("is_healthy", False):
                healthy_cells += 1
        
        tissue_health_score = (healthy_cells / max(total_cells, 1)) * 100
        
        return {
            "tissue_id": self.tissue_id,
            "status": self.status.value,
            "health_score": tissue_health_score,
            "healthy_cells": healthy_cells,
            "total_cells": total_cells,
            "cell_health": cell_health,
            "is_healthy": tissue_health_score > 70.0 and self.status == CellularStatus.ACTIVE
        }

class OrganInterface(ABC):
    """Abstract base class for organ-level components"""
    
    def __init__(self, organ_id: str, organ_type: str, config: Dict[str, Any] = None):
        self.organ_id = organ_id
        self.organ_type = organ_type
        self.config = config or {}
        self.tissues: Dict[str, TissueInterface] = {}
        self.status = CellularStatus.INACTIVE
        self.created_at = datetime.now()
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the organ component"""
        pass
    
    @abstractmethod
    async def orchestrate_tissues(self, operation: str, data: OrganData) -> OrganData:
        """Orchestrate operations across tissues in the organ"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the organ component gracefully"""
        pass
    
    def add_tissue(self, tissue: TissueInterface):
        """Add tissue to organ"""
        self.tissues[tissue.tissue_id] = tissue
        tissue.register_event_handler("status_change", self._handle_tissue_status_change)
        self.emit_event("tissue_added", {"tissue_id": tissue.tissue_id})
    
    def remove_tissue(self, tissue_id: str):
        """Remove tissue from organ"""
        if tissue_id in self.tissues:
            tissue = self.tissues.pop(tissue_id)
            self.emit_event("tissue_removed", {"tissue_id": tissue_id})
    
    def get_tissue(self, tissue_id: str) -> Optional[TissueInterface]:
        """Get tissue by ID"""
        return self.tissues.get(tissue_id)
    
    def _handle_tissue_status_change(self, tissue_id: str, event_type: str, data: Dict[str, Any]):
        """Handle tissue status changes"""
        self.emit_event("tissue_status_change", {"tissue_id": tissue_id, "data": data})
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to registered handlers"""
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(self.organ_id, event_type, data)
            except Exception as e:
                logger.error(f"Event handler error in organ {self.organ_id}: {e}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on organ and all tissues"""
        tissue_health = {}
        healthy_tissues = 0
        total_tissues = len(self.tissues)
        
        for tissue_id, tissue in self.tissues.items():
            health = await tissue.health_check()
            tissue_health[tissue_id] = health
            if health.get("is_healthy", False):
                healthy_tissues += 1
        
        organ_health_score = (healthy_tissues / max(total_tissues, 1)) * 100
        
        return {
            "organ_id": self.organ_id,
            "status": self.status.value,
            "health_score": organ_health_score,
            "healthy_tissues": healthy_tissues,
            "total_tissues": total_tissues,
            "tissue_health": tissue_health,
            "is_healthy": organ_health_score > 70.0 and self.status == CellularStatus.ACTIVE
        }

class CellularArchitectureManager:
    """Enhanced Cellular Architecture Manager with comprehensive orchestration"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.cells: Dict[str, CellularInterface] = {}
        self.tissues: Dict[str, TissueInterface] = {}
        self.organs: Dict[str, OrganInterface] = {}
        self.connections: Dict[str, List[CellularConnection]] = defaultdict(list)
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.is_running = False
        self.health_monitor_task: Optional[asyncio.Task] = None
        
    async def initialize(self) -> bool:
        """Initialize the cellular architecture manager"""
        try:
            logger.info("Initializing Cellular Architecture Manager")
            self.is_running = True
            
            # Start health monitoring
            self.health_monitor_task = asyncio.create_task(self._health_monitor_loop())
            
            # Initialize all organs
            for organ in self.organs.values():
                await organ.initialize()
            
            # Initialize all tissues
            for tissue in self.tissues.values():
                await tissue.initialize()
            
            # Initialize all cells
            for cell in self.cells.values():
                await cell.initialize()
            
            logger.info("Cellular Architecture Manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Cellular Architecture Manager: {e}")
            return False
    
    async def shutdown(self) -> bool:
        """Shutdown the cellular architecture manager gracefully"""
        try:
            logger.info("Shutting down Cellular Architecture Manager")
            self.is_running = False
            
            # Cancel health monitoring
            if self.health_monitor_task:
                self.health_monitor_task.cancel()
            
            # Shutdown all cells
            for cell in self.cells.values():
                await cell.shutdown()
            
            # Shutdown all tissues
            for tissue in self.tissues.values():
                await tissue.shutdown()
            
            # Shutdown all organs
            for organ in self.organs.values():
                await organ.shutdown()
            
            # Shutdown executor
            self.executor.shutdown(wait=True)
            
            logger.info("Cellular Architecture Manager shutdown complete")
            return True
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            return False
    
    def register_cell(self, cell: CellularInterface):
        """Register a cellular component"""
        self.cells[cell.cell_id] = cell
        cell.register_event_handler("status_change", self._handle_cell_event)
        self.emit_event("cell_registered", {"cell_id": cell.cell_id})
        logger.info(f"Cell registered: {cell.cell_id}")
    
    def register_tissue(self, tissue: TissueInterface):
        """Register a tissue component"""
        self.tissues[tissue.tissue_id] = tissue
        tissue.register_event_handler("status_change", self._handle_tissue_event)
        self.emit_event("tissue_registered", {"tissue_id": tissue.tissue_id})
        logger.info(f"Tissue registered: {tissue.tissue_id}")
    
    def register_organ(self, organ: OrganInterface):
        """Register an organ component"""
        self.organs[organ.organ_id] = organ
        organ.register_event_handler("status_change", self._handle_organ_event)
        self.emit_event("organ_registered", {"organ_id": organ.organ_id})
        logger.info(f"Organ registered: {organ.organ_id}")
    
    def create_connection(self, source_cell_id: str, target_cell_id: str, 
                         connection_type: ConnectionType, strength: float = 1.0,
                         is_bidirectional: bool = True) -> bool:
        """Create connection between cellular components"""
        try:
            if source_cell_id not in self.cells or target_cell_id not in self.cells:
                logger.error(f"Cannot create connection: cells not found")
                return False
            
            connection = CellularConnection(
                source_cell=source_cell_id,
                target_cell=target_cell_id,
                connection_type=connection_type,
                strength=strength,
                bandwidth=1000.0,  # Default bandwidth
                latency=10.0,      # Default latency
                is_bidirectional=is_bidirectional
            )
            
            # Add connection to source cell
            self.cells[source_cell_id].add_connection(connection)
            self.connections[source_cell_id].append(connection)
            
            # Add reverse connection if bidirectional
            if is_bidirectional:
                reverse_connection = CellularConnection(
                    source_cell=target_cell_id,
                    target_cell=source_cell_id,
                    connection_type=connection_type,
                    strength=strength,
                    bandwidth=1000.0,
                    latency=10.0,
                    is_bidirectional=True
                )
                self.cells[target_cell_id].add_connection(reverse_connection)
                self.connections[target_cell_id].append(reverse_connection)
            
            self.emit_event("connection_created", {
                "source": source_cell_id,
                "target": target_cell_id,
                "type": connection_type.value
            })
            
            logger.info(f"Connection created: {source_cell_id} -> {target_cell_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            return False
    
    async def process_data(self, cell_id: str, data: CellData, 
                          priority: CellularPriority = CellularPriority.MEDIUM) -> Optional[CellData]:
        """Process data through a specific cellular component"""
        try:
            if cell_id not in self.cells:
                logger.error(f"Cell not found: {cell_id}")
                return None
            
            cell = self.cells[cell_id]
            start_time = datetime.now()
            
            # Process data
            result = await cell.process(data)
            
            # Update metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            cell.update_metrics(processing_time, success=True)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing data in cell {cell_id}: {e}")
            if cell_id in self.cells:
                self.cells[cell_id].update_metrics(success=False)
                self.cells[cell_id].last_error = e
            return None
    
    async def broadcast_data(self, source_cell_id: str, data: CellData, 
                           connection_types: List[ConnectionType] = None) -> Dict[str, Any]:
        """Broadcast data to connected cells"""
        try:
            if source_cell_id not in self.cells:
                logger.error(f"Source cell not found: {source_cell_id}")
                return {}
            
            results = {}
            connections = self.connections.get(source_cell_id, [])
            
            # Filter connections by type if specified
            if connection_types:
                connections = [conn for conn in connections if conn.connection_type in connection_types]
            
            # Process data in parallel across connected cells
            tasks = []
            for connection in connections:
                task = self.process_data(connection.target_cell, data)
                tasks.append((connection.target_cell, task))
            
            # Wait for all tasks to complete
            for cell_id, task in tasks:
                try:
                    result = await task
                    results[cell_id] = result
                except Exception as e:
                    logger.error(f"Error in broadcast to cell {cell_id}: {e}")
                    results[cell_id] = None
            
            return results
            
        except Exception as e:
            logger.error(f"Error in broadcast from cell {source_cell_id}: {e}")
            return {}
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health report"""
        try:
            health_report = {
                "timestamp": datetime.now().isoformat(),
                "overall_status": "healthy",
                "cells": {},
                "tissues": {},
                "organs": {},
                "connections": len(sum(self.connections.values(), [])),
                "summary": {
                    "total_cells": len(self.cells),
                    "healthy_cells": 0,
                    "total_tissues": len(self.tissues),
                    "healthy_tissues": 0,
                    "total_organs": len(self.organs),
                    "healthy_organs": 0
                }
            }
            
            # Check cell health
            for cell_id, cell in self.cells.items():
                health = await cell.health_check()
                health_report["cells"][cell_id] = health
                if health.get("is_healthy", False):
                    health_report["summary"]["healthy_cells"] += 1
            
            # Check tissue health
            for tissue_id, tissue in self.tissues.items():
                health = await tissue.health_check()
                health_report["tissues"][tissue_id] = health
                if health.get("is_healthy", False):
                    health_report["summary"]["healthy_tissues"] += 1
            
            # Check organ health
            for organ_id, organ in self.organs.items():
                health = await organ.health_check()
                health_report["organs"][organ_id] = health
                if health.get("is_healthy", False):
                    health_report["summary"]["healthy_organs"] += 1
            
            # Calculate overall health
            total_components = (health_report["summary"]["total_cells"] + 
                              health_report["summary"]["total_tissues"] + 
                              health_report["summary"]["total_organs"])
            
            healthy_components = (health_report["summary"]["healthy_cells"] + 
                                health_report["summary"]["healthy_tissues"] + 
                                health_report["summary"]["healthy_organs"])
            
            if total_components > 0:
                overall_health_percentage = (healthy_components / total_components) * 100
                if overall_health_percentage < 50:
                    health_report["overall_status"] = "critical"
                elif overall_health_percentage < 70:
                    health_report["overall_status"] = "degraded"
                elif overall_health_percentage < 90:
                    health_report["overall_status"] = "warning"
                else:
                    health_report["overall_status"] = "healthy"
            
            return health_report
            
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "overall_status": "error",
                "error": str(e)
            }
    
    async def _health_monitor_loop(self):
        """Background health monitoring loop"""
        while self.is_running:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                health_report = await self.get_system_health()
                
                # Emit health events for critical issues
                if health_report["overall_status"] in ["critical", "degraded"]:
                    self.emit_event("system_health_warning", health_report)
                
                # Log health summary
                summary = health_report.get("summary", {})
                logger.info(f"Health Check - Cells: {summary.get('healthy_cells', 0)}/{summary.get('total_cells', 0)}, "
                           f"Tissues: {summary.get('healthy_tissues', 0)}/{summary.get('total_tissues', 0)}, "
                           f"Organs: {summary.get('healthy_organs', 0)}/{summary.get('total_organs', 0)}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health monitor loop: {e}")
    
    def _handle_cell_event(self, cell_id: str, event_type: str, data: Dict[str, Any]):
        """Handle cell events"""
        self.emit_event(f"cell_{event_type}", {"cell_id": cell_id, "data": data})
    
    def _handle_tissue_event(self, tissue_id: str, event_type: str, data: Dict[str, Any]):
        """Handle tissue events"""
        self.emit_event(f"tissue_{event_type}", {"tissue_id": tissue_id, "data": data})
    
    def _handle_organ_event(self, organ_id: str, event_type: str, data: Dict[str, Any]):
        """Handle organ events"""
        self.emit_event(f"organ_{event_type}", {"organ_id": organ_id, "data": data})
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit system-level event"""
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(event_type, data)
            except Exception as e:
                logger.error(f"Event handler error: {e}")
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register system-level event handler"""
        self.event_handlers[event_type].append(handler)

# Global cellular architecture manager instance
cellular_manager = CellularArchitectureManager()

# Export key classes and functions
__all__ = [
    'CellularInterface',
    'TissueInterface', 
    'OrganInterface',
    'CellularArchitectureManager',
    'CellularStatus',
    'ConnectionType',
    'CellularPriority',
    'CellularMetrics',
    'CellularConnection',
    'cellular_manager'
]

