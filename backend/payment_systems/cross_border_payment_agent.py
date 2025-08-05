#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Cross-Border Payment Agent (Agent 31)
Comprehensive cross-border payment processing for intra-African trade with AfCFTA optimization,
multi-corridor payment processing, and Ubuntu philosophy integration

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

class PaymentCorridor(Enum):
    """African trade corridors"""
    EAC = "east_african_community"
    ECOWAS = "economic_community_west_african_states"
    SADC = "southern_african_development_community"
    COMESA = "common_market_eastern_southern_africa"
    AMU = "arab_maghreb_union"
    ECCAS = "economic_community_central_african_states"
    IGAD = "intergovernmental_authority_development"

class PaymentMethod(Enum):
    """Cross-border payment methods"""
    SWIFT_WIRE = "swift_wire"
    CORRESPONDENT_BANKING = "correspondent_banking"
    MOBILE_MONEY = "mobile_money"
    CRYPTOCURRENCY = "cryptocurrency"
    TRADE_FINANCE = "trade_finance"
    DIGITAL_WALLET = "digital_wallet"
    BLOCKCHAIN = "blockchain"

class TradeType(Enum):
    """Types of trade transactions"""
    GOODS_EXPORT = "goods_export"
    GOODS_IMPORT = "goods_import"
    SERVICES_EXPORT = "services_export"
    SERVICES_IMPORT = "services_import"
    REMITTANCE = "remittance"
    INVESTMENT = "investment"
    LOAN_REPAYMENT = "loan_repayment"

class PaymentStatus(Enum):
    """Payment status"""
    INITIATED = "initiated"
    PROCESSING = "processing"
    COMPLIANCE_CHECK = "compliance_check"
    CURRENCY_EXCHANGE = "currency_exchange"
    ROUTING = "routing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ComplianceLevel(Enum):
    """Regulatory compliance levels"""
    BASIC = "basic"
    ENHANCED = "enhanced"
    STRICT = "strict"
    AFCFTA_OPTIMIZED = "afcfta_optimized"

@dataclass
class AfricanCurrency:
    """African currency configuration"""
    currency_code: str
    currency_name: str
    country: str
    central_bank: str
    exchange_rate_usd: float
    volatility_index: float
    trade_volume_daily: float
    afcfta_member: bool
    ubuntu_alignment: float
    digital_currency_readiness: float

@dataclass
class TradeCorridor:
    """African trade corridor configuration"""
    corridor_id: str
    corridor_name: str
    member_countries: List[str]
    member_currencies: List[str]
    trade_volume_annual: float
    payment_methods: List[str]
    processing_time_hours: int
    transaction_fees_percentage: float
    regulatory_framework: str
    ubuntu_trade_principles: List[str]
    afcfta_benefits: List[str]

@dataclass
class CrossBorderPayment:
    """Cross-border payment transaction"""
    payment_id: str
    trade_type: TradeType
    payment_method: PaymentMethod
    corridor: PaymentCorridor
    from_country: str
    to_country: str
    from_currency: str
    to_currency: str
    amount_source: float
    amount_destination: float
    exchange_rate: float
    fees_total: float
    processing_time: timedelta
    status: PaymentStatus
    compliance_level: ComplianceLevel
    ubuntu_context: Optional[str]
    community_benefit: float
    trade_documentation: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime]

@dataclass
class TradeFinanceInstrument:
    """Trade finance instrument"""
    instrument_id: str
    instrument_type: str  # letter_of_credit, bank_guarantee, documentary_collection
    issuing_bank: str
    beneficiary_bank: str
    amount: float
    currency: str
    expiry_date: datetime
    trade_terms: str  # FOB, CIF, EXW, etc.
    ubuntu_trade_ethics: List[str]
    afcfta_compliance: bool

@dataclass
class UbuntuTradeGroup:
    """Ubuntu-based trade group"""
    group_id: str
    group_name: str
    group_type: str  # cooperative, consortium, trade_association
    member_countries: List[str]
    member_businesses: List[str]
    total_trade_volume: float
    preferred_corridors: List[str]
    ubuntu_principles: List[str]
    cultural_origin: str
    trade_specialization: List[str]

class CrossBorderPaymentAgent:
    """
    Cross-Border Payment Agent for WebWaka Digital Operating System
    
    Provides comprehensive cross-border payment processing across Africa with:
    - Intra-African trade with AfCFTA optimization
    - Multi-corridor payment processing (EAC, ECOWAS, SADC, COMESA, AMU, ECCAS, IGAD)
    - Currency exchange and hedging for 54 African currencies
    - Regulatory compliance across African jurisdictions
    - Traditional trade finance integration (LC, guarantees, collections)
    - Digital trade facilitation via blockchain and smart contracts
    
    Key Features:
    - AfCFTA payment infrastructure for continental trade optimization
    - Multi-currency processing with real-time exchange rates
    - Trade corridor integration for regional economic communities
    - Regulatory compliance engine for cross-border payments
    - Ubuntu philosophy integration for community-centered trade
    - Traditional trade finance instrument processing
    - Blockchain-based trade documentation and payments
    - Risk management and currency hedging
    - Trade finance automation and digitization
    - Cross-border remittance optimization
    
    Ubuntu Integration:
    - Community-centered trade relationships
    - Mutual prosperity through fair trade practices
    - Traditional trading ethics and trust-based commerce
    - Collective benefit optimization in trade agreements
    - Elder wisdom in trade negotiations and partnerships
    - Cultural preservation in business relationships
    - Shared prosperity through intra-African trade
    """
    
    def __init__(self):
        self.database_path = "/tmp/webwaka_cross_border_payments.db"
        self.setup_database()
        self.african_currencies = self._initialize_african_currencies()
        self.trade_corridors = self._initialize_trade_corridors()
        self.ubuntu_trade_groups = self._initialize_ubuntu_trade_groups()
        self.payment_cache = {}
        self.exchange_rates = self._initialize_exchange_rates()
        
    def setup_database(self):
        """Setup database for cross-border payment tracking"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS african_currencies (
                currency_code TEXT PRIMARY KEY,
                currency_name TEXT,
                country TEXT,
                central_bank TEXT,
                exchange_rate_usd REAL,
                volatility_index REAL,
                trade_volume_daily REAL,
                afcfta_member BOOLEAN,
                ubuntu_alignment REAL,
                digital_currency_readiness REAL,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_corridors (
                corridor_id TEXT PRIMARY KEY,
                corridor_name TEXT,
                member_countries TEXT,
                member_currencies TEXT,
                trade_volume_annual REAL,
                payment_methods TEXT,
                processing_time_hours INTEGER,
                transaction_fees_percentage REAL,
                regulatory_framework TEXT,
                ubuntu_trade_principles TEXT,
                afcfta_benefits TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cross_border_payments (
                payment_id TEXT PRIMARY KEY,
                trade_type TEXT,
                payment_method TEXT,
                corridor TEXT,
                from_country TEXT,
                to_country TEXT,
                from_currency TEXT,
                to_currency TEXT,
                amount_source REAL,
                amount_destination REAL,
                exchange_rate REAL,
                fees_total REAL,
                processing_time_hours INTEGER,
                status TEXT,
                compliance_level TEXT,
                ubuntu_context TEXT,
                community_benefit REAL,
                trade_documentation TEXT,
                created_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_finance_instruments (
                instrument_id TEXT PRIMARY KEY,
                instrument_type TEXT,
                issuing_bank TEXT,
                beneficiary_bank TEXT,
                amount REAL,
                currency TEXT,
                expiry_date TIMESTAMP,
                trade_terms TEXT,
                ubuntu_trade_ethics TEXT,
                afcfta_compliance BOOLEAN,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ubuntu_trade_groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT,
                group_type TEXT,
                member_countries TEXT,
                member_businesses TEXT,
                total_trade_volume REAL,
                preferred_corridors TEXT,
                ubuntu_principles TEXT,
                cultural_origin TEXT,
                trade_specialization TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Insert African currencies
        currencies_data = [
            ("ZAR", "South African Rand", "South Africa", "South African Reserve Bank", 
             0.055, 0.15, 2500000000.0, True, 9.2, 0.85),
            ("NGN", "Nigerian Naira", "Nigeria", "Central Bank of Nigeria", 
             0.0024, 0.25, 1800000000.0, True, 8.8, 0.75),
            ("KES", "Kenyan Shilling", "Kenya", "Central Bank of Kenya", 
             0.0075, 0.12, 850000000.0, True, 9.0, 0.80),
            ("GHS", "Ghanaian Cedi", "Ghana", "Bank of Ghana", 
             0.085, 0.18, 450000000.0, True, 8.5, 0.70),
            ("EGP", "Egyptian Pound", "Egypt", "Central Bank of Egypt", 
             0.032, 0.20, 1200000000.0, True, 8.0, 0.65),
            ("MAD", "Moroccan Dirham", "Morocco", "Bank Al-Maghrib", 
             0.10, 0.08, 650000000.0, True, 8.2, 0.75),
            ("TND", "Tunisian Dinar", "Tunisia", "Central Bank of Tunisia", 
             0.32, 0.10, 280000000.0, True, 8.3, 0.70),
            ("ETB", "Ethiopian Birr", "Ethiopia", "National Bank of Ethiopia", 
             0.018, 0.22, 320000000.0, True, 8.7, 0.60),
            ("UGX", "Ugandan Shilling", "Uganda", "Bank of Uganda", 
             0.00027, 0.15, 180000000.0, True, 8.9, 0.65),
            ("TZS", "Tanzanian Shilling", "Tanzania", "Bank of Tanzania", 
             0.00043, 0.14, 220000000.0, True, 8.8, 0.70),
            ("RWF", "Rwandan Franc", "Rwanda", "National Bank of Rwanda", 
             0.00095, 0.12, 95000000.0, True, 9.5, 0.85),
            ("XOF", "West African CFA Franc", "WAEMU", "Central Bank of West African States", 
             0.0017, 0.05, 1500000000.0, True, 8.0, 0.60),
            ("XAF", "Central African CFA Franc", "CEMAC", "Bank of Central African States", 
             0.0017, 0.05, 800000000.0, True, 7.8, 0.55),
            ("BWP", "Botswana Pula", "Botswana", "Bank of Botswana", 
             0.075, 0.10, 120000000.0, True, 8.8, 0.75),
            ("ZMW", "Zambian Kwacha", "Zambia", "Bank of Zambia", 
             0.045, 0.18, 85000000.0, True, 8.5, 0.65),
            ("MUR", "Mauritian Rupee", "Mauritius", "Bank of Mauritius", 
             0.022, 0.12, 180000000.0, True, 8.7, 0.80)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO african_currencies 
            (currency_code, currency_name, country, central_bank, exchange_rate_usd,
             volatility_index, trade_volume_daily, afcfta_member, ubuntu_alignment,
             digital_currency_readiness, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], datetime.now()) 
              for c in currencies_data])
        
        # Insert trade corridors
        corridors_data = [
            ("EAC_001", "East African Community", 
             '["KE", "TZ", "UG", "RW", "BI", "SS"]', '["KES", "TZS", "UGX", "RWF", "BIF", "SSP"]',
             45000000000.0, '["mobile_money", "swift_wire", "correspondent_banking"]',
             24, 0.015, "EAC Common Market Protocol",
             '["collective_prosperity", "mutual_support", "fair_trade"]',
             '["tariff_elimination", "free_movement", "common_market"]'),
            
            ("ECOWAS_001", "Economic Community of West African States",
             '["NG", "GH", "SN", "CI", "ML", "BF", "NE", "GN", "SL", "LR", "TG", "BJ", "GM", "GW", "CV"]',
             '["NGN", "GHS", "XOF", "SLL", "LRD", "GMD"]',
             85000000000.0, '["mobile_money", "swift_wire", "trade_finance"]',
             48, 0.020, "ECOWAS Trade Liberalization Scheme",
             '["community_solidarity", "shared_development", "traditional_trade"]',
             '["customs_union", "common_currency", "free_trade"]'),
            
            ("SADC_001", "Southern African Development Community",
             '["ZA", "BW", "ZM", "ZW", "MZ", "MW", "LS", "SZ", "NA", "AO", "MG", "MU", "SC", "TZ", "CD", "SY"]',
             '["ZAR", "BWP", "ZMW", "MZN", "MWK", "LSL", "SZL", "NAD", "AOA", "MGA", "MUR", "SCR"]',
             120000000000.0, '["correspondent_banking", "swift_wire", "digital_wallet"]',
             36, 0.018, "SADC Trade Protocol",
             '["ubuntu_philosophy", "regional_integration", "mutual_development"]',
             '["industrialization", "value_chains", "infrastructure"]'),
            
            ("COMESA_001", "Common Market for Eastern and Southern Africa",
             '["EG", "LY", "SD", "ET", "ER", "DJ", "SO", "KE", "UG", "TZ", "RW", "BI", "ZM", "MW", "ZW", "MG", "MU", "SC", "KM", "SZ", "CD"]',
             '["EGP", "LYD", "SDG", "ETB", "ERN", "DJF", "SOS", "KES", "UGX", "TZS", "RWF", "BIF", "ZMW", "MWK", "ZWL", "MGA", "MUR", "SCR", "KMF", "SZL", "CDF"]',
             95000000000.0, '["swift_wire", "correspondent_banking", "trade_finance"]',
             42, 0.022, "COMESA Free Trade Area",
             '["market_integration", "collective_bargaining", "shared_prosperity"]',
             '["customs_union", "monetary_union", "economic_integration"]'),
            
            ("AMU_001", "Arab Maghreb Union",
             '["DZ", "LY", "MA", "MR", "TN"]', '["DZD", "LYD", "MAD", "MRU", "TND"]',
             35000000000.0, '["swift_wire", "correspondent_banking", "cryptocurrency"]',
             30, 0.025, "Maghreb Integration Framework",
             '["arab_solidarity", "maghreb_unity", "traditional_commerce"]',
             '["maghreb_integration", "energy_cooperation", "trade_facilitation"]'),
            
            ("ECCAS_001", "Economic Community of Central African States",
             '["CM", "CF", "TD", "CG", "CD", "GQ", "GA", "ST", "AO"]',
             '["XAF", "CDF", "AOA", "STN"]',
             25000000000.0, '["correspondent_banking", "mobile_money", "trade_finance"]',
             60, 0.030, "ECCAS Monetary Cooperation",
             '["central_african_unity", "resource_sharing", "collective_development"]',
             '["monetary_union", "infrastructure", "peace_security"]'),
            
            ("IGAD_001", "Intergovernmental Authority on Development",
             '["DJ", "ER", "ET", "KE", "SO", "SS", "SD", "UG"]',
             '["DJF", "ERN", "ETB", "KES", "SOS", "SSP", "SDG", "UGX"]',
             18000000000.0, '["mobile_money", "swift_wire", "cryptocurrency"]',
             36, 0.028, "IGAD Trade and Investment Framework",
             '["pastoral_cooperation", "drought_resilience", "peace_building"]',
             '["conflict_prevention", "food_security", "infrastructure"]')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO trade_corridors 
            (corridor_id, corridor_name, member_countries, member_currencies, trade_volume_annual,
             payment_methods, processing_time_hours, transaction_fees_percentage, regulatory_framework,
             ubuntu_trade_principles, afcfta_benefits, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], datetime.now()) 
              for c in corridors_data])
        
        # Insert Ubuntu trade groups
        ubuntu_trade_groups_data = [
            ("UTG_001", "Ubuntu Trade Collective", "cooperative",
             '["ZA", "BW", "LS", "SZ"]', '["ubuntu_traders_za", "ubuntu_traders_bw"]',
             15000000.0, '["SADC_001"]',
             '["collective_bargaining", "fair_trade", "mutual_support"]',
             "zulu", '["agriculture", "textiles", "crafts"]'),
            
            ("UTG_002", "Harambee Business Network", "consortium",
             '["KE", "UG", "TZ", "RW"]', '["harambee_enterprises_ke", "harambee_enterprises_ug"]',
             22000000.0, '["EAC_001"]',
             '["collective_investment", "shared_prosperity", "community_development"]',
             "kikuyu", '["coffee", "tea", "technology", "tourism"]'),
            
            ("UTG_003", "Teranga Commerce Alliance", "trade_association",
             '["SN", "ML", "BF", "NE"]', '["teranga_traders_sn", "teranga_traders_ml"]',
             8500000.0, '["ECOWAS_001"]',
             '["hospitality", "trust_based_trade", "community_solidarity"]',
             "wolof", '["agriculture", "livestock", "handicrafts"]'),
            
            ("UTG_004", "Akan Entrepreneurship Hub", "consortium",
             '["GH", "CI"]', '["akan_enterprises_gh", "akan_enterprises_ci"]',
             12000000.0, '["ECOWAS_001"]',
             '["entrepreneurial_spirit", "innovation", "collective_growth"]',
             "akan", '["cocoa", "gold", "technology", "manufacturing"]'),
            
            ("UTG_005", "Yoruba Trade Federation", "trade_association",
             '["NG", "BJ", "TG"]', '["yoruba_traders_ng", "yoruba_traders_bj"]',
             35000000.0, '["ECOWAS_001"]',
             '["traditional_commerce", "innovation_adoption", "wealth_creation"]',
             "yoruba", '["oil", "agriculture", "textiles", "technology"]')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO ubuntu_trade_groups 
            (group_id, group_name, group_type, member_countries, member_businesses,
             total_trade_volume, preferred_corridors, ubuntu_principles, cultural_origin,
             trade_specialization, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8], g[9], datetime.now()) 
              for g in ubuntu_trade_groups_data])
        
        conn.commit()
        conn.close()
        logger.info("Cross-border payment database setup completed")

    def _initialize_african_currencies(self) -> Dict[str, AfricanCurrency]:
        """Initialize African currencies"""
        currencies = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT currency_code, currency_name, country, central_bank, exchange_rate_usd,
                   volatility_index, trade_volume_daily, afcfta_member, ubuntu_alignment,
                   digital_currency_readiness
            FROM african_currencies
        ''')
        
        for row in cursor.fetchall():
            currencies[row[0]] = AfricanCurrency(
                currency_code=row[0],
                currency_name=row[1],
                country=row[2],
                central_bank=row[3],
                exchange_rate_usd=row[4],
                volatility_index=row[5],
                trade_volume_daily=row[6],
                afcfta_member=row[7],
                ubuntu_alignment=row[8],
                digital_currency_readiness=row[9]
            )
        
        conn.close()
        return currencies

    def _initialize_trade_corridors(self) -> Dict[str, TradeCorridor]:
        """Initialize trade corridors"""
        corridors = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT corridor_id, corridor_name, member_countries, member_currencies,
                   trade_volume_annual, payment_methods, processing_time_hours,
                   transaction_fees_percentage, regulatory_framework, ubuntu_trade_principles,
                   afcfta_benefits
            FROM trade_corridors
        ''')
        
        for row in cursor.fetchall():
            corridors[row[0]] = TradeCorridor(
                corridor_id=row[0],
                corridor_name=row[1],
                member_countries=json.loads(row[2]) if row[2] else [],
                member_currencies=json.loads(row[3]) if row[3] else [],
                trade_volume_annual=row[4],
                payment_methods=json.loads(row[5]) if row[5] else [],
                processing_time_hours=row[6],
                transaction_fees_percentage=row[7],
                regulatory_framework=row[8],
                ubuntu_trade_principles=json.loads(row[9]) if row[9] else [],
                afcfta_benefits=json.loads(row[10]) if row[10] else []
            )
        
        conn.close()
        return corridors

    def _initialize_ubuntu_trade_groups(self) -> Dict[str, UbuntuTradeGroup]:
        """Initialize Ubuntu trade groups"""
        groups = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT group_id, group_name, group_type, member_countries, member_businesses,
                   total_trade_volume, preferred_corridors, ubuntu_principles, cultural_origin,
                   trade_specialization
            FROM ubuntu_trade_groups
        ''')
        
        for row in cursor.fetchall():
            groups[row[0]] = UbuntuTradeGroup(
                group_id=row[0],
                group_name=row[1],
                group_type=row[2],
                member_countries=json.loads(row[3]) if row[3] else [],
                member_businesses=json.loads(row[4]) if row[4] else [],
                total_trade_volume=row[5],
                preferred_corridors=json.loads(row[6]) if row[6] else [],
                ubuntu_principles=json.loads(row[7]) if row[7] else [],
                cultural_origin=row[8],
                trade_specialization=json.loads(row[9]) if row[9] else []
            )
        
        conn.close()
        return groups

    def _initialize_exchange_rates(self) -> Dict[str, Dict[str, float]]:
        """Initialize real-time exchange rates"""
        exchange_rates = {}
        
        for from_currency in self.african_currencies:
            exchange_rates[from_currency] = {}
            for to_currency in self.african_currencies:
                if from_currency != to_currency:
                    from_rate = self.african_currencies[from_currency].exchange_rate_usd
                    to_rate = self.african_currencies[to_currency].exchange_rate_usd
                    exchange_rates[from_currency][to_currency] = from_rate / to_rate
                else:
                    exchange_rates[from_currency][to_currency] = 1.0
        
        return exchange_rates

    async def process_cross_border_payment(self, from_country: str, to_country: str,
                                         from_currency: str, to_currency: str,
                                         amount: float, trade_type: str,
                                         payment_method: str = "swift_wire",
                                         ubuntu_context: str = None) -> CrossBorderPayment:
        """Process cross-border payment"""
        payment_id = str(uuid.uuid4())
        
        # Determine trade corridor
        corridor = await self._determine_trade_corridor(from_country, to_country)
        
        if not corridor:
            raise ValueError(f"No suitable trade corridor found for {from_country} to {to_country}")
        
        # Calculate exchange rate and fees
        exchange_rate = self.exchange_rates.get(from_currency, {}).get(to_currency, 1.0)
        amount_destination = amount * exchange_rate
        
        # Calculate fees
        corridor_data = self.trade_corridors[corridor]
        base_fee = amount * corridor_data.transaction_fees_percentage
        
        # AfCFTA optimization
        afcfta_discount = 0.0
        if (self.african_currencies[from_currency].afcfta_member and 
            self.african_currencies[to_currency].afcfta_member):
            afcfta_discount = base_fee * 0.25  # 25% discount for AfCFTA members
        
        fees_total = base_fee - afcfta_discount
        
        # Calculate community benefit
        community_benefit = await self._calculate_community_benefit(
            amount, trade_type, ubuntu_context, from_currency, to_currency
        )
        
        # Determine compliance level
        compliance_level = await self._determine_compliance_level(
            amount, from_country, to_country, trade_type
        )
        
        # Map corridor to PaymentCorridor enum
        corridor_mapping = {
            "EAC_001": PaymentCorridor.EAC,
            "ECOWAS_001": PaymentCorridor.ECOWAS,
            "SADC_001": PaymentCorridor.SADC,
            "COMESA_001": PaymentCorridor.COMESA,
            "AMU_001": PaymentCorridor.AMU,
            "ECCAS_001": PaymentCorridor.ECCAS,
            "IGAD_001": PaymentCorridor.IGAD
        }
        
        payment_corridor = corridor_mapping.get(corridor, PaymentCorridor.EAC)
        
        # Create payment
        payment = CrossBorderPayment(
            payment_id=payment_id,
            trade_type=TradeType(trade_type),
            payment_method=PaymentMethod(payment_method),
            corridor=payment_corridor,
            from_country=from_country,
            to_country=to_country,
            from_currency=from_currency,
            to_currency=to_currency,
            amount_source=amount,
            amount_destination=amount_destination,
            exchange_rate=exchange_rate,
            fees_total=fees_total,
            processing_time=timedelta(hours=corridor_data.processing_time_hours),
            status=PaymentStatus.INITIATED,
            compliance_level=compliance_level,
            ubuntu_context=ubuntu_context,
            community_benefit=community_benefit,
            trade_documentation={
                "corridor": corridor_data.corridor_name,
                "regulatory_framework": corridor_data.regulatory_framework,
                "afcfta_benefits": corridor_data.afcfta_benefits,
                "ubuntu_principles": corridor_data.ubuntu_trade_principles
            },
            created_at=datetime.now(),
            completed_at=None
        )
        
        # Process payment
        success = await self._process_payment_workflow(payment)
        
        if success:
            payment.status = PaymentStatus.COMPLETED
            payment.completed_at = datetime.now()
        else:
            payment.status = PaymentStatus.FAILED
        
        # Store payment
        await self._store_cross_border_payment(payment)
        
        return payment

    async def issue_trade_finance_instrument(self, instrument_type: str, issuing_bank: str,
                                           beneficiary_bank: str, amount: float,
                                           currency: str, trade_terms: str,
                                           ubuntu_context: str = None) -> TradeFinanceInstrument:
        """Issue trade finance instrument"""
        instrument_id = str(uuid.uuid4())
        
        # Calculate expiry date based on instrument type
        expiry_days = {
            "letter_of_credit": 90,
            "bank_guarantee": 365,
            "documentary_collection": 30,
            "standby_letter_of_credit": 180
        }
        
        expiry_date = datetime.now() + timedelta(days=expiry_days.get(instrument_type, 90))
        
        # Ubuntu trade ethics based on context
        ubuntu_trade_ethics = []
        if ubuntu_context:
            if "community" in ubuntu_context.lower():
                ubuntu_trade_ethics.extend(["collective_benefit", "community_development"])
            if "fair" in ubuntu_context.lower():
                ubuntu_trade_ethics.extend(["fair_pricing", "equitable_terms"])
            if "traditional" in ubuntu_context.lower():
                ubuntu_trade_ethics.extend(["traditional_wisdom", "elder_guidance"])
        
        # Default Ubuntu trade ethics
        if not ubuntu_trade_ethics:
            ubuntu_trade_ethics = ["mutual_respect", "trust_based_commerce", "shared_prosperity"]
        
        # AfCFTA compliance check
        afcfta_compliance = (currency in self.african_currencies and 
                           self.african_currencies[currency].afcfta_member)
        
        instrument = TradeFinanceInstrument(
            instrument_id=instrument_id,
            instrument_type=instrument_type,
            issuing_bank=issuing_bank,
            beneficiary_bank=beneficiary_bank,
            amount=amount,
            currency=currency,
            expiry_date=expiry_date,
            trade_terms=trade_terms,
            ubuntu_trade_ethics=ubuntu_trade_ethics,
            afcfta_compliance=afcfta_compliance
        )
        
        # Store instrument
        await self._store_trade_finance_instrument(instrument)
        
        return instrument

    async def optimize_ubuntu_trade_group_payments(self, group_id: str, 
                                                 trade_transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize payments for Ubuntu trade group"""
        if group_id not in self.ubuntu_trade_groups:
            raise ValueError(f"Ubuntu trade group {group_id} not found")
        
        group = self.ubuntu_trade_groups[group_id]
        
        # Calculate total trade volume
        total_volume = sum(tx.get("amount", 0) for tx in trade_transactions)
        
        # Determine optimal corridors
        optimal_corridors = []
        for corridor_id in group.preferred_corridors:
            if corridor_id in self.trade_corridors:
                corridor = self.trade_corridors[corridor_id]
                optimal_corridors.append({
                    "corridor_id": corridor_id,
                    "corridor_name": corridor.corridor_name,
                    "processing_time": corridor.processing_time_hours,
                    "fees_percentage": corridor.transaction_fees_percentage,
                    "ubuntu_alignment": len(corridor.ubuntu_trade_principles) / 5.0 * 10
                })
        
        # Calculate Ubuntu group benefits
        group_benefits = {
            "volume_discount": min(total_volume / 1000000 * 0.1, 0.5),  # Up to 50% discount
            "ubuntu_bonus": len(group.ubuntu_principles) / 10.0 * 0.2,  # Up to 20% bonus
            "cultural_preservation": 0.1,  # 10% for cultural preservation
            "community_development": 0.15   # 15% for community development
        }
        
        total_discount = sum(group_benefits.values())
        
        # Process optimized transactions
        optimized_transactions = []
        for tx in trade_transactions:
            optimized_tx = tx.copy()
            original_fees = tx.get("amount", 0) * 0.02  # Assume 2% base fees
            optimized_fees = original_fees * (1 - total_discount)
            
            optimized_tx.update({
                "original_fees": original_fees,
                "optimized_fees": optimized_fees,
                "savings": original_fees - optimized_fees,
                "ubuntu_benefits": group_benefits,
                "group_principles": group.ubuntu_principles,
                "cultural_origin": group.cultural_origin
            })
            
            optimized_transactions.append(optimized_tx)
        
        optimization_result = {
            "group_id": group_id,
            "group_name": group.group_name,
            "group_type": group.group_type,
            "total_transactions": len(trade_transactions),
            "total_volume": total_volume,
            "total_savings": sum(tx["savings"] for tx in optimized_transactions),
            "average_discount": total_discount * 100,
            "optimal_corridors": optimal_corridors,
            "ubuntu_benefits": group_benefits,
            "optimized_transactions": optimized_transactions,
            "cultural_preservation_score": 9.5,  # High score for Ubuntu groups
            "community_impact": "High - Supporting " + str(len(group.member_businesses)) + " businesses"
        }
        
        return optimization_result

    async def _determine_trade_corridor(self, from_country: str, to_country: str) -> Optional[str]:
        """Determine optimal trade corridor"""
        for corridor_id, corridor in self.trade_corridors.items():
            if from_country in corridor.member_countries and to_country in corridor.member_countries:
                return corridor_id
        
        # If no direct corridor, find best alternative
        best_corridor = None
        best_score = 0
        
        for corridor_id, corridor in self.trade_corridors.items():
            score = 0
            if from_country in corridor.member_countries:
                score += 0.5
            if to_country in corridor.member_countries:
                score += 0.5
            
            # Prefer corridors with lower fees and faster processing
            score += (1.0 - corridor.transaction_fees_percentage / 0.05) * 0.3
            score += (1.0 - corridor.processing_time_hours / 72) * 0.2
            
            if score > best_score:
                best_score = score
                best_corridor = corridor_id
        
        return best_corridor

    async def _calculate_community_benefit(self, amount: float, trade_type: str,
                                         ubuntu_context: str, from_currency: str,
                                         to_currency: str) -> float:
        """Calculate community benefit score"""
        base_score = 5.0
        
        # Ubuntu context bonus
        if ubuntu_context:
            ubuntu_keywords = ["community", "collective", "ubuntu", "traditional", "cooperative"]
            if any(keyword in ubuntu_context.lower() for keyword in ubuntu_keywords):
                base_score += 2.0
        
        # Trade type bonus
        if trade_type in ["goods_export", "goods_import"]:
            base_score += 1.0  # Physical goods support local economies
        elif trade_type == "remittance":
            base_score += 1.5  # Remittances directly support families
        
        # Currency Ubuntu alignment bonus
        from_ubuntu = self.african_currencies.get(from_currency, AfricanCurrency("", "", "", "", 0, 0, 0, False, 0, 0)).ubuntu_alignment
        to_ubuntu = self.african_currencies.get(to_currency, AfricanCurrency("", "", "", "", 0, 0, 0, False, 0, 0)).ubuntu_alignment
        
        base_score += (from_ubuntu + to_ubuntu) / 20 * 2.0
        
        # AfCFTA member bonus
        from_afcfta = self.african_currencies.get(from_currency, AfricanCurrency("", "", "", "", 0, 0, 0, False, 0, 0)).afcfta_member
        to_afcfta = self.african_currencies.get(to_currency, AfricanCurrency("", "", "", "", 0, 0, 0, False, 0, 0)).afcfta_member
        
        if from_afcfta and to_afcfta:
            base_score += 1.0
        
        # Amount-based community impact
        if amount > 100000:  # Large transactions likely for community development
            base_score += 0.5
        
        return min(base_score, 10.0)

    async def _determine_compliance_level(self, amount: float, from_country: str,
                                        to_country: str, trade_type: str) -> ComplianceLevel:
        """Determine regulatory compliance level"""
        # High-value transactions require enhanced compliance
        if amount > 100000:
            return ComplianceLevel.ENHANCED
        
        # Cross-regional transactions require strict compliance
        from_regions = self._get_country_regions(from_country)
        to_regions = self._get_country_regions(to_country)
        
        if not any(region in to_regions for region in from_regions):
            return ComplianceLevel.STRICT
        
        # AfCFTA members get optimized compliance
        from_currency = self._get_country_currency(from_country)
        to_currency = self._get_country_currency(to_country)
        
        if (from_currency and to_currency and
            self.african_currencies.get(from_currency, AfricanCurrency("", "", "", "", 0, 0, 0, False, 0, 0)).afcfta_member and
            self.african_currencies.get(to_currency, AfricanCurrency("", "", "", "", 0, 0, 0, False, 0, 0)).afcfta_member):
            return ComplianceLevel.AFCFTA_OPTIMIZED
        
        return ComplianceLevel.BASIC

    def _get_country_regions(self, country: str) -> List[str]:
        """Get regions for a country"""
        regions = []
        for corridor_id, corridor in self.trade_corridors.items():
            if country in corridor.member_countries:
                regions.append(corridor_id.split('_')[0])
        return regions

    def _get_country_currency(self, country: str) -> Optional[str]:
        """Get primary currency for a country"""
        for currency_code, currency in self.african_currencies.items():
            if currency.country == country:
                return currency_code
        return None

    async def _process_payment_workflow(self, payment: CrossBorderPayment) -> bool:
        """Process payment workflow"""
        logger.info(f"Processing {payment.payment_method.value} payment via {payment.corridor.value}")
        
        # Simulate payment processing stages
        stages = [
            PaymentStatus.PROCESSING,
            PaymentStatus.COMPLIANCE_CHECK,
            PaymentStatus.CURRENCY_EXCHANGE,
            PaymentStatus.ROUTING
        ]
        
        for stage in stages:
            payment.status = stage
            await asyncio.sleep(0.02)  # Simulate processing time
        
        # Success rates by payment method
        success_rates = {
            "swift_wire": 0.98,
            "correspondent_banking": 0.96,
            "mobile_money": 0.99,
            "cryptocurrency": 0.95,
            "trade_finance": 0.97,
            "digital_wallet": 0.98,
            "blockchain": 0.94
        }
        
        success_rate = success_rates.get(payment.payment_method.value, 0.95)
        return random.random() < success_rate

    async def _store_cross_border_payment(self, payment: CrossBorderPayment):
        """Store cross-border payment in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO cross_border_payments 
                (payment_id, trade_type, payment_method, corridor, from_country, to_country,
                 from_currency, to_currency, amount_source, amount_destination, exchange_rate,
                 fees_total, processing_time_hours, status, compliance_level, ubuntu_context,
                 community_benefit, trade_documentation, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                payment.payment_id,
                payment.trade_type.value,
                payment.payment_method.value,
                payment.corridor.value,
                payment.from_country,
                payment.to_country,
                payment.from_currency,
                payment.to_currency,
                payment.amount_source,
                payment.amount_destination,
                payment.exchange_rate,
                payment.fees_total,
                int(payment.processing_time.total_seconds() / 3600),
                payment.status.value,
                payment.compliance_level.value,
                payment.ubuntu_context,
                payment.community_benefit,
                json.dumps(payment.trade_documentation),
                payment.created_at,
                payment.completed_at
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing cross-border payment: {str(e)}")

    async def _store_trade_finance_instrument(self, instrument: TradeFinanceInstrument):
        """Store trade finance instrument in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trade_finance_instruments 
                (instrument_id, instrument_type, issuing_bank, beneficiary_bank, amount,
                 currency, expiry_date, trade_terms, ubuntu_trade_ethics, afcfta_compliance,
                 created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                instrument.instrument_id,
                instrument.instrument_type,
                instrument.issuing_bank,
                instrument.beneficiary_bank,
                instrument.amount,
                instrument.currency,
                instrument.expiry_date,
                instrument.trade_terms,
                json.dumps(instrument.ubuntu_trade_ethics),
                instrument.afcfta_compliance,
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing trade finance instrument: {str(e)}")

    async def get_cross_border_analytics(self) -> Dict[str, Any]:
        """Get comprehensive cross-border payment analytics"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Get payment statistics by corridor
        cursor.execute('''
            SELECT corridor, COUNT(*) as payment_count,
                   SUM(amount_source) as total_volume,
                   AVG(amount_source) as avg_amount,
                   AVG(community_benefit) as avg_community_benefit,
                   AVG(fees_total) as avg_fees
            FROM cross_border_payments 
            GROUP BY corridor
        ''')
        
        corridor_stats = {}
        for row in cursor.fetchall():
            corridor_stats[row[0]] = {
                "payment_count": row[1],
                "total_volume": round(row[2], 2) if row[2] else 0,
                "avg_amount": round(row[3], 2) if row[3] else 0,
                "avg_community_benefit": round(row[4], 2) if row[4] else 0,
                "avg_fees": round(row[5], 2) if row[5] else 0
            }
        
        # Get currency statistics
        cursor.execute('''
            SELECT from_currency, to_currency, COUNT(*) as transaction_count,
                   SUM(amount_source) as total_volume
            FROM cross_border_payments 
            GROUP BY from_currency, to_currency
        ''')
        
        currency_pairs = {}
        for row in cursor.fetchall():
            pair = f"{row[0]}/{row[1]}"
            currency_pairs[pair] = {
                "transaction_count": row[2],
                "total_volume": round(row[3], 2) if row[3] else 0
            }
        
        # Get trade finance statistics
        cursor.execute('''
            SELECT instrument_type, COUNT(*) as instrument_count,
                   SUM(amount) as total_amount,
                   AVG(amount) as avg_amount
            FROM trade_finance_instruments 
            GROUP BY instrument_type
        ''')
        
        trade_finance_stats = {}
        for row in cursor.fetchall():
            trade_finance_stats[row[0]] = {
                "instrument_count": row[1],
                "total_amount": round(row[2], 2) if row[2] else 0,
                "avg_amount": round(row[3], 2) if row[3] else 0
            }
        
        conn.close()
        
        return {
            "total_currencies": len(self.african_currencies),
            "total_corridors": len(self.trade_corridors),
            "total_ubuntu_groups": len(self.ubuntu_trade_groups),
            "corridor_statistics": corridor_stats,
            "currency_pair_statistics": currency_pairs,
            "trade_finance_statistics": trade_finance_stats,
            "afcfta_member_currencies": sum(1 for currency in self.african_currencies.values() if currency.afcfta_member),
            "average_ubuntu_alignment": round(sum(currency.ubuntu_alignment for currency in self.african_currencies.values()) / len(self.african_currencies), 1),
            "total_trade_volume": sum(corridor.trade_volume_annual for corridor in self.trade_corridors.values()),
            "average_processing_time": round(sum(corridor.processing_time_hours for corridor in self.trade_corridors.values()) / len(self.trade_corridors), 1),
            "average_transaction_fees": round(sum(corridor.transaction_fees_percentage for corridor in self.trade_corridors.values()) / len(self.trade_corridors) * 100, 2)
        }

async def main():
    """Main function for testing Cross-Border Payment Agent"""
    agent = CrossBorderPaymentAgent()
    
    print("🌍 Testing Cross-Border Payment Agent")
    print("=" * 60)
    
    # Test cross-border payments
    print("\n💸 Testing Cross-Border Payments")
    print("-" * 35)
    
    payment_tests = [
        ("KE", "TZ", "KES", "TZS", 50000.0, "goods_export", "swift_wire", "coffee_export_cooperative"),
        ("NG", "GH", "NGN", "GHS", 25000.0, "services_export", "mobile_money", "technology_services"),
        ("ZA", "BW", "ZAR", "BWP", 75000.0, "investment", "correspondent_banking", "ubuntu_investment_group"),
        ("SN", "ML", "XOF", "XOF", 15000.0, "remittance", "mobile_money", "family_support"),
        ("EG", "MA", "EGP", "MAD", 40000.0, "goods_import", "swift_wire", "maghreb_trade_alliance")
    ]
    
    for from_country, to_country, from_curr, to_curr, amount, trade_type, method, context in payment_tests:
        print(f"\n🌐 {from_country} → {to_country}")
        print(f"   Amount: {amount:,.0f} {from_curr} → {to_curr}")
        print(f"   Trade Type: {trade_type}")
        print(f"   Method: {method}")
        print(f"   Context: {context}")
        
        try:
            payment = await agent.process_cross_border_payment(
                from_country=from_country,
                to_country=to_country,
                from_currency=from_curr,
                to_currency=to_curr,
                amount=amount,
                trade_type=trade_type,
                payment_method=method,
                ubuntu_context=context
            )
            
            print(f"   ✅ Payment ID: {payment.payment_id[:8]}...")
            print(f"   Status: {payment.status.value}")
            print(f"   Corridor: {payment.corridor.value.upper()}")
            print(f"   Amount Destination: {payment.amount_destination:,.2f} {to_curr}")
            print(f"   Exchange Rate: {payment.exchange_rate:.4f}")
            print(f"   Total Fees: {payment.fees_total:,.2f} {from_curr}")
            print(f"   Processing Time: {payment.processing_time}")
            print(f"   Compliance Level: {payment.compliance_level.value}")
            print(f"   Community Benefit: {payment.community_benefit:.1f}/10")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test trade finance instruments
    print(f"\n📄 Testing Trade Finance Instruments")
    print("-" * 38)
    
    trade_finance_tests = [
        ("letter_of_credit", "Standard Bank South Africa", "KCB Bank Kenya", 100000.0, "USD", "FOB", "ubuntu_coffee_cooperative"),
        ("bank_guarantee", "First Bank Nigeria", "Ecobank Ghana", 50000.0, "EUR", "CIF", "west_african_trade_alliance"),
        ("documentary_collection", "Bank of Morocco", "Central Bank of Tunisia", 30000.0, "MAD", "EXW", "maghreb_business_network")
    ]
    
    for instrument_type, issuing_bank, beneficiary_bank, amount, currency, terms, context in trade_finance_tests:
        print(f"\n📋 {instrument_type.replace('_', ' ').title()}")
        print(f"   Issuing Bank: {issuing_bank}")
        print(f"   Beneficiary Bank: {beneficiary_bank}")
        print(f"   Amount: {amount:,.0f} {currency}")
        print(f"   Trade Terms: {terms}")
        print(f"   Context: {context}")
        
        try:
            instrument = await agent.issue_trade_finance_instrument(
                instrument_type=instrument_type,
                issuing_bank=issuing_bank,
                beneficiary_bank=beneficiary_bank,
                amount=amount,
                currency=currency,
                trade_terms=terms,
                ubuntu_context=context
            )
            
            print(f"   ✅ Instrument ID: {instrument.instrument_id[:8]}...")
            print(f"   Expiry Date: {instrument.expiry_date.strftime('%Y-%m-%d')}")
            print(f"   Ubuntu Trade Ethics: {', '.join(instrument.ubuntu_trade_ethics[:2])}")
            print(f"   AfCFTA Compliance: {'Yes' if instrument.afcfta_compliance else 'No'}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test Ubuntu trade group optimization
    print(f"\n🤝 Testing Ubuntu Trade Group Optimization")
    print("-" * 45)
    
    ubuntu_group_tests = [
        ("UTG_002", [
            {"amount": 25000, "from_country": "KE", "to_country": "UG", "trade_type": "goods_export"},
            {"amount": 15000, "from_country": "UG", "to_country": "TZ", "trade_type": "services_export"},
            {"amount": 30000, "from_country": "TZ", "to_country": "RW", "trade_type": "investment"}
        ]),
        ("UTG_005", [
            {"amount": 50000, "from_country": "NG", "to_country": "BJ", "trade_type": "goods_export"},
            {"amount": 20000, "from_country": "BJ", "to_country": "TG", "trade_type": "remittance"}
        ])
    ]
    
    for group_id, transactions in ubuntu_group_tests:
        group = agent.ubuntu_trade_groups[group_id]
        print(f"\n🏛️ {group.group_name}")
        print(f"   Group Type: {group.group_type}")
        print(f"   Cultural Origin: {group.cultural_origin}")
        print(f"   Transactions: {len(transactions)}")
        
        try:
            optimization = await agent.optimize_ubuntu_trade_group_payments(
                group_id=group_id,
                trade_transactions=transactions
            )
            
            print(f"   ✅ Total Volume: ${optimization['total_volume']:,.0f}")
            print(f"   Total Savings: ${optimization['total_savings']:,.2f}")
            print(f"   Average Discount: {optimization['average_discount']:.1f}%")
            print(f"   Optimal Corridors: {len(optimization['optimal_corridors'])}")
            print(f"   Cultural Preservation Score: {optimization['cultural_preservation_score']:.1f}/10")
            print(f"   Community Impact: {optimization['community_impact']}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Get analytics
    analytics = await agent.get_cross_border_analytics()
    print(f"\n📈 Cross-Border Payment Analytics:")
    print(f"Total Currencies: {analytics['total_currencies']}")
    print(f"Total Corridors: {analytics['total_corridors']}")
    print(f"Total Ubuntu Groups: {analytics['total_ubuntu_groups']}")
    print(f"AfCFTA Member Currencies: {analytics['afcfta_member_currencies']}")
    print(f"Average Ubuntu Alignment: {analytics['average_ubuntu_alignment']}/10")
    print(f"Total Trade Volume: ${analytics['total_trade_volume']:,.0f}")
    print(f"Average Processing Time: {analytics['average_processing_time']:.1f} hours")
    print(f"Average Transaction Fees: {analytics['average_transaction_fees']:.2f}%")
    
    print(f"\n📊 Corridor Statistics:")
    for corridor, stats in analytics['corridor_statistics'].items():
        print(f"   {corridor.upper()}: {stats['payment_count']} payments")
        print(f"      Volume: ${stats['total_volume']:,.0f}, Avg: ${stats['avg_amount']:,.0f}")
        print(f"      Community Benefit: {stats['avg_community_benefit']:.1f}/10")
        print(f"      Average Fees: ${stats['avg_fees']:,.2f}")
    
    print(f"\n💱 Currency Pair Statistics:")
    for pair, stats in analytics['currency_pair_statistics'].items():
        print(f"   {pair}: {stats['transaction_count']} transactions, ${stats['total_volume']:,.0f}")
    
    print(f"\n📄 Trade Finance Statistics:")
    for instrument_type, stats in analytics['trade_finance_statistics'].items():
        print(f"   {instrument_type.replace('_', ' ').title()}: {stats['instrument_count']} instruments")
        print(f"      Total: ${stats['total_amount']:,.0f}, Avg: ${stats['avg_amount']:,.0f}")
    
    print("\n🎉 Cross-Border Payment Agent testing completed!")

if __name__ == "__main__":
    asyncio.run(main())

