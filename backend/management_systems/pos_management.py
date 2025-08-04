"""
WebWaka Point of Sale (POS) Management System
AI-powered POS with voice activation and African cultural adaptation
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from decimal import Decimal, ROUND_HALF_UP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionStatus(Enum):
    """Transaction status types"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIAL_REFUND = "partial_refund"

class PaymentMethod(Enum):
    """Payment method types"""
    CASH = "cash"
    MOBILE_MONEY = "mobile_money"
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    CREDIT = "credit"
    BARTER = "barter"  # Traditional African trading

class ProductCategory(Enum):
    """Product category types"""
    FOOD_BEVERAGE = "food_beverage"
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"
    HOUSEHOLD = "household"
    HEALTH_BEAUTY = "health_beauty"
    AGRICULTURE = "agriculture"
    SERVICES = "services"
    TRADITIONAL_CRAFTS = "traditional_crafts"

@dataclass
class Product:
    """Product information"""
    product_id: str
    tenant_id: str
    name: str
    local_names: Dict[str, str]  # Names in local languages
    category: ProductCategory
    price: Decimal
    cost: Decimal
    stock_quantity: int
    minimum_stock: int
    barcode: Optional[str]
    description: str
    cultural_significance: Optional[str]
    seasonal_availability: Optional[Dict[str, bool]]
    unit_of_measure: str
    tax_rate: Decimal
    discount_eligible: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class Customer:
    """Customer information"""
    customer_id: str
    tenant_id: str
    name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    loyalty_points: int
    total_purchases: Decimal
    preferred_language: str
    cultural_preferences: Dict[str, Any]
    payment_preferences: List[PaymentMethod]
    created_at: datetime
    last_purchase: Optional[datetime]

@dataclass
class TransactionItem:
    """Individual transaction item"""
    item_id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal
    discount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    voice_command: Optional[str]  # Original voice command

@dataclass
class Transaction:
    """Complete transaction record"""
    transaction_id: str
    tenant_id: str
    customer_id: Optional[str]
    cashier_id: str
    items: List[TransactionItem]
    subtotal: Decimal
    tax_total: Decimal
    discount_total: Decimal
    total_amount: Decimal
    payment_method: PaymentMethod
    payment_details: Dict[str, Any]
    status: TransactionStatus
    created_at: datetime
    completed_at: Optional[datetime]
    voice_interaction: bool
    cultural_context: Dict[str, Any]

class VoiceCommandProcessor:
    """Process voice commands for POS operations"""
    
    def __init__(self):
        self.command_patterns = self._initialize_command_patterns()
        self.supported_languages = [
            'en', 'sw', 'ha', 'yo', 'ig', 'am', 'om', 'ti', 'zu', 'xh', 'af', 'fr', 'ar'
        ]
    
    def _initialize_command_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize voice command patterns for different languages"""
        return {
            'en': {
                'add_item': [
                    'add {quantity} {item}',
                    'sell {quantity} {item}',
                    'I want to sell {quantity} {item}',
                    '{quantity} {item} please',
                    'give me {quantity} {item}'
                ],
                'remove_item': [
                    'remove {item}',
                    'cancel {item}',
                    'delete {item}'
                ],
                'complete_sale': [
                    'complete sale',
                    'finish transaction',
                    'checkout',
                    'total please'
                ],
                'payment': [
                    'payment by {method}',
                    'pay with {method}',
                    '{method} payment'
                ]
            },
            'sw': {  # Swahili
                'add_item': [
                    'ongeza {quantity} {item}',
                    'uza {quantity} {item}',
                    'nataka kuuza {quantity} {item}',
                    'nipe {quantity} {item}'
                ],
                'remove_item': [
                    'ondoa {item}',
                    'futa {item}'
                ],
                'complete_sale': [
                    'maliza mauzo',
                    'jumla tafadhali'
                ],
                'payment': [
                    'malipo kwa {method}',
                    'lipa kwa {method}'
                ]
            },
            'ha': {  # Hausa
                'add_item': [
                    'kara {quantity} {item}',
                    'sayar da {quantity} {item}',
                    'ina son sayar da {quantity} {item}'
                ],
                'remove_item': [
                    'cire {item}',
                    'share {item}'
                ],
                'complete_sale': [
                    'kammala sayarwa',
                    'jimla don Allah'
                ]
            }
        }
    
    def process_voice_command(self, command: str, language: str = 'en') -> Dict[str, Any]:
        """Process voice command and extract intent and entities"""
        try:
            command_lower = command.lower().strip()
            
            # Get patterns for language
            patterns = self.command_patterns.get(language, self.command_patterns['en'])
            
            # Try to match command patterns
            for intent, pattern_list in patterns.items():
                for pattern in pattern_list:
                    match_result = self._match_pattern(command_lower, pattern)
                    if match_result:
                        return {
                            'intent': intent,
                            'entities': match_result,
                            'original_command': command,
                            'language': language,
                            'confidence': 0.9  # High confidence for exact matches
                        }
            
            # If no exact match, use AI-powered NLU
            return self._ai_powered_nlu(command, language)
            
        except Exception as e:
            logger.error(f"Voice command processing failed: {str(e)}")
            return {
                'intent': 'unknown',
                'entities': {},
                'original_command': command,
                'language': language,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _match_pattern(self, command: str, pattern: str) -> Optional[Dict[str, str]]:
        """Match command against pattern and extract entities"""
        # Simple pattern matching - in production, use more sophisticated NLP
        import re
        
        # Convert pattern to regex
        regex_pattern = pattern.replace('{quantity}', r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)')
        regex_pattern = regex_pattern.replace('{item}', r'([a-zA-Z\s]+)')
        regex_pattern = regex_pattern.replace('{method}', r'(cash|mobile money|card|mpesa|airtel money)')
        
        match = re.search(regex_pattern, command, re.IGNORECASE)
        if match:
            groups = match.groups()
            entities = {}
            
            if '{quantity}' in pattern and len(groups) > 0:
                entities['quantity'] = self._parse_quantity(groups[0])
            
            if '{item}' in pattern and len(groups) > 1:
                entities['item'] = groups[1].strip()
            elif '{item}' in pattern and len(groups) == 1 and '{quantity}' not in pattern:
                entities['item'] = groups[0].strip()
            
            if '{method}' in pattern:
                method_group = groups[-1] if groups else None
                if method_group:
                    entities['method'] = self._normalize_payment_method(method_group)
            
            return entities
        
        return None
    
    def _parse_quantity(self, quantity_str: str) -> int:
        """Parse quantity from string"""
        quantity_map = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        if quantity_str.isdigit():
            return int(quantity_str)
        
        return quantity_map.get(quantity_str.lower(), 1)
    
    def _normalize_payment_method(self, method_str: str) -> str:
        """Normalize payment method string"""
        method_map = {
            'cash': 'cash',
            'mobile money': 'mobile_money',
            'mpesa': 'mobile_money',
            'airtel money': 'mobile_money',
            'card': 'card',
            'credit card': 'card',
            'debit card': 'card'
        }
        
        return method_map.get(method_str.lower(), 'cash')
    
    def _ai_powered_nlu(self, command: str, language: str) -> Dict[str, Any]:
        """Use AI for natural language understanding"""
        # This would integrate with Eden AI or Hugging Face for NLU
        # For now, return basic fallback
        return {
            'intent': 'unknown',
            'entities': {},
            'original_command': command,
            'language': language,
            'confidence': 0.3,
            'ai_processed': True
        }

class POSManager:
    """Main POS management system"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.products = {}
        self.customers = {}
        self.transactions = {}
        self.current_transaction = None
        self.voice_processor = VoiceCommandProcessor()
        self.cultural_adapter = CulturalAdapter()
        self.ai_assistant = POSAIAssistant()
        
    def add_product(self, product_data: Dict[str, Any]) -> Product:
        """Add new product to inventory"""
        try:
            product_id = str(uuid.uuid4())
            
            product = Product(
                product_id=product_id,
                tenant_id=self.tenant_id,
                name=product_data['name'],
                local_names=product_data.get('local_names', {}),
                category=ProductCategory(product_data['category']),
                price=Decimal(str(product_data['price'])),
                cost=Decimal(str(product_data.get('cost', 0))),
                stock_quantity=product_data['stock_quantity'],
                minimum_stock=product_data.get('minimum_stock', 5),
                barcode=product_data.get('barcode'),
                description=product_data.get('description', ''),
                cultural_significance=product_data.get('cultural_significance'),
                seasonal_availability=product_data.get('seasonal_availability'),
                unit_of_measure=product_data.get('unit_of_measure', 'piece'),
                tax_rate=Decimal(str(product_data.get('tax_rate', 0.16))),  # 16% VAT default
                discount_eligible=product_data.get('discount_eligible', True),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.products[product_id] = product
            
            logger.info(f"Added product {product.name} with ID {product_id}")
            return product
            
        except Exception as e:
            logger.error(f"Failed to add product: {str(e)}")
            raise POSException(f"Product addition failed: {str(e)}")
    
    def find_product_by_name(self, name: str, language: str = 'en') -> Optional[Product]:
        """Find product by name or local name"""
        name_lower = name.lower().strip()
        
        for product in self.products.values():
            # Check main name
            if product.name.lower() == name_lower:
                return product
            
            # Check local names
            for lang, local_name in product.local_names.items():
                if local_name.lower() == name_lower:
                    return product
            
            # Fuzzy matching for similar names
            if self._is_similar_name(product.name, name):
                return product
        
        return None
    
    def _is_similar_name(self, product_name: str, search_name: str) -> bool:
        """Check if names are similar (basic implementation)"""
        # Simple similarity check - in production, use more sophisticated matching
        product_words = set(product_name.lower().split())
        search_words = set(search_name.lower().split())
        
        # If any word matches, consider it similar
        return len(product_words.intersection(search_words)) > 0
    
    def process_voice_command(self, command: str, language: str = 'en', 
                            cashier_id: str = None) -> Dict[str, Any]:
        """Process voice command for POS operations"""
        try:
            # Process voice command
            command_result = self.voice_processor.process_voice_command(command, language)
            
            if command_result['confidence'] < 0.5:
                return {
                    'success': False,
                    'message': 'Could not understand the command',
                    'original_command': command,
                    'suggestions': self._get_command_suggestions(language)
                }
            
            # Execute command based on intent
            intent = command_result['intent']
            entities = command_result['entities']
            
            if intent == 'add_item':
                return self._handle_add_item_voice(entities, command, cashier_id)
            elif intent == 'remove_item':
                return self._handle_remove_item_voice(entities, command)
            elif intent == 'complete_sale':
                return self._handle_complete_sale_voice(entities, command)
            elif intent == 'payment':
                return self._handle_payment_voice(entities, command)
            else:
                return {
                    'success': False,
                    'message': f'Unknown command intent: {intent}',
                    'original_command': command
                }
                
        except Exception as e:
            logger.error(f"Voice command processing failed: {str(e)}")
            return {
                'success': False,
                'message': 'Voice command processing failed',
                'error': str(e),
                'original_command': command
            }
    
    def _handle_add_item_voice(self, entities: Dict[str, Any], 
                              original_command: str, cashier_id: str) -> Dict[str, Any]:
        """Handle add item voice command"""
        try:
            item_name = entities.get('item', '').strip()
            quantity = entities.get('quantity', 1)
            
            if not item_name:
                return {
                    'success': False,
                    'message': 'Product name not specified',
                    'original_command': original_command
                }
            
            # Find product
            product = self.find_product_by_name(item_name)
            if not product:
                # Use AI to suggest similar products
                suggestions = self.ai_assistant.suggest_similar_products(item_name, list(self.products.values()))
                return {
                    'success': False,
                    'message': f'Product "{item_name}" not found',
                    'suggestions': suggestions,
                    'original_command': original_command
                }
            
            # Check stock
            if product.stock_quantity < quantity:
                return {
                    'success': False,
                    'message': f'Insufficient stock. Available: {product.stock_quantity}',
                    'available_quantity': product.stock_quantity,
                    'original_command': original_command
                }
            
            # Add to current transaction
            result = self.add_item_to_transaction(product.product_id, quantity, cashier_id, original_command)
            
            return {
                'success': True,
                'message': f'Added {quantity} {product.name} to cart',
                'product': asdict(product),
                'quantity': quantity,
                'transaction_total': str(self.current_transaction.total_amount) if self.current_transaction else '0',
                'original_command': original_command
            }
            
        except Exception as e:
            logger.error(f"Add item voice command failed: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to add item',
                'error': str(e),
                'original_command': original_command
            }
    
    def add_item_to_transaction(self, product_id: str, quantity: int, 
                               cashier_id: str, voice_command: str = None) -> Dict[str, Any]:
        """Add item to current transaction"""
        try:
            product = self.products.get(product_id)
            if not product:
                raise POSException(f"Product {product_id} not found")
            
            # Create new transaction if none exists
            if not self.current_transaction:
                self.current_transaction = Transaction(
                    transaction_id=str(uuid.uuid4()),
                    tenant_id=self.tenant_id,
                    customer_id=None,
                    cashier_id=cashier_id,
                    items=[],
                    subtotal=Decimal('0'),
                    tax_total=Decimal('0'),
                    discount_total=Decimal('0'),
                    total_amount=Decimal('0'),
                    payment_method=PaymentMethod.CASH,
                    payment_details={},
                    status=TransactionStatus.PENDING,
                    created_at=datetime.utcnow(),
                    completed_at=None,
                    voice_interaction=bool(voice_command),
                    cultural_context={}
                )
            
            # Calculate amounts
            unit_price = product.price
            discount = Decimal('0')  # Apply discount logic here
            tax_amount = (unit_price * quantity * product.tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_amount = (unit_price * quantity - discount + tax_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Create transaction item
            item = TransactionItem(
                item_id=str(uuid.uuid4()),
                product_id=product_id,
                product_name=product.name,
                quantity=quantity,
                unit_price=unit_price,
                discount=discount,
                tax_amount=tax_amount,
                total_amount=total_amount,
                voice_command=voice_command
            )
            
            # Add to transaction
            self.current_transaction.items.append(item)
            
            # Update transaction totals
            self._update_transaction_totals()
            
            # Update product stock
            product.stock_quantity -= quantity
            product.updated_at = datetime.utcnow()
            
            logger.info(f"Added {quantity} {product.name} to transaction {self.current_transaction.transaction_id}")
            
            return {
                'success': True,
                'item': asdict(item),
                'transaction_total': str(self.current_transaction.total_amount)
            }
            
        except Exception as e:
            logger.error(f"Failed to add item to transaction: {str(e)}")
            raise POSException(f"Add item failed: {str(e)}")
    
    def _update_transaction_totals(self):
        """Update transaction totals"""
        if not self.current_transaction:
            return
        
        subtotal = sum(item.unit_price * item.quantity - item.discount for item in self.current_transaction.items)
        tax_total = sum(item.tax_amount for item in self.current_transaction.items)
        discount_total = sum(item.discount for item in self.current_transaction.items)
        total_amount = subtotal + tax_total
        
        self.current_transaction.subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.current_transaction.tax_total = tax_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.current_transaction.discount_total = discount_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.current_transaction.total_amount = total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def complete_transaction(self, payment_method: PaymentMethod, 
                           payment_details: Dict[str, Any]) -> Transaction:
        """Complete current transaction"""
        try:
            if not self.current_transaction:
                raise POSException("No active transaction")
            
            if not self.current_transaction.items:
                raise POSException("Transaction has no items")
            
            # Update payment information
            self.current_transaction.payment_method = payment_method
            self.current_transaction.payment_details = payment_details
            self.current_transaction.status = TransactionStatus.COMPLETED
            self.current_transaction.completed_at = datetime.utcnow()
            
            # Store completed transaction
            self.transactions[self.current_transaction.transaction_id] = self.current_transaction
            
            # Generate receipt
            receipt = self._generate_receipt(self.current_transaction)
            
            # Clear current transaction
            completed_transaction = self.current_transaction
            self.current_transaction = None
            
            logger.info(f"Completed transaction {completed_transaction.transaction_id}")
            
            return completed_transaction
            
        except Exception as e:
            logger.error(f"Failed to complete transaction: {str(e)}")
            raise POSException(f"Transaction completion failed: {str(e)}")
    
    def _generate_receipt(self, transaction: Transaction) -> Dict[str, Any]:
        """Generate receipt for transaction"""
        receipt = {
            'transaction_id': transaction.transaction_id,
            'date': transaction.completed_at.isoformat(),
            'cashier_id': transaction.cashier_id,
            'items': [
                {
                    'name': item.product_name,
                    'quantity': item.quantity,
                    'unit_price': str(item.unit_price),
                    'total': str(item.total_amount)
                }
                for item in transaction.items
            ],
            'subtotal': str(transaction.subtotal),
            'tax': str(transaction.tax_total),
            'total': str(transaction.total_amount),
            'payment_method': transaction.payment_method.value,
            'voice_interaction': transaction.voice_interaction
        }
        
        return receipt
    
    def get_sales_analytics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get sales analytics for date range"""
        try:
            relevant_transactions = [
                t for t in self.transactions.values()
                if t.status == TransactionStatus.COMPLETED
                and start_date <= t.completed_at <= end_date
            ]
            
            total_sales = sum(t.total_amount for t in relevant_transactions)
            total_transactions = len(relevant_transactions)
            voice_transactions = sum(1 for t in relevant_transactions if t.voice_interaction)
            
            # Product analytics
            product_sales = {}
            for transaction in relevant_transactions:
                for item in transaction.items:
                    if item.product_id not in product_sales:
                        product_sales[item.product_id] = {
                            'name': item.product_name,
                            'quantity_sold': 0,
                            'revenue': Decimal('0')
                        }
                    product_sales[item.product_id]['quantity_sold'] += item.quantity
                    product_sales[item.product_id]['revenue'] += item.total_amount
            
            # Top selling products
            top_products = sorted(
                product_sales.items(),
                key=lambda x: x[1]['quantity_sold'],
                reverse=True
            )[:10]
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'summary': {
                    'total_sales': str(total_sales),
                    'total_transactions': total_transactions,
                    'voice_transactions': voice_transactions,
                    'voice_percentage': (voice_transactions / total_transactions * 100) if total_transactions > 0 else 0,
                    'average_transaction': str(total_sales / total_transactions) if total_transactions > 0 else '0'
                },
                'top_products': [
                    {
                        'product_id': pid,
                        'name': data['name'],
                        'quantity_sold': data['quantity_sold'],
                        'revenue': str(data['revenue'])
                    }
                    for pid, data in top_products
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get sales analytics: {str(e)}")
            raise POSException(f"Sales analytics failed: {str(e)}")
    
    def _get_command_suggestions(self, language: str) -> List[str]:
        """Get command suggestions for language"""
        patterns = self.voice_processor.command_patterns.get(language, self.voice_processor.command_patterns['en'])
        suggestions = []
        
        for intent, pattern_list in patterns.items():
            suggestions.extend(pattern_list[:2])  # Take first 2 patterns per intent
        
        return suggestions[:5]  # Return top 5 suggestions

class CulturalAdapter:
    """Adapt POS system for African cultural contexts"""
    
    def __init__(self):
        self.cultural_contexts = self._initialize_cultural_contexts()
    
    def _initialize_cultural_contexts(self) -> Dict[str, Dict[str, Any]]:
        """Initialize cultural adaptation contexts"""
        return {
            'west_africa': {
                'preferred_payment_methods': ['mobile_money', 'cash'],
                'bargaining_culture': True,
                'community_discounts': True,
                'seasonal_products': ['palm_oil', 'yam', 'cassava'],
                'greeting_importance': True
            },
            'east_africa': {
                'preferred_payment_methods': ['mobile_money', 'cash'],
                'livestock_trading': True,
                'cooperative_purchasing': True,
                'seasonal_products': ['coffee', 'tea', 'maize'],
                'ubuntu_philosophy': True
            },
            'southern_africa': {
                'preferred_payment_methods': ['card', 'mobile_money', 'cash'],
                'mining_community_focus': True,
                'traditional_crafts': True,
                'seasonal_products': ['maize', 'sorghum', 'cattle'],
                'multilingual_support': True
            }
        }
    
    def adapt_for_region(self, region: str, pos_config: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt POS configuration for specific region"""
        cultural_context = self.cultural_contexts.get(region, {})
        
        adapted_config = pos_config.copy()
        
        # Adapt payment methods
        if 'preferred_payment_methods' in cultural_context:
            adapted_config['payment_methods'] = cultural_context['preferred_payment_methods']
        
        # Enable bargaining if culturally appropriate
        if cultural_context.get('bargaining_culture'):
            adapted_config['enable_bargaining'] = True
            adapted_config['discount_flexibility'] = 0.15  # 15% discount flexibility
        
        # Community features
        if cultural_context.get('community_discounts'):
            adapted_config['community_discount_rate'] = 0.05  # 5% community discount
        
        return adapted_config

class POSAIAssistant:
    """AI assistant for POS operations"""
    
    def __init__(self):
        self.product_similarity_threshold = 0.7
    
    def suggest_similar_products(self, search_term: str, products: List[Product]) -> List[Dict[str, Any]]:
        """Suggest similar products when exact match not found"""
        suggestions = []
        search_lower = search_term.lower()
        
        for product in products:
            # Simple similarity scoring
            score = self._calculate_similarity(search_lower, product.name.lower())
            
            # Check local names too
            for lang, local_name in product.local_names.items():
                local_score = self._calculate_similarity(search_lower, local_name.lower())
                score = max(score, local_score)
            
            if score > self.product_similarity_threshold:
                suggestions.append({
                    'product_id': product.product_id,
                    'name': product.name,
                    'similarity_score': score,
                    'price': str(product.price),
                    'stock': product.stock_quantity
                })
        
        # Sort by similarity score
        suggestions.sort(key=lambda x: x['similarity_score'], reverse=True)
        return suggestions[:5]  # Return top 5 suggestions
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings"""
        # Simple Jaccard similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def predict_demand(self, product_id: str, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict product demand based on historical data"""
        # Simple demand prediction - in production, use more sophisticated ML
        if not historical_data:
            return {'predicted_demand': 0, 'confidence': 0.0}
        
        recent_sales = [d['quantity'] for d in historical_data[-30:]]  # Last 30 records
        avg_demand = sum(recent_sales) / len(recent_sales) if recent_sales else 0
        
        return {
            'predicted_demand': int(avg_demand * 1.1),  # 10% buffer
            'confidence': 0.7,
            'recommendation': 'reorder' if avg_demand > 5 else 'monitor'
        }

class POSException(Exception):
    """Custom POS exception"""
    pass

# Example usage and testing
def create_sample_pos_system():
    """Create sample POS system for testing"""
    pos = POSManager("tenant_123")
    
    # Add sample products
    products_data = [
        {
            'name': 'Sugar Packet',
            'local_names': {'sw': 'Sukari', 'ha': 'Sukari'},
            'category': 'food_beverage',
            'price': 2.50,
            'cost': 2.00,
            'stock_quantity': 100,
            'minimum_stock': 10,
            'description': '1kg sugar packet',
            'unit_of_measure': 'packet'
        },
        {
            'name': 'Rice Bag',
            'local_names': {'sw': 'Mchele', 'ha': 'Shinkafa'},
            'category': 'food_beverage',
            'price': 25.00,
            'cost': 20.00,
            'stock_quantity': 50,
            'minimum_stock': 5,
            'description': '5kg rice bag',
            'unit_of_measure': 'bag'
        }
    ]
    
    for product_data in products_data:
        pos.add_product(product_data)
    
    return pos

# Initialize POS system
pos_system = create_sample_pos_system()

