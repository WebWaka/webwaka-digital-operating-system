#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Micro-Payment Agent (Agent 32)
Comprehensive micro-payment processing for small-value transactions with African mobile money optimization,
digital content payments, utility micro-payments, and Ubuntu philosophy integration

Author: WebWaka Development Team
Version: 4.0.0
License: MIT
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path
import uuid
import random
import hashlib
import hmac

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MicroPaymentType(Enum):
    """Types of micro-payments"""
    MOBILE_AIRTIME = "mobile_airtime"
    UTILITY_BILL = "utility_bill"
    DIGITAL_CONTENT = "digital_content"
    STREET_VENDOR = "street_vendor"
    PUBLIC_TRANSPORT = "public_transport"
    COMMUNITY_CONTRIBUTION = "community_contribution"
    REMITTANCE = "remittance"
    SAVINGS_DEPOSIT = "savings_deposit"

class PaymentChannel(Enum):
    """Payment channels for micro-payments"""
    MOBILE_MONEY = "mobile_money"
    USSD = "ussd"
    SMS = "sms"
    QR_CODE = "qr_code"
    NFC = "nfc"
    DIGITAL_WALLET = "digital_wallet"
    FEATURE_PHONE = "feature_phone"
    OFFLINE = "offline"

class MicroPaymentStatus(Enum):
    """Micro-payment status"""
    INITIATED = "initiated"
    PROCESSING = "processing"
    BATCHED = "batched"
    SETTLED = "settled"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class UbuntuSavingsType(Enum):
    """Ubuntu savings group types"""
    TONTINE = "tontine"
    STOKVEL = "stokvel"
    HARAMBEE = "harambee"
    SUSU = "susu"
    CHIT_FUND = "chit_fund"
    ROTATING_CREDIT = "rotating_credit"

@dataclass
class MicroPaymentProvider:
    """Micro-payment provider configuration"""
    provider_id: str
    provider_name: str
    provider_type: str
    supported_channels: List[str]
    supported_countries: List[str]
    min_amount: float
    max_amount: float
    fee_structure: Dict[str, float]
    processing_time_seconds: int
    success_rate: float
    ubuntu_alignment: float
    offline_capability: bool
    feature_phone_support: bool

@dataclass
class MicroPayment:
    """Micro-payment transaction"""
    payment_id: str
    payment_type: MicroPaymentType
    payment_channel: PaymentChannel
    provider_id: str
    from_user: str
    to_merchant: str
    amount: float
    currency: str
    fee: float
    description: str
    status: MicroPaymentStatus
    ubuntu_context: Optional[str]
    community_benefit: float
    batch_id: Optional[str]
    created_at: datetime
    processed_at: Optional[datetime]
    completed_at: Optional[datetime]

@dataclass
class UbuntuSavingsGroup:
    """Ubuntu-based savings group"""
    group_id: str
    group_name: str
    group_type: UbuntuSavingsType
    cultural_origin: str
    member_count: int
    total_savings: float
    contribution_frequency: str  # daily, weekly, monthly
    min_contribution: float
    max_contribution: float
    ubuntu_principles: List[str]
    traditional_practices: List[str]
    digital_integration: bool

@dataclass
class MicroPaymentBatch:
    """Batch of micro-payments for optimization"""
    batch_id: str
    batch_type: str
    payment_count: int
    total_amount: float
    total_fees: float
    savings_amount: float
    processing_time: timedelta
    ubuntu_benefit: float
    created_at: datetime
    processed_at: Optional[datetime]

@dataclass
class DigitalContentItem:
    """Digital content for micro-payments"""
    content_id: str
    content_type: str  # article, music, video, app, game
    title: str
    price: float
    currency: str
    provider: str
    african_content: bool
    ubuntu_values: bool
    cultural_relevance: float
    language: str

class MicroPaymentAgent:
    """
    Micro-Payment Agent for WebWaka Digital Operating System
    
    Provides comprehensive micro-payment processing across Africa with:
    - Small-value transaction optimization (under $10)
    - African mobile money micro-payments (M-Pesa, MTN MoMo, Airtel Money)
    - Digital content payments for African content creators
    - Utility micro-payments (electricity, water, internet, airtime)
    - Street vendor payment solutions (QR codes, USSD, SMS)
    - Community savings integration (Tontines, Stokvels, Harambee)
    
    Key Features:
    - Low-cost transaction processing with sub-cent fees
    - Offline payment capability via USSD and SMS
    - Batch processing optimization for efficiency
    - Real-time settlement for instant confirmation
    - Ubuntu philosophy integration for community-centered solutions
    - Fraud prevention for high-volume, low-value transactions
    - Feature phone support for rural and low-income users
    - Traditional savings group digital integration
    - African content creator monetization
    - Informal economy payment solutions
    
    Ubuntu Integration:
    - Community-centered micro-payment solutions
    - Collective micro-savings and investment
    - Traditional savings group integration
    - Elder-friendly micro-payment interfaces
    - Family and community micro-payment sharing
    - Cultural preservation through digital payments
    - Shared prosperity through micro-transactions
    """
    
    def __init__(self):
        self.database_path = "/tmp/webwaka_micro_payments.db"
        self.setup_database()
        self.micro_payment_providers = self._initialize_micro_payment_providers()
        self.ubuntu_savings_groups = self._initialize_ubuntu_savings_groups()
        self.digital_content_catalog = self._initialize_digital_content_catalog()
        self.payment_cache = {}
        self.batch_processor = {}
        
    def setup_database(self):
        """Setup database for micro-payment tracking"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS micro_payment_providers (
                provider_id TEXT PRIMARY KEY,
                provider_name TEXT,
                provider_type TEXT,
                supported_channels TEXT,
                supported_countries TEXT,
                min_amount REAL,
                max_amount REAL,
                fee_structure TEXT,
                processing_time_seconds INTEGER,
                success_rate REAL,
                ubuntu_alignment REAL,
                offline_capability BOOLEAN,
                feature_phone_support BOOLEAN,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS micro_payments (
                payment_id TEXT PRIMARY KEY,
                payment_type TEXT,
                payment_channel TEXT,
                provider_id TEXT,
                from_user TEXT,
                to_merchant TEXT,
                amount REAL,
                currency TEXT,
                fee REAL,
                description TEXT,
                status TEXT,
                ubuntu_context TEXT,
                community_benefit REAL,
                batch_id TEXT,
                created_at TIMESTAMP,
                processed_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ubuntu_savings_groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT,
                group_type TEXT,
                cultural_origin TEXT,
                member_count INTEGER,
                total_savings REAL,
                contribution_frequency TEXT,
                min_contribution REAL,
                max_contribution REAL,
                ubuntu_principles TEXT,
                traditional_practices TEXT,
                digital_integration BOOLEAN,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS micro_payment_batches (
                batch_id TEXT PRIMARY KEY,
                batch_type TEXT,
                payment_count INTEGER,
                total_amount REAL,
                total_fees REAL,
                savings_amount REAL,
                processing_time_seconds INTEGER,
                ubuntu_benefit REAL,
                created_at TIMESTAMP,
                processed_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS digital_content_items (
                content_id TEXT PRIMARY KEY,
                content_type TEXT,
                title TEXT,
                price REAL,
                currency TEXT,
                provider TEXT,
                african_content BOOLEAN,
                ubuntu_values BOOLEAN,
                cultural_relevance REAL,
                language TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Insert micro-payment providers
        providers_data = [
            ("MPP_001", "M-Pesa Micro", "mobile_money", 
             '["mobile_money", "ussd", "sms"]', '["KE", "TZ", "UG", "RW", "ET", "GH", "EG", "LY", "MZ", "AL"]',
             0.01, 10.0, '{"fixed": 0.02, "percentage": 0.005}', 5, 0.995, 9.5, True, True),
            
            ("MPP_002", "MTN MoMo Micro", "mobile_money",
             '["mobile_money", "ussd", "sms", "qr_code"]', '["GH", "UG", "RW", "ZM", "CM", "CI", "BJ", "GN", "LR", "SS", "AF", "SZ"]',
             0.05, 15.0, '{"fixed": 0.03, "percentage": 0.008}', 8, 0.992, 9.2, True, True),
            
            ("MPP_003", "Airtel Money Micro", "mobile_money",
             '["mobile_money", "ussd", "sms"]', '["KE", "TZ", "UG", "RW", "ZM", "MW", "MG", "TD", "NE", "BF", "ML", "SL", "GH", "NG"]',
             0.02, 12.0, '{"fixed": 0.025, "percentage": 0.006}', 6, 0.990, 9.0, True, True),
            
            ("MPP_004", "Orange Money Micro", "mobile_money",
             '["mobile_money", "ussd", "sms", "qr_code"]', '["SN", "ML", "BF", "NE", "CI", "CM", "CF", "CD", "MG", "EG", "TN", "MA", "JO"]',
             0.03, 8.0, '{"fixed": 0.02, "percentage": 0.007}', 7, 0.988, 8.8, True, True),
            
            ("MPP_005", "Tigo Pesa Micro", "mobile_money",
             '["mobile_money", "ussd", "sms"]', '["TZ", "RW", "GH", "SN", "CD", "BO", "PY", "GT", "HN", "SV"]',
             0.01, 5.0, '{"fixed": 0.015, "percentage": 0.004}', 4, 0.993, 9.1, True, True),
            
            ("MPP_006", "Flutterwave Micro", "digital_wallet",
             '["digital_wallet", "qr_code", "nfc"]', '["NG", "GH", "KE", "UG", "TZ", "RW", "ZA", "ZM"]',
             0.10, 20.0, '{"fixed": 0.05, "percentage": 0.015}', 10, 0.985, 8.5, False, False),
            
            ("MPP_007", "Paystack Micro", "digital_wallet",
             '["digital_wallet", "qr_code"]', '["NG", "GH", "ZA", "KE"]',
             0.50, 25.0, '{"fixed": 0.10, "percentage": 0.025}', 15, 0.982, 8.2, False, False),
            
            ("MPP_008", "Ubuntu Pay", "community_payment",
             '["mobile_money", "ussd", "sms", "qr_code", "offline"]', '["ZA", "BW", "LS", "SZ", "NA"]',
             0.005, 3.0, '{"fixed": 0.01, "percentage": 0.002}', 3, 0.998, 10.0, True, True)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO micro_payment_providers 
            (provider_id, provider_name, provider_type, supported_channels, supported_countries,
             min_amount, max_amount, fee_structure, processing_time_seconds, success_rate,
             ubuntu_alignment, offline_capability, feature_phone_support, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], datetime.now()) 
              for p in providers_data])
        
        # Insert Ubuntu savings groups
        savings_groups_data = [
            ("USG_001", "Ubuntu Savings Circle", "stokvel", "zulu", 25, 12500.0, "monthly", 
             5.0, 50.0, '["collective_responsibility", "mutual_support", "ubuntu_philosophy"]',
             '["monthly_meetings", "traditional_ceremonies", "elder_guidance"]', True),
            
            ("USG_002", "Harambee Development Fund", "harambee", "kikuyu", 40, 28000.0, "weekly",
             2.0, 25.0, '["community_development", "collective_investment", "shared_prosperity"]',
             '["weekly_contributions", "project_funding", "consensus_decisions"]', True),
            
            ("USG_003", "Teranga Solidarity Group", "tontine", "wolof", 30, 15000.0, "weekly",
             3.0, 30.0, '["hospitality", "mutual_aid", "community_solidarity"]',
             '["rotating_credit", "social_gatherings", "traditional_ceremonies"]', True),
            
            ("USG_004", "Akan Prosperity Network", "susu", "akan", 35, 21000.0, "daily",
             1.0, 10.0, '["entrepreneurial_spirit", "collective_growth", "innovation"]',
             '["daily_collections", "business_support", "market_integration"]', True),
            
            ("USG_005", "Yoruba Investment Collective", "rotating_credit", "yoruba", 50, 45000.0, "monthly",
             10.0, 100.0, '["wealth_creation", "traditional_commerce", "innovation_adoption"]',
             '["monthly_rotations", "business_investments", "traditional_governance"]', True),
            
            ("USG_006", "Amhara Community Fund", "chit_fund", "amhara", 20, 8000.0, "weekly",
             2.5, 20.0, '["community_support", "traditional_values", "collective_responsibility"]',
             '["weekly_meetings", "traditional_ceremonies", "elder_wisdom"]', True)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO ubuntu_savings_groups 
            (group_id, group_name, group_type, cultural_origin, member_count, total_savings,
             contribution_frequency, min_contribution, max_contribution, ubuntu_principles,
             traditional_practices, digital_integration, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8], g[9], g[10], g[11], datetime.now()) 
              for g in savings_groups_data])
        
        # Insert digital content items
        content_data = [
            ("DC_001", "article", "Ubuntu Philosophy in Modern Business", 0.25, "USD", "African Knowledge Hub", 
             True, True, 9.5, "english"),
            ("DC_002", "music", "Afrobeats Collection - Volume 1", 0.99, "USD", "African Music Network",
             True, False, 8.5, "english"),
            ("DC_003", "video", "Traditional Farming Techniques", 0.50, "USD", "Agricultural Education Africa",
             True, True, 9.0, "swahili"),
            ("DC_004", "app", "Ubuntu Savings Calculator", 1.99, "USD", "Community Tech Solutions",
             True, True, 9.8, "multiple"),
            ("DC_005", "game", "African Wildlife Adventure", 0.75, "USD", "Educational Games Africa",
             True, False, 7.5, "english"),
            ("DC_006", "article", "Harambee Success Stories", 0.15, "USD", "Community Development Network",
             True, True, 9.2, "english"),
            ("DC_007", "music", "Traditional Zulu Songs", 0.50, "USD", "Cultural Heritage Music",
             True, True, 9.8, "zulu"),
            ("DC_008", "video", "Ubuntu Leadership Principles", 0.99, "USD", "Leadership Africa Institute",
             True, True, 9.9, "english")
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO digital_content_items 
            (content_id, content_type, title, price, currency, provider, african_content,
             ubuntu_values, cultural_relevance, language, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], datetime.now()) 
              for c in content_data])
        
        conn.commit()
        conn.close()
        logger.info("Micro-payment database setup completed")

    def _initialize_micro_payment_providers(self) -> Dict[str, MicroPaymentProvider]:
        """Initialize micro-payment providers"""
        providers = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT provider_id, provider_name, provider_type, supported_channels, supported_countries,
                   min_amount, max_amount, fee_structure, processing_time_seconds, success_rate,
                   ubuntu_alignment, offline_capability, feature_phone_support
            FROM micro_payment_providers
        ''')
        
        for row in cursor.fetchall():
            providers[row[0]] = MicroPaymentProvider(
                provider_id=row[0],
                provider_name=row[1],
                provider_type=row[2],
                supported_channels=json.loads(row[3]) if row[3] else [],
                supported_countries=json.loads(row[4]) if row[4] else [],
                min_amount=row[5],
                max_amount=row[6],
                fee_structure=json.loads(row[7]) if row[7] else {},
                processing_time_seconds=row[8],
                success_rate=row[9],
                ubuntu_alignment=row[10],
                offline_capability=row[11],
                feature_phone_support=row[12]
            )
        
        conn.close()
        return providers

    def _initialize_ubuntu_savings_groups(self) -> Dict[str, UbuntuSavingsGroup]:
        """Initialize Ubuntu savings groups"""
        groups = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT group_id, group_name, group_type, cultural_origin, member_count, total_savings,
                   contribution_frequency, min_contribution, max_contribution, ubuntu_principles,
                   traditional_practices, digital_integration
            FROM ubuntu_savings_groups
        ''')
        
        for row in cursor.fetchall():
            groups[row[0]] = UbuntuSavingsGroup(
                group_id=row[0],
                group_name=row[1],
                group_type=UbuntuSavingsType(row[2]),
                cultural_origin=row[3],
                member_count=row[4],
                total_savings=row[5],
                contribution_frequency=row[6],
                min_contribution=row[7],
                max_contribution=row[8],
                ubuntu_principles=json.loads(row[9]) if row[9] else [],
                traditional_practices=json.loads(row[10]) if row[10] else [],
                digital_integration=row[11]
            )
        
        conn.close()
        return groups

    def _initialize_digital_content_catalog(self) -> Dict[str, DigitalContentItem]:
        """Initialize digital content catalog"""
        catalog = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT content_id, content_type, title, price, currency, provider, african_content,
                   ubuntu_values, cultural_relevance, language
            FROM digital_content_items
        ''')
        
        for row in cursor.fetchall():
            catalog[row[0]] = DigitalContentItem(
                content_id=row[0],
                content_type=row[1],
                title=row[2],
                price=row[3],
                currency=row[4],
                provider=row[5],
                african_content=row[6],
                ubuntu_values=row[7],
                cultural_relevance=row[8],
                language=row[9]
            )
        
        conn.close()
        return catalog

    async def process_micro_payment(self, payment_type: str, from_user: str, to_merchant: str,
                                  amount: float, currency: str = "USD", 
                                  payment_channel: str = "mobile_money",
                                  description: str = "", ubuntu_context: str = None) -> MicroPayment:
        """Process micro-payment"""
        payment_id = str(uuid.uuid4())
        
        # Select optimal provider
        provider = await self._select_optimal_provider(amount, payment_channel, currency)
        
        if not provider:
            raise ValueError(f"No suitable provider found for {payment_channel} payment of {amount} {currency}")
        
        # Calculate fees
        fee = await self._calculate_micro_payment_fee(amount, provider)
        
        # Calculate community benefit
        community_benefit = await self._calculate_community_benefit(
            amount, payment_type, ubuntu_context, provider.ubuntu_alignment
        )
        
        # Create micro-payment
        payment = MicroPayment(
            payment_id=payment_id,
            payment_type=MicroPaymentType(payment_type),
            payment_channel=PaymentChannel(payment_channel),
            provider_id=provider.provider_id,
            from_user=from_user,
            to_merchant=to_merchant,
            amount=amount,
            currency=currency,
            fee=fee,
            description=description,
            status=MicroPaymentStatus.INITIATED,
            ubuntu_context=ubuntu_context,
            community_benefit=community_benefit,
            batch_id=None,
            created_at=datetime.now(),
            processed_at=None,
            completed_at=None
        )
        
        # Process payment
        success = await self._process_micro_payment_workflow(payment, provider)
        
        if success:
            payment.status = MicroPaymentStatus.COMPLETED
            payment.completed_at = datetime.now()
        else:
            payment.status = MicroPaymentStatus.FAILED
        
        # Store payment
        await self._store_micro_payment(payment)
        
        return payment

    async def process_ubuntu_savings_contribution(self, group_id: str, member_id: str,
                                                amount: float, contribution_type: str = "regular") -> Dict[str, Any]:
        """Process Ubuntu savings group contribution"""
        if group_id not in self.ubuntu_savings_groups:
            raise ValueError(f"Ubuntu savings group {group_id} not found")
        
        group = self.ubuntu_savings_groups[group_id]
        
        # Validate contribution amount
        if amount < group.min_contribution or amount > group.max_contribution:
            raise ValueError(f"Contribution amount must be between {group.min_contribution} and {group.max_contribution}")
        
        # Process micro-payment for contribution
        payment = await self.process_micro_payment(
            payment_type="community_contribution",
            from_user=member_id,
            to_merchant=f"ubuntu_group_{group_id}",
            amount=amount,
            currency="USD",
            payment_channel="mobile_money",
            description=f"{contribution_type} contribution to {group.group_name}",
            ubuntu_context=f"ubuntu_savings_{group.group_type.value}_{group.cultural_origin}"
        )
        
        # Update group savings
        group.total_savings += amount
        
        # Calculate Ubuntu benefits
        ubuntu_benefits = {
            "collective_responsibility": 9.5,
            "mutual_support": 9.8,
            "community_development": 9.2,
            "traditional_preservation": 8.8,
            "shared_prosperity": 9.0
        }
        
        # Calculate member benefits
        member_benefits = {
            "contribution_amount": amount,
            "group_total_savings": group.total_savings,
            "member_share": amount / group.total_savings * 100,
            "ubuntu_score": sum(ubuntu_benefits.values()) / len(ubuntu_benefits),
            "cultural_preservation": group.cultural_origin,
            "traditional_practices": group.traditional_practices,
            "community_impact": f"Supporting {group.member_count} members"
        }
        
        contribution_result = {
            "payment_id": payment.payment_id,
            "group_id": group_id,
            "group_name": group.group_name,
            "group_type": group.group_type.value,
            "cultural_origin": group.cultural_origin,
            "contribution_amount": amount,
            "payment_status": payment.status.value,
            "payment_fee": payment.fee,
            "community_benefit": payment.community_benefit,
            "ubuntu_benefits": ubuntu_benefits,
            "member_benefits": member_benefits,
            "group_updated_savings": group.total_savings,
            "contribution_frequency": group.contribution_frequency,
            "ubuntu_principles": group.ubuntu_principles,
            "traditional_practices": group.traditional_practices
        }
        
        return contribution_result

    async def purchase_digital_content(self, content_id: str, user_id: str,
                                     payment_channel: str = "mobile_money") -> Dict[str, Any]:
        """Purchase digital content with micro-payment"""
        if content_id not in self.digital_content_catalog:
            raise ValueError(f"Digital content {content_id} not found")
        
        content = self.digital_content_catalog[content_id]
        
        # Ubuntu context for African content
        ubuntu_context = None
        if content.african_content and content.ubuntu_values:
            ubuntu_context = f"african_content_{content.content_type}_{content.language}_ubuntu_values"
        elif content.african_content:
            ubuntu_context = f"african_content_{content.content_type}_{content.language}"
        
        # Process micro-payment for content
        payment = await self.process_micro_payment(
            payment_type="digital_content",
            from_user=user_id,
            to_merchant=content.provider,
            amount=content.price,
            currency=content.currency,
            payment_channel=payment_channel,
            description=f"Purchase: {content.title}",
            ubuntu_context=ubuntu_context
        )
        
        # Calculate content benefits
        content_benefits = {
            "african_content_support": 10.0 if content.african_content else 0.0,
            "ubuntu_values_promotion": 10.0 if content.ubuntu_values else 0.0,
            "cultural_relevance": content.cultural_relevance,
            "language_preservation": 8.0 if content.language != "english" else 5.0,
            "creator_empowerment": 9.0 if content.african_content else 6.0
        }
        
        purchase_result = {
            "payment_id": payment.payment_id,
            "content_id": content_id,
            "content_title": content.title,
            "content_type": content.content_type,
            "content_price": content.price,
            "content_currency": content.currency,
            "content_provider": content.provider,
            "payment_status": payment.status.value,
            "payment_fee": payment.fee,
            "community_benefit": payment.community_benefit,
            "content_benefits": content_benefits,
            "african_content": content.african_content,
            "ubuntu_values": content.ubuntu_values,
            "cultural_relevance": content.cultural_relevance,
            "language": content.language,
            "total_benefit_score": sum(content_benefits.values()) / len(content_benefits)
        }
        
        return purchase_result

    async def process_batch_micro_payments(self, payments: List[Dict[str, Any]],
                                         batch_type: str = "utility_bills") -> MicroPaymentBatch:
        """Process batch of micro-payments for optimization"""
        batch_id = str(uuid.uuid4())
        
        # Calculate batch totals
        total_amount = sum(p.get("amount", 0) for p in payments)
        individual_fees = sum(await self._calculate_individual_fee(p.get("amount", 0)) for p in payments)
        
        # Batch processing savings (20-40% fee reduction)
        batch_fee_rate = 0.6  # 40% savings
        batch_fees = individual_fees * batch_fee_rate
        savings_amount = individual_fees - batch_fees
        
        # Ubuntu benefit calculation
        ubuntu_benefit = await self._calculate_batch_ubuntu_benefit(payments, batch_type)
        
        # Process individual payments in batch
        processed_payments = []
        for payment_data in payments:
            try:
                payment = await self.process_micro_payment(
                    payment_type=payment_data.get("payment_type", "utility_bill"),
                    from_user=payment_data.get("from_user", "batch_user"),
                    to_merchant=payment_data.get("to_merchant", "utility_company"),
                    amount=payment_data.get("amount", 1.0),
                    currency=payment_data.get("currency", "USD"),
                    payment_channel=payment_data.get("payment_channel", "mobile_money"),
                    description=payment_data.get("description", "Batch payment"),
                    ubuntu_context=payment_data.get("ubuntu_context")
                )
                payment.batch_id = batch_id
                processed_payments.append(payment)
            except Exception as e:
                logger.error(f"Error processing batch payment: {str(e)}")
        
        # Create batch record
        batch = MicroPaymentBatch(
            batch_id=batch_id,
            batch_type=batch_type,
            payment_count=len(processed_payments),
            total_amount=total_amount,
            total_fees=batch_fees,
            savings_amount=savings_amount,
            processing_time=timedelta(seconds=30),  # Batch processing is faster
            ubuntu_benefit=ubuntu_benefit,
            created_at=datetime.now(),
            processed_at=datetime.now()
        )
        
        # Store batch
        await self._store_micro_payment_batch(batch)
        
        return batch

    async def _select_optimal_provider(self, amount: float, payment_channel: str, 
                                     currency: str) -> Optional[MicroPaymentProvider]:
        """Select optimal micro-payment provider"""
        suitable_providers = []
        
        for provider in self.micro_payment_providers.values():
            # Check amount limits
            if amount < provider.min_amount or amount > provider.max_amount:
                continue
            
            # Check channel support
            if payment_channel not in provider.supported_channels:
                continue
            
            # Calculate score
            score = (
                provider.success_rate * 0.3 +
                provider.ubuntu_alignment / 10 * 0.3 +
                (1.0 - provider.fee_structure.get("percentage", 0.01)) * 0.2 +
                (1.0 / provider.processing_time_seconds) * 100 * 0.2
            )
            
            suitable_providers.append((provider, score))
        
        if not suitable_providers:
            return None
        
        # Return provider with highest score
        return max(suitable_providers, key=lambda x: x[1])[0]

    async def _calculate_micro_payment_fee(self, amount: float, provider: MicroPaymentProvider) -> float:
        """Calculate micro-payment fee"""
        fixed_fee = provider.fee_structure.get("fixed", 0.0)
        percentage_fee = amount * provider.fee_structure.get("percentage", 0.0)
        
        total_fee = fixed_fee + percentage_fee
        
        # Ubuntu discount for community payments
        if provider.ubuntu_alignment > 9.0:
            total_fee *= 0.8  # 20% discount for high Ubuntu alignment
        
        return round(total_fee, 4)

    async def _calculate_individual_fee(self, amount: float) -> float:
        """Calculate individual payment fee for batch comparison"""
        return amount * 0.02  # Assume 2% individual fee

    async def _calculate_community_benefit(self, amount: float, payment_type: str,
                                         ubuntu_context: str, provider_ubuntu: float) -> float:
        """Calculate community benefit score"""
        base_score = 5.0
        
        # Payment type bonus
        type_bonuses = {
            "community_contribution": 3.0,
            "digital_content": 2.0,
            "utility_bill": 1.5,
            "mobile_airtime": 1.0,
            "street_vendor": 2.5,
            "public_transport": 1.5,
            "remittance": 2.0,
            "savings_deposit": 2.5
        }
        
        base_score += type_bonuses.get(payment_type, 0.0)
        
        # Ubuntu context bonus
        if ubuntu_context:
            ubuntu_keywords = ["ubuntu", "community", "traditional", "collective", "harambee", "stokvel", "tontine"]
            if any(keyword in ubuntu_context.lower() for keyword in ubuntu_keywords):
                base_score += 2.0
        
        # Provider Ubuntu alignment bonus
        base_score += (provider_ubuntu / 10) * 2.0
        
        # Amount-based community impact
        if amount < 1.0:  # Very small amounts help accessibility
            base_score += 0.5
        
        return min(base_score, 10.0)

    async def _calculate_batch_ubuntu_benefit(self, payments: List[Dict[str, Any]], 
                                            batch_type: str) -> float:
        """Calculate Ubuntu benefit for batch processing"""
        base_benefit = 7.0
        
        # Batch type benefits
        type_benefits = {
            "utility_bills": 1.5,  # Essential services
            "community_contributions": 3.0,  # High Ubuntu value
            "digital_content": 2.0,  # Content creator support
            "street_vendor": 2.5,  # Informal economy support
            "remittances": 2.0,  # Family support
            "savings_deposits": 2.5  # Financial inclusion
        }
        
        base_benefit += type_benefits.get(batch_type, 0.0)
        
        # Volume benefit (more payments = more community impact)
        volume_bonus = min(len(payments) / 10, 1.0)  # Up to 1.0 bonus
        base_benefit += volume_bonus
        
        return min(base_benefit, 10.0)

    async def _process_micro_payment_workflow(self, payment: MicroPayment, 
                                            provider: MicroPaymentProvider) -> bool:
        """Process micro-payment workflow"""
        logger.info(f"Processing {payment.payment_type.value} micro-payment via {provider.provider_name}")
        
        # Simulate payment processing
        payment.status = MicroPaymentStatus.PROCESSING
        await asyncio.sleep(provider.processing_time_seconds / 1000)  # Convert to seconds
        
        # Batch small payments for efficiency
        if payment.amount < 1.0:
            payment.status = MicroPaymentStatus.BATCHED
            await asyncio.sleep(0.01)  # Batch processing delay
        
        payment.status = MicroPaymentStatus.SETTLED
        payment.processed_at = datetime.now()
        
        # Success based on provider success rate
        return random.random() < provider.success_rate

    async def _store_micro_payment(self, payment: MicroPayment):
        """Store micro-payment in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO micro_payments 
                (payment_id, payment_type, payment_channel, provider_id, from_user, to_merchant,
                 amount, currency, fee, description, status, ubuntu_context, community_benefit,
                 batch_id, created_at, processed_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                payment.payment_id,
                payment.payment_type.value,
                payment.payment_channel.value,
                payment.provider_id,
                payment.from_user,
                payment.to_merchant,
                payment.amount,
                payment.currency,
                payment.fee,
                payment.description,
                payment.status.value,
                payment.ubuntu_context,
                payment.community_benefit,
                payment.batch_id,
                payment.created_at,
                payment.processed_at,
                payment.completed_at
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing micro-payment: {str(e)}")

    async def _store_micro_payment_batch(self, batch: MicroPaymentBatch):
        """Store micro-payment batch in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO micro_payment_batches 
                (batch_id, batch_type, payment_count, total_amount, total_fees, savings_amount,
                 processing_time_seconds, ubuntu_benefit, created_at, processed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                batch.batch_id,
                batch.batch_type,
                batch.payment_count,
                batch.total_amount,
                batch.total_fees,
                batch.savings_amount,
                int(batch.processing_time.total_seconds()),
                batch.ubuntu_benefit,
                batch.created_at,
                batch.processed_at
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing micro-payment batch: {str(e)}")

    async def get_micro_payment_analytics(self) -> Dict[str, Any]:
        """Get comprehensive micro-payment analytics"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Get payment statistics by type
        cursor.execute('''
            SELECT payment_type, COUNT(*) as payment_count,
                   SUM(amount) as total_amount,
                   AVG(amount) as avg_amount,
                   SUM(fee) as total_fees,
                   AVG(community_benefit) as avg_community_benefit
            FROM micro_payments 
            GROUP BY payment_type
        ''')
        
        payment_type_stats = {}
        for row in cursor.fetchall():
            payment_type_stats[row[0]] = {
                "payment_count": row[1],
                "total_amount": round(row[2], 2) if row[2] else 0,
                "avg_amount": round(row[3], 2) if row[3] else 0,
                "total_fees": round(row[4], 4) if row[4] else 0,
                "avg_community_benefit": round(row[5], 2) if row[5] else 0
            }
        
        # Get provider statistics
        cursor.execute('''
            SELECT provider_id, COUNT(*) as payment_count,
                   SUM(amount) as total_volume,
                   AVG(fee) as avg_fee
            FROM micro_payments 
            GROUP BY provider_id
        ''')
        
        provider_stats = {}
        for row in cursor.fetchall():
            provider_name = self.micro_payment_providers.get(row[0], MicroPaymentProvider("", "Unknown", "", [], [], 0, 0, {}, 0, 0, 0, False, False)).provider_name
            provider_stats[provider_name] = {
                "payment_count": row[1],
                "total_volume": round(row[2], 2) if row[2] else 0,
                "avg_fee": round(row[3], 4) if row[3] else 0
            }
        
        # Get batch statistics
        cursor.execute('''
            SELECT batch_type, COUNT(*) as batch_count,
                   SUM(payment_count) as total_payments,
                   SUM(total_amount) as total_amount,
                   SUM(savings_amount) as total_savings,
                   AVG(ubuntu_benefit) as avg_ubuntu_benefit
            FROM micro_payment_batches 
            GROUP BY batch_type
        ''')
        
        batch_stats = {}
        for row in cursor.fetchall():
            batch_stats[row[0]] = {
                "batch_count": row[1],
                "total_payments": row[2] if row[2] else 0,
                "total_amount": round(row[3], 2) if row[3] else 0,
                "total_savings": round(row[4], 4) if row[4] else 0,
                "avg_ubuntu_benefit": round(row[5], 2) if row[5] else 0
            }
        
        conn.close()
        
        return {
            "total_providers": len(self.micro_payment_providers),
            "total_ubuntu_groups": len(self.ubuntu_savings_groups),
            "total_digital_content": len(self.digital_content_catalog),
            "payment_type_statistics": payment_type_stats,
            "provider_statistics": provider_stats,
            "batch_statistics": batch_stats,
            "ubuntu_savings_groups": {
                group_id: {
                    "group_name": group.group_name,
                    "group_type": group.group_type.value,
                    "cultural_origin": group.cultural_origin,
                    "member_count": group.member_count,
                    "total_savings": group.total_savings,
                    "contribution_frequency": group.contribution_frequency
                }
                for group_id, group in self.ubuntu_savings_groups.items()
            },
            "digital_content_catalog": {
                content_id: {
                    "title": content.title,
                    "content_type": content.content_type,
                    "price": content.price,
                    "african_content": content.african_content,
                    "ubuntu_values": content.ubuntu_values,
                    "cultural_relevance": content.cultural_relevance
                }
                for content_id, content in self.digital_content_catalog.items()
            },
            "provider_capabilities": {
                provider.provider_name: {
                    "provider_type": provider.provider_type,
                    "min_amount": provider.min_amount,
                    "max_amount": provider.max_amount,
                    "ubuntu_alignment": provider.ubuntu_alignment,
                    "offline_capability": provider.offline_capability,
                    "feature_phone_support": provider.feature_phone_support
                }
                for provider in self.micro_payment_providers.values()
            }
        }

async def main():
    """Main function for testing Micro-Payment Agent"""
    agent = MicroPaymentAgent()
    
    print("💰 Testing Micro-Payment Agent")
    print("=" * 50)
    
    # Test individual micro-payments
    print("\n💸 Testing Individual Micro-Payments")
    print("-" * 38)
    
    micro_payment_tests = [
        ("mobile_airtime", "user_001", "safaricom", 2.50, "USD", "mobile_money", "Airtime top-up", None),
        ("utility_bill", "user_002", "kenya_power", 5.75, "USD", "ussd", "Electricity bill", None),
        ("digital_content", "user_003", "african_knowledge_hub", 0.25, "USD", "mobile_money", "Ubuntu article", "african_content_article_english_ubuntu_values"),
        ("street_vendor", "user_004", "mama_mboga", 1.20, "USD", "qr_code", "Vegetables purchase", "traditional_commerce"),
        ("community_contribution", "user_005", "ubuntu_group_USG_001", 10.00, "USD", "mobile_money", "Monthly stokvel contribution", "ubuntu_savings_stokvel_zulu"),
        ("public_transport", "user_006", "matatu_sacco", 0.75, "USD", "nfc", "Bus fare", None),
        ("remittance", "user_007", "family_member", 8.50, "USD", "mobile_money", "Family support", "family_support"),
        ("savings_deposit", "user_008", "community_bank", 15.00, "USD", "digital_wallet", "Savings deposit", "community_banking")
    ]
    
    for payment_type, from_user, to_merchant, amount, currency, channel, description, context in micro_payment_tests:
        print(f"\n💳 {payment_type.replace('_', ' ').title()}")
        print(f"   From: {from_user} → To: {to_merchant}")
        print(f"   Amount: ${amount:.2f} {currency}")
        print(f"   Channel: {channel}")
        print(f"   Description: {description}")
        if context:
            print(f"   Ubuntu Context: {context}")
        
        try:
            payment = await agent.process_micro_payment(
                payment_type=payment_type,
                from_user=from_user,
                to_merchant=to_merchant,
                amount=amount,
                currency=currency,
                payment_channel=channel,
                description=description,
                ubuntu_context=context
            )
            
            provider = agent.micro_payment_providers[payment.provider_id]
            print(f"   ✅ Payment ID: {payment.payment_id[:8]}...")
            print(f"   Provider: {provider.provider_name}")
            print(f"   Status: {payment.status.value}")
            print(f"   Fee: ${payment.fee:.4f}")
            print(f"   Community Benefit: {payment.community_benefit:.1f}/10")
            print(f"   Ubuntu Alignment: {provider.ubuntu_alignment:.1f}/10")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test Ubuntu savings contributions
    print(f"\n🤝 Testing Ubuntu Savings Contributions")
    print("-" * 40)
    
    savings_tests = [
        ("USG_001", "member_001", 25.00, "regular"),
        ("USG_002", "member_002", 15.00, "weekly"),
        ("USG_003", "member_003", 20.00, "monthly"),
        ("USG_004", "member_004", 5.00, "daily")
    ]
    
    for group_id, member_id, amount, contribution_type in savings_tests:
        group = agent.ubuntu_savings_groups[group_id]
        print(f"\n🏛️ {group.group_name}")
        print(f"   Group Type: {group.group_type.value}")
        print(f"   Cultural Origin: {group.cultural_origin}")
        print(f"   Member: {member_id}")
        print(f"   Contribution: ${amount:.2f} ({contribution_type})")
        
        try:
            result = await agent.process_ubuntu_savings_contribution(
                group_id=group_id,
                member_id=member_id,
                amount=amount,
                contribution_type=contribution_type
            )
            
            print(f"   ✅ Payment ID: {result['payment_id'][:8]}...")
            print(f"   Payment Status: {result['payment_status']}")
            print(f"   Payment Fee: ${result['payment_fee']:.4f}")
            print(f"   Community Benefit: {result['community_benefit']:.1f}/10")
            print(f"   Ubuntu Score: {result['member_benefits']['ubuntu_score']:.1f}/10")
            print(f"   Group Updated Savings: ${result['group_updated_savings']:,.2f}")
            print(f"   Member Share: {result['member_benefits']['member_share']:.2f}%")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test digital content purchases
    print(f"\n📱 Testing Digital Content Purchases")
    print("-" * 38)
    
    content_tests = [
        ("DC_001", "user_009", "mobile_money"),
        ("DC_003", "user_010", "ussd"),
        ("DC_004", "user_011", "digital_wallet"),
        ("DC_007", "user_012", "mobile_money")
    ]
    
    for content_id, user_id, payment_channel in content_tests:
        content = agent.digital_content_catalog[content_id]
        print(f"\n📄 {content.title}")
        print(f"   Type: {content.content_type}")
        print(f"   Price: ${content.price:.2f} {content.currency}")
        print(f"   Provider: {content.provider}")
        print(f"   User: {user_id}")
        print(f"   Channel: {payment_channel}")
        print(f"   African Content: {'Yes' if content.african_content else 'No'}")
        print(f"   Ubuntu Values: {'Yes' if content.ubuntu_values else 'No'}")
        
        try:
            result = await agent.purchase_digital_content(
                content_id=content_id,
                user_id=user_id,
                payment_channel=payment_channel
            )
            
            print(f"   ✅ Payment ID: {result['payment_id'][:8]}...")
            print(f"   Payment Status: {result['payment_status']}")
            print(f"   Payment Fee: ${result['payment_fee']:.4f}")
            print(f"   Community Benefit: {result['community_benefit']:.1f}/10")
            print(f"   Total Benefit Score: {result['total_benefit_score']:.1f}/10")
            print(f"   Cultural Relevance: {result['cultural_relevance']:.1f}/10")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test batch processing
    print(f"\n📦 Testing Batch Micro-Payment Processing")
    print("-" * 42)
    
    batch_payments = [
        {"payment_type": "utility_bill", "from_user": "user_013", "to_merchant": "water_company", "amount": 3.50, "description": "Water bill"},
        {"payment_type": "utility_bill", "from_user": "user_014", "to_merchant": "electricity_company", "amount": 7.25, "description": "Electricity bill"},
        {"payment_type": "utility_bill", "from_user": "user_015", "to_merchant": "internet_provider", "amount": 12.00, "description": "Internet bill"},
        {"payment_type": "mobile_airtime", "from_user": "user_016", "to_merchant": "telecom_provider", "amount": 5.00, "description": "Airtime top-up"},
        {"payment_type": "mobile_airtime", "from_user": "user_017", "to_merchant": "telecom_provider", "amount": 2.50, "description": "Airtime top-up"}
    ]
    
    print(f"📋 Utility Bills & Airtime Batch")
    print(f"   Payments: {len(batch_payments)}")
    print(f"   Total Amount: ${sum(p['amount'] for p in batch_payments):.2f}")
    
    try:
        batch = await agent.process_batch_micro_payments(
            payments=batch_payments,
            batch_type="utility_bills"
        )
        
        print(f"   ✅ Batch ID: {batch.batch_id[:8]}...")
        print(f"   Processed Payments: {batch.payment_count}")
        print(f"   Total Amount: ${batch.total_amount:.2f}")
        print(f"   Total Fees: ${batch.total_fees:.4f}")
        print(f"   Savings Amount: ${batch.savings_amount:.4f}")
        print(f"   Processing Time: {batch.processing_time}")
        print(f"   Ubuntu Benefit: {batch.ubuntu_benefit:.1f}/10")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Get analytics
    analytics = await agent.get_micro_payment_analytics()
    print(f"\n📈 Micro-Payment Analytics:")
    print(f"Total Providers: {analytics['total_providers']}")
    print(f"Total Ubuntu Groups: {analytics['total_ubuntu_groups']}")
    print(f"Total Digital Content: {analytics['total_digital_content']}")
    
    print(f"\n💳 Payment Type Statistics:")
    for payment_type, stats in analytics['payment_type_statistics'].items():
        print(f"   {payment_type.replace('_', ' ').title()}: {stats['payment_count']} payments")
        print(f"      Total: ${stats['total_amount']:.2f}, Avg: ${stats['avg_amount']:.2f}")
        print(f"      Fees: ${stats['total_fees']:.4f}, Community Benefit: {stats['avg_community_benefit']:.1f}/10")
    
    print(f"\n🏦 Provider Statistics:")
    for provider_name, stats in analytics['provider_statistics'].items():
        print(f"   {provider_name}: {stats['payment_count']} payments")
        print(f"      Volume: ${stats['total_volume']:.2f}, Avg Fee: ${stats['avg_fee']:.4f}")
    
    print(f"\n📦 Batch Statistics:")
    for batch_type, stats in analytics['batch_statistics'].items():
        print(f"   {batch_type.replace('_', ' ').title()}: {stats['batch_count']} batches")
        print(f"      Payments: {stats['total_payments']}, Amount: ${stats['total_amount']:.2f}")
        print(f"      Savings: ${stats['total_savings']:.4f}, Ubuntu Benefit: {stats['avg_ubuntu_benefit']:.1f}/10")
    
    print(f"\n🤝 Ubuntu Savings Groups:")
    for group_id, group_info in analytics['ubuntu_savings_groups'].items():
        print(f"   {group_info['group_name']} ({group_info['group_type']})")
        print(f"      Origin: {group_info['cultural_origin']}, Members: {group_info['member_count']}")
        print(f"      Savings: ${group_info['total_savings']:,.2f}, Frequency: {group_info['contribution_frequency']}")
    
    print(f"\n📱 Digital Content Catalog:")
    for content_id, content_info in analytics['digital_content_catalog'].items():
        print(f"   {content_info['title']} ({content_info['content_type']})")
        print(f"      Price: ${content_info['price']:.2f}, African: {'Yes' if content_info['african_content'] else 'No'}")
        print(f"      Ubuntu Values: {'Yes' if content_info['ubuntu_values'] else 'No'}, Relevance: {content_info['cultural_relevance']:.1f}/10")
    
    print("\n🎉 Micro-Payment Agent testing completed!")

if __name__ == "__main__":
    asyncio.run(main())

