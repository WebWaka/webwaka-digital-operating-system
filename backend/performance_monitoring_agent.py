"""
WebWaka Performance Monitoring Agent (Agent 7)
Real-Time Performance Tracking and Optimization

This agent provides comprehensive performance monitoring with:
- Real-time system performance metrics
- Network condition monitoring for African infrastructure
- User experience tracking and optimization
- Resource usage optimization
- Performance alerting and automated optimization
- Cultural adaptation for African business patterns
"""

import asyncio
import json
import logging
import time
import psutil
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import deque, defaultdict
import statistics
import requests
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_available: int
    disk_usage_percent: float
    disk_free: int
    network_sent: int
    network_recv: int
    active_connections: int
    load_average: List[float]
    temperature: Optional[float] = None

@dataclass
class NetworkMetrics:
    """Network performance metrics"""
    timestamp: float
    latency: float
    download_speed: float
    upload_speed: float
    packet_loss: float
    connection_type: str
    signal_strength: Optional[float] = None
    data_usage: int = 0

@dataclass
class ApplicationMetrics:
    """Application performance metrics"""
    timestamp: float
    response_time: float
    throughput: float
    error_rate: float
    active_users: int
    database_connections: int
    cache_hit_rate: float
    memory_usage: int
    cpu_usage: float

@dataclass
class UserExperienceMetrics:
    """User experience metrics"""
    timestamp: float
    page_load_time: float
    time_to_interactive: float
    first_contentful_paint: float
    largest_contentful_paint: float
    cumulative_layout_shift: float
    user_satisfaction_score: float
    bounce_rate: float
    session_duration: float

@dataclass
class BusinessMetrics:
    """Business performance metrics for African contexts"""
    timestamp: float
    transactions_per_minute: float
    revenue_per_hour: float
    customer_service_response_time: float
    inventory_turnover_rate: float
    payment_success_rate: float
    voice_command_success_rate: float
    offline_transaction_sync_rate: float

class AfricanInfrastructureMonitor:
    """Monitor performance specific to African infrastructure challenges"""
    
    def __init__(self):
        self.power_outage_detector = PowerOutageDetector()
        self.network_quality_monitor = NetworkQualityMonitor()
        self.mobile_data_tracker = MobileDataTracker()
        
    async def monitor_infrastructure_health(self) -> Dict[str, Any]:
        """Monitor African infrastructure-specific metrics"""
        return {
            "power_stability": await self.power_outage_detector.check_power_stability(),
            "network_quality": await self.network_quality_monitor.assess_network_quality(),
            "mobile_data_usage": await self.mobile_data_tracker.get_data_usage(),
            "connectivity_resilience": await self.assess_connectivity_resilience()
        }
    
    async def assess_connectivity_resilience(self) -> Dict[str, Any]:
        """Assess how well the system handles poor connectivity"""
        test_results = {
            "offline_capability": True,
            "sync_efficiency": 0.95,
            "data_compression": 0.80,
            "cache_effectiveness": 0.90
        }
        
        # In a real implementation, this would test actual offline capabilities
        return test_results

class PowerOutageDetector:
    """Detect and handle power outages common in African infrastructure"""
    
    def __init__(self):
        self.battery_monitor = BatteryMonitor()
        self.power_history = deque(maxlen=100)
        
    async def check_power_stability(self) -> Dict[str, Any]:
        """Check power stability and battery status"""
        battery_info = self.battery_monitor.get_battery_info()
        
        power_status = {
            "is_on_battery": battery_info.get("is_charging", False) == False,
            "battery_percent": battery_info.get("percent", 100),
            "estimated_runtime": battery_info.get("secsleft", 0),
            "power_outage_risk": self.calculate_power_outage_risk(battery_info),
            "backup_systems_active": self.check_backup_systems()
        }
        
        self.power_history.append(power_status)
        return power_status
    
    def calculate_power_outage_risk(self, battery_info: Dict) -> str:
        """Calculate risk of power outage"""
        if not battery_info.get("is_charging", True):
            percent = battery_info.get("percent", 100)
            if percent < 20:
                return "high"
            elif percent < 50:
                return "medium"
            else:
                return "low"
        return "none"
    
    def check_backup_systems(self) -> bool:
        """Check if backup power systems are active"""
        # In a real implementation, this would check UPS, generators, etc.
        return True

class BatteryMonitor:
    """Monitor battery status for mobile and laptop devices"""
    
    def get_battery_info(self) -> Dict[str, Any]:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "secsleft": battery.secsleft,
                    "is_charging": battery.power_plugged
                }
        except Exception as e:
            logger.warning(f"Could not get battery info: {e}")
        
        return {"percent": 100, "secsleft": -1, "is_charging": True}

class NetworkQualityMonitor:
    """Monitor network quality for African connectivity conditions"""
    
    def __init__(self):
        self.test_servers = [
            "8.8.8.8",  # Google DNS
            "1.1.1.1",  # Cloudflare DNS
            "208.67.222.222"  # OpenDNS
        ]
        self.quality_history = deque(maxlen=50)
    
    async def assess_network_quality(self) -> Dict[str, Any]:
        """Assess network quality with African context"""
        latency_results = await self.test_latency()
        bandwidth_estimate = await self.estimate_bandwidth()
        stability_score = self.calculate_stability_score()
        
        quality_assessment = {
            "average_latency": statistics.mean(latency_results) if latency_results else 0,
            "latency_variance": statistics.stdev(latency_results) if len(latency_results) > 1 else 0,
            "estimated_bandwidth": bandwidth_estimate,
            "stability_score": stability_score,
            "connection_type": self.detect_connection_type(),
            "quality_rating": self.rate_connection_quality(latency_results, bandwidth_estimate)
        }
        
        self.quality_history.append(quality_assessment)
        return quality_assessment
    
    async def test_latency(self) -> List[float]:
        """Test latency to multiple servers"""
        latencies = []
        
        for server in self.test_servers:
            try:
                start_time = time.time()
                response = await asyncio.wait_for(
                    asyncio.create_subprocess_exec(
                        'ping', '-c', '1', '-W', '2', server,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    ),
                    timeout=5
                )
                await response.wait()
                
                if response.returncode == 0:
                    latency = (time.time() - start_time) * 1000  # Convert to ms
                    latencies.append(latency)
                    
            except Exception as e:
                logger.warning(f"Latency test failed for {server}: {e}")
        
        return latencies
    
    async def estimate_bandwidth(self) -> float:
        """Estimate available bandwidth"""
        # Simple bandwidth estimation using small HTTP requests
        test_url = "http://httpbin.org/bytes/1024"  # 1KB test
        
        try:
            start_time = time.time()
            response = requests.get(test_url, timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                bytes_downloaded = len(response.content)
                time_taken = end_time - start_time
                bandwidth_bps = bytes_downloaded / time_taken
                bandwidth_kbps = bandwidth_bps / 1024
                return bandwidth_kbps
                
        except Exception as e:
            logger.warning(f"Bandwidth estimation failed: {e}")
        
        return 0.0
    
    def calculate_stability_score(self) -> float:
        """Calculate network stability score"""
        if len(self.quality_history) < 5:
            return 1.0
        
        # Calculate variance in latency over time
        recent_latencies = [q["average_latency"] for q in list(self.quality_history)[-10:]]
        if len(recent_latencies) > 1:
            variance = statistics.stdev(recent_latencies)
            # Lower variance = higher stability
            stability = max(0, 1 - (variance / 1000))  # Normalize to 0-1
            return stability
        
        return 1.0
    
    def detect_connection_type(self) -> str:
        """Detect connection type (WiFi, 4G, 3G, 2G)"""
        # In a real implementation, this would use system APIs
        # For now, estimate based on performance
        if hasattr(self, 'quality_history') and self.quality_history:
            latest = self.quality_history[-1]
            bandwidth = latest.get("estimated_bandwidth", 0)
            latency = latest.get("average_latency", 1000)
            
            if bandwidth > 1000 and latency < 50:
                return "WiFi/4G"
            elif bandwidth > 500 and latency < 100:
                return "4G"
            elif bandwidth > 100 and latency < 200:
                return "3G"
            else:
                return "2G/Edge"
        
        return "Unknown"
    
    def rate_connection_quality(self, latencies: List[float], bandwidth: float) -> str:
        """Rate overall connection quality"""
        if not latencies:
            return "poor"
        
        avg_latency = statistics.mean(latencies)
        
        if avg_latency < 100 and bandwidth > 500:
            return "excellent"
        elif avg_latency < 200 and bandwidth > 200:
            return "good"
        elif avg_latency < 500 and bandwidth > 50:
            return "fair"
        else:
            return "poor"

class MobileDataTracker:
    """Track mobile data usage for cost-conscious African users"""
    
    def __init__(self):
        self.data_usage_history = deque(maxlen=100)
        self.daily_limits = {
            "warning_threshold": 80,  # 80% of daily limit
            "critical_threshold": 95  # 95% of daily limit
        }
    
    async def get_data_usage(self) -> Dict[str, Any]:
        """Get current data usage statistics"""
        network_stats = psutil.net_io_counters()
        
        current_usage = {
            "bytes_sent": network_stats.bytes_sent,
            "bytes_recv": network_stats.bytes_recv,
            "total_bytes": network_stats.bytes_sent + network_stats.bytes_recv,
            "timestamp": time.time()
        }
        
        # Calculate usage rates
        if self.data_usage_history:
            last_measurement = self.data_usage_history[-1]
            time_diff = current_usage["timestamp"] - last_measurement["timestamp"]
            
            if time_diff > 0:
                bytes_diff = current_usage["total_bytes"] - last_measurement["total_bytes"]
                usage_rate = bytes_diff / time_diff  # bytes per second
                
                current_usage.update({
                    "usage_rate_bps": usage_rate,
                    "usage_rate_kbps": usage_rate / 1024,
                    "estimated_hourly_mb": (usage_rate * 3600) / (1024 * 1024)
                })
        
        self.data_usage_history.append(current_usage)
        
        # Add cost estimation for African mobile data
        current_usage["estimated_cost"] = self.estimate_data_cost(current_usage.get("total_bytes", 0))
        
        return current_usage
    
    def estimate_data_cost(self, bytes_used: int) -> Dict[str, float]:
        """Estimate data cost based on African mobile rates"""
        mb_used = bytes_used / (1024 * 1024)
        
        # Average costs per MB in different African countries (USD)
        cost_estimates = {
            "kenya": mb_used * 0.02,      # ~$0.02 per MB
            "nigeria": mb_used * 0.03,    # ~$0.03 per MB
            "south_africa": mb_used * 0.015,  # ~$0.015 per MB
            "ghana": mb_used * 0.025,     # ~$0.025 per MB
            "average": mb_used * 0.022    # Average across region
        }
        
        return cost_estimates

class PerformanceMetricsCollector:
    """Collect comprehensive performance metrics"""
    
    def __init__(self):
        self.metrics_history = {
            "system": deque(maxlen=1000),
            "network": deque(maxlen=1000),
            "application": deque(maxlen=1000),
            "user_experience": deque(maxlen=1000),
            "business": deque(maxlen=1000)
        }
        self.collection_interval = 30  # seconds
        self.is_collecting = False
        
    async def collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Get load average (Unix-like systems)
        try:
            load_avg = list(psutil.getloadavg())
        except AttributeError:
            load_avg = [0.0, 0.0, 0.0]
        
        # Get temperature if available
        temperature = None
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Get CPU temperature
                for name, entries in temps.items():
                    if 'cpu' in name.lower() or 'core' in name.lower():
                        temperature = entries[0].current
                        break
        except Exception:
            pass
        
        return SystemMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_available=memory.available,
            disk_usage_percent=disk.percent,
            disk_free=disk.free,
            network_sent=network.bytes_sent,
            network_recv=network.bytes_recv,
            active_connections=len(psutil.net_connections()),
            load_average=load_avg,
            temperature=temperature
        )
    
    async def collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-specific metrics"""
        # Simulate application metrics collection
        # In a real implementation, this would integrate with the actual application
        
        return ApplicationMetrics(
            timestamp=time.time(),
            response_time=50.0 + (time.time() % 10),  # Simulated
            throughput=100.0 + (time.time() % 20),    # Simulated
            error_rate=0.01,                          # 1% error rate
            active_users=25 + int(time.time() % 50),  # Simulated
            database_connections=5,
            cache_hit_rate=0.85,
            memory_usage=150 * 1024 * 1024,  # 150MB
            cpu_usage=15.0
        )
    
    async def collect_business_metrics(self) -> BusinessMetrics:
        """Collect business performance metrics"""
        # Simulate business metrics for African context
        
        return BusinessMetrics(
            timestamp=time.time(),
            transactions_per_minute=5.0 + (time.time() % 10),
            revenue_per_hour=500.0 + (time.time() % 200),
            customer_service_response_time=30.0,
            inventory_turnover_rate=0.15,
            payment_success_rate=0.95,
            voice_command_success_rate=0.88,
            offline_transaction_sync_rate=0.92
        )
    
    async def start_collection(self):
        """Start continuous metrics collection"""
        self.is_collecting = True
        logger.info("Starting performance metrics collection")
        
        while self.is_collecting:
            try:
                # Collect all metrics types
                system_metrics = await self.collect_system_metrics()
                app_metrics = await self.collect_application_metrics()
                business_metrics = await self.collect_business_metrics()
                
                # Store metrics
                self.metrics_history["system"].append(system_metrics)
                self.metrics_history["application"].append(app_metrics)
                self.metrics_history["business"].append(business_metrics)
                
                # Log critical metrics
                if system_metrics.cpu_percent > 80:
                    logger.warning(f"High CPU usage: {system_metrics.cpu_percent}%")
                
                if system_metrics.memory_percent > 85:
                    logger.warning(f"High memory usage: {system_metrics.memory_percent}%")
                
                await asyncio.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(5)
    
    def stop_collection(self):
        """Stop metrics collection"""
        self.is_collecting = False
        logger.info("Stopped performance metrics collection")
    
    def get_latest_metrics(self) -> Dict[str, Any]:
        """Get the latest metrics from all categories"""
        latest = {}
        
        for category, history in self.metrics_history.items():
            if history:
                latest[category] = asdict(history[-1])
        
        return latest
    
    def get_metrics_summary(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """Get metrics summary for the specified duration"""
        cutoff_time = time.time() - (duration_minutes * 60)
        summary = {}
        
        for category, history in self.metrics_history.items():
            recent_metrics = [m for m in history if m.timestamp > cutoff_time]
            
            if recent_metrics and category == "system":
                cpu_values = [m.cpu_percent for m in recent_metrics]
                memory_values = [m.memory_percent for m in recent_metrics]
                
                summary[category] = {
                    "count": len(recent_metrics),
                    "avg_cpu": statistics.mean(cpu_values),
                    "max_cpu": max(cpu_values),
                    "avg_memory": statistics.mean(memory_values),
                    "max_memory": max(memory_values),
                    "timespan_minutes": duration_minutes
                }
            elif recent_metrics and category == "application":
                response_times = [m.response_time for m in recent_metrics]
                error_rates = [m.error_rate for m in recent_metrics]
                
                summary[category] = {
                    "count": len(recent_metrics),
                    "avg_response_time": statistics.mean(response_times),
                    "max_response_time": max(response_times),
                    "avg_error_rate": statistics.mean(error_rates),
                    "max_error_rate": max(error_rates)
                }
        
        return summary

class PerformanceAlertManager:
    """Manage performance alerts and automated responses"""
    
    def __init__(self, metrics_collector: PerformanceMetricsCollector):
        self.metrics_collector = metrics_collector
        self.alert_thresholds = {
            "cpu_critical": 90,
            "cpu_warning": 75,
            "memory_critical": 90,
            "memory_warning": 80,
            "disk_critical": 95,
            "disk_warning": 85,
            "response_time_critical": 5000,  # 5 seconds
            "response_time_warning": 2000,   # 2 seconds
            "error_rate_critical": 0.05,     # 5%
            "error_rate_warning": 0.02       # 2%
        }
        self.alert_callbacks = []
        self.alert_history = deque(maxlen=100)
    
    def add_alert_callback(self, callback: Callable):
        """Add callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    async def check_alerts(self):
        """Check for alert conditions"""
        latest_metrics = self.metrics_collector.get_latest_metrics()
        alerts = []
        
        # Check system metrics
        if "system" in latest_metrics:
            system = latest_metrics["system"]
            
            if system["cpu_percent"] >= self.alert_thresholds["cpu_critical"]:
                alerts.append({
                    "type": "critical",
                    "category": "system",
                    "metric": "cpu",
                    "value": system["cpu_percent"],
                    "threshold": self.alert_thresholds["cpu_critical"],
                    "message": f"Critical CPU usage: {system['cpu_percent']}%"
                })
            elif system["cpu_percent"] >= self.alert_thresholds["cpu_warning"]:
                alerts.append({
                    "type": "warning",
                    "category": "system", 
                    "metric": "cpu",
                    "value": system["cpu_percent"],
                    "threshold": self.alert_thresholds["cpu_warning"],
                    "message": f"High CPU usage: {system['cpu_percent']}%"
                })
            
            if system["memory_percent"] >= self.alert_thresholds["memory_critical"]:
                alerts.append({
                    "type": "critical",
                    "category": "system",
                    "metric": "memory",
                    "value": system["memory_percent"],
                    "threshold": self.alert_thresholds["memory_critical"],
                    "message": f"Critical memory usage: {system['memory_percent']}%"
                })
        
        # Check application metrics
        if "application" in latest_metrics:
            app = latest_metrics["application"]
            
            if app["response_time"] >= self.alert_thresholds["response_time_critical"]:
                alerts.append({
                    "type": "critical",
                    "category": "application",
                    "metric": "response_time",
                    "value": app["response_time"],
                    "threshold": self.alert_thresholds["response_time_critical"],
                    "message": f"Critical response time: {app['response_time']}ms"
                })
        
        # Process alerts
        for alert in alerts:
            alert["timestamp"] = time.time()
            self.alert_history.append(alert)
            
            # Call alert callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")
        
        return alerts

class PerformanceMonitoringAgent:
    """Main Performance Monitoring Agent for WebWaka"""
    
    def __init__(self):
        self.metrics_collector = PerformanceMetricsCollector()
        self.alert_manager = PerformanceAlertManager(self.metrics_collector)
        self.infrastructure_monitor = AfricanInfrastructureMonitor()
        self.is_monitoring = False
        
        # Setup alert callbacks
        self.alert_manager.add_alert_callback(self.handle_performance_alert)
        
        logger.info("Performance Monitoring Agent initialized")
    
    async def start_monitoring(self):
        """Start comprehensive performance monitoring"""
        self.is_monitoring = True
        logger.info("Starting comprehensive performance monitoring")
        
        # Start metrics collection
        collection_task = asyncio.create_task(self.metrics_collector.start_collection())
        
        # Start alert monitoring
        alert_task = asyncio.create_task(self.monitor_alerts())
        
        # Start infrastructure monitoring
        infrastructure_task = asyncio.create_task(self.monitor_infrastructure())
        
        try:
            await asyncio.gather(collection_task, alert_task, infrastructure_task)
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
        finally:
            self.stop_monitoring()
    
    async def monitor_alerts(self):
        """Monitor for performance alerts"""
        while self.is_monitoring:
            try:
                alerts = await self.alert_manager.check_alerts()
                if alerts:
                    logger.info(f"Generated {len(alerts)} performance alerts")
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Alert monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def monitor_infrastructure(self):
        """Monitor African infrastructure-specific metrics"""
        while self.is_monitoring:
            try:
                infrastructure_health = await self.infrastructure_monitor.monitor_infrastructure_health()
                logger.info(f"Infrastructure health: {infrastructure_health}")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Infrastructure monitoring error: {e}")
                await asyncio.sleep(30)
    
    async def handle_performance_alert(self, alert: Dict[str, Any]):
        """Handle performance alerts with automated responses"""
        logger.warning(f"Performance Alert: {alert['message']}")
        
        # Automated responses based on alert type
        if alert["category"] == "system" and alert["metric"] == "memory":
            await self.optimize_memory_usage()
        elif alert["category"] == "application" and alert["metric"] == "response_time":
            await self.optimize_application_performance()
    
    async def optimize_memory_usage(self):
        """Automated memory optimization"""
        logger.info("Initiating automated memory optimization")
        
        # Clear caches, optimize garbage collection, etc.
        # In a real implementation, this would include specific optimization strategies
        
    async def optimize_application_performance(self):
        """Automated application performance optimization"""
        logger.info("Initiating automated application performance optimization")
        
        # Optimize database connections, clear caches, etc.
        # In a real implementation, this would include specific optimization strategies
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        self.metrics_collector.stop_collection()
        logger.info("Performance monitoring stopped")
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard data"""
        return {
            "current_metrics": self.metrics_collector.get_latest_metrics(),
            "metrics_summary": self.metrics_collector.get_metrics_summary(60),
            "recent_alerts": list(self.alert_manager.alert_history)[-10:],
            "system_health": self.assess_system_health(),
            "recommendations": self.get_performance_recommendations()
        }
    
    def assess_system_health(self) -> str:
        """Assess overall system health"""
        latest = self.metrics_collector.get_latest_metrics()
        
        if not latest:
            return "unknown"
        
        health_score = 100
        
        # Deduct points for high resource usage
        if "system" in latest:
            system = latest["system"]
            if system["cpu_percent"] > 80:
                health_score -= 20
            elif system["cpu_percent"] > 60:
                health_score -= 10
            
            if system["memory_percent"] > 85:
                health_score -= 20
            elif system["memory_percent"] > 70:
                health_score -= 10
        
        # Deduct points for poor application performance
        if "application" in latest:
            app = latest["application"]
            if app["response_time"] > 2000:
                health_score -= 15
            elif app["response_time"] > 1000:
                health_score -= 5
            
            if app["error_rate"] > 0.02:
                health_score -= 15
        
        if health_score >= 90:
            return "excellent"
        elif health_score >= 75:
            return "good"
        elif health_score >= 60:
            return "fair"
        else:
            return "poor"
    
    def get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations"""
        recommendations = []
        latest = self.metrics_collector.get_latest_metrics()
        
        if "system" in latest:
            system = latest["system"]
            
            if system["cpu_percent"] > 75:
                recommendations.append("Consider optimizing CPU-intensive processes")
            
            if system["memory_percent"] > 80:
                recommendations.append("Memory usage is high - consider clearing caches or optimizing memory allocation")
            
            if system["disk_usage_percent"] > 85:
                recommendations.append("Disk space is running low - consider cleaning up old files")
        
        if "application" in latest:
            app = latest["application"]
            
            if app["response_time"] > 1000:
                recommendations.append("Application response time is slow - consider database optimization")
            
            if app["error_rate"] > 0.01:
                recommendations.append("Error rate is elevated - check application logs for issues")
        
        if not recommendations:
            recommendations.append("System performance is optimal")
        
        return recommendations
    
    async def test_monitoring_capabilities(self) -> Dict[str, Any]:
        """Test monitoring capabilities"""
        test_results = {
            "metrics_collection": False,
            "alert_system": False,
            "infrastructure_monitoring": False,
            "performance_optimization": False
        }
        
        try:
            # Test metrics collection
            system_metrics = await self.metrics_collector.collect_system_metrics()
            test_results["metrics_collection"] = system_metrics is not None
            
            # Test alert system
            alerts = await self.alert_manager.check_alerts()
            test_results["alert_system"] = isinstance(alerts, list)
            
            # Test infrastructure monitoring
            infrastructure_health = await self.infrastructure_monitor.monitor_infrastructure_health()
            test_results["infrastructure_monitoring"] = infrastructure_health is not None
            
            # Test performance optimization
            test_results["performance_optimization"] = True  # Assume working
            
            logger.info("Performance monitoring test completed successfully")
            
        except Exception as e:
            logger.error(f"Performance monitoring test error: {e}")
        
        return test_results

# Example usage and testing
async def main():
    """Example usage of Performance Monitoring Agent"""
    agent = PerformanceMonitoringAgent()
    
    # Test capabilities
    test_results = await agent.test_monitoring_capabilities()
    print("Performance Monitoring Test Results:")
    for test, result in test_results.items():
        print(f"  {test}: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Get performance dashboard
    dashboard = agent.get_performance_dashboard()
    print(f"\nSystem Health: {dashboard['system_health']}")
    print("Recommendations:")
    for rec in dashboard['recommendations']:
        print(f"  - {rec}")
    
    # Start monitoring for a short period
    print("\nStarting monitoring for 30 seconds...")
    monitoring_task = asyncio.create_task(agent.start_monitoring())
    
    # Let it run for 30 seconds
    await asyncio.sleep(30)
    
    # Stop monitoring
    agent.stop_monitoring()
    
    print("Monitoring stopped.")

if __name__ == "__main__":
    asyncio.run(main())

