"""
WebWaka Inventory Management System
AI-powered inventory optimization with predictive analytics and African market adaptation
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from decimal import Decimal, ROUND_HALF_UP
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventoryStatus(Enum):
    """Inventory status types"""
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    OVERSTOCKED = "overstocked"
    DISCONTINUED = "discontinued"

class MovementType(Enum):
    """Inventory movement types"""
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"
    RETURN = "return"
    DAMAGE = "damage"
    THEFT = "theft"
    EXPIRED = "expired"

class SupplierStatus(Enum):
    """Supplier status types"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLACKLISTED = "blacklisted"
    PENDING_APPROVAL = "pending_approval"

class SeasonalPattern(Enum):
    """Seasonal demand patterns"""
    HIGH_SEASON = "high_season"
    LOW_SEASON = "low_season"
    HARVEST_SEASON = "harvest_season"
    PLANTING_SEASON = "planting_season"
    FESTIVAL_SEASON = "festival_season"

@dataclass
class InventoryItem:
    """Inventory item information"""
    item_id: str
    tenant_id: str
    sku: str
    name: str
    local_names: Dict[str, str]
    category: str
    subcategory: Optional[str]
    current_stock: int
    minimum_stock: int
    maximum_stock: int
    reorder_point: int
    reorder_quantity: int
    unit_cost: Decimal
    selling_price: Decimal
    supplier_id: Optional[str]
    location: str
    shelf_life_days: Optional[int]
    expiry_date: Optional[datetime]
    batch_number: Optional[str]
    barcode: Optional[str]
    weight: Optional[Decimal]
    dimensions: Optional[Dict[str, Decimal]]
    seasonal_pattern: Optional[SeasonalPattern]
    cultural_significance: Optional[str]
    storage_requirements: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    last_counted: Optional[datetime]

@dataclass
class Supplier:
    """Supplier information"""
    supplier_id: str
    tenant_id: str
    name: str
    contact_person: str
    phone: str
    email: Optional[str]
    address: str
    country: str
    payment_terms: str
    lead_time_days: int
    minimum_order_value: Decimal
    reliability_score: float
    quality_score: float
    delivery_score: float
    status: SupplierStatus
    preferred_payment_method: str
    cultural_context: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

@dataclass
class InventoryMovement:
    """Inventory movement record"""
    movement_id: str
    tenant_id: str
    item_id: str
    movement_type: MovementType
    quantity: int
    unit_cost: Optional[Decimal]
    total_value: Optional[Decimal]
    reference_id: Optional[str]  # PO, Sale, etc.
    notes: str
    performed_by: str
    location_from: Optional[str]
    location_to: Optional[str]
    batch_number: Optional[str]
    expiry_date: Optional[datetime]
    created_at: datetime

@dataclass
class PurchaseOrder:
    """Purchase order information"""
    po_id: str
    tenant_id: str
    supplier_id: str
    items: List[Dict[str, Any]]
    total_amount: Decimal
    status: str
    order_date: datetime
    expected_delivery: datetime
    actual_delivery: Optional[datetime]
    created_by: str
    approved_by: Optional[str]
    notes: str

@dataclass
class StockAlert:
    """Stock alert information"""
    alert_id: str
    tenant_id: str
    item_id: str
    alert_type: str
    message: str
    severity: str
    created_at: datetime
    acknowledged: bool
    acknowledged_by: Optional[str]
    acknowledged_at: Optional[datetime]

class AIInventoryOptimizer:
    """AI-powered inventory optimization"""
    
    def __init__(self):
        self.demand_patterns = {}
        self.seasonal_factors = {}
        self.supplier_performance = {}
    
    def analyze_demand_patterns(self, item_id: str, 
                               historical_movements: List[InventoryMovement]) -> Dict[str, Any]:
        """Analyze demand patterns for an item"""
        try:
            # Filter sales movements
            sales_movements = [
                m for m in historical_movements 
                if m.movement_type == MovementType.SALE and m.item_id == item_id
            ]
            
            if len(sales_movements) < 7:  # Need at least a week of data
                return {
                    'pattern': 'insufficient_data',
                    'confidence': 0.0,
                    'recommendation': 'collect_more_data'
                }
            
            # Calculate daily demand
            daily_demand = {}
            for movement in sales_movements:
                date_key = movement.created_at.date()
                if date_key not in daily_demand:
                    daily_demand[date_key] = 0
                daily_demand[date_key] += movement.quantity
            
            # Calculate statistics
            demands = list(daily_demand.values())
            avg_demand = statistics.mean(demands)
            std_demand = statistics.stdev(demands) if len(demands) > 1 else 0
            
            # Identify pattern
            pattern = self._identify_demand_pattern(demands)
            
            # Calculate seasonal factors
            seasonal_factor = self._calculate_seasonal_factor(sales_movements)
            
            # Predict future demand
            future_demand = self._predict_demand(demands, seasonal_factor)
            
            return {
                'pattern': pattern,
                'average_daily_demand': avg_demand,
                'demand_variability': std_demand,
                'seasonal_factor': seasonal_factor,
                'predicted_weekly_demand': future_demand * 7,
                'confidence': self._calculate_confidence(len(demands)),
                'recommendation': self._generate_recommendation(avg_demand, std_demand, future_demand)
            }
            
        except Exception as e:
            logger.error(f"Demand pattern analysis failed: {str(e)}")
            return {
                'pattern': 'analysis_error',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _identify_demand_pattern(self, demands: List[float]) -> str:
        """Identify demand pattern type"""
        if not demands:
            return 'no_data'
        
        # Calculate trend
        if len(demands) < 3:
            return 'stable'
        
        # Simple trend analysis
        first_third = demands[:len(demands)//3]
        last_third = demands[-len(demands)//3:]
        
        first_avg = statistics.mean(first_third)
        last_avg = statistics.mean(last_third)
        
        change_ratio = (last_avg - first_avg) / first_avg if first_avg > 0 else 0
        
        if change_ratio > 0.2:
            return 'increasing'
        elif change_ratio < -0.2:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_seasonal_factor(self, movements: List[InventoryMovement]) -> float:
        """Calculate seasonal demand factor"""
        if not movements:
            return 1.0
        
        # Group by month
        monthly_demand = {}
        for movement in movements:
            month = movement.created_at.month
            if month not in monthly_demand:
                monthly_demand[month] = 0
            monthly_demand[month] += movement.quantity
        
        if len(monthly_demand) < 2:
            return 1.0
        
        # Calculate current month factor
        current_month = datetime.now().month
        current_demand = monthly_demand.get(current_month, 0)
        avg_demand = statistics.mean(monthly_demand.values())
        
        return current_demand / avg_demand if avg_demand > 0 else 1.0
    
    def _predict_demand(self, historical_demands: List[float], seasonal_factor: float) -> float:
        """Predict future demand"""
        if not historical_demands:
            return 0.0
        
        # Simple moving average with seasonal adjustment
        recent_demands = historical_demands[-7:]  # Last 7 periods
        base_demand = statistics.mean(recent_demands)
        
        return base_demand * seasonal_factor
    
    def _calculate_confidence(self, data_points: int) -> float:
        """Calculate confidence level based on data points"""
        if data_points < 7:
            return 0.3
        elif data_points < 30:
            return 0.6
        elif data_points < 90:
            return 0.8
        else:
            return 0.9
    
    def _generate_recommendation(self, avg_demand: float, std_demand: float, 
                               predicted_demand: float) -> str:
        """Generate inventory recommendation"""
        if predicted_demand > avg_demand * 1.5:
            return 'increase_stock_high_demand_predicted'
        elif predicted_demand < avg_demand * 0.5:
            return 'reduce_stock_low_demand_predicted'
        elif std_demand > avg_demand:
            return 'increase_safety_stock_high_variability'
        else:
            return 'maintain_current_levels'
    
    def optimize_reorder_points(self, item: InventoryItem, 
                               demand_analysis: Dict[str, Any],
                               supplier: Optional[Supplier] = None) -> Dict[str, int]:
        """Optimize reorder points and quantities"""
        try:
            avg_daily_demand = demand_analysis.get('average_daily_demand', 1)
            demand_variability = demand_analysis.get('demand_variability', 0)
            
            # Lead time (default to 7 days if no supplier info)
            lead_time = supplier.lead_time_days if supplier else 7
            
            # Safety stock calculation (covers demand variability and lead time uncertainty)
            safety_stock = int(avg_daily_demand * lead_time * 0.5 + demand_variability * 2)
            
            # Reorder point = (Average daily demand × Lead time) + Safety stock
            reorder_point = int(avg_daily_demand * lead_time) + safety_stock
            
            # Economic order quantity (simplified)
            # EOQ = sqrt((2 × Annual demand × Order cost) / Holding cost)
            annual_demand = avg_daily_demand * 365
            order_cost = 100  # Simplified order cost
            holding_cost_rate = 0.2  # 20% of item value
            holding_cost = float(item.unit_cost) * holding_cost_rate
            
            if holding_cost > 0:
                eoq = int((2 * annual_demand * order_cost / holding_cost) ** 0.5)
            else:
                eoq = int(avg_daily_demand * 30)  # 30 days supply
            
            # Ensure minimum order quantities
            if supplier and supplier.minimum_order_value > 0:
                min_qty = int(supplier.minimum_order_value / item.unit_cost)
                eoq = max(eoq, min_qty)
            
            return {
                'reorder_point': max(reorder_point, 1),
                'reorder_quantity': max(eoq, 1),
                'safety_stock': max(safety_stock, 1),
                'max_stock': max(eoq * 2, item.maximum_stock)
            }
            
        except Exception as e:
            logger.error(f"Reorder optimization failed: {str(e)}")
            return {
                'reorder_point': item.reorder_point,
                'reorder_quantity': item.reorder_quantity,
                'safety_stock': item.minimum_stock,
                'max_stock': item.maximum_stock
            }

class InventoryManager:
    """Main inventory management system"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.inventory_items = {}
        self.suppliers = {}
        self.movements = {}
        self.purchase_orders = {}
        self.stock_alerts = {}
        self.ai_optimizer = AIInventoryOptimizer()
        self.cultural_adapter = AfricanInventoryAdapter()
    
    def add_inventory_item(self, item_data: Dict[str, Any]) -> InventoryItem:
        """Add new inventory item"""
        try:
            item_id = str(uuid.uuid4())
            sku = item_data.get('sku', f"SKU-{item_id[:8]}")
            
            item = InventoryItem(
                item_id=item_id,
                tenant_id=self.tenant_id,
                sku=sku,
                name=item_data['name'],
                local_names=item_data.get('local_names', {}),
                category=item_data['category'],
                subcategory=item_data.get('subcategory'),
                current_stock=item_data.get('current_stock', 0),
                minimum_stock=item_data.get('minimum_stock', 5),
                maximum_stock=item_data.get('maximum_stock', 1000),
                reorder_point=item_data.get('reorder_point', 10),
                reorder_quantity=item_data.get('reorder_quantity', 50),
                unit_cost=Decimal(str(item_data.get('unit_cost', 0))),
                selling_price=Decimal(str(item_data.get('selling_price', 0))),
                supplier_id=item_data.get('supplier_id'),
                location=item_data.get('location', 'Main Warehouse'),
                shelf_life_days=item_data.get('shelf_life_days'),
                expiry_date=item_data.get('expiry_date'),
                batch_number=item_data.get('batch_number'),
                barcode=item_data.get('barcode'),
                weight=Decimal(str(item_data.get('weight', 0))) if item_data.get('weight') else None,
                dimensions=item_data.get('dimensions'),
                seasonal_pattern=SeasonalPattern(item_data['seasonal_pattern']) if item_data.get('seasonal_pattern') else None,
                cultural_significance=item_data.get('cultural_significance'),
                storage_requirements=item_data.get('storage_requirements', {}),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                last_counted=None
            )
            
            self.inventory_items[item_id] = item
            
            # Create initial stock movement if current_stock > 0
            if item.current_stock > 0:
                self._create_movement(
                    item_id=item_id,
                    movement_type=MovementType.ADJUSTMENT,
                    quantity=item.current_stock,
                    notes="Initial stock entry",
                    performed_by="system"
                )
            
            logger.info(f"Added inventory item {item.name} with ID {item_id}")
            return item
            
        except Exception as e:
            logger.error(f"Failed to add inventory item: {str(e)}")
            raise InventoryException(f"Item addition failed: {str(e)}")
    
    def add_supplier(self, supplier_data: Dict[str, Any]) -> Supplier:
        """Add new supplier"""
        try:
            supplier_id = str(uuid.uuid4())
            
            supplier = Supplier(
                supplier_id=supplier_id,
                tenant_id=self.tenant_id,
                name=supplier_data['name'],
                contact_person=supplier_data['contact_person'],
                phone=supplier_data['phone'],
                email=supplier_data.get('email'),
                address=supplier_data['address'],
                country=supplier_data['country'],
                payment_terms=supplier_data.get('payment_terms', 'Net 30'),
                lead_time_days=supplier_data.get('lead_time_days', 7),
                minimum_order_value=Decimal(str(supplier_data.get('minimum_order_value', 0))),
                reliability_score=supplier_data.get('reliability_score', 5.0),
                quality_score=supplier_data.get('quality_score', 5.0),
                delivery_score=supplier_data.get('delivery_score', 5.0),
                status=SupplierStatus(supplier_data.get('status', 'active')),
                preferred_payment_method=supplier_data.get('preferred_payment_method', 'bank_transfer'),
                cultural_context=supplier_data.get('cultural_context', {}),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.suppliers[supplier_id] = supplier
            
            logger.info(f"Added supplier {supplier.name} with ID {supplier_id}")
            return supplier
            
        except Exception as e:
            logger.error(f"Failed to add supplier: {str(e)}")
            raise InventoryException(f"Supplier addition failed: {str(e)}")
    
    def update_stock(self, item_id: str, quantity_change: int, 
                    movement_type: MovementType, reference_id: str = None,
                    notes: str = "", performed_by: str = "system") -> InventoryMovement:
        """Update stock levels and create movement record"""
        try:
            item = self.inventory_items.get(item_id)
            if not item:
                raise InventoryException(f"Item {item_id} not found")
            
            # Validate stock change
            if movement_type in [MovementType.SALE, MovementType.DAMAGE, MovementType.THEFT]:
                if item.current_stock < abs(quantity_change):
                    raise InventoryException(f"Insufficient stock. Available: {item.current_stock}")
                quantity_change = -abs(quantity_change)  # Ensure negative for outgoing
            elif movement_type in [MovementType.PURCHASE, MovementType.RETURN, MovementType.ADJUSTMENT]:
                quantity_change = abs(quantity_change)  # Ensure positive for incoming
            
            # Update stock level
            old_stock = item.current_stock
            item.current_stock += quantity_change
            item.updated_at = datetime.utcnow()
            
            # Create movement record
            movement = self._create_movement(
                item_id=item_id,
                movement_type=movement_type,
                quantity=abs(quantity_change),
                reference_id=reference_id,
                notes=notes,
                performed_by=performed_by
            )
            
            # Check for stock alerts
            self._check_stock_alerts(item)
            
            logger.info(f"Updated stock for {item.name}: {old_stock} -> {item.current_stock}")
            return movement
            
        except Exception as e:
            logger.error(f"Stock update failed: {str(e)}")
            raise InventoryException(f"Stock update failed: {str(e)}")
    
    def _create_movement(self, item_id: str, movement_type: MovementType,
                        quantity: int, reference_id: str = None,
                        notes: str = "", performed_by: str = "system") -> InventoryMovement:
        """Create inventory movement record"""
        movement_id = str(uuid.uuid4())
        
        item = self.inventory_items[item_id]
        
        movement = InventoryMovement(
            movement_id=movement_id,
            tenant_id=self.tenant_id,
            item_id=item_id,
            movement_type=movement_type,
            quantity=quantity,
            unit_cost=item.unit_cost,
            total_value=item.unit_cost * quantity,
            reference_id=reference_id,
            notes=notes,
            performed_by=performed_by,
            location_from=None,
            location_to=item.location,
            batch_number=item.batch_number,
            expiry_date=item.expiry_date,
            created_at=datetime.utcnow()
        )
        
        self.movements[movement_id] = movement
        return movement
    
    def _check_stock_alerts(self, item: InventoryItem):
        """Check and create stock alerts"""
        alerts_to_create = []
        
        # Low stock alert
        if item.current_stock <= item.minimum_stock:
            alerts_to_create.append({
                'alert_type': 'low_stock',
                'message': f"{item.name} is running low (Current: {item.current_stock}, Min: {item.minimum_stock})",
                'severity': 'high' if item.current_stock == 0 else 'medium'
            })
        
        # Overstock alert
        if item.current_stock > item.maximum_stock:
            alerts_to_create.append({
                'alert_type': 'overstock',
                'message': f"{item.name} is overstocked (Current: {item.current_stock}, Max: {item.maximum_stock})",
                'severity': 'low'
            })
        
        # Expiry alert
        if item.expiry_date and item.expiry_date <= datetime.utcnow() + timedelta(days=7):
            days_to_expiry = (item.expiry_date - datetime.utcnow()).days
            alerts_to_create.append({
                'alert_type': 'expiry_warning',
                'message': f"{item.name} expires in {days_to_expiry} days",
                'severity': 'high' if days_to_expiry <= 3 else 'medium'
            })
        
        # Create alerts
        for alert_data in alerts_to_create:
            self._create_stock_alert(item.item_id, alert_data)
    
    def _create_stock_alert(self, item_id: str, alert_data: Dict[str, Any]):
        """Create stock alert"""
        alert_id = str(uuid.uuid4())
        
        alert = StockAlert(
            alert_id=alert_id,
            tenant_id=self.tenant_id,
            item_id=item_id,
            alert_type=alert_data['alert_type'],
            message=alert_data['message'],
            severity=alert_data['severity'],
            created_at=datetime.utcnow(),
            acknowledged=False,
            acknowledged_by=None,
            acknowledged_at=None
        )
        
        self.stock_alerts[alert_id] = alert
        logger.info(f"Created stock alert: {alert.message}")
    
    def generate_purchase_order(self, supplier_id: str, items: List[Dict[str, Any]],
                               created_by: str) -> PurchaseOrder:
        """Generate purchase order"""
        try:
            supplier = self.suppliers.get(supplier_id)
            if not supplier:
                raise InventoryException(f"Supplier {supplier_id} not found")
            
            po_id = f"PO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            
            # Calculate total amount
            total_amount = Decimal('0')
            po_items = []
            
            for item_data in items:
                item_id = item_data['item_id']
                quantity = item_data['quantity']
                
                inventory_item = self.inventory_items.get(item_id)
                if not inventory_item:
                    raise InventoryException(f"Item {item_id} not found")
                
                unit_cost = item_data.get('unit_cost', inventory_item.unit_cost)
                line_total = Decimal(str(unit_cost)) * quantity
                total_amount += line_total
                
                po_items.append({
                    'item_id': item_id,
                    'item_name': inventory_item.name,
                    'quantity': quantity,
                    'unit_cost': str(unit_cost),
                    'line_total': str(line_total)
                })
            
            # Check minimum order value
            if total_amount < supplier.minimum_order_value:
                raise InventoryException(
                    f"Order total {total_amount} is below minimum order value {supplier.minimum_order_value}"
                )
            
            # Calculate expected delivery date
            expected_delivery = datetime.utcnow() + timedelta(days=supplier.lead_time_days)
            
            purchase_order = PurchaseOrder(
                po_id=po_id,
                tenant_id=self.tenant_id,
                supplier_id=supplier_id,
                items=po_items,
                total_amount=total_amount,
                status='pending',
                order_date=datetime.utcnow(),
                expected_delivery=expected_delivery,
                actual_delivery=None,
                created_by=created_by,
                approved_by=None,
                notes=""
            )
            
            self.purchase_orders[po_id] = purchase_order
            
            logger.info(f"Generated purchase order {po_id} for supplier {supplier.name}")
            return purchase_order
            
        except Exception as e:
            logger.error(f"Purchase order generation failed: {str(e)}")
            raise InventoryException(f"Purchase order generation failed: {str(e)}")
    
    def receive_purchase_order(self, po_id: str, received_items: List[Dict[str, Any]],
                              received_by: str) -> Dict[str, Any]:
        """Receive items from purchase order"""
        try:
            po = self.purchase_orders.get(po_id)
            if not po:
                raise InventoryException(f"Purchase order {po_id} not found")
            
            if po.status != 'pending':
                raise InventoryException(f"Purchase order {po_id} is not pending")
            
            received_summary = []
            
            for received_item in received_items:
                item_id = received_item['item_id']
                received_qty = received_item['received_quantity']
                
                # Update stock
                movement = self.update_stock(
                    item_id=item_id,
                    quantity_change=received_qty,
                    movement_type=MovementType.PURCHASE,
                    reference_id=po_id,
                    notes=f"Received from PO {po_id}",
                    performed_by=received_by
                )
                
                received_summary.append({
                    'item_id': item_id,
                    'received_quantity': received_qty,
                    'movement_id': movement.movement_id
                })
            
            # Update PO status
            po.status = 'received'
            po.actual_delivery = datetime.utcnow()
            
            logger.info(f"Received purchase order {po_id}")
            
            return {
                'po_id': po_id,
                'received_items': received_summary,
                'received_date': po.actual_delivery.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Purchase order receipt failed: {str(e)}")
            raise InventoryException(f"Purchase order receipt failed: {str(e)}")
    
    def get_inventory_status(self) -> Dict[str, Any]:
        """Get overall inventory status"""
        try:
            total_items = len(self.inventory_items)
            total_value = sum(
                item.current_stock * item.unit_cost 
                for item in self.inventory_items.values()
            )
            
            # Count items by status
            status_counts = {
                'in_stock': 0,
                'low_stock': 0,
                'out_of_stock': 0,
                'overstocked': 0
            }
            
            for item in self.inventory_items.values():
                if item.current_stock == 0:
                    status_counts['out_of_stock'] += 1
                elif item.current_stock <= item.minimum_stock:
                    status_counts['low_stock'] += 1
                elif item.current_stock > item.maximum_stock:
                    status_counts['overstocked'] += 1
                else:
                    status_counts['in_stock'] += 1
            
            # Active alerts
            active_alerts = len([a for a in self.stock_alerts.values() if not a.acknowledged])
            
            return {
                'total_items': total_items,
                'total_value': str(total_value),
                'status_breakdown': status_counts,
                'active_alerts': active_alerts,
                'total_suppliers': len(self.suppliers),
                'pending_purchase_orders': len([po for po in self.purchase_orders.values() if po.status == 'pending'])
            }
            
        except Exception as e:
            logger.error(f"Inventory status retrieval failed: {str(e)}")
            raise InventoryException(f"Inventory status retrieval failed: {str(e)}")
    
    def get_ai_recommendations(self, item_id: str) -> Dict[str, Any]:
        """Get AI-powered inventory recommendations"""
        try:
            item = self.inventory_items.get(item_id)
            if not item:
                raise InventoryException(f"Item {item_id} not found")
            
            # Get historical movements
            item_movements = [m for m in self.movements.values() if m.item_id == item_id]
            
            # Analyze demand patterns
            demand_analysis = self.ai_optimizer.analyze_demand_patterns(item_id, item_movements)
            
            # Get supplier info
            supplier = self.suppliers.get(item.supplier_id) if item.supplier_id else None
            
            # Optimize reorder points
            optimization = self.ai_optimizer.optimize_reorder_points(item, demand_analysis, supplier)
            
            # Generate recommendations
            recommendations = []
            
            if item.current_stock <= optimization['reorder_point']:
                recommendations.append({
                    'type': 'reorder',
                    'priority': 'high',
                    'message': f"Reorder {optimization['reorder_quantity']} units",
                    'action': 'create_purchase_order'
                })
            
            if demand_analysis['pattern'] == 'increasing':
                recommendations.append({
                    'type': 'demand_increase',
                    'priority': 'medium',
                    'message': 'Demand is increasing, consider increasing stock levels',
                    'action': 'review_stock_levels'
                })
            
            return {
                'item_id': item_id,
                'item_name': item.name,
                'current_stock': item.current_stock,
                'demand_analysis': demand_analysis,
                'optimization': optimization,
                'recommendations': recommendations,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI recommendations failed: {str(e)}")
            raise InventoryException(f"AI recommendations failed: {str(e)}")

class AfricanInventoryAdapter:
    """Adapt inventory management for African contexts"""
    
    def __init__(self):
        self.seasonal_patterns = self._initialize_seasonal_patterns()
        self.cultural_considerations = self._initialize_cultural_considerations()
    
    def _initialize_seasonal_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize African seasonal patterns"""
        return {
            'agriculture': {
                'planting_season': {'months': [3, 4, 5], 'demand_factor': 1.5},
                'harvest_season': {'months': [9, 10, 11], 'demand_factor': 0.7},
                'dry_season': {'months': [12, 1, 2], 'demand_factor': 1.2}
            },
            'retail': {
                'festival_season': {'months': [12, 1], 'demand_factor': 2.0},
                'school_season': {'months': [1, 2, 9], 'demand_factor': 1.3},
                'harvest_celebration': {'months': [10, 11], 'demand_factor': 1.4}
            }
        }
    
    def _initialize_cultural_considerations(self) -> Dict[str, Any]:
        """Initialize cultural considerations"""
        return {
            'community_buying': {
                'bulk_discounts': True,
                'group_orders': True,
                'cooperative_purchasing': True
            },
            'traditional_products': {
                'seasonal_availability': True,
                'cultural_significance': True,
                'local_sourcing_preference': True
            },
            'payment_flexibility': {
                'harvest_payment_terms': True,
                'barter_system': True,
                'mobile_money_integration': True
            }
        }
    
    def adapt_reorder_strategy(self, item: InventoryItem, 
                              region: str) -> Dict[str, Any]:
        """Adapt reorder strategy for African context"""
        adaptations = {}
        
        # Seasonal adjustments
        current_month = datetime.now().month
        if item.category in self.seasonal_patterns:
            patterns = self.seasonal_patterns[item.category]
            for season, data in patterns.items():
                if current_month in data['months']:
                    adaptations['seasonal_factor'] = data['demand_factor']
                    adaptations['season'] = season
                    break
        
        # Cultural adaptations
        if item.cultural_significance:
            adaptations['cultural_premium'] = 1.2
            adaptations['local_sourcing_preferred'] = True
        
        # Regional considerations
        if region in ['rural', 'remote']:
            adaptations['lead_time_buffer'] = 1.5  # 50% more lead time
            adaptations['safety_stock_multiplier'] = 1.3
        
        return adaptations

class InventoryException(Exception):
    """Custom inventory exception"""
    pass

# Example usage and testing
def create_sample_inventory_system():
    """Create sample inventory system for testing"""
    inventory = InventoryManager("tenant_123")
    
    # Add sample supplier
    supplier_data = {
        'name': 'Local Farm Cooperative',
        'contact_person': 'John Mwangi',
        'phone': '+254712345678',
        'address': 'Nakuru, Kenya',
        'country': 'Kenya',
        'lead_time_days': 5,
        'minimum_order_value': 1000,
        'cultural_context': {'cooperative': True, 'local_community': True}
    }
    supplier = inventory.add_supplier(supplier_data)
    
    # Add sample inventory items
    items_data = [
        {
            'name': 'Maize Seeds',
            'local_names': {'sw': 'Mbegu za Mahindi', 'ki': 'Mbegu cia Mbembe'},
            'category': 'agriculture',
            'subcategory': 'seeds',
            'current_stock': 100,
            'minimum_stock': 20,
            'maximum_stock': 500,
            'unit_cost': 5.00,
            'selling_price': 7.50,
            'supplier_id': supplier.supplier_id,
            'seasonal_pattern': 'planting_season',
            'cultural_significance': 'Staple crop for local community'
        },
        {
            'name': 'Fertilizer',
            'local_names': {'sw': 'Mbolea', 'ki': 'Mbolea'},
            'category': 'agriculture',
            'subcategory': 'inputs',
            'current_stock': 50,
            'minimum_stock': 10,
            'maximum_stock': 200,
            'unit_cost': 25.00,
            'selling_price': 35.00,
            'supplier_id': supplier.supplier_id,
            'shelf_life_days': 365
        }
    ]
    
    for item_data in items_data:
        inventory.add_inventory_item(item_data)
    
    return inventory

# Initialize inventory system
inventory_system = create_sample_inventory_system()

