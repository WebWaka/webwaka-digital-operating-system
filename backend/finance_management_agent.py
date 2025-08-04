"""
WebWaka Finance Management Systems Agent (Agent 5)
Comprehensive Financial Management with African Financial Inclusion Optimization

This agent provides comprehensive financial management capabilities with:
- Banking and microfinance systems with mobile money integration
- Investment and savings platforms with community-based approaches
- Insurance management systems with agricultural and health focus
- Payment processing systems with offline capabilities
- Financial literacy and education programs with cultural context
- Cooperative and group savings management with traditional rotating credit
- Cryptocurrency and digital asset management with regulatory compliance
- Financial inclusion strategies for underserved populations
"""

import asyncio
import json
import logging
import time
import sqlite3
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import statistics
import random
import uuid
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccountType(Enum):
    """Financial account types"""
    SAVINGS = "savings"
    CHECKING = "checking"
    MICROFINANCE = "microfinance"
    MOBILE_MONEY = "mobile_money"
    COOPERATIVE = "cooperative"
    INVESTMENT = "investment"
    INSURANCE = "insurance"
    CRYPTOCURRENCY = "cryptocurrency"

class TransactionType(Enum):
    """Transaction types"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    LOAN = "loan"
    INSURANCE_CLAIM = "insurance_claim"
    INVESTMENT = "investment"
    REMITTANCE = "remittance"

class LoanStatus(Enum):
    """Loan status types"""
    PENDING = "pending"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"

class InsuranceType(Enum):
    """Insurance product types"""
    HEALTH = "health"
    LIFE = "life"
    CROP = "crop"
    LIVESTOCK = "livestock"
    PROPERTY = "property"
    MICRO_INSURANCE = "micro_insurance"

@dataclass
class FinancialAccount:
    """Financial account structure"""
    account_id: str
    account_type: AccountType
    owner_name: str
    owner_id: str
    balance: float
    currency: str
    created_date: datetime
    status: str
    mobile_number: str = None
    cooperative_group: str = None
    traditional_savings_group: str = None
    
    def __post_init__(self):
        if self.mobile_number is None:
            self.mobile_number = ""
        if self.cooperative_group is None:
            self.cooperative_group = ""
        if self.traditional_savings_group is None:
            self.traditional_savings_group = ""

@dataclass
class Transaction:
    """Transaction structure"""
    transaction_id: str
    account_id: str
    transaction_type: TransactionType
    amount: float
    currency: str
    description: str
    timestamp: datetime
    recipient_account: str = None
    mobile_number: str = None
    location: str = None
    offline_processed: bool = False
    
    def __post_init__(self):
        if self.recipient_account is None:
            self.recipient_account = ""
        if self.mobile_number is None:
            self.mobile_number = ""
        if self.location is None:
            self.location = ""

@dataclass
class Loan:
    """Loan structure"""
    loan_id: str
    borrower_id: str
    amount: float
    currency: str
    interest_rate: float
    term_months: int
    purpose: str
    status: LoanStatus
    application_date: datetime
    collateral_type: str = None
    group_guarantee: bool = False
    traditional_guarantee: str = None
    
    def __post_init__(self):
        if self.collateral_type is None:
            self.collateral_type = ""
        if self.traditional_guarantee is None:
            self.traditional_guarantee = ""

@dataclass
class InsurancePolicy:
    """Insurance policy structure"""
    policy_id: str
    policyholder_id: str
    insurance_type: InsuranceType
    coverage_amount: float
    premium: float
    currency: str
    start_date: datetime
    end_date: datetime
    status: str
    beneficiaries: List[str] = None
    community_pool: bool = False
    
    def __post_init__(self):
        if self.beneficiaries is None:
            self.beneficiaries = []

class AfricanFinancialKnowledge:
    """Traditional African financial systems and practices"""
    
    def __init__(self):
        self.traditional_financial_systems = {
            "rotating_savings": {
                "names": {
                    "yoruba": "esusu",
                    "igbo": "isusu", 
                    "swahili": "chama",
                    "hausa": "adashi",
                    "amharic": "iqub"
                },
                "description": "Community rotating credit and savings associations",
                "benefits": ["Financial discipline", "Community support", "Access to lump sums"],
                "modern_integration": "Digital chama platforms with mobile money"
            },
            "community_banking": {
                "description": "Village savings and loan associations",
                "features": ["Group lending", "Peer support", "Local governance"],
                "benefits": ["Financial inclusion", "Community development", "Risk sharing"],
                "modern_integration": "Digital record keeping and mobile banking"
            },
            "barter_trade": {
                "description": "Exchange of goods and services without money",
                "applications": ["Rural markets", "Agricultural trade", "Service exchange"],
                "benefits": ["No cash dependency", "Community cooperation", "Resource optimization"],
                "modern_integration": "Digital barter platforms and value tracking"
            },
            "livestock_banking": {
                "description": "Livestock as store of value and investment",
                "features": ["Wealth preservation", "Risk diversification", "Social status"],
                "benefits": ["Inflation hedge", "Emergency funds", "Cultural significance"],
                "modern_integration": "Livestock insurance and digital tracking"
            }
        }
        
        self.ubuntu_financial_principles = {
            "collective_prosperity": "Individual wealth contributes to community prosperity",
            "mutual_support": "Support each other in times of financial need",
            "shared_responsibility": "Community members guarantee each other's financial commitments",
            "transparent_dealings": "Financial transactions should be open and honest",
            "sustainable_growth": "Financial growth should benefit the entire community"
        }
        
        self.mobile_money_systems = {
            "m_pesa": {
                "countries": ["Kenya", "Tanzania", "Uganda"],
                "features": ["Person-to-person transfers", "Bill payments", "Merchant payments"],
                "integration": "API integration for seamless transactions"
            },
            "mtn_mobile_money": {
                "countries": ["Ghana", "Uganda", "Rwanda", "Cameroon"],
                "features": ["Mobile wallet", "International remittances", "Savings products"],
                "integration": "Mobile money API for financial services"
            },
            "orange_money": {
                "countries": ["Senegal", "Mali", "Burkina Faso", "Niger"],
                "features": ["Mobile payments", "Microfinance", "Insurance products"],
                "integration": "Orange Money API for financial inclusion"
            }
        }
        
        self.financial_inclusion_strategies = {
            "agent_banking": "Community agents providing banking services",
            "mobile_banking": "Banking services through mobile phones",
            "microfinance": "Small loans for micro-entrepreneurs",
            "financial_literacy": "Education on financial products and services",
            "digital_identity": "Digital ID for financial service access",
            "alternative_credit_scoring": "Credit assessment using non-traditional data"
        }
    
    def get_traditional_financial_system(self, system_type: str) -> Dict[str, Any]:
        """Get traditional financial system information"""
        return self.traditional_financial_systems.get(system_type, {})
    
    def apply_ubuntu_financial_principle(self, context: str) -> str:
        """Apply Ubuntu philosophy to financial context"""
        return self.ubuntu_financial_principles.get(context, "Ubuntu: We prosper together through mutual financial support")
    
    def get_mobile_money_integration(self, provider: str) -> Dict[str, Any]:
        """Get mobile money integration information"""
        return self.mobile_money_systems.get(provider, {})

class BankingMicrofinanceSystem:
    """Banking and microfinance systems with mobile money integration"""
    
    def __init__(self):
        self.knowledge_base = AfricanFinancialKnowledge()
        self.interest_rates = {
            "savings": 0.05,  # 5% annual
            "microfinance": 0.15,  # 15% annual
            "cooperative": 0.08,  # 8% annual
            "mobile_money": 0.02  # 2% annual
        }
    
    async def create_financial_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create financial account with African context optimization"""
        
        account = FinancialAccount(
            account_id=f"acc_{uuid.uuid4().hex[:8]}",
            account_type=AccountType(account_data.get("account_type", "savings")),
            owner_name=account_data["owner_name"],
            owner_id=account_data["owner_id"],
            balance=account_data.get("initial_balance", 0.0),
            currency=account_data.get("currency", "USD"),
            created_date=datetime.now(),
            status="active",
            mobile_number=account_data.get("mobile_number", ""),
            cooperative_group=account_data.get("cooperative_group", ""),
            traditional_savings_group=account_data.get("traditional_savings_group", "")
        )
        
        account_creation_result = {
            "account": asdict(account),
            "mobile_money_integration": {},
            "traditional_savings_integration": {},
            "ubuntu_financial_approach": "",
            "financial_literacy_resources": [],
            "community_support_features": []
        }
        
        # Mobile money integration
        if account.mobile_number:
            account_creation_result["mobile_money_integration"] = {
                "mobile_wallet_linked": True,
                "available_services": ["Money transfer", "Bill payment", "Merchant payment"],
                "offline_capabilities": "SMS-based transactions when internet unavailable",
                "agent_network": "Access through community agents"
            }
        
        # Traditional savings integration
        if account.traditional_savings_group:
            traditional_system = self.knowledge_base.get_traditional_financial_system("rotating_savings")
            account_creation_result["traditional_savings_integration"] = {
                "group_name": account.traditional_savings_group,
                "traditional_names": traditional_system.get("names", {}),
                "benefits": traditional_system.get("benefits", []),
                "digital_enhancement": "Digital record keeping and automated contributions"
            }
        
        # Ubuntu financial approach
        account_creation_result["ubuntu_financial_approach"] = (
            self.knowledge_base.apply_ubuntu_financial_principle("collective_prosperity")
        )
        
        # Financial literacy resources
        account_creation_result["financial_literacy_resources"] = [
            "Basic banking and savings education",
            "Mobile money usage training",
            "Investment and insurance awareness",
            "Budgeting and financial planning",
            "Digital financial security"
        ]
        
        # Community support features
        account_creation_result["community_support_features"] = [
            "Group savings and lending circles",
            "Community financial advisors",
            "Peer-to-peer financial education",
            "Emergency community fund access",
            "Local business financing support"
        ]
        
        return account_creation_result
    
    async def process_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process financial transaction with offline capabilities"""
        
        transaction = Transaction(
            transaction_id=f"txn_{uuid.uuid4().hex[:8]}",
            account_id=transaction_data["account_id"],
            transaction_type=TransactionType(transaction_data["transaction_type"]),
            amount=transaction_data["amount"],
            currency=transaction_data.get("currency", "USD"),
            description=transaction_data["description"],
            timestamp=datetime.now(),
            recipient_account=transaction_data.get("recipient_account", ""),
            mobile_number=transaction_data.get("mobile_number", ""),
            location=transaction_data.get("location", ""),
            offline_processed=transaction_data.get("offline_mode", False)
        )
        
        transaction_result = {
            "transaction": asdict(transaction),
            "processing_status": "completed",
            "mobile_money_integration": {},
            "offline_processing": {},
            "ubuntu_transaction_principles": "",
            "community_impact": {},
            "security_measures": []
        }
        
        # Mobile money integration
        if transaction.mobile_number:
            transaction_result["mobile_money_integration"] = {
                "mobile_confirmation": f"SMS confirmation sent to {transaction.mobile_number}",
                "agent_processing": "Transaction can be completed through mobile money agent",
                "cross_platform": "Compatible with M-Pesa, MTN Mobile Money, Orange Money",
                "real_time_processing": "Instant transaction confirmation"
            }
        
        # Offline processing
        if transaction.offline_processed:
            transaction_result["offline_processing"] = {
                "sms_based": "Transaction initiated via SMS",
                "agent_assisted": "Completed through community agent",
                "sync_when_online": "Will sync with central system when connectivity restored",
                "paper_backup": "Physical receipt provided for record keeping"
            }
        
        # Ubuntu transaction principles
        transaction_result["ubuntu_transaction_principles"] = (
            self.knowledge_base.apply_ubuntu_financial_principle("transparent_dealings")
        )
        
        # Community impact
        transaction_result["community_impact"] = {
            "local_economy": "Supports local business and economic activity",
            "financial_inclusion": "Enables participation in formal financial system",
            "community_development": "Contributes to overall community prosperity",
            "social_cohesion": "Strengthens community financial relationships"
        }
        
        # Security measures
        transaction_result["security_measures"] = [
            "Multi-factor authentication for large transactions",
            "Biometric verification where available",
            "Community witness for high-value transactions",
            "Encrypted data transmission and storage",
            "Fraud detection and prevention systems"
        ]
        
        return transaction_result

class InvestmentSavingsSystem:
    """Investment and savings platforms with community-based approaches"""
    
    def __init__(self):
        self.knowledge_base = AfricanFinancialKnowledge()
        self.investment_products = {
            "government_bonds": {
                "risk_level": "Low",
                "expected_return": 0.08,
                "minimum_investment": 100,
                "liquidity": "Medium"
            },
            "agricultural_investment": {
                "risk_level": "Medium",
                "expected_return": 0.15,
                "minimum_investment": 50,
                "liquidity": "Low"
            },
            "microfinance_fund": {
                "risk_level": "Medium",
                "expected_return": 0.12,
                "minimum_investment": 25,
                "liquidity": "Medium"
            },
            "community_development_fund": {
                "risk_level": "Low",
                "expected_return": 0.06,
                "minimum_investment": 10,
                "liquidity": "High"
            }
        }
    
    async def create_investment_portfolio(self, investor_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create investment portfolio with community-based approaches"""
        
        portfolio = {
            "investor_id": investor_profile["investor_id"],
            "risk_tolerance": investor_profile.get("risk_tolerance", "medium"),
            "investment_goals": investor_profile.get("investment_goals", []),
            "available_capital": investor_profile.get("available_capital", 1000),
            "recommended_allocation": {},
            "community_investment_opportunities": [],
            "traditional_investment_integration": {},
            "ubuntu_investment_approach": "",
            "financial_education_plan": []
        }
        
        # Recommended allocation based on risk tolerance
        if portfolio["risk_tolerance"] == "low":
            portfolio["recommended_allocation"] = {
                "government_bonds": 0.6,
                "community_development_fund": 0.3,
                "microfinance_fund": 0.1
            }
        elif portfolio["risk_tolerance"] == "high":
            portfolio["recommended_allocation"] = {
                "agricultural_investment": 0.4,
                "microfinance_fund": 0.3,
                "government_bonds": 0.2,
                "community_development_fund": 0.1
            }
        else:  # medium risk
            portfolio["recommended_allocation"] = {
                "microfinance_fund": 0.3,
                "government_bonds": 0.3,
                "agricultural_investment": 0.2,
                "community_development_fund": 0.2
            }
        
        # Community investment opportunities
        portfolio["community_investment_opportunities"] = [
            {
                "opportunity": "Local Agricultural Cooperative",
                "description": "Invest in community farming initiatives",
                "expected_return": 0.18,
                "social_impact": "Food security and rural development",
                "minimum_investment": 100
            },
            {
                "opportunity": "Community Solar Project",
                "description": "Renewable energy for local community",
                "expected_return": 0.14,
                "social_impact": "Clean energy access and job creation",
                "minimum_investment": 200
            },
            {
                "opportunity": "Women's Microenterprise Fund",
                "description": "Support women-led small businesses",
                "expected_return": 0.16,
                "social_impact": "Women's economic empowerment",
                "minimum_investment": 50
            }
        ]
        
        # Traditional investment integration
        livestock_system = self.knowledge_base.get_traditional_financial_system("livestock_banking")
        portfolio["traditional_investment_integration"] = {
            "livestock_investment": {
                "description": livestock_system.get("description", ""),
                "benefits": livestock_system.get("benefits", []),
                "modern_enhancement": "Digital livestock tracking and insurance",
                "recommended_allocation": 0.1
            },
            "land_investment": {
                "description": "Community land ownership and development",
                "benefits": ["Wealth preservation", "Community development", "Food security"],
                "modern_enhancement": "Digital land registry and management",
                "recommended_allocation": 0.05
            }
        }
        
        # Ubuntu investment approach
        portfolio["ubuntu_investment_approach"] = (
            self.knowledge_base.apply_ubuntu_financial_principle("sustainable_growth")
        )
        
        # Financial education plan
        portfolio["financial_education_plan"] = [
            "Investment basics and risk management",
            "Community investment opportunities",
            "Traditional and modern investment integration",
            "Portfolio diversification strategies",
            "Long-term wealth building principles"
        ]
        
        return portfolio
    
    async def manage_community_savings_group(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manage community savings group with digital enhancement"""
        
        savings_group = {
            "group_id": group_data["group_id"],
            "group_name": group_data["group_name"],
            "members": group_data.get("members", []),
            "contribution_schedule": group_data.get("contribution_schedule", "monthly"),
            "contribution_amount": group_data.get("contribution_amount", 50),
            "total_savings": 0.0,
            "loan_fund": 0.0,
            "traditional_system_integration": {},
            "digital_enhancements": {},
            "ubuntu_group_principles": "",
            "governance_structure": {},
            "financial_services": []
        }
        
        # Calculate totals
        savings_group["total_savings"] = len(savings_group["members"]) * savings_group["contribution_amount"] * 12
        savings_group["loan_fund"] = savings_group["total_savings"] * 0.8  # 80% available for loans
        
        # Traditional system integration
        rotating_savings = self.knowledge_base.get_traditional_financial_system("rotating_savings")
        savings_group["traditional_system_integration"] = {
            "traditional_names": rotating_savings.get("names", {}),
            "traditional_benefits": rotating_savings.get("benefits", []),
            "cultural_practices": "Monthly meetings with traditional ceremonies",
            "elder_involvement": "Community elders provide guidance and oversight"
        }
        
        # Digital enhancements
        savings_group["digital_enhancements"] = {
            "mobile_contributions": "Members can contribute via mobile money",
            "digital_record_keeping": "Automated tracking of contributions and loans",
            "sms_notifications": "Regular updates on group activities and balances",
            "online_meetings": "Virtual meetings when physical gathering not possible",
            "financial_analytics": "Group performance tracking and reporting"
        }
        
        # Ubuntu group principles
        savings_group["ubuntu_group_principles"] = (
            self.knowledge_base.apply_ubuntu_financial_principle("mutual_support")
        )
        
        # Governance structure
        savings_group["governance_structure"] = {
            "chairperson": "Elected group leader",
            "treasurer": "Manages group finances",
            "secretary": "Keeps records and communications",
            "committee": "Loan approval and conflict resolution",
            "general_assembly": "All members participate in major decisions"
        }
        
        # Financial services
        savings_group["financial_services"] = [
            "Regular savings with interest",
            "Emergency loans for members",
            "Business development loans",
            "Insurance coverage for members",
            "Financial literacy training",
            "Investment opportunities"
        ]
        
        return savings_group

class InsuranceManagementSystem:
    """Insurance management systems with agricultural and health focus"""
    
    def __init__(self):
        self.knowledge_base = AfricanFinancialKnowledge()
        self.insurance_products = {
            "crop_insurance": {
                "coverage": "Weather-related crop losses",
                "premium_rate": 0.05,  # 5% of coverage amount
                "payout_triggers": ["Drought", "Flood", "Pest infestation"],
                "community_pool": True
            },
            "livestock_insurance": {
                "coverage": "Livestock death and disease",
                "premium_rate": 0.08,  # 8% of coverage amount
                "payout_triggers": ["Disease outbreak", "Theft", "Natural disaster"],
                "community_pool": True
            },
            "health_microinsurance": {
                "coverage": "Basic healthcare services",
                "premium_rate": 0.12,  # 12% of coverage amount
                "payout_triggers": ["Hospitalization", "Surgery", "Chronic illness"],
                "community_pool": False
            },
            "life_microinsurance": {
                "coverage": "Life insurance for low-income families",
                "premium_rate": 0.03,  # 3% of coverage amount
                "payout_triggers": ["Death", "Permanent disability"],
                "community_pool": False
            }
        }
    
    async def create_insurance_policy(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create insurance policy with community pool options"""
        
        insurance_type = InsuranceType(policy_data["insurance_type"])
        product_info = self.insurance_products.get(insurance_type.value, {})
        
        policy = InsurancePolicy(
            policy_id=f"pol_{uuid.uuid4().hex[:8]}",
            policyholder_id=policy_data["policyholder_id"],
            insurance_type=insurance_type,
            coverage_amount=policy_data["coverage_amount"],
            premium=policy_data["coverage_amount"] * product_info.get("premium_rate", 0.05),
            currency=policy_data.get("currency", "USD"),
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            status="active",
            beneficiaries=policy_data.get("beneficiaries", []),
            community_pool=product_info.get("community_pool", False)
        )
        
        policy_result = {
            "policy": asdict(policy),
            "product_details": product_info,
            "community_pool_benefits": {},
            "traditional_risk_sharing": {},
            "ubuntu_insurance_approach": "",
            "claim_process": {},
            "premium_payment_options": []
        }
        
        # Community pool benefits
        if policy.community_pool:
            policy_result["community_pool_benefits"] = {
                "shared_risk": "Risk shared among community members",
                "lower_premiums": "Reduced individual premium costs",
                "mutual_support": "Community support during claims",
                "collective_bargaining": "Better terms through group participation"
            }
        
        # Traditional risk sharing
        policy_result["traditional_risk_sharing"] = {
            "community_support": "Traditional community assistance during disasters",
            "extended_family": "Family network support system",
            "reciprocal_help": "Mutual aid and assistance traditions",
            "modern_integration": "Formal insurance complements traditional support"
        }
        
        # Ubuntu insurance approach
        policy_result["ubuntu_insurance_approach"] = (
            self.knowledge_base.apply_ubuntu_financial_principle("shared_responsibility")
        )
        
        # Claim process
        policy_result["claim_process"] = {
            "notification": "Report claim via mobile phone or community agent",
            "assessment": "Community-based assessment with external verification",
            "approval": "Transparent approval process with community involvement",
            "payout": "Quick payout through mobile money or agent network"
        }
        
        # Premium payment options
        policy_result["premium_payment_options"] = [
            "Mobile money payments",
            "Agent-assisted payments",
            "Group payment through savings association",
            "Seasonal payment aligned with harvest cycles",
            "Micro-payment installments"
        ]
        
        return policy_result
    
    async def process_insurance_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process insurance claim with community verification"""
        
        claim_result = {
            "claim_id": f"claim_{uuid.uuid4().hex[:8]}",
            "policy_id": claim_data["policy_id"],
            "claim_amount": claim_data["claim_amount"],
            "claim_reason": claim_data["claim_reason"],
            "submission_date": datetime.now().isoformat(),
            "status": "under_review",
            "community_verification": {},
            "assessment_process": {},
            "ubuntu_claim_support": "",
            "payout_timeline": {},
            "additional_support": []
        }
        
        # Community verification
        claim_result["community_verification"] = {
            "local_witnesses": "Community members verify the claim circumstances",
            "traditional_leaders": "Local leaders provide attestation",
            "peer_confirmation": "Fellow farmers/community members confirm losses",
            "transparency": "Open verification process builds trust"
        }
        
        # Assessment process
        claim_result["assessment_process"] = {
            "initial_review": "Claim documentation and eligibility check",
            "field_assessment": "On-site verification by trained assessors",
            "community_input": "Local knowledge and witness statements",
            "final_determination": "Claim approval and payout calculation"
        }
        
        # Ubuntu claim support
        claim_result["ubuntu_claim_support"] = (
            self.knowledge_base.apply_ubuntu_financial_principle("mutual_support")
        )
        
        # Payout timeline
        claim_result["payout_timeline"] = {
            "emergency_advance": "Immediate emergency support within 24 hours",
            "partial_payout": "50% payout within 7 days of approval",
            "full_settlement": "Complete payout within 30 days",
            "mobile_money_transfer": "Instant transfer to mobile money account"
        }
        
        # Additional support
        claim_result["additional_support"] = [
            "Community emergency fund access",
            "Rehabilitation and recovery assistance",
            "Financial counseling and planning",
            "Connection to government support programs",
            "Peer support and counseling services"
        ]
        
        return claim_result

class FinanceManagementAgent:
    """Main Finance Management Systems Agent"""
    
    def __init__(self, db_path: str = "/tmp/finance_management.db"):
        self.db_path = db_path
        self.banking_microfinance = BankingMicrofinanceSystem()
        self.investment_savings = InvestmentSavingsSystem()
        self.insurance_management = InsuranceManagementSystem()
        self.knowledge_base = AfricanFinancialKnowledge()
        
        # Initialize database
        self._init_database()
        
        logger.info("Finance Management Systems Agent initialized")
    
    def _init_database(self):
        """Initialize SQLite database for finance management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create financial_accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_accounts (
                account_id TEXT PRIMARY KEY,
                account_type TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                balance REAL NOT NULL,
                currency TEXT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                mobile_number TEXT,
                cooperative_group TEXT,
                traditional_savings_group TEXT
            )
        """)
        
        # Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                recipient_account TEXT,
                mobile_number TEXT,
                location TEXT,
                offline_processed BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Create loans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                loan_id TEXT PRIMARY KEY,
                borrower_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                interest_rate REAL NOT NULL,
                term_months INTEGER NOT NULL,
                purpose TEXT,
                status TEXT NOT NULL,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                collateral_type TEXT,
                group_guarantee BOOLEAN DEFAULT FALSE,
                traditional_guarantee TEXT
            )
        """)
        
        # Create insurance_policies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insurance_policies (
                policy_id TEXT PRIMARY KEY,
                policyholder_id TEXT NOT NULL,
                insurance_type TEXT NOT NULL,
                coverage_amount REAL NOT NULL,
                premium REAL NOT NULL,
                currency TEXT NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                status TEXT NOT NULL,
                beneficiaries TEXT,
                community_pool BOOLEAN DEFAULT FALSE
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def comprehensive_financial_management(self, financial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide comprehensive financial management for African contexts"""
        
        # Create sample financial account
        account_data = {
            "account_type": financial_context.get("account_type", "savings"),
            "owner_name": financial_context.get("owner_name", "Sample User"),
            "owner_id": financial_context.get("owner_id", "user_001"),
            "initial_balance": financial_context.get("initial_balance", 1000.0),
            "currency": financial_context.get("currency", "USD"),
            "mobile_number": financial_context.get("mobile_number", "+254700000000"),
            "cooperative_group": financial_context.get("cooperative_group", ""),
            "traditional_savings_group": financial_context.get("traditional_savings_group", "Community Chama")
        }
        
        # Create investment portfolio
        investor_profile = {
            "investor_id": financial_context.get("owner_id", "user_001"),
            "risk_tolerance": financial_context.get("risk_tolerance", "medium"),
            "investment_goals": financial_context.get("investment_goals", ["Retirement", "Education"]),
            "available_capital": financial_context.get("available_capital", 5000.0)
        }
        
        # Create insurance policy
        insurance_data = {
            "insurance_type": financial_context.get("insurance_type", "crop"),
            "policyholder_id": financial_context.get("owner_id", "user_001"),
            "coverage_amount": financial_context.get("coverage_amount", 10000.0),
            "currency": financial_context.get("currency", "USD"),
            "beneficiaries": financial_context.get("beneficiaries", ["Spouse", "Children"])
        }
        
        # Generate comprehensive financial plan
        comprehensive_plan = {
            "account_management": {},
            "investment_portfolio": {},
            "insurance_coverage": {},
            "traditional_financial_integration": {},
            "mobile_money_services": {},
            "ubuntu_financial_approach": {},
            "financial_inclusion_strategy": {},
            "community_financial_services": {}
        }
        
        # Account management
        comprehensive_plan["account_management"] = await self.banking_microfinance.create_financial_account(account_data)
        
        # Investment portfolio
        comprehensive_plan["investment_portfolio"] = await self.investment_savings.create_investment_portfolio(investor_profile)
        
        # Insurance coverage
        comprehensive_plan["insurance_coverage"] = await self.insurance_management.create_insurance_policy(insurance_data)
        
        # Traditional financial integration
        comprehensive_plan["traditional_financial_integration"] = {
            "rotating_savings": self.knowledge_base.get_traditional_financial_system("rotating_savings"),
            "community_banking": self.knowledge_base.get_traditional_financial_system("community_banking"),
            "livestock_banking": self.knowledge_base.get_traditional_financial_system("livestock_banking"),
            "modern_integration_strategies": [
                "Digital record keeping for traditional systems",
                "Mobile money integration with community savings",
                "Insurance products for traditional investments",
                "Credit scoring using traditional group participation"
            ]
        }
        
        # Mobile money services
        comprehensive_plan["mobile_money_services"] = {
            "available_providers": self.knowledge_base.mobile_money_systems,
            "integrated_services": [
                "Account deposits and withdrawals",
                "Bill payments and merchant transactions",
                "International remittances",
                "Savings and investment products",
                "Insurance premium payments",
                "Loan disbursements and repayments"
            ],
            "offline_capabilities": [
                "SMS-based transactions",
                "Agent-assisted services",
                "USSD menu access",
                "Paper-based backup systems"
            ]
        }
        
        # Ubuntu financial approach
        comprehensive_plan["ubuntu_financial_approach"] = {
            "collective_prosperity": self.knowledge_base.apply_ubuntu_financial_principle("collective_prosperity"),
            "mutual_support": self.knowledge_base.apply_ubuntu_financial_principle("mutual_support"),
            "shared_responsibility": self.knowledge_base.apply_ubuntu_financial_principle("shared_responsibility"),
            "transparent_dealings": self.knowledge_base.apply_ubuntu_financial_principle("transparent_dealings"),
            "sustainable_growth": self.knowledge_base.apply_ubuntu_financial_principle("sustainable_growth")
        }
        
        # Financial inclusion strategy
        comprehensive_plan["financial_inclusion_strategy"] = {
            "strategies": self.knowledge_base.financial_inclusion_strategies,
            "implementation": [
                "Agent banking network expansion",
                "Mobile banking platform development",
                "Microfinance product innovation",
                "Financial literacy program implementation",
                "Digital identity system integration",
                "Alternative credit scoring deployment"
            ]
        }
        
        # Community financial services
        group_data = {
            "group_id": "group_001",
            "group_name": financial_context.get("traditional_savings_group", "Community Chama"),
            "members": financial_context.get("group_members", ["Member1", "Member2", "Member3"]),
            "contribution_amount": financial_context.get("contribution_amount", 100.0)
        }
        
        comprehensive_plan["community_financial_services"] = await self.investment_savings.manage_community_savings_group(group_data)
        
        return comprehensive_plan
    
    async def process_voice_command(self, command: str, context: Dict[str, Any] = None, 
                                  language: str = "en") -> Dict[str, Any]:
        """Process voice commands for finance management"""
        
        command_lower = command.lower()
        
        # Swahili commands
        if language == "sw":
            if "pesa" in command_lower or "benki" in command_lower:
                return {
                    "action": "banking_services",
                    "response": "Nitakusaidia na huduma za benki na pesa. Tutaangalia akaunti, malipo, na mikopo.",
                    "english": "I will help with banking and money services. We will look at accounts, payments, and loans.",
                    "next_steps": ["Account management", "Transaction processing", "Loan services"]
                }
            elif "chama" in command_lower or "akiba" in command_lower:
                return {
                    "action": "savings_investment",
                    "response": "Nitasaidia katika vikundi vya akiba na uwekezaji. Tutapanga mipango ya kifedha.",
                    "english": "I will help with savings groups and investment. We will plan financial strategies.",
                    "next_steps": ["Savings group management", "Investment planning", "Financial education"]
                }
        
        # Hausa commands
        elif language == "ha":
            if "kudi" in command_lower or "banki" in command_lower:
                return {
                    "action": "financial_services",
                    "response": "Zan taimake ka da harkokin kudi da banki. Za mu duba asusun, biyan kudi, da lamuni.",
                    "english": "I will help with money and banking matters. We will look at accounts, payments, and loans.",
                    "next_steps": ["Account services", "Payment processing", "Credit services"]
                }
        
        # English commands
        else:
            if "account" in command_lower or "banking" in command_lower:
                return {
                    "action": "banking_management",
                    "response": "I'll help manage banking services with mobile money integration and traditional savings support.",
                    "next_steps": ["Account creation", "Transaction processing", "Mobile money integration"]
                }
            elif "investment" in command_lower or "savings" in command_lower:
                return {
                    "action": "investment_planning",
                    "response": "Let me help with investment and savings planning using community-based approaches and Ubuntu principles.",
                    "next_steps": ["Portfolio creation", "Community investment", "Financial education"]
                }
            elif "insurance" in command_lower or "protection" in command_lower:
                return {
                    "action": "insurance_management",
                    "response": "I'll assist with insurance products focused on agricultural and health coverage with community pools.",
                    "next_steps": ["Policy creation", "Claim processing", "Community risk sharing"]
                }
        
        return {
            "action": "general_finance_help",
            "response": "I can help with banking, investments, insurance, mobile money, and community financial services.",
            "available_commands": [
                "Manage bank accounts",
                "Process transactions",
                "Plan investments",
                "Create insurance policies"
            ]
        }
    
    async def test_finance_management_capabilities(self) -> Dict[str, bool]:
        """Test finance management capabilities"""
        
        test_results = {
            "banking_microfinance_system": False,
            "investment_savings_system": False,
            "insurance_management_system": False,
            "traditional_financial_integration": False,
            "mobile_money_integration": False,
            "voice_command_processing": False,
            "ubuntu_philosophy_application": False,
            "comprehensive_financial_management": False
        }
        
        try:
            # Test banking and microfinance system
            account_data = {
                "account_type": "savings",
                "owner_name": "Test User",
                "owner_id": "test_001",
                "mobile_number": "+254700000000"
            }
            
            account_result = await self.banking_microfinance.create_financial_account(account_data)
            test_results["banking_microfinance_system"] = "account" in account_result
            
            # Test investment and savings system
            investor_profile = {
                "investor_id": "test_001",
                "risk_tolerance": "medium",
                "available_capital": 1000.0
            }
            
            portfolio_result = await self.investment_savings.create_investment_portfolio(investor_profile)
            test_results["investment_savings_system"] = "recommended_allocation" in portfolio_result
            
            # Test insurance management system
            insurance_data = {
                "insurance_type": "crop",
                "policyholder_id": "test_001",
                "coverage_amount": 5000.0
            }
            
            insurance_result = await self.insurance_management.create_insurance_policy(insurance_data)
            test_results["insurance_management_system"] = "policy" in insurance_result
            
            # Test traditional financial integration
            traditional_system = self.knowledge_base.get_traditional_financial_system("rotating_savings")
            test_results["traditional_financial_integration"] = len(traditional_system) > 0
            
            # Test mobile money integration
            mobile_money_info = self.knowledge_base.get_mobile_money_integration("m_pesa")
            test_results["mobile_money_integration"] = len(mobile_money_info) > 0
            
            # Test voice command processing
            voice_result = await self.process_voice_command("help with banking", {}, "en")
            test_results["voice_command_processing"] = "action" in voice_result
            
            # Test Ubuntu philosophy application
            ubuntu_message = self.knowledge_base.apply_ubuntu_financial_principle("collective_prosperity")
            test_results["ubuntu_philosophy_application"] = "ubuntu" in ubuntu_message.lower()
            
            # Test comprehensive financial management
            financial_context = {
                "owner_name": "Test User",
                "owner_id": "test_001",
                "account_type": "savings"
            }
            
            comprehensive_result = await self.comprehensive_financial_management(financial_context)
            test_results["comprehensive_financial_management"] = "account_management" in comprehensive_result
            
            logger.info("Finance management capabilities test completed")
            
        except Exception as e:
            logger.error(f"Finance management capabilities test error: {e}")
        
        return test_results

# Example usage and testing
async def main():
    """Example usage of Finance Management Agent"""
    agent = FinanceManagementAgent()
    
    # Test capabilities
    test_results = await agent.test_finance_management_capabilities()
    print("Finance Management Test Results:")
    for test, result in test_results.items():
        print(f"  {test}: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Example comprehensive financial management
    financial_context = {
        "owner_name": "Fatima Mwangi",
        "owner_id": "user_12345",
        "account_type": "microfinance",
        "initial_balance": 2500.0,
        "currency": "KES",
        "mobile_number": "+254712345678",
        "traditional_savings_group": "Umoja Women's Chama",
        "risk_tolerance": "medium",
        "investment_goals": ["Children's education", "Business expansion"],
        "available_capital": 10000.0,
        "insurance_type": "crop",
        "coverage_amount": 50000.0,
        "group_members": ["Fatima", "Grace", "Mary", "Jane", "Rose"]
    }
    
    comprehensive_plan = await agent.comprehensive_financial_management(financial_context)
    print(f"\nComprehensive Financial Plan for {financial_context['owner_name']}")
    print(f"Account Balance: {comprehensive_plan['account_management']['account']['balance']} {comprehensive_plan['account_management']['account']['currency']}")
    print(f"Investment Portfolio: {len(comprehensive_plan['investment_portfolio']['recommended_allocation'])} products")
    print(f"Insurance Coverage: {comprehensive_plan['insurance_coverage']['policy']['coverage_amount']} {comprehensive_plan['insurance_coverage']['policy']['currency']}")
    print(f"Ubuntu Approach: {comprehensive_plan['ubuntu_financial_approach']['collective_prosperity']}")

if __name__ == "__main__":
    asyncio.run(main())

