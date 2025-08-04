"""
WebWaka Customer Relationship Management (CRM) System
AI-powered CRM with predictive analytics and African cultural adaptation
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

class CustomerStatus(Enum):
    """Customer status types"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"
    LEAD = "lead"
    VIP = "vip"
    CHURNED = "churned"

class InteractionType(Enum):
    """Customer interaction types"""
    PHONE_CALL = "phone_call"
    EMAIL = "email"
    MEETING = "meeting"
    VOICE_COMMAND = "voice_command"
    WHATSAPP = "whatsapp"
    SMS = "sms"
    VISIT = "visit"
    COMPLAINT = "complaint"
    SUPPORT = "support"

class LeadSource(Enum):
    """Lead source types"""
    REFERRAL = "referral"
    SOCIAL_MEDIA = "social_media"
    WEBSITE = "website"
    COLD_CALL = "cold_call"
    COMMUNITY_EVENT = "community_event"
    WORD_OF_MOUTH = "word_of_mouth"
    TRADITIONAL_MEDIA = "traditional_media"

class OpportunityStage(Enum):
    """Sales opportunity stages"""
    QUALIFICATION = "qualification"
    NEEDS_ANALYSIS = "needs_analysis"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

@dataclass
class Customer:
    """Customer information with African cultural context"""
    customer_id: str
    tenant_id: str
    first_name: str
    last_name: str
    local_name: Optional[str]
    title: Optional[str]
    company: Optional[str]
    phone: str
    email: Optional[str]
    address: str
    city: str
    region: str
    country: str
    preferred_language: str
    cultural_background: Dict[str, Any]
    status: CustomerStatus
    customer_since: datetime
    last_interaction: Optional[datetime]
    total_value: Decimal
    lifetime_value: Decimal
    loyalty_score: float
    satisfaction_score: float
    preferred_contact_method: str
    family_size: Optional[int]
    occupation: Optional[str]
    income_level: Optional[str]
    community_role: Optional[str]
    referral_source: Optional[str]
    tags: List[str]
    notes: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Interaction:
    """Customer interaction record"""
    interaction_id: str
    tenant_id: str
    customer_id: str
    interaction_type: InteractionType
    subject: str
    description: str
    outcome: str
    duration_minutes: Optional[int]
    performed_by: str
    scheduled_at: Optional[datetime]
    completed_at: datetime
    follow_up_required: bool
    follow_up_date: Optional[datetime]
    voice_transcript: Optional[str]
    sentiment_score: Optional[float]
    cultural_context: Dict[str, Any]
    created_at: datetime

@dataclass
class Lead:
    """Sales lead information"""
    lead_id: str
    tenant_id: str
    first_name: str
    last_name: str
    company: Optional[str]
    phone: str
    email: Optional[str]
    source: LeadSource
    status: str
    score: int
    interest_level: str
    budget: Optional[Decimal]
    timeline: Optional[str]
    assigned_to: str
    created_at: datetime
    last_contacted: Optional[datetime]
    converted_at: Optional[datetime]
    conversion_value: Optional[Decimal]

@dataclass
class Opportunity:
    """Sales opportunity"""
    opportunity_id: str
    tenant_id: str
    customer_id: str
    name: str
    description: str
    value: Decimal
    probability: float
    stage: OpportunityStage
    expected_close_date: datetime
    actual_close_date: Optional[datetime]
    assigned_to: str
    products_services: List[str]
    competitors: List[str]
    next_steps: str
    created_at: datetime
    updated_at: datetime

class VoiceCRMProcessor:
    """Process voice commands for CRM operations"""
    
    def __init__(self):
        self.command_patterns = self._initialize_crm_commands()
    
    def _initialize_crm_commands(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize CRM voice command patterns"""
        return {
            'en': {
                'create_customer': [
                    'create customer {name}',
                    'add new customer {name}',
                    'register customer {name}'
                ],
                'find_customer': [
                    'find customer {name}',
                    'search for {name}',
                    'show me {name}'
                ],
                'log_interaction': [
                    'log call with {name}',
                    'record meeting with {name}',
                    'note interaction with {name}'
                ],
                'schedule_followup': [
                    'schedule follow up with {name}',
                    'remind me to call {name}',
                    'set reminder for {name}'
                ]
            },
            'sw': {  # Swahili
                'create_customer': [
                    'unda mteja {name}',
                    'ongeza mteja mpya {name}'
                ],
                'find_customer': [
                    'tafuta mteja {name}',
                    'nionyeshe {name}'
                ],
                'log_interaction': [
                    'rekodi mazungumzo na {name}',
                    'andika mkutano na {name}'
                ]
            }
        }
    
    def process_voice_command(self, command: str, language: str = 'en') -> Dict[str, Any]:
        """Process CRM voice command"""
        try:
            command_lower = command.lower().strip()
            patterns = self.command_patterns.get(language, self.command_patterns['en'])
            
            for intent, pattern_list in patterns.items():
                for pattern in pattern_list:
                    match_result = self._match_crm_pattern(command_lower, pattern)
                    if match_result:
                        return {
                            'intent': intent,
                            'entities': match_result,
                            'original_command': command,
                            'language': language,
                            'confidence': 0.9
                        }
            
            return self._ai_powered_crm_nlu(command, language)
            
        except Exception as e:
            logger.error(f"CRM voice command processing failed: {str(e)}")
            return {
                'intent': 'unknown',
                'entities': {},
                'error': str(e)
            }
    
    def _match_crm_pattern(self, command: str, pattern: str) -> Optional[Dict[str, str]]:
        """Match CRM command pattern"""
        import re
        
        regex_pattern = pattern.replace('{name}', r'([a-zA-Z\s]+)')
        match = re.search(regex_pattern, command, re.IGNORECASE)
        
        if match:
            return {'name': match.group(1).strip()}
        
        return None
    
    def _ai_powered_crm_nlu(self, command: str, language: str) -> Dict[str, Any]:
        """AI-powered CRM natural language understanding"""
        return {
            'intent': 'unknown',
            'entities': {},
            'original_command': command,
            'language': language,
            'confidence': 0.3,
            'ai_processed': True
        }

class CRMAnalytics:
    """CRM analytics and predictive modeling"""
    
    def __init__(self):
        self.churn_indicators = [
            'decreased_interaction_frequency',
            'negative_sentiment',
            'payment_delays',
            'competitor_mentions',
            'reduced_purchase_value'
        ]
    
    def calculate_customer_lifetime_value(self, customer: Customer, 
                                        interactions: List[Interaction],
                                        purchases: List[Dict[str, Any]]) -> Decimal:
        """Calculate customer lifetime value"""
        try:
            if not purchases:
                return Decimal('0')
            
            # Calculate average purchase value
            total_value = sum(Decimal(str(p.get('amount', 0))) for p in purchases)
            avg_purchase_value = total_value / len(purchases)
            
            # Calculate purchase frequency (purchases per month)
            if len(purchases) < 2:
                purchase_frequency = 1
            else:
                first_purchase = min(p['date'] for p in purchases)
                last_purchase = max(p['date'] for p in purchases)
                months_active = max(1, (last_purchase - first_purchase).days / 30)
                purchase_frequency = len(purchases) / months_active
            
            # Estimate customer lifespan based on interaction patterns
            avg_lifespan_months = self._estimate_customer_lifespan(customer, interactions)
            
            # CLV = Average Purchase Value × Purchase Frequency × Customer Lifespan
            clv = avg_purchase_value * Decimal(str(purchase_frequency)) * Decimal(str(avg_lifespan_months))
            
            return clv.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        except Exception as e:
            logger.error(f"CLV calculation failed: {str(e)}")
            return Decimal('0')
    
    def _estimate_customer_lifespan(self, customer: Customer, 
                                   interactions: List[Interaction]) -> float:
        """Estimate customer lifespan in months"""
        # Base lifespan by customer status
        base_lifespan = {
            CustomerStatus.VIP: 36,
            CustomerStatus.ACTIVE: 24,
            CustomerStatus.INACTIVE: 12,
            CustomerStatus.PROSPECT: 6,
            CustomerStatus.LEAD: 3
        }
        
        lifespan = base_lifespan.get(customer.status, 12)
        
        # Adjust based on interaction frequency
        if interactions:
            recent_interactions = [
                i for i in interactions 
                if i.completed_at > datetime.utcnow() - timedelta(days=90)
            ]
            
            if len(recent_interactions) > 10:
                lifespan *= 1.5  # High engagement
            elif len(recent_interactions) < 2:
                lifespan *= 0.7  # Low engagement
        
        # Adjust based on satisfaction score
        if customer.satisfaction_score > 4.0:
            lifespan *= 1.3
        elif customer.satisfaction_score < 2.0:
            lifespan *= 0.5
        
        return lifespan
    
    def predict_churn_risk(self, customer: Customer, 
                          interactions: List[Interaction],
                          purchases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict customer churn risk"""
        try:
            risk_score = 0.0
            risk_factors = []
            
            # Check interaction frequency
            recent_interactions = [
                i for i in interactions 
                if i.completed_at > datetime.utcnow() - timedelta(days=60)
            ]
            
            if len(recent_interactions) == 0:
                risk_score += 0.3
                risk_factors.append('no_recent_interactions')
            elif len(recent_interactions) < 2:
                risk_score += 0.2
                risk_factors.append('low_interaction_frequency')
            
            # Check purchase recency
            if purchases:
                last_purchase = max(p['date'] for p in purchases)
                days_since_purchase = (datetime.utcnow() - last_purchase).days
                
                if days_since_purchase > 90:
                    risk_score += 0.25
                    risk_factors.append('no_recent_purchases')
                elif days_since_purchase > 60:
                    risk_score += 0.15
                    risk_factors.append('declining_purchase_frequency')
            else:
                risk_score += 0.4
                risk_factors.append('no_purchases')
            
            # Check sentiment trends
            recent_sentiment = [
                i.sentiment_score for i in recent_interactions 
                if i.sentiment_score is not None
            ]
            
            if recent_sentiment:
                avg_sentiment = sum(recent_sentiment) / len(recent_sentiment)
                if avg_sentiment < 0.3:
                    risk_score += 0.2
                    risk_factors.append('negative_sentiment')
            
            # Check satisfaction score
            if customer.satisfaction_score < 2.5:
                risk_score += 0.15
                risk_factors.append('low_satisfaction')
            
            # Determine risk level
            if risk_score >= 0.7:
                risk_level = 'high'
            elif risk_score >= 0.4:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            return {
                'customer_id': customer.customer_id,
                'risk_score': min(risk_score, 1.0),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': self._generate_retention_recommendations(risk_factors)
            }
            
        except Exception as e:
            logger.error(f"Churn prediction failed: {str(e)}")
            return {
                'customer_id': customer.customer_id,
                'risk_score': 0.0,
                'risk_level': 'unknown',
                'error': str(e)
            }
    
    def _generate_retention_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate customer retention recommendations"""
        recommendations = []
        
        if 'no_recent_interactions' in risk_factors:
            recommendations.append('Schedule immediate check-in call')
            recommendations.append('Send personalized re-engagement campaign')
        
        if 'no_recent_purchases' in risk_factors:
            recommendations.append('Offer special discount or promotion')
            recommendations.append('Recommend relevant products/services')
        
        if 'negative_sentiment' in risk_factors:
            recommendations.append('Address customer concerns immediately')
            recommendations.append('Assign dedicated account manager')
        
        if 'low_satisfaction' in risk_factors:
            recommendations.append('Conduct satisfaction survey')
            recommendations.append('Implement service recovery plan')
        
        return recommendations

class CRMManager:
    """Main CRM management system"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.customers = {}
        self.interactions = {}
        self.leads = {}
        self.opportunities = {}
        self.voice_processor = VoiceCRMProcessor()
        self.analytics = CRMAnalytics()
        self.cultural_adapter = AfricanCRMAdapter()
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """Create new customer"""
        try:
            customer_id = str(uuid.uuid4())
            
            customer = Customer(
                customer_id=customer_id,
                tenant_id=self.tenant_id,
                first_name=customer_data['first_name'],
                last_name=customer_data['last_name'],
                local_name=customer_data.get('local_name'),
                title=customer_data.get('title'),
                company=customer_data.get('company'),
                phone=customer_data['phone'],
                email=customer_data.get('email'),
                address=customer_data.get('address', ''),
                city=customer_data.get('city', ''),
                region=customer_data.get('region', ''),
                country=customer_data.get('country', ''),
                preferred_language=customer_data.get('preferred_language', 'en'),
                cultural_background=customer_data.get('cultural_background', {}),
                status=CustomerStatus(customer_data.get('status', 'prospect')),
                customer_since=datetime.utcnow(),
                last_interaction=None,
                total_value=Decimal('0'),
                lifetime_value=Decimal('0'),
                loyalty_score=0.0,
                satisfaction_score=5.0,  # Default neutral score
                preferred_contact_method=customer_data.get('preferred_contact_method', 'phone'),
                family_size=customer_data.get('family_size'),
                occupation=customer_data.get('occupation'),
                income_level=customer_data.get('income_level'),
                community_role=customer_data.get('community_role'),
                referral_source=customer_data.get('referral_source'),
                tags=customer_data.get('tags', []),
                notes=customer_data.get('notes', ''),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.customers[customer_id] = customer
            
            # Apply cultural adaptations
            self.cultural_adapter.adapt_customer_profile(customer)
            
            logger.info(f"Created customer {customer.first_name} {customer.last_name} with ID {customer_id}")
            return customer
            
        except Exception as e:
            logger.error(f"Customer creation failed: {str(e)}")
            raise CRMException(f"Customer creation failed: {str(e)}")
    
    def log_interaction(self, interaction_data: Dict[str, Any]) -> Interaction:
        """Log customer interaction"""
        try:
            interaction_id = str(uuid.uuid4())
            
            interaction = Interaction(
                interaction_id=interaction_id,
                tenant_id=self.tenant_id,
                customer_id=interaction_data['customer_id'],
                interaction_type=InteractionType(interaction_data['interaction_type']),
                subject=interaction_data['subject'],
                description=interaction_data['description'],
                outcome=interaction_data.get('outcome', ''),
                duration_minutes=interaction_data.get('duration_minutes'),
                performed_by=interaction_data['performed_by'],
                scheduled_at=interaction_data.get('scheduled_at'),
                completed_at=interaction_data.get('completed_at', datetime.utcnow()),
                follow_up_required=interaction_data.get('follow_up_required', False),
                follow_up_date=interaction_data.get('follow_up_date'),
                voice_transcript=interaction_data.get('voice_transcript'),
                sentiment_score=interaction_data.get('sentiment_score'),
                cultural_context=interaction_data.get('cultural_context', {}),
                created_at=datetime.utcnow()
            )
            
            self.interactions[interaction_id] = interaction
            
            # Update customer last interaction
            customer = self.customers.get(interaction.customer_id)
            if customer:
                customer.last_interaction = interaction.completed_at
                customer.updated_at = datetime.utcnow()
            
            logger.info(f"Logged interaction {interaction_id} for customer {interaction.customer_id}")
            return interaction
            
        except Exception as e:
            logger.error(f"Interaction logging failed: {str(e)}")
            raise CRMException(f"Interaction logging failed: {str(e)}")
    
    def process_voice_command(self, command: str, language: str = 'en',
                             user_id: str = None) -> Dict[str, Any]:
        """Process voice command for CRM operations"""
        try:
            command_result = self.voice_processor.process_voice_command(command, language)
            
            if command_result['confidence'] < 0.5:
                return {
                    'success': False,
                    'message': 'Could not understand the CRM command',
                    'original_command': command
                }
            
            intent = command_result['intent']
            entities = command_result['entities']
            
            if intent == 'find_customer':
                return self._handle_find_customer_voice(entities, command)
            elif intent == 'create_customer':
                return self._handle_create_customer_voice(entities, command, user_id)
            elif intent == 'log_interaction':
                return self._handle_log_interaction_voice(entities, command, user_id)
            elif intent == 'schedule_followup':
                return self._handle_schedule_followup_voice(entities, command, user_id)
            else:
                return {
                    'success': False,
                    'message': f'Unknown CRM command: {intent}',
                    'original_command': command
                }
                
        except Exception as e:
            logger.error(f"CRM voice command processing failed: {str(e)}")
            return {
                'success': False,
                'message': 'CRM voice command processing failed',
                'error': str(e)
            }
    
    def _handle_find_customer_voice(self, entities: Dict[str, Any], 
                                   original_command: str) -> Dict[str, Any]:
        """Handle find customer voice command"""
        try:
            name = entities.get('name', '').strip()
            if not name:
                return {
                    'success': False,
                    'message': 'Customer name not specified',
                    'original_command': original_command
                }
            
            # Search customers by name
            matching_customers = []
            name_lower = name.lower()
            
            for customer in self.customers.values():
                full_name = f"{customer.first_name} {customer.last_name}".lower()
                if (name_lower in full_name or 
                    (customer.local_name and name_lower in customer.local_name.lower())):
                    matching_customers.append(customer)
            
            if not matching_customers:
                return {
                    'success': False,
                    'message': f'No customers found matching "{name}"',
                    'original_command': original_command
                }
            
            return {
                'success': True,
                'message': f'Found {len(matching_customers)} customer(s)',
                'customers': [asdict(c) for c in matching_customers],
                'original_command': original_command
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'Customer search failed',
                'error': str(e)
            }
    
    def create_opportunity(self, opportunity_data: Dict[str, Any]) -> Opportunity:
        """Create sales opportunity"""
        try:
            opportunity_id = str(uuid.uuid4())
            
            opportunity = Opportunity(
                opportunity_id=opportunity_id,
                tenant_id=self.tenant_id,
                customer_id=opportunity_data['customer_id'],
                name=opportunity_data['name'],
                description=opportunity_data.get('description', ''),
                value=Decimal(str(opportunity_data['value'])),
                probability=opportunity_data.get('probability', 0.5),
                stage=OpportunityStage(opportunity_data.get('stage', 'qualification')),
                expected_close_date=opportunity_data['expected_close_date'],
                actual_close_date=None,
                assigned_to=opportunity_data['assigned_to'],
                products_services=opportunity_data.get('products_services', []),
                competitors=opportunity_data.get('competitors', []),
                next_steps=opportunity_data.get('next_steps', ''),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.opportunities[opportunity_id] = opportunity
            
            logger.info(f"Created opportunity {opportunity.name} with ID {opportunity_id}")
            return opportunity
            
        except Exception as e:
            logger.error(f"Opportunity creation failed: {str(e)}")
            raise CRMException(f"Opportunity creation failed: {str(e)}")
    
    def get_customer_analytics(self, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive customer analytics"""
        try:
            customer = self.customers.get(customer_id)
            if not customer:
                raise CRMException(f"Customer {customer_id} not found")
            
            # Get customer interactions
            customer_interactions = [
                i for i in self.interactions.values() 
                if i.customer_id == customer_id
            ]
            
            # Get customer opportunities
            customer_opportunities = [
                o for o in self.opportunities.values() 
                if o.customer_id == customer_id
            ]
            
            # Mock purchase data (would come from sales system)
            purchases = []  # This would be populated from actual sales data
            
            # Calculate CLV
            clv = self.analytics.calculate_customer_lifetime_value(
                customer, customer_interactions, purchases
            )
            
            # Predict churn risk
            churn_risk = self.analytics.predict_churn_risk(
                customer, customer_interactions, purchases
            )
            
            # Interaction analytics
            interaction_stats = self._calculate_interaction_stats(customer_interactions)
            
            return {
                'customer': asdict(customer),
                'lifetime_value': str(clv),
                'churn_risk': churn_risk,
                'interaction_stats': interaction_stats,
                'opportunities_count': len(customer_opportunities),
                'total_opportunity_value': str(sum(o.value for o in customer_opportunities)),
                'last_interaction_days': (datetime.utcnow() - customer.last_interaction).days if customer.last_interaction else None
            }
            
        except Exception as e:
            logger.error(f"Customer analytics failed: {str(e)}")
            raise CRMException(f"Customer analytics failed: {str(e)}")
    
    def _calculate_interaction_stats(self, interactions: List[Interaction]) -> Dict[str, Any]:
        """Calculate interaction statistics"""
        if not interactions:
            return {
                'total_interactions': 0,
                'avg_sentiment': 0.0,
                'interaction_types': {},
                'monthly_frequency': 0.0
            }
        
        # Count by type
        type_counts = {}
        for interaction in interactions:
            interaction_type = interaction.interaction_type.value
            type_counts[interaction_type] = type_counts.get(interaction_type, 0) + 1
        
        # Calculate average sentiment
        sentiments = [i.sentiment_score for i in interactions if i.sentiment_score is not None]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        
        # Calculate monthly frequency
        if len(interactions) > 1:
            first_interaction = min(i.completed_at for i in interactions)
            last_interaction = max(i.completed_at for i in interactions)
            months = max(1, (last_interaction - first_interaction).days / 30)
            monthly_frequency = len(interactions) / months
        else:
            monthly_frequency = 1.0
        
        return {
            'total_interactions': len(interactions),
            'avg_sentiment': avg_sentiment,
            'interaction_types': type_counts,
            'monthly_frequency': monthly_frequency
        }
    
    def get_crm_dashboard(self) -> Dict[str, Any]:
        """Get CRM dashboard data"""
        try:
            total_customers = len(self.customers)
            active_customers = len([c for c in self.customers.values() if c.status == CustomerStatus.ACTIVE])
            total_opportunities = len(self.opportunities)
            pipeline_value = sum(o.value for o in self.opportunities.values() if o.stage != OpportunityStage.CLOSED_LOST)
            
            # Recent interactions
            recent_interactions = sorted(
                self.interactions.values(),
                key=lambda x: x.completed_at,
                reverse=True
            )[:10]
            
            # Top customers by value
            top_customers = sorted(
                self.customers.values(),
                key=lambda x: x.total_value,
                reverse=True
            )[:10]
            
            return {
                'summary': {
                    'total_customers': total_customers,
                    'active_customers': active_customers,
                    'total_opportunities': total_opportunities,
                    'pipeline_value': str(pipeline_value)
                },
                'recent_interactions': [asdict(i) for i in recent_interactions],
                'top_customers': [
                    {
                        'customer_id': c.customer_id,
                        'name': f"{c.first_name} {c.last_name}",
                        'total_value': str(c.total_value),
                        'status': c.status.value
                    }
                    for c in top_customers
                ]
            }
            
        except Exception as e:
            logger.error(f"CRM dashboard generation failed: {str(e)}")
            raise CRMException(f"CRM dashboard generation failed: {str(e)}")

class AfricanCRMAdapter:
    """Adapt CRM for African cultural contexts"""
    
    def __init__(self):
        self.cultural_contexts = self._initialize_cultural_contexts()
    
    def _initialize_cultural_contexts(self) -> Dict[str, Dict[str, Any]]:
        """Initialize African cultural contexts"""
        return {
            'ubuntu_philosophy': {
                'community_focus': True,
                'relationship_priority': True,
                'collective_decision_making': True,
                'extended_family_influence': True
            },
            'respect_hierarchy': {
                'elder_respect': True,
                'title_importance': True,
                'formal_greetings': True,
                'authority_recognition': True
            },
            'communication_style': {
                'indirect_communication': True,
                'story_telling': True,
                'proverb_usage': True,
                'patience_valued': True
            }
        }
    
    def adapt_customer_profile(self, customer: Customer):
        """Adapt customer profile for African context"""
        # Add cultural context fields
        if not customer.cultural_background:
            customer.cultural_background = {}
        
        # Set default cultural preferences
        customer.cultural_background.setdefault('greeting_style', 'formal')
        customer.cultural_background.setdefault('decision_making', 'consultative')
        customer.cultural_background.setdefault('communication_preference', 'relationship_first')
        
        # Adjust interaction approach based on region
        if customer.country.lower() in ['south africa', 'botswana', 'namibia']:
            customer.cultural_background['ubuntu_influence'] = True
        
        if customer.community_role in ['elder', 'chief', 'leader']:
            customer.cultural_background['high_respect_required'] = True

class CRMException(Exception):
    """Custom CRM exception"""
    pass

# Example usage and testing
def create_sample_crm_system():
    """Create sample CRM system for testing"""
    crm = CRMManager("tenant_123")
    
    # Add sample customers
    customers_data = [
        {
            'first_name': 'Amara',
            'last_name': 'Okafor',
            'local_name': 'Mama Amara',
            'phone': '+234801234567',
            'email': 'amara@example.com',
            'city': 'Lagos',
            'country': 'Nigeria',
            'preferred_language': 'en',
            'status': 'active',
            'occupation': 'Small Business Owner',
            'community_role': 'Women\'s Group Leader'
        },
        {
            'first_name': 'Kwame',
            'last_name': 'Asante',
            'phone': '+233241234567',
            'city': 'Accra',
            'country': 'Ghana',
            'preferred_language': 'en',
            'status': 'prospect',
            'occupation': 'Farmer'
        }
    ]
    
    for customer_data in customers_data:
        crm.create_customer(customer_data)
    
    return crm

# Initialize CRM system
crm_system = create_sample_crm_system()

