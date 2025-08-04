"""
WebWaka Financial Management System
AI-powered financial management with fraud detection and African financial contexts
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

class AccountType(Enum):
    """Account types"""
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

class TransactionType(Enum):
    """Transaction types"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"

class PaymentMethod(Enum):
    """Payment methods"""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    CARD = "card"
    CHEQUE = "cheque"
    BARTER = "barter"
    CRYPTOCURRENCY = "cryptocurrency"

class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    RECONCILED = "reconciled"

class InvoiceStatus(Enum):
    """Invoice status"""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

@dataclass
class Account:
    """Financial account"""
    account_id: str
    tenant_id: str
    account_code: str
    account_name: str
    account_type: AccountType
    parent_account_id: Optional[str]
    currency: str
    balance: Decimal
    opening_balance: Decimal
    description: str
    is_active: bool
    bank_details: Optional[Dict[str, str]]
    mobile_money_details: Optional[Dict[str, str]]
    created_at: datetime
    updated_at: datetime

@dataclass
class Transaction:
    """Financial transaction"""
    transaction_id: str
    tenant_id: str
    transaction_number: str
    transaction_type: TransactionType
    amount: Decimal
    currency: str
    exchange_rate: Optional[Decimal]
    base_amount: Optional[Decimal]  # Amount in base currency
    description: str
    reference: Optional[str]
    debit_account_id: str
    credit_account_id: str
    payment_method: PaymentMethod
    payment_details: Dict[str, Any]
    status: TransactionStatus
    transaction_date: datetime
    due_date: Optional[datetime]
    customer_id: Optional[str]
    supplier_id: Optional[str]
    invoice_id: Optional[str]
    receipt_number: Optional[str]
    attachments: List[str]
    tags: List[str]
    notes: str
    created_by: str
    approved_by: Optional[str]
    fraud_score: Optional[float]
    created_at: datetime
    updated_at: datetime

@dataclass
class Invoice:
    """Invoice information"""
    invoice_id: str
    tenant_id: str
    invoice_number: str
    customer_id: str
    issue_date: datetime
    due_date: datetime
    currency: str
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    balance_due: Decimal
    status: InvoiceStatus
    payment_terms: str
    line_items: List[Dict[str, Any]]
    notes: str
    created_by: str
    sent_at: Optional[datetime]
    viewed_at: Optional[datetime]
    paid_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

@dataclass
class Budget:
    """Budget information"""
    budget_id: str
    tenant_id: str
    name: str
    description: str
    period_start: datetime
    period_end: datetime
    currency: str
    total_budgeted: Decimal
    total_actual: Decimal
    variance: Decimal
    variance_percentage: float
    categories: Dict[str, Dict[str, Decimal]]  # category -> {budgeted, actual, variance}
    status: str
    created_by: str
    approved_by: Optional[str]
    created_at: datetime
    updated_at: datetime

class VoiceFinancialProcessor:
    """Process voice commands for financial operations"""
    
    def __init__(self):
        self.command_patterns = self._initialize_financial_commands()
    
    def _initialize_financial_commands(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize financial voice command patterns"""
        return {
            'en': {
                'record_expense': [
                    'record expense of {amount}',
                    'add expense {amount} for {description}',
                    'spent {amount} on {description}'
                ],
                'record_income': [
                    'record income of {amount}',
                    'received {amount} from {description}',
                    'got paid {amount}'
                ],
                'check_balance': [
                    'check account balance',
                    'what is my balance',
                    'show account balance'
                ],
                'create_invoice': [
                    'create invoice for {amount}',
                    'bill customer {amount}',
                    'invoice {customer} for {amount}'
                ]
            },
            'sw': {  # Swahili
                'record_expense': [
                    'rekodi gharama ya {amount}',
                    'ongeza gharama {amount}'
                ],
                'record_income': [
                    'rekodi mapato ya {amount}',
                    'nilipokea {amount}'
                ],
                'check_balance': [
                    'angalia salio la akaunti',
                    'nina kiasi gani'
                ]
            }
        }
    
    def process_voice_command(self, command: str, language: str = 'en') -> Dict[str, Any]:
        """Process financial voice command"""
        try:
            command_lower = command.lower().strip()
            patterns = self.command_patterns.get(language, self.command_patterns['en'])
            
            for intent, pattern_list in patterns.items():
                for pattern in pattern_list:
                    match_result = self._match_financial_pattern(command_lower, pattern)
                    if match_result:
                        return {
                            'intent': intent,
                            'entities': match_result,
                            'original_command': command,
                            'language': language,
                            'confidence': 0.9
                        }
            
            return self._ai_powered_financial_nlu(command, language)
            
        except Exception as e:
            logger.error(f"Financial voice command processing failed: {str(e)}")
            return {
                'intent': 'unknown',
                'entities': {},
                'error': str(e)
            }
    
    def _match_financial_pattern(self, command: str, pattern: str) -> Optional[Dict[str, str]]:
        """Match financial command pattern"""
        import re
        
        # Replace placeholders with regex patterns
        regex_pattern = pattern.replace('{amount}', r'(\d+(?:\.\d{2})?)')
        regex_pattern = regex_pattern.replace('{description}', r'([a-zA-Z\s]+)')
        regex_pattern = regex_pattern.replace('{customer}', r'([a-zA-Z\s]+)')
        
        match = re.search(regex_pattern, command, re.IGNORECASE)
        
        if match:
            entities = {}
            groups = match.groups()
            
            # Extract amount
            for group in groups:
                if re.match(r'\d+(?:\.\d{2})?', group):
                    entities['amount'] = float(group)
                    break
            
            # Extract description/customer
            text_groups = [g for g in groups if not re.match(r'\d+(?:\.\d{2})?', g)]
            if text_groups:
                if '{customer}' in pattern:
                    entities['customer'] = text_groups[0].strip()
                elif '{description}' in pattern:
                    entities['description'] = text_groups[0].strip()
            
            return entities
        
        return None
    
    def _ai_powered_financial_nlu(self, command: str, language: str) -> Dict[str, Any]:
        """AI-powered financial natural language understanding"""
        return {
            'intent': 'unknown',
            'entities': {},
            'original_command': command,
            'language': language,
            'confidence': 0.3,
            'ai_processed': True
        }

class FraudDetectionEngine:
    """AI-powered fraud detection for financial transactions"""
    
    def __init__(self):
        self.fraud_indicators = [
            'unusual_amount',
            'unusual_time',
            'unusual_location',
            'rapid_transactions',
            'round_numbers',
            'duplicate_transactions',
            'suspicious_description'
        ]
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    
    def analyze_transaction(self, transaction: Transaction, 
                          historical_transactions: List[Transaction]) -> Dict[str, Any]:
        """Analyze transaction for fraud indicators"""
        try:
            fraud_score = 0.0
            indicators = []
            
            # Amount analysis
            amount_score = self._analyze_amount(transaction, historical_transactions)
            fraud_score += amount_score['score']
            if amount_score['indicators']:
                indicators.extend(amount_score['indicators'])
            
            # Time analysis
            time_score = self._analyze_timing(transaction, historical_transactions)
            fraud_score += time_score['score']
            if time_score['indicators']:
                indicators.extend(time_score['indicators'])
            
            # Pattern analysis
            pattern_score = self._analyze_patterns(transaction, historical_transactions)
            fraud_score += pattern_score['score']
            if pattern_score['indicators']:
                indicators.extend(pattern_score['indicators'])
            
            # Determine risk level
            if fraud_score >= self.risk_thresholds['high']:
                risk_level = 'high'
            elif fraud_score >= self.risk_thresholds['medium']:
                risk_level = 'medium'
            elif fraud_score >= self.risk_thresholds['low']:
                risk_level = 'low'
            else:
                risk_level = 'minimal'
            
            return {
                'transaction_id': transaction.transaction_id,
                'fraud_score': min(fraud_score, 1.0),
                'risk_level': risk_level,
                'indicators': indicators,
                'recommendations': self._generate_fraud_recommendations(risk_level, indicators)
            }
            
        except Exception as e:
            logger.error(f"Fraud analysis failed: {str(e)}")
            return {
                'transaction_id': transaction.transaction_id,
                'fraud_score': 0.0,
                'risk_level': 'unknown',
                'error': str(e)
            }
    
    def _analyze_amount(self, transaction: Transaction, 
                       historical_transactions: List[Transaction]) -> Dict[str, Any]:
        """Analyze transaction amount for anomalies"""
        score = 0.0
        indicators = []
        
        if not historical_transactions:
            return {'score': 0.0, 'indicators': []}
        
        # Calculate typical transaction amounts
        amounts = [float(t.amount) for t in historical_transactions]
        avg_amount = sum(amounts) / len(amounts)
        
        transaction_amount = float(transaction.amount)
        
        # Check for unusually large amounts
        if transaction_amount > avg_amount * 5:
            score += 0.3
            indicators.append('unusually_large_amount')
        
        # Check for round numbers (potential fraud indicator)
        if transaction_amount % 100 == 0 and transaction_amount >= 1000:
            score += 0.1
            indicators.append('round_number_amount')
        
        return {'score': score, 'indicators': indicators}
    
    def _analyze_timing(self, transaction: Transaction, 
                       historical_transactions: List[Transaction]) -> Dict[str, Any]:
        """Analyze transaction timing for anomalies"""
        score = 0.0
        indicators = []
        
        # Check for unusual hours
        hour = transaction.transaction_date.hour
        if hour < 6 or hour > 22:  # Outside normal business hours
            score += 0.2
            indicators.append('unusual_hour')
        
        # Check for rapid transactions
        recent_transactions = [
            t for t in historical_transactions
            if abs((t.transaction_date - transaction.transaction_date).total_seconds()) < 300  # 5 minutes
        ]
        
        if len(recent_transactions) > 3:
            score += 0.3
            indicators.append('rapid_transactions')
        
        return {'score': score, 'indicators': indicators}
    
    def _analyze_patterns(self, transaction: Transaction, 
                         historical_transactions: List[Transaction]) -> Dict[str, Any]:
        """Analyze transaction patterns for anomalies"""
        score = 0.0
        indicators = []
        
        # Check for duplicate transactions
        duplicates = [
            t for t in historical_transactions
            if (t.amount == transaction.amount and 
                t.description == transaction.description and
                abs((t.transaction_date - transaction.transaction_date).total_seconds()) < 3600)  # 1 hour
        ]
        
        if duplicates:
            score += 0.4
            indicators.append('potential_duplicate')
        
        # Check for suspicious descriptions
        suspicious_keywords = ['test', 'temp', 'fake', 'dummy']
        if any(keyword in transaction.description.lower() for keyword in suspicious_keywords):
            score += 0.2
            indicators.append('suspicious_description')
        
        return {'score': score, 'indicators': indicators}
    
    def _generate_fraud_recommendations(self, risk_level: str, indicators: List[str]) -> List[str]:
        """Generate fraud prevention recommendations"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append('Block transaction immediately')
            recommendations.append('Require additional verification')
            recommendations.append('Flag for manual review')
        elif risk_level == 'medium':
            recommendations.append('Require additional verification')
            recommendations.append('Monitor closely')
        elif risk_level == 'low':
            recommendations.append('Log for monitoring')
        
        if 'rapid_transactions' in indicators:
            recommendations.append('Implement transaction velocity limits')
        
        if 'unusual_hour' in indicators:
            recommendations.append('Verify user identity for off-hours transactions')
        
        return recommendations

class FinancialManager:
    """Main financial management system"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.accounts = {}
        self.transactions = {}
        self.invoices = {}
        self.budgets = {}
        self.voice_processor = VoiceFinancialProcessor()
        self.fraud_detector = FraudDetectionEngine()
        self.african_adapter = AfricanFinancialAdapter()
        self._initialize_default_accounts()
    
    def _initialize_default_accounts(self):
        """Initialize default chart of accounts"""
        default_accounts = [
            {
                'account_code': '1000',
                'account_name': 'Cash',
                'account_type': AccountType.ASSET,
                'description': 'Cash on hand'
            },
            {
                'account_code': '1100',
                'account_name': 'Bank Account',
                'account_type': AccountType.ASSET,
                'description': 'Bank account balance'
            },
            {
                'account_code': '1200',
                'account_name': 'Mobile Money',
                'account_type': AccountType.ASSET,
                'description': 'Mobile money account'
            },
            {
                'account_code': '4000',
                'account_name': 'Sales Revenue',
                'account_type': AccountType.REVENUE,
                'description': 'Revenue from sales'
            },
            {
                'account_code': '5000',
                'account_name': 'Operating Expenses',
                'account_type': AccountType.EXPENSE,
                'description': 'General operating expenses'
            }
        ]
        
        for account_data in default_accounts:
            self.create_account(account_data)
    
    def create_account(self, account_data: Dict[str, Any]) -> Account:
        """Create new financial account"""
        try:
            account_id = str(uuid.uuid4())
            
            account = Account(
                account_id=account_id,
                tenant_id=self.tenant_id,
                account_code=account_data['account_code'],
                account_name=account_data['account_name'],
                account_type=AccountType(account_data['account_type']),
                parent_account_id=account_data.get('parent_account_id'),
                currency=account_data.get('currency', 'USD'),
                balance=Decimal('0'),
                opening_balance=Decimal(str(account_data.get('opening_balance', 0))),
                description=account_data.get('description', ''),
                is_active=account_data.get('is_active', True),
                bank_details=account_data.get('bank_details'),
                mobile_money_details=account_data.get('mobile_money_details'),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.accounts[account_id] = account
            
            # Set initial balance if opening balance provided
            if account.opening_balance != 0:
                account.balance = account.opening_balance
            
            logger.info(f"Created account {account.account_name} with ID {account_id}")
            return account
            
        except Exception as e:
            logger.error(f"Account creation failed: {str(e)}")
            raise FinancialException(f"Account creation failed: {str(e)}")
    
    def create_transaction(self, transaction_data: Dict[str, Any]) -> Transaction:
        """Create new financial transaction"""
        try:
            transaction_id = str(uuid.uuid4())
            transaction_number = transaction_data.get('transaction_number', f"TXN-{transaction_id[:8]}")
            
            transaction = Transaction(
                transaction_id=transaction_id,
                tenant_id=self.tenant_id,
                transaction_number=transaction_number,
                transaction_type=TransactionType(transaction_data['transaction_type']),
                amount=Decimal(str(transaction_data['amount'])),
                currency=transaction_data.get('currency', 'USD'),
                exchange_rate=Decimal(str(transaction_data['exchange_rate'])) if transaction_data.get('exchange_rate') else None,
                base_amount=None,  # Will be calculated
                description=transaction_data['description'],
                reference=transaction_data.get('reference'),
                debit_account_id=transaction_data['debit_account_id'],
                credit_account_id=transaction_data['credit_account_id'],
                payment_method=PaymentMethod(transaction_data.get('payment_method', 'cash')),
                payment_details=transaction_data.get('payment_details', {}),
                status=TransactionStatus.PENDING,
                transaction_date=transaction_data.get('transaction_date', datetime.utcnow()),
                due_date=transaction_data.get('due_date'),
                customer_id=transaction_data.get('customer_id'),
                supplier_id=transaction_data.get('supplier_id'),
                invoice_id=transaction_data.get('invoice_id'),
                receipt_number=transaction_data.get('receipt_number'),
                attachments=transaction_data.get('attachments', []),
                tags=transaction_data.get('tags', []),
                notes=transaction_data.get('notes', ''),
                created_by=transaction_data['created_by'],
                approved_by=None,
                fraud_score=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Calculate base amount if exchange rate provided
            if transaction.exchange_rate:
                transaction.base_amount = transaction.amount * transaction.exchange_rate
            
            # Run fraud detection
            historical_transactions = list(self.transactions.values())
            fraud_analysis = self.fraud_detector.analyze_transaction(transaction, historical_transactions)
            transaction.fraud_score = fraud_analysis['fraud_score']
            
            # Auto-approve low-risk transactions
            if fraud_analysis['risk_level'] in ['minimal', 'low']:
                transaction.status = TransactionStatus.COMPLETED
                self._update_account_balances(transaction)
            
            self.transactions[transaction_id] = transaction
            
            logger.info(f"Created transaction {transaction_number} with fraud score {fraud_analysis['fraud_score']}")
            return transaction
            
        except Exception as e:
            logger.error(f"Transaction creation failed: {str(e)}")
            raise FinancialException(f"Transaction creation failed: {str(e)}")
    
    def _update_account_balances(self, transaction: Transaction):
        """Update account balances for completed transaction"""
        try:
            debit_account = self.accounts.get(transaction.debit_account_id)
            credit_account = self.accounts.get(transaction.credit_account_id)
            
            if not debit_account or not credit_account:
                raise FinancialException("Invalid account IDs in transaction")
            
            # Update debit account (increase for assets/expenses, decrease for liabilities/equity/revenue)
            if debit_account.account_type in [AccountType.ASSET, AccountType.EXPENSE]:
                debit_account.balance += transaction.amount
            else:
                debit_account.balance -= transaction.amount
            
            # Update credit account (decrease for assets/expenses, increase for liabilities/equity/revenue)
            if credit_account.account_type in [AccountType.ASSET, AccountType.EXPENSE]:
                credit_account.balance -= transaction.amount
            else:
                credit_account.balance += transaction.amount
            
            # Update timestamps
            debit_account.updated_at = datetime.utcnow()
            credit_account.updated_at = datetime.utcnow()
            
        except Exception as e:
            logger.error(f"Balance update failed: {str(e)}")
            raise FinancialException(f"Balance update failed: {str(e)}")
    
    def process_voice_command(self, command: str, language: str = 'en',
                             user_id: str = None) -> Dict[str, Any]:
        """Process voice command for financial operations"""
        try:
            command_result = self.voice_processor.process_voice_command(command, language)
            
            if command_result['confidence'] < 0.5:
                return {
                    'success': False,
                    'message': 'Could not understand the financial command',
                    'original_command': command
                }
            
            intent = command_result['intent']
            entities = command_result['entities']
            
            if intent == 'record_expense':
                return self._handle_record_expense_voice(entities, command, user_id)
            elif intent == 'record_income':
                return self._handle_record_income_voice(entities, command, user_id)
            elif intent == 'check_balance':
                return self._handle_check_balance_voice(entities, command)
            elif intent == 'create_invoice':
                return self._handle_create_invoice_voice(entities, command, user_id)
            else:
                return {
                    'success': False,
                    'message': f'Unknown financial command: {intent}',
                    'original_command': command
                }
                
        except Exception as e:
            logger.error(f"Financial voice command processing failed: {str(e)}")
            return {
                'success': False,
                'message': 'Financial voice command processing failed',
                'error': str(e)
            }
    
    def _handle_record_expense_voice(self, entities: Dict[str, Any], 
                                    original_command: str, user_id: str) -> Dict[str, Any]:
        """Handle record expense voice command"""
        try:
            amount = entities.get('amount')
            description = entities.get('description', 'Voice recorded expense')
            
            if not amount:
                return {
                    'success': False,
                    'message': 'Amount not specified',
                    'original_command': original_command
                }
            
            # Find cash and expense accounts
            cash_account = None
            expense_account = None
            
            for account in self.accounts.values():
                if account.account_code == '1000':  # Cash
                    cash_account = account
                elif account.account_code == '5000':  # Operating Expenses
                    expense_account = account
            
            if not cash_account or not expense_account:
                return {
                    'success': False,
                    'message': 'Required accounts not found',
                    'original_command': original_command
                }
            
            # Create expense transaction
            transaction_data = {
                'transaction_type': 'expense',
                'amount': amount,
                'description': description,
                'debit_account_id': expense_account.account_id,
                'credit_account_id': cash_account.account_id,
                'created_by': user_id or 'voice_system'
            }
            
            transaction = self.create_transaction(transaction_data)
            
            return {
                'success': True,
                'message': f'Recorded expense of {amount} for {description}',
                'transaction_id': transaction.transaction_id,
                'original_command': original_command
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'Failed to record expense',
                'error': str(e)
            }
    
    def create_invoice(self, invoice_data: Dict[str, Any]) -> Invoice:
        """Create new invoice"""
        try:
            invoice_id = str(uuid.uuid4())
            invoice_number = invoice_data.get('invoice_number', f"INV-{invoice_id[:8]}")
            
            # Calculate totals
            line_items = invoice_data.get('line_items', [])
            subtotal = sum(Decimal(str(item.get('amount', 0))) for item in line_items)
            tax_amount = subtotal * Decimal(str(invoice_data.get('tax_rate', 0.16)))  # 16% default
            discount_amount = Decimal(str(invoice_data.get('discount_amount', 0)))
            total_amount = subtotal + tax_amount - discount_amount
            
            invoice = Invoice(
                invoice_id=invoice_id,
                tenant_id=self.tenant_id,
                invoice_number=invoice_number,
                customer_id=invoice_data['customer_id'],
                issue_date=invoice_data.get('issue_date', datetime.utcnow()),
                due_date=invoice_data['due_date'],
                currency=invoice_data.get('currency', 'USD'),
                subtotal=subtotal,
                tax_amount=tax_amount,
                discount_amount=discount_amount,
                total_amount=total_amount,
                paid_amount=Decimal('0'),
                balance_due=total_amount,
                status=InvoiceStatus.DRAFT,
                payment_terms=invoice_data.get('payment_terms', 'Net 30'),
                line_items=line_items,
                notes=invoice_data.get('notes', ''),
                created_by=invoice_data['created_by'],
                sent_at=None,
                viewed_at=None,
                paid_at=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.invoices[invoice_id] = invoice
            
            logger.info(f"Created invoice {invoice_number} for customer {invoice_data['customer_id']}")
            return invoice
            
        except Exception as e:
            logger.error(f"Invoice creation failed: {str(e)}")
            raise FinancialException(f"Invoice creation failed: {str(e)}")
    
    def get_financial_dashboard(self) -> Dict[str, Any]:
        """Get financial dashboard data"""
        try:
            # Account balances
            cash_balance = Decimal('0')
            bank_balance = Decimal('0')
            total_assets = Decimal('0')
            total_liabilities = Decimal('0')
            
            for account in self.accounts.values():
                if account.account_code == '1000':  # Cash
                    cash_balance = account.balance
                elif account.account_code == '1100':  # Bank
                    bank_balance = account.balance
                
                if account.account_type == AccountType.ASSET:
                    total_assets += account.balance
                elif account.account_type == AccountType.LIABILITY:
                    total_liabilities += account.balance
            
            # Recent transactions
            recent_transactions = sorted(
                self.transactions.values(),
                key=lambda x: x.created_at,
                reverse=True
            )[:10]
            
            # Outstanding invoices
            outstanding_invoices = [
                i for i in self.invoices.values() 
                if i.status in [InvoiceStatus.SENT, InvoiceStatus.VIEWED, InvoiceStatus.OVERDUE]
            ]
            
            total_outstanding = sum(i.balance_due for i in outstanding_invoices)
            
            return {
                'summary': {
                    'cash_balance': str(cash_balance),
                    'bank_balance': str(bank_balance),
                    'total_assets': str(total_assets),
                    'total_liabilities': str(total_liabilities),
                    'outstanding_invoices': len(outstanding_invoices),
                    'total_outstanding': str(total_outstanding)
                },
                'recent_transactions': [
                    {
                        'transaction_id': t.transaction_id,
                        'description': t.description,
                        'amount': str(t.amount),
                        'date': t.transaction_date.isoformat(),
                        'status': t.status.value
                    }
                    for t in recent_transactions
                ],
                'outstanding_invoices': [
                    {
                        'invoice_id': i.invoice_id,
                        'invoice_number': i.invoice_number,
                        'customer_id': i.customer_id,
                        'total_amount': str(i.total_amount),
                        'balance_due': str(i.balance_due),
                        'due_date': i.due_date.isoformat()
                    }
                    for i in outstanding_invoices
                ]
            }
            
        except Exception as e:
            logger.error(f"Financial dashboard generation failed: {str(e)}")
            raise FinancialException(f"Financial dashboard generation failed: {str(e)}")

class AfricanFinancialAdapter:
    """Adapt financial management for African contexts"""
    
    def __init__(self):
        self.mobile_money_providers = {
            'kenya': ['mpesa', 'airtel_money', 'tkash'],
            'ghana': ['mtn_mobile_money', 'airtel_tigo_cash', 'vodafone_cash'],
            'nigeria': ['paga', 'quickteller', 'paycom'],
            'uganda': ['mtn_mobile_money', 'airtel_money'],
            'tanzania': ['mpesa', 'airtel_money', 'tigo_pesa']
        }
        
        self.local_currencies = {
            'kenya': 'KES',
            'ghana': 'GHS',
            'nigeria': 'NGN',
            'uganda': 'UGX',
            'tanzania': 'TZS',
            'south_africa': 'ZAR'
        }
    
    def adapt_payment_methods(self, country: str) -> List[str]:
        """Get available payment methods for country"""
        methods = ['cash', 'bank_transfer']
        
        if country.lower() in self.mobile_money_providers:
            methods.extend(self.mobile_money_providers[country.lower()])
        
        return methods
    
    def get_local_currency(self, country: str) -> str:
        """Get local currency for country"""
        return self.local_currencies.get(country.lower(), 'USD')

class FinancialException(Exception):
    """Custom financial exception"""
    pass

# Example usage and testing
def create_sample_financial_system():
    """Create sample financial system for testing"""
    financial = FinancialManager("tenant_123")
    
    # Create sample transaction
    transaction_data = {
        'transaction_type': 'expense',
        'amount': 150.00,
        'description': 'Office supplies',
        'debit_account_id': list(financial.accounts.values())[4].account_id,  # Operating Expenses
        'credit_account_id': list(financial.accounts.values())[0].account_id,  # Cash
        'created_by': 'admin'
    }
    
    financial.create_transaction(transaction_data)
    
    return financial

# Initialize financial system
financial_system = create_sample_financial_system()

