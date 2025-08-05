#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Traditional Banking Agent (Agent 29)
Comprehensive traditional banking integration for major African banks with Ubuntu philosophy,
SWIFT network connectivity, RTGS integration, and community banking services

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

class BankType(Enum):
    """Bank types"""
    COMMERCIAL_BANK = "commercial_bank"
    DEVELOPMENT_BANK = "development_bank"
    MICROFINANCE_BANK = "microfinance_bank"
    INVESTMENT_BANK = "investment_bank"
    COOPERATIVE_BANK = "cooperative_bank"
    ISLAMIC_BANK = "islamic_bank"

class TransactionType(Enum):
    """Banking transaction types"""
    ACCOUNT_TRANSFER = "account_transfer"
    WIRE_TRANSFER = "wire_transfer"
    SWIFT_TRANSFER = "swift_transfer"
    RTGS_TRANSFER = "rtgs_transfer"
    BILL_PAYMENT = "bill_payment"
    LOAN_DISBURSEMENT = "loan_disbursement"
    LOAN_REPAYMENT = "loan_repayment"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    STANDING_ORDER = "standing_order"

class AccountType(Enum):
    """Bank account types"""
    SAVINGS_ACCOUNT = "savings_account"
    CURRENT_ACCOUNT = "current_account"
    FIXED_DEPOSIT = "fixed_deposit"
    LOAN_ACCOUNT = "loan_account"
    INVESTMENT_ACCOUNT = "investment_account"
    SACCO_ACCOUNT = "sacco_account"
    GROUP_ACCOUNT = "group_account"

class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVERSED = "reversed"
    UNDER_REVIEW = "under_review"

@dataclass
class AfricanBank:
    """African bank configuration"""
    bank_id: str
    bank_name: str
    bank_code: str
    swift_code: str
    bank_type: BankType
    countries: List[str]
    headquarters: str
    api_endpoint: str
    api_version: str
    supported_currencies: List[str]
    branch_count: int
    atm_count: int
    digital_banking: bool
    mobile_banking: bool
    internet_banking: bool
    swift_enabled: bool
    rtgs_enabled: bool
    ubuntu_alignment: float
    community_banking: bool
    sacco_integration: bool

@dataclass
class BankAccount:
    """Bank account"""
    account_id: str
    account_number: str
    account_type: AccountType
    bank_id: str
    customer_id: str
    account_name: str
    currency: str
    balance: float
    available_balance: float
    overdraft_limit: float
    interest_rate: float
    ubuntu_group_id: Optional[str]
    is_active: bool
    created_at: datetime

@dataclass
class BankingTransaction:
    """Banking transaction"""
    transaction_id: str
    transaction_type: TransactionType
    source_account: str
    destination_account: str
    amount: float
    currency: str
    exchange_rate: Optional[float]
    reference: str
    description: str
    swift_message: Optional[str]
    status: TransactionStatus
    ubuntu_context: Optional[str]
    community_benefit: float
    fees: float
    processing_time: timedelta
    created_at: datetime
    completed_at: Optional[datetime]

@dataclass
class UbuntuBankingGroup:
    """Ubuntu-based banking group (SACCO, Investment Club, etc.)"""
    group_id: str
    group_name: str
    group_type: str  # sacco, investment_club, savings_group
    bank_id: str
    group_account_number: str
    members: List[str]
    admin_customer_id: str
    total_deposits: float
    total_loans: float
    interest_rate: float
    ubuntu_principles: List[str]
    cultural_origin: str
    governance_structure: str

class TraditionalBankingAgent:
    """
    Traditional Banking Agent for WebWaka Digital Operating System
    
    Provides comprehensive traditional banking integration across Africa with:
    - Standard Bank Group - South Africa, pan-African presence (20 countries)
    - Equity Bank - Kenya, East African expansion (6 countries)  
    - First Bank of Nigeria - Nigeria, West African presence (9 countries)
    - Ecobank - Pan-African bank (33 countries)
    - KCB Group - Kenya Commercial Bank, East African focus (7 countries)
    - Absa Group - South Africa, African expansion (12 countries)
    
    Key Features:
    - Multi-bank API integration with unified interface
    - Core banking system connectivity for real-time processing
    - SWIFT network integration for international transfers
    - Real-Time Gross Settlement (RTGS) system integration
    - Internet and mobile banking platform connectivity
    - Branch and ATM network integration
    - Ubuntu philosophy integration for community banking
    - SACCO (Savings and Credit Cooperative) integration
    - Group lending and community guarantee systems
    - Islamic banking compliance for Muslim communities
    - Microfinance integration for rural communities
    - Cross-border payment facilitation
    - Regulatory compliance across African jurisdictions
    
    Ubuntu Integration:
    - Community banking and collective financial services
    - Traditional savings and credit associations (SACCOs)
    - Group lending with community guarantee systems
    - Elder financial wisdom and guidance integration
    - Collective prosperity and shared financial growth
    - Traditional governance in banking decisions
    - Cultural preservation in banking practices
    """
    
    def __init__(self):
        self.database_path = "/tmp/webwaka_traditional_banking.db"
        self.setup_database()
        self.banks = self._initialize_banks()
        self.ubuntu_banking_groups = self._initialize_ubuntu_banking_groups()
        self.transaction_cache = {}
        self.api_keys = self._initialize_api_keys()
        
    def setup_database(self):
        """Setup database for traditional banking integration tracking"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS african_banks (
                bank_id TEXT PRIMARY KEY,
                bank_name TEXT,
                bank_code TEXT,
                swift_code TEXT,
                bank_type TEXT,
                countries TEXT,
                headquarters TEXT,
                api_endpoint TEXT,
                api_version TEXT,
                supported_currencies TEXT,
                branch_count INTEGER,
                atm_count INTEGER,
                digital_banking BOOLEAN,
                mobile_banking BOOLEAN,
                internet_banking BOOLEAN,
                swift_enabled BOOLEAN,
                rtgs_enabled BOOLEAN,
                ubuntu_alignment REAL,
                community_banking BOOLEAN,
                sacco_integration BOOLEAN,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bank_accounts (
                account_id TEXT PRIMARY KEY,
                account_number TEXT,
                account_type TEXT,
                bank_id TEXT,
                customer_id TEXT,
                account_name TEXT,
                currency TEXT,
                balance REAL,
                available_balance REAL,
                overdraft_limit REAL,
                interest_rate REAL,
                ubuntu_group_id TEXT,
                is_active BOOLEAN,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS banking_transactions (
                transaction_id TEXT PRIMARY KEY,
                transaction_type TEXT,
                source_account TEXT,
                destination_account TEXT,
                amount REAL,
                currency TEXT,
                exchange_rate REAL,
                reference TEXT,
                description TEXT,
                swift_message TEXT,
                status TEXT,
                ubuntu_context TEXT,
                community_benefit REAL,
                fees REAL,
                processing_time_seconds INTEGER,
                created_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ubuntu_banking_groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT,
                group_type TEXT,
                bank_id TEXT,
                group_account_number TEXT,
                members TEXT,
                admin_customer_id TEXT,
                total_deposits REAL,
                total_loans REAL,
                interest_rate REAL,
                ubuntu_principles TEXT,
                cultural_origin TEXT,
                governance_structure TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS swift_messages (
                message_id TEXT PRIMARY KEY,
                transaction_id TEXT,
                message_type TEXT,
                sender_bic TEXT,
                receiver_bic TEXT,
                message_content TEXT,
                processing_status TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Insert major African banks
        banks_data = [
            ("STD_001", "Standard Bank Group", "051", "SBZAZAJJ", "commercial_bank",
             '["ZA", "BW", "GH", "KE", "MW", "MZ", "NA", "NG", "TZ", "UG", "ZM", "ZW", "AO", "CD", "SS", "SZ", "LS", "MU", "SC", "MG"]',
             "Johannesburg, South Africa", "https://api.standardbank.co.za/v1/", "v1",
             '["ZAR", "USD", "EUR", "GBP", "BWP", "GHS", "KES", "MWK", "MZN", "NAD", "NGN", "TZS", "UGX", "ZMW", "ZWL"]',
             1200, 8500, True, True, True, True, True, 8.5, True, True),
            
            ("EQB_001", "Equity Bank Group", "068", "EQBLKENA", "commercial_bank",
             '["KE", "UG", "TZ", "RW", "SS", "CD"]',
             "Nairobi, Kenya", "https://api.equitybank.co.ke/v1/", "v1",
             '["KES", "UGX", "TZS", "RWF", "SSP", "CDF", "USD"]',
             280, 1200, True, True, True, True, True, 9.2, True, True),
            
            ("FBN_001", "First Bank of Nigeria", "011", "FBNINGLA", "commercial_bank",
             '["NG", "GH", "SL", "LR", "GM", "GN", "SN", "BF", "CI"]',
             "Lagos, Nigeria", "https://api.firstbanknigeria.com/v1/", "v1",
             '["NGN", "GHS", "SLL", "LRD", "GMD", "GNF", "XOF", "USD", "EUR"]',
             750, 3200, True, True, True, True, True, 8.8, True, False),
            
            ("ECO_001", "Ecobank Group", "050", "ECOCNGLA", "commercial_bank",
             '["NG", "GH", "CI", "SN", "ML", "BF", "NE", "TG", "BJ", "GN", "SL", "LR", "GM", "GW", "CV", "CM", "GA", "GQ", "CF", "TD", "CD", "CG", "ST", "AO", "KE", "UG", "TZ", "RW", "BI", "MW", "ZM", "ZW", "MZ"]',
             "Lomé, Togo", "https://api.ecobank.com/v1/", "v1",
             '["XOF", "XAF", "NGN", "GHS", "SLL", "LRD", "GMD", "GNF", "CVE", "KES", "UGX", "TZS", "RWF", "BIF", "MWK", "ZMW", "ZWL", "MZN", "USD", "EUR"]',
             1400, 2800, True, True, True, True, True, 8.3, True, True),
            
            ("KCB_001", "KCB Group", "001", "KCBLKENX", "commercial_bank",
             '["KE", "UG", "TZ", "RW", "BI", "SS", "ET"]',
             "Nairobi, Kenya", "https://api.kcbgroup.com/v1/", "v1",
             '["KES", "UGX", "TZS", "RWF", "BIF", "SSP", "ETB", "USD"]',
             350, 900, True, True, True, True, True, 9.0, True, True),
            
            ("ABS_001", "Absa Group", "632005", "ABSAZAJJ", "commercial_bank",
             '["ZA", "BW", "GH", "KE", "MU", "SC", "TZ", "UG", "ZM", "ZW", "MZ", "MW"]',
             "Johannesburg, South Africa", "https://api.absa.africa/v1/", "v1",
             '["ZAR", "BWP", "GHS", "KES", "MUR", "SCR", "TZS", "UGX", "ZMW", "ZWL", "MZN", "MWK", "USD", "EUR"]',
             800, 4200, True, True, True, True, True, 8.7, True, True)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO african_banks 
            (bank_id, bank_name, bank_code, swift_code, bank_type, countries, headquarters,
             api_endpoint, api_version, supported_currencies, branch_count, atm_count,
             digital_banking, mobile_banking, internet_banking, swift_enabled, rtgs_enabled,
             ubuntu_alignment, community_banking, sacco_integration, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], 
               b[12], b[13], b[14], b[15], b[16], b[17], b[18], b[19], datetime.now()) 
              for b in banks_data])
        
        # Insert sample bank accounts
        accounts_data = [
            ("ACC_001", "1234567890", "savings_account", "STD_001", "CUST_001", "John Mthembu", "ZAR", 
             25000.0, 25000.0, 0.0, 0.045, "UBG_001", True),
            ("ACC_002", "2345678901", "current_account", "EQB_001", "CUST_002", "Mary Wanjiku", "KES", 
             180000.0, 180000.0, 50000.0, 0.02, "UBG_002", True),
            ("ACC_003", "3456789012", "sacco_account", "KCB_001", "CUST_003", "Kibera SACCO", "KES", 
             500000.0, 500000.0, 0.0, 0.08, "UBG_003", True),
            ("ACC_004", "4567890123", "savings_account", "FBN_001", "CUST_004", "Adebayo Ogundimu", "NGN", 
             750000.0, 750000.0, 0.0, 0.055, "UBG_004", True),
            ("ACC_005", "5678901234", "group_account", "ECO_001", "CUST_005", "Dakar Women Cooperative", "XOF", 
             1200000.0, 1200000.0, 0.0, 0.06, "UBG_005", True),
            ("ACC_006", "6789012345", "investment_account", "ABS_001", "CUST_006", "Ubuntu Investment Club", "ZAR", 
             350000.0, 350000.0, 0.0, 0.075, "UBG_006", True)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO bank_accounts 
            (account_id, account_number, account_type, bank_id, customer_id, account_name,
             currency, balance, available_balance, overdraft_limit, interest_rate,
             ubuntu_group_id, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], datetime.now()) 
              for a in accounts_data])
        
        # Insert Ubuntu banking groups
        ubuntu_groups_data = [
            ("UBG_001", "Soweto Ubuntu Banking Circle", "savings_group", "STD_001", "1111111111",
             '["CUST_001", "CUST_007", "CUST_008", "CUST_009", "CUST_010"]', "CUST_001",
             125000.0, 0.0, 0.045, '["collective_responsibility", "mutual_support", "elder_wisdom"]',
             "zulu", "traditional_council"),
            
            ("UBG_002", "Nairobi Harambee Investment Group", "investment_club", "EQB_001", "2222222222",
             '["CUST_002", "CUST_011", "CUST_012", "CUST_013"]', "CUST_002",
             450000.0, 0.0, 0.075, '["harambee_spirit", "collective_investment", "community_development"]',
             "kikuyu", "democratic_committee"),
            
            ("UBG_003", "Kibera Community SACCO", "sacco", "KCB_001", "3333333333",
             '["CUST_003", "CUST_014", "CUST_015", "CUST_016", "CUST_017", "CUST_018"]', "CUST_003",
             800000.0, 200000.0, 0.08, '["cooperative_principles", "self_help", "community_ownership"]',
             "luo", "cooperative_board"),
            
            ("UBG_004", "Lagos Business Cooperative", "savings_group", "FBN_001", "4444444444",
             '["CUST_004", "CUST_019", "CUST_020", "CUST_021"]', "CUST_004",
             320000.0, 50000.0, 0.055, '["entrepreneurship", "collective_growth", "mutual_guarantee"]',
             "yoruba", "age_grade_system"),
            
            ("UBG_005", "Dakar Women Cooperative", "microfinance_group", "ECO_001", "5555555555",
             '["CUST_005", "CUST_022", "CUST_023", "CUST_024", "CUST_025"]', "CUST_005",
             280000.0, 80000.0, 0.06, '["women_empowerment", "collective_savings", "mutual_support"]',
             "wolof", "women_council"),
            
            ("UBG_006", "Cape Town Ubuntu Investment Club", "investment_club", "ABS_001", "6666666666",
             '["CUST_006", "CUST_026", "CUST_027", "CUST_028"]', "CUST_006",
             520000.0, 0.0, 0.075, '["ubuntu_philosophy", "shared_prosperity", "collective_wisdom"]',
             "xhosa", "ubuntu_circle")
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO ubuntu_banking_groups 
            (group_id, group_name, group_type, bank_id, group_account_number, members,
             admin_customer_id, total_deposits, total_loans, interest_rate, ubuntu_principles,
             cultural_origin, governance_structure, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [(g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8], g[9], g[10], g[11], g[12], datetime.now()) 
              for g in ubuntu_groups_data])
        
        conn.commit()
        conn.close()
        logger.info("Traditional banking database setup completed")

    def _initialize_banks(self) -> Dict[str, Dict[str, Any]]:
        """Initialize African banks"""
        banks = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT bank_id, bank_name, bank_code, swift_code, bank_type, countries, headquarters,
                   api_endpoint, api_version, supported_currencies, branch_count, atm_count,
                   digital_banking, mobile_banking, internet_banking, swift_enabled, rtgs_enabled,
                   ubuntu_alignment, community_banking, sacco_integration
            FROM african_banks
        ''')
        
        for row in cursor.fetchall():
            banks[row[0]] = {
                "bank_name": row[1],
                "bank_code": row[2],
                "swift_code": row[3],
                "bank_type": row[4],
                "countries": json.loads(row[5]) if row[5] else [],
                "headquarters": row[6],
                "api_endpoint": row[7],
                "api_version": row[8],
                "supported_currencies": json.loads(row[9]) if row[9] else [],
                "branch_count": row[10],
                "atm_count": row[11],
                "digital_banking": row[12],
                "mobile_banking": row[13],
                "internet_banking": row[14],
                "swift_enabled": row[15],
                "rtgs_enabled": row[16],
                "ubuntu_alignment": row[17],
                "community_banking": row[18],
                "sacco_integration": row[19]
            }
        
        conn.close()
        return banks

    def _initialize_ubuntu_banking_groups(self) -> Dict[str, UbuntuBankingGroup]:
        """Initialize Ubuntu banking groups"""
        groups = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT group_id, group_name, group_type, bank_id, group_account_number, members,
                   admin_customer_id, total_deposits, total_loans, interest_rate, ubuntu_principles,
                   cultural_origin, governance_structure
            FROM ubuntu_banking_groups
        ''')
        
        for row in cursor.fetchall():
            groups[row[0]] = UbuntuBankingGroup(
                group_id=row[0],
                group_name=row[1],
                group_type=row[2],
                bank_id=row[3],
                group_account_number=row[4],
                members=json.loads(row[5]) if row[5] else [],
                admin_customer_id=row[6],
                total_deposits=row[7],
                total_loans=row[8],
                interest_rate=row[9],
                ubuntu_principles=json.loads(row[10]) if row[10] else [],
                cultural_origin=row[11],
                governance_structure=row[12]
            )
        
        conn.close()
        return groups

    def _initialize_api_keys(self) -> Dict[str, Dict[str, str]]:
        """Initialize API keys for African banks"""
        return {
            "STD_001": {
                "client_id": "STANDARD_BANK_CLIENT_ID_PLACEHOLDER",
                "client_secret": "STANDARD_BANK_CLIENT_SECRET_PLACEHOLDER",
                "api_key": "STANDARD_BANK_API_KEY_PLACEHOLDER"
            },
            "EQB_001": {
                "username": "EQUITY_BANK_USERNAME_PLACEHOLDER",
                "password": "EQUITY_BANK_PASSWORD_PLACEHOLDER",
                "api_key": "EQUITY_BANK_API_KEY_PLACEHOLDER"
            },
            "FBN_001": {
                "client_id": "FIRST_BANK_CLIENT_ID_PLACEHOLDER",
                "client_secret": "FIRST_BANK_CLIENT_SECRET_PLACEHOLDER"
            },
            "ECO_001": {
                "merchant_id": "ECOBANK_MERCHANT_ID_PLACEHOLDER",
                "api_key": "ECOBANK_API_KEY_PLACEHOLDER"
            },
            "KCB_001": {
                "consumer_key": "KCB_CONSUMER_KEY_PLACEHOLDER",
                "consumer_secret": "KCB_CONSUMER_SECRET_PLACEHOLDER"
            },
            "ABS_001": {
                "client_id": "ABSA_CLIENT_ID_PLACEHOLDER",
                "client_secret": "ABSA_CLIENT_SECRET_PLACEHOLDER"
            }
        }

    async def process_bank_transfer(self, source_account_id: str, destination_account_id: str,
                                  amount: float, currency: str, reference: str = "",
                                  description: str = "", ubuntu_context: str = None,
                                  transaction_type: TransactionType = TransactionType.ACCOUNT_TRANSFER) -> BankingTransaction:
        """Process bank transfer between accounts"""
        transaction_id = str(uuid.uuid4())
        
        # Get account details
        source_account = await self._get_account_details(source_account_id)
        destination_account = await self._get_account_details(destination_account_id)
        
        if not source_account or not destination_account:
            raise ValueError("Invalid account details")
        
        # Validate sufficient balance
        if source_account["available_balance"] < amount:
            raise ValueError("Insufficient balance")
        
        # Calculate fees
        fees = await self._calculate_transfer_fees(source_account, destination_account, amount, transaction_type)
        
        # Calculate community benefit score
        community_benefit = await self._calculate_community_benefit(amount, ubuntu_context, source_account, destination_account)
        
        # Determine processing time
        processing_time = await self._estimate_processing_time(source_account, destination_account, transaction_type)
        
        # Create transaction
        transaction = BankingTransaction(
            transaction_id=transaction_id,
            transaction_type=transaction_type,
            source_account=source_account_id,
            destination_account=destination_account_id,
            amount=amount,
            currency=currency,
            exchange_rate=None,
            reference=reference,
            description=description,
            swift_message=None,
            status=TransactionStatus.PENDING,
            ubuntu_context=ubuntu_context,
            community_benefit=community_benefit,
            fees=fees,
            processing_time=processing_time,
            created_at=datetime.now(),
            completed_at=None
        )
        
        # Process transaction
        success = await self._process_banking_transaction(transaction, source_account, destination_account)
        
        if success:
            transaction.status = TransactionStatus.COMPLETED
            transaction.completed_at = datetime.now()
            
            # Update account balances
            await self._update_account_balance(source_account_id, -amount - fees)
            await self._update_account_balance(destination_account_id, amount)
        else:
            transaction.status = TransactionStatus.FAILED
        
        # Store transaction
        await self._store_transaction(transaction)
        
        return transaction

    async def process_swift_transfer(self, source_account_id: str, destination_swift_code: str,
                                   destination_account_number: str, amount: float, currency: str,
                                   beneficiary_name: str, beneficiary_address: str,
                                   purpose_code: str = "", ubuntu_context: str = None) -> BankingTransaction:
        """Process SWIFT international transfer"""
        transaction_id = str(uuid.uuid4())
        
        # Get source account details
        source_account = await self._get_account_details(source_account_id)
        if not source_account:
            raise ValueError("Invalid source account")
        
        # Validate SWIFT capability
        source_bank = self.banks[source_account["bank_id"]]
        if not source_bank["swift_enabled"]:
            raise ValueError("Source bank does not support SWIFT transfers")
        
        # Calculate fees (higher for international transfers)
        fees = amount * 0.015 + 25.0  # 1.5% + $25 flat fee
        
        # Validate sufficient balance
        if source_account["available_balance"] < amount + fees:
            raise ValueError("Insufficient balance for SWIFT transfer")
        
        # Generate SWIFT message
        swift_message = await self._generate_swift_message(
            source_account, destination_swift_code, destination_account_number,
            amount, currency, beneficiary_name, beneficiary_address, purpose_code
        )
        
        # Calculate community benefit (lower for international transfers)
        community_benefit = await self._calculate_community_benefit(amount, ubuntu_context, source_account, None) * 0.5
        
        # Create transaction
        transaction = BankingTransaction(
            transaction_id=transaction_id,
            transaction_type=TransactionType.SWIFT_TRANSFER,
            source_account=source_account_id,
            destination_account=f"{destination_swift_code}:{destination_account_number}",
            amount=amount,
            currency=currency,
            exchange_rate=None,
            reference=f"SWIFT_{transaction_id[:8]}",
            description=f"International transfer to {beneficiary_name}",
            swift_message=swift_message,
            status=TransactionStatus.PENDING,
            ubuntu_context=ubuntu_context,
            community_benefit=community_benefit,
            fees=fees,
            processing_time=timedelta(hours=24),  # 1-3 business days
            created_at=datetime.now(),
            completed_at=None
        )
        
        # Process SWIFT transaction
        success = await self._process_swift_transaction(transaction, source_account)
        
        if success:
            transaction.status = TransactionStatus.PROCESSING  # SWIFT takes time
            # Update source account balance
            await self._update_account_balance(source_account_id, -amount - fees)
        else:
            transaction.status = TransactionStatus.FAILED
        
        # Store transaction and SWIFT message
        await self._store_transaction(transaction)
        await self._store_swift_message(transaction)
        
        return transaction

    async def process_ubuntu_group_loan(self, group_id: str, borrower_customer_id: str,
                                      loan_amount: float, loan_purpose: str,
                                      guarantors: List[str]) -> Dict[str, Any]:
        """Process Ubuntu group loan with community guarantee"""
        if group_id not in self.ubuntu_banking_groups:
            raise ValueError(f"Ubuntu group {group_id} not found")
        
        group = self.ubuntu_banking_groups[group_id]
        
        # Validate borrower is group member
        if borrower_customer_id not in group.members:
            raise ValueError(f"Customer {borrower_customer_id} is not a member of group {group_id}")
        
        # Validate guarantors are group members
        for guarantor in guarantors:
            if guarantor not in group.members:
                raise ValueError(f"Guarantor {guarantor} is not a member of group {group_id}")
        
        # Check group loan capacity
        max_loan = group.total_deposits * 2.0  # Can loan up to 2x deposits
        if group.total_loans + loan_amount > max_loan:
            raise ValueError(f"Loan amount exceeds group capacity. Max available: {max_loan - group.total_loans}")
        
        # Create loan account
        loan_account_id = str(uuid.uuid4())
        loan_account_number = f"LOAN_{group_id}_{borrower_customer_id}_{datetime.now().strftime('%Y%m%d')}"
        
        # Process loan disbursement
        disbursement_transaction = await self.process_bank_transfer(
            source_account_id=f"GROUP_{group_id}",  # Group account
            destination_account_id=f"CUSTOMER_{borrower_customer_id}",  # Borrower account
            amount=loan_amount,
            currency="KES",  # Default currency, should be configurable
            reference=f"Ubuntu_loan_{group_id}",
            description=f"Ubuntu group loan for {loan_purpose}",
            ubuntu_context=f"group_loan_{group.group_type}",
            transaction_type=TransactionType.LOAN_DISBURSEMENT
        )
        
        # Update group loan total
        group.total_loans += loan_amount
        await self._update_ubuntu_group(group)
        
        # Create loan record with Ubuntu principles
        loan_record = {
            "loan_id": loan_account_id,
            "loan_account_number": loan_account_number,
            "group_id": group_id,
            "borrower_customer_id": borrower_customer_id,
            "loan_amount": loan_amount,
            "loan_purpose": loan_purpose,
            "guarantors": guarantors,
            "interest_rate": group.interest_rate,
            "ubuntu_principles_applied": group.ubuntu_principles,
            "cultural_governance": group.governance_structure,
            "disbursement_transaction": disbursement_transaction,
            "repayment_schedule": await self._generate_ubuntu_repayment_schedule(loan_amount, group.interest_rate),
            "community_benefit_score": disbursement_transaction.community_benefit
        }
        
        return loan_record

    async def _get_account_details(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account details from database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_id, account_number, account_type, bank_id, customer_id, account_name,
                   currency, balance, available_balance, overdraft_limit, interest_rate,
                   ubuntu_group_id, is_active
            FROM bank_accounts 
            WHERE account_id = ? OR account_number = ?
        ''', (account_id, account_id))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "account_id": row[0],
                "account_number": row[1],
                "account_type": row[2],
                "bank_id": row[3],
                "customer_id": row[4],
                "account_name": row[5],
                "currency": row[6],
                "balance": row[7],
                "available_balance": row[8],
                "overdraft_limit": row[9],
                "interest_rate": row[10],
                "ubuntu_group_id": row[11],
                "is_active": row[12]
            }
        return None

    async def _calculate_transfer_fees(self, source_account: Dict[str, Any], destination_account: Dict[str, Any],
                                     amount: float, transaction_type: TransactionType) -> float:
        """Calculate transfer fees"""
        base_fee = 0.0
        
        if transaction_type == TransactionType.ACCOUNT_TRANSFER:
            if source_account["bank_id"] == destination_account["bank_id"]:
                # Same bank transfer
                base_fee = min(amount * 0.001, 10.0)  # 0.1% max $10
            else:
                # Inter-bank transfer
                base_fee = min(amount * 0.005, 25.0)  # 0.5% max $25
        elif transaction_type == TransactionType.RTGS_TRANSFER:
            base_fee = min(amount * 0.002, 50.0)  # 0.2% max $50
        elif transaction_type == TransactionType.SWIFT_TRANSFER:
            base_fee = amount * 0.015 + 25.0  # 1.5% + $25
        
        # Ubuntu discount for community transactions
        if source_account.get("ubuntu_group_id") or destination_account.get("ubuntu_group_id"):
            base_fee *= 0.8  # 20% discount for Ubuntu group members
        
        return base_fee

    async def _calculate_community_benefit(self, amount: float, ubuntu_context: str,
                                         source_account: Dict[str, Any], destination_account: Optional[Dict[str, Any]]) -> float:
        """Calculate community benefit score for banking transaction"""
        base_score = 5.0
        
        # Ubuntu context bonus
        if ubuntu_context:
            ubuntu_keywords = ["community", "group", "sacco", "cooperative", "harambee", "ubuntu", "collective"]
            if any(keyword in ubuntu_context.lower() for keyword in ubuntu_keywords):
                base_score += 2.0
        
        # Ubuntu group involvement bonus
        if source_account.get("ubuntu_group_id"):
            base_score += 1.5
        if destination_account and destination_account.get("ubuntu_group_id"):
            base_score += 1.5
        
        # Amount-based community impact
        if amount > 50000:  # Larger amounts likely for community purposes
            base_score += 1.0
        
        # Bank Ubuntu alignment bonus
        source_bank = self.banks.get(source_account["bank_id"], {})
        ubuntu_alignment = source_bank.get("ubuntu_alignment", 0)
        base_score += (ubuntu_alignment / 10) * 1.0
        
        return min(base_score, 10.0)

    async def _estimate_processing_time(self, source_account: Dict[str, Any], destination_account: Dict[str, Any],
                                      transaction_type: TransactionType) -> timedelta:
        """Estimate transaction processing time"""
        if transaction_type == TransactionType.ACCOUNT_TRANSFER:
            if source_account["bank_id"] == destination_account["bank_id"]:
                return timedelta(minutes=5)  # Same bank - instant
            else:
                return timedelta(hours=2)  # Inter-bank - 2 hours
        elif transaction_type == TransactionType.RTGS_TRANSFER:
            return timedelta(minutes=30)  # RTGS - 30 minutes
        elif transaction_type == TransactionType.SWIFT_TRANSFER:
            return timedelta(days=2)  # International - 1-3 days
        else:
            return timedelta(hours=1)  # Default

    async def _process_banking_transaction(self, transaction: BankingTransaction,
                                         source_account: Dict[str, Any], destination_account: Dict[str, Any]) -> bool:
        """Process banking transaction with specific bank"""
        source_bank = self.banks[source_account["bank_id"]]
        
        # Simulate bank API call
        logger.info(f"Processing {transaction.transaction_type.value} via {source_bank['bank_name']}")
        
        # Simulate network delay
        await asyncio.sleep(0.1)
        
        # Simulate success rate based on bank reliability
        success_rates = {
            "STD_001": 0.98,  # Standard Bank
            "EQB_001": 0.96,  # Equity Bank
            "FBN_001": 0.94,  # First Bank Nigeria
            "ECO_001": 0.92,  # Ecobank
            "KCB_001": 0.97,  # KCB Group
            "ABS_001": 0.95   # Absa Group
        }
        
        success_rate = success_rates.get(source_account["bank_id"], 0.90)
        return random.random() < success_rate

    async def _process_swift_transaction(self, transaction: BankingTransaction, source_account: Dict[str, Any]) -> bool:
        """Process SWIFT transaction"""
        logger.info(f"Processing SWIFT transfer: {transaction.transaction_id}")
        
        # Simulate SWIFT network processing
        await asyncio.sleep(0.2)
        
        # SWIFT has high success rate but takes longer
        return random.random() < 0.95

    async def _generate_swift_message(self, source_account: Dict[str, Any], destination_swift_code: str,
                                    destination_account_number: str, amount: float, currency: str,
                                    beneficiary_name: str, beneficiary_address: str, purpose_code: str) -> str:
        """Generate SWIFT MT103 message"""
        source_bank = self.banks[source_account["bank_id"]]
        
        swift_message = f"""{{1:F01{source_bank['swift_code']}0000000000}}
{{2:I103{destination_swift_code}XXXXN}}
{{3:{{108:MT103}}}}
{{4:
:20:{datetime.now().strftime('%Y%m%d')}REF{random.randint(1000, 9999)}
:23B:CRED
:32A:{datetime.now().strftime('%y%m%d')}{currency}{amount:.2f}
:50K:/{source_account['account_number']}
{source_account['account_name']}
:59:/{destination_account_number}
{beneficiary_name}
{beneficiary_address}
:70:{purpose_code or 'Payment'}
:71A:OUR
-}}"""
        
        return swift_message

    async def _generate_ubuntu_repayment_schedule(self, loan_amount: float, interest_rate: float) -> List[Dict[str, Any]]:
        """Generate Ubuntu-based repayment schedule"""
        # Ubuntu principle: Flexible repayment based on community support
        monthly_payment = (loan_amount * (1 + interest_rate)) / 12
        
        schedule = []
        for month in range(1, 13):
            due_date = datetime.now() + timedelta(days=30 * month)
            schedule.append({
                "month": month,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "principal": loan_amount / 12,
                "interest": (loan_amount * interest_rate) / 12,
                "total_payment": monthly_payment,
                "ubuntu_flexibility": "Community support available for payment difficulties",
                "grace_period_days": 7  # Ubuntu principle: Give people time
            })
        
        return schedule

    async def _update_account_balance(self, account_id: str, amount_change: float):
        """Update account balance"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE bank_accounts 
                SET balance = balance + ?, available_balance = available_balance + ?
                WHERE account_id = ?
            ''', (amount_change, amount_change, account_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating account balance: {str(e)}")

    async def _update_ubuntu_group(self, group: UbuntuBankingGroup):
        """Update Ubuntu group in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE ubuntu_banking_groups 
                SET total_deposits = ?, total_loans = ?
                WHERE group_id = ?
            ''', (group.total_deposits, group.total_loans, group.group_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating Ubuntu group: {str(e)}")

    async def _store_transaction(self, transaction: BankingTransaction):
        """Store transaction in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO banking_transactions 
                (transaction_id, transaction_type, source_account, destination_account, amount,
                 currency, exchange_rate, reference, description, swift_message, status,
                 ubuntu_context, community_benefit, fees, processing_time_seconds, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction.transaction_id,
                transaction.transaction_type.value,
                transaction.source_account,
                transaction.destination_account,
                transaction.amount,
                transaction.currency,
                transaction.exchange_rate,
                transaction.reference,
                transaction.description,
                transaction.swift_message,
                transaction.status.value,
                transaction.ubuntu_context,
                transaction.community_benefit,
                transaction.fees,
                int(transaction.processing_time.total_seconds()),
                transaction.created_at,
                transaction.completed_at
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing transaction: {str(e)}")

    async def _store_swift_message(self, transaction: BankingTransaction):
        """Store SWIFT message in database"""
        if not transaction.swift_message:
            return
        
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO swift_messages 
                (message_id, transaction_id, message_type, sender_bic, receiver_bic,
                 message_content, processing_status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                transaction.transaction_id,
                "MT103",
                "SENDER_BIC",  # Extract from SWIFT message
                "RECEIVER_BIC",  # Extract from SWIFT message
                transaction.swift_message,
                "SENT",
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing SWIFT message: {str(e)}")

    async def get_banking_analytics(self) -> Dict[str, Any]:
        """Get comprehensive banking analytics"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Get bank statistics
        cursor.execute('''
            SELECT bank_id, COUNT(*) as account_count,
                   SUM(balance) as total_deposits,
                   AVG(balance) as avg_balance
            FROM bank_accounts 
            WHERE is_active = 1
            GROUP BY bank_id
        ''')
        
        bank_stats = {}
        for row in cursor.fetchall():
            bank_name = self.banks[row[0]]["bank_name"]
            bank_stats[bank_name] = {
                "account_count": row[1],
                "total_deposits": round(row[2], 2) if row[2] else 0,
                "avg_balance": round(row[3], 2) if row[3] else 0
            }
        
        # Get transaction statistics
        cursor.execute('''
            SELECT transaction_type, COUNT(*) as transaction_count,
                   SUM(amount) as total_volume,
                   AVG(amount) as avg_amount,
                   AVG(community_benefit) as avg_community_benefit,
                   AVG(fees) as avg_fees
            FROM banking_transactions 
            GROUP BY transaction_type
        ''')
        
        transaction_stats = {}
        for row in cursor.fetchall():
            transaction_stats[row[0]] = {
                "transaction_count": row[1],
                "total_volume": round(row[2], 2) if row[2] else 0,
                "avg_amount": round(row[3], 2) if row[3] else 0,
                "avg_community_benefit": round(row[4], 2) if row[4] else 0,
                "avg_fees": round(row[5], 2) if row[5] else 0
            }
        
        # Get Ubuntu group statistics
        cursor.execute('''
            SELECT group_type, COUNT(*) as group_count,
                   SUM(total_deposits) as total_deposits,
                   SUM(total_loans) as total_loans,
                   AVG(interest_rate) as avg_interest_rate
            FROM ubuntu_banking_groups 
            GROUP BY group_type
        ''')
        
        ubuntu_stats = {}
        for row in cursor.fetchall():
            ubuntu_stats[row[0]] = {
                "group_count": row[1],
                "total_deposits": round(row[2], 2) if row[2] else 0,
                "total_loans": round(row[3], 2) if row[3] else 0,
                "avg_interest_rate": round(row[4] * 100, 1) if row[4] else 0  # Convert to percentage
            }
        
        conn.close()
        
        return {
            "total_banks": len(self.banks),
            "bank_statistics": bank_stats,
            "transaction_statistics": transaction_stats,
            "ubuntu_group_statistics": ubuntu_stats,
            "supported_countries": list(set([country for bank in self.banks.values() 
                                           for country in bank.get("countries", [])])),
            "total_ubuntu_groups": len(self.ubuntu_banking_groups),
            "swift_enabled_banks": sum(1 for bank in self.banks.values() if bank.get("swift_enabled", False)),
            "rtgs_enabled_banks": sum(1 for bank in self.banks.values() if bank.get("rtgs_enabled", False)),
            "community_banking_coverage": sum(1 for bank in self.banks.values() if bank.get("community_banking", False)),
            "average_ubuntu_alignment": round(sum(bank.get("ubuntu_alignment", 0) for bank in self.banks.values()) / len(self.banks), 1)
        }

async def main():
    """Main function for testing Traditional Banking Agent"""
    agent = TraditionalBankingAgent()
    
    print("🏦 Testing Traditional Banking Agent")
    print("=" * 60)
    
    # Test bank transfers
    print("\n💸 Testing Bank Transfers")
    print("-" * 30)
    
    transfer_tests = [
        ("ACC_001", "ACC_002", 5000.0, "ZAR", "family_support", "Same bank transfer"),
        ("ACC_002", "ACC_003", 15000.0, "KES", "sacco_contribution", "SACCO contribution"),
        ("ACC_004", "ACC_005", 25000.0, "NGN", "cooperative_investment", "Inter-bank transfer"),
        ("ACC_006", "ACC_001", 10000.0, "ZAR", "ubuntu_investment", "Investment club payout")
    ]
    
    for source, dest, amount, currency, context, description in transfer_tests:
        print(f"\n🔄 {description}")
        print(f"   From: {source} To: {dest}")
        print(f"   Amount: {amount} {currency}")
        print(f"   Context: {context}")
        
        try:
            transaction = await agent.process_bank_transfer(
                source_account_id=source,
                destination_account_id=dest,
                amount=amount,
                currency=currency,
                ubuntu_context=context,
                description=description
            )
            
            print(f"   ✅ Transaction ID: {transaction.transaction_id[:8]}...")
            print(f"   Status: {transaction.status.value}")
            print(f"   Community Benefit: {transaction.community_benefit:.1f}/10")
            print(f"   Fees: {transaction.fees:.2f} {currency}")
            print(f"   Processing Time: {transaction.processing_time}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test SWIFT transfer
    print(f"\n🌍 Testing SWIFT International Transfer")
    print("-" * 40)
    
    try:
        swift_transaction = await agent.process_swift_transfer(
            source_account_id="ACC_001",
            destination_swift_code="CHASUS33",
            destination_account_number="1234567890",
            amount=1000.0,
            currency="USD",
            beneficiary_name="John Smith",
            beneficiary_address="123 Main St, New York, USA",
            purpose_code="Family support",
            ubuntu_context="diaspora_remittance"
        )
        
        print(f"🌐 SWIFT Transfer to USA")
        print(f"   Transaction ID: {swift_transaction.transaction_id[:8]}...")
        print(f"   Status: {swift_transaction.status.value}")
        print(f"   Amount: {swift_transaction.amount} {swift_transaction.currency}")
        print(f"   Fees: {swift_transaction.fees:.2f}")
        print(f"   Processing Time: {swift_transaction.processing_time}")
        print(f"   Community Benefit: {swift_transaction.community_benefit:.1f}/10")
        print(f"   SWIFT Message Generated: {'✅ Yes' if swift_transaction.swift_message else '❌ No'}")
        
    except Exception as e:
        print(f"   ❌ SWIFT Error: {str(e)}")
    
    # Test Ubuntu group loan
    print(f"\n🤝 Testing Ubuntu Group Loan")
    print("-" * 30)
    
    ubuntu_loan_tests = [
        ("UBG_003", "CUST_014", 50000.0, "Small business expansion", ["CUST_015", "CUST_016"]),
        ("UBG_001", "CUST_007", 25000.0, "Education fees", ["CUST_008", "CUST_009"]),
        ("UBG_005", "CUST_022", 15000.0, "Market stall setup", ["CUST_023", "CUST_024"])
    ]
    
    for group_id, borrower, amount, purpose, guarantors in ubuntu_loan_tests:
        group = agent.ubuntu_banking_groups[group_id]
        print(f"\n🏛️ {group.group_name} ({group.group_type})")
        print(f"   Borrower: {borrower}")
        print(f"   Loan Amount: {amount}")
        print(f"   Purpose: {purpose}")
        print(f"   Guarantors: {len(guarantors)}")
        print(f"   Cultural Origin: {group.cultural_origin}")
        print(f"   Governance: {group.governance_structure}")
        
        try:
            loan_record = await agent.process_ubuntu_group_loan(
                group_id=group_id,
                borrower_customer_id=borrower,
                loan_amount=amount,
                loan_purpose=purpose,
                guarantors=guarantors
            )
            
            print(f"   ✅ Loan ID: {loan_record['loan_id'][:8]}...")
            print(f"   Interest Rate: {loan_record['interest_rate']*100:.1f}%")
            print(f"   Ubuntu Principles: {', '.join(loan_record['ubuntu_principles_applied'][:2])}")
            print(f"   Disbursement Status: {loan_record['disbursement_transaction'].status.value}")
            print(f"   Community Benefit: {loan_record['community_benefit_score']:.1f}/10")
            print(f"   Repayment Schedule: {len(loan_record['repayment_schedule'])} months")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Get analytics
    analytics = await agent.get_banking_analytics()
    print(f"\n📈 Traditional Banking Analytics:")
    print(f"Total Banks: {analytics['total_banks']}")
    print(f"Supported Countries: {len(analytics['supported_countries'])}")
    print(f"Total Ubuntu Groups: {analytics['total_ubuntu_groups']}")
    print(f"SWIFT Enabled Banks: {analytics['swift_enabled_banks']}")
    print(f"RTGS Enabled Banks: {analytics['rtgs_enabled_banks']}")
    print(f"Community Banking Coverage: {analytics['community_banking_coverage']}")
    print(f"Average Ubuntu Alignment: {analytics['average_ubuntu_alignment']}/10")
    
    print(f"\n📊 Bank Statistics:")
    for bank_name, stats in analytics['bank_statistics'].items():
        print(f"   {bank_name}: {stats['account_count']} accounts")
        print(f"      Total Deposits: {stats['total_deposits']:.0f}")
        print(f"      Average Balance: {stats['avg_balance']:.0f}")
    
    print(f"\n💳 Transaction Statistics:")
    for tx_type, stats in analytics['transaction_statistics'].items():
        print(f"   {tx_type.replace('_', ' ').title()}: {stats['transaction_count']} transactions")
        print(f"      Volume: {stats['total_volume']:.0f}, Avg: {stats['avg_amount']:.0f}")
        print(f"      Community Benefit: {stats['avg_community_benefit']:.1f}/10")
        print(f"      Average Fees: {stats['avg_fees']:.2f}")
    
    print(f"\n🤝 Ubuntu Group Statistics:")
    for group_type, stats in analytics['ubuntu_group_statistics'].items():
        print(f"   {group_type.replace('_', ' ').title()}: {stats['group_count']} groups")
        print(f"      Total Deposits: {stats['total_deposits']:.0f}")
        print(f"      Total Loans: {stats['total_loans']:.0f}")
        print(f"      Average Interest Rate: {stats['avg_interest_rate']:.1f}%")
    
    print("\n🎉 Traditional Banking Agent testing completed!")

if __name__ == "__main__":
    asyncio.run(main())

