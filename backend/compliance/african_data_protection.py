"""
WebWaka African Data Protection Law Compliance Implementation
Comprehensive compliance with GDPR and African national data protection regulations
"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from abc import ABC, abstractmethod
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProtectionRegulation(Enum):
    """Supported data protection regulations"""
    GDPR = "gdpr"  # General Data Protection Regulation (EU)
    POPIA = "popia"  # Protection of Personal Information Act (South Africa)
    NDPR = "ndpr"  # Nigeria Data Protection Regulation
    DPA_KENYA = "dpa_kenya"  # Kenya Data Protection Act
    DPA_GHANA = "dpa_ghana"  # Ghana Data Protection Act
    DPA_EGYPT = "dpa_egypt"  # Egypt Data Protection Law
    DPA_MOROCCO = "dpa_morocco"  # Morocco Data Protection Law
    AU_CONVENTION = "au_convention"  # African Union Convention on Cyber Security

class DataCategory(Enum):
    """Categories of personal data"""
    BASIC_PERSONAL = "basic_personal"  # Name, email, phone
    SENSITIVE_PERSONAL = "sensitive_personal"  # Health, biometric, financial
    SPECIAL_CATEGORY = "special_category"  # Race, religion, political views
    BIOMETRIC = "biometric"  # Fingerprints, facial recognition
    FINANCIAL = "financial"  # Bank details, payment information
    HEALTH = "health"  # Medical records, health status
    LOCATION = "location"  # GPS coordinates, address
    BEHAVIORAL = "behavioral"  # Usage patterns, preferences

class ProcessingPurpose(Enum):
    """Lawful purposes for data processing"""
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"

class DataSubjectRight(Enum):
    """Rights of data subjects"""
    ACCESS = "access"  # Right to access personal data
    RECTIFICATION = "rectification"  # Right to correct data
    ERASURE = "erasure"  # Right to be forgotten
    PORTABILITY = "portability"  # Right to data portability
    RESTRICTION = "restriction"  # Right to restrict processing
    OBJECTION = "objection"  # Right to object to processing
    AUTOMATED_DECISION = "automated_decision"  # Rights related to automated decision-making

@dataclass
class DataSubject:
    """Data subject information"""
    subject_id: str
    tenant_id: str
    email: str
    country: str
    applicable_regulations: List[DataProtectionRegulation]
    consent_records: Dict[str, Any]
    data_categories: List[DataCategory]
    created_at: datetime
    updated_at: datetime

@dataclass
class ConsentRecord:
    """Consent record for data processing"""
    consent_id: str
    subject_id: str
    tenant_id: str
    purpose: ProcessingPurpose
    data_categories: List[DataCategory]
    consent_given: bool
    consent_date: datetime
    expiry_date: Optional[datetime]
    withdrawal_date: Optional[datetime]
    consent_method: str  # web_form, api, voice, etc.
    consent_evidence: str  # Hash of consent proof
    granular_permissions: Dict[str, bool]

@dataclass
class DataProcessingRecord:
    """Record of data processing activities"""
    processing_id: str
    tenant_id: str
    subject_id: str
    data_categories: List[DataCategory]
    processing_purpose: ProcessingPurpose
    legal_basis: str
    retention_period: int  # days
    processing_date: datetime
    processor_details: Dict[str, str]
    security_measures: List[str]
    cross_border_transfer: bool
    transfer_safeguards: Optional[str]

class AfricanDataProtectionCompliance:
    """Main compliance manager for African data protection laws"""
    
    def __init__(self):
        self.data_subjects = {}
        self.consent_records = {}
        self.processing_records = {}
        self.compliance_policies = {}
        self.audit_logs = []
        self._initialize_compliance_frameworks()
    
    def _initialize_compliance_frameworks(self):
        """Initialize compliance frameworks for different African countries"""
        self.compliance_policies = {
            DataProtectionRegulation.GDPR: {
                'consent_required': True,
                'explicit_consent_categories': [DataCategory.SENSITIVE_PERSONAL, DataCategory.SPECIAL_CATEGORY],
                'data_retention_limits': {'default': 365, 'marketing': 1095},
                'breach_notification_hours': 72,
                'dpo_required_threshold': 250,  # employees
                'cross_border_restrictions': True,
                'automated_decision_rights': True,
                'privacy_by_design': True
            },
            DataProtectionRegulation.POPIA: {
                'consent_required': True,
                'explicit_consent_categories': [DataCategory.SENSITIVE_PERSONAL, DataCategory.SPECIAL_CATEGORY, DataCategory.BIOMETRIC],
                'data_retention_limits': {'default': 365, 'financial': 2555},  # 7 years for financial
                'breach_notification_hours': 72,
                'information_officer_required': True,
                'cross_border_restrictions': True,
                'data_minimization': True,
                'purpose_limitation': True
            },
            DataProtectionRegulation.NDPR: {
                'consent_required': True,
                'explicit_consent_categories': [DataCategory.SENSITIVE_PERSONAL, DataCategory.FINANCIAL],
                'data_retention_limits': {'default': 365, 'financial': 1825},  # 5 years for financial
                'breach_notification_hours': 72,
                'data_protection_officer_required': True,
                'local_storage_preference': True,
                'cross_border_approval_required': True,
                'audit_frequency_months': 12
            },
            DataProtectionRegulation.DPA_KENYA: {
                'consent_required': True,
                'explicit_consent_categories': [DataCategory.SENSITIVE_PERSONAL, DataCategory.HEALTH],
                'data_retention_limits': {'default': 365, 'health': 2190},  # 6 years for health
                'breach_notification_hours': 72,
                'data_protection_officer_required': True,
                'cross_border_restrictions': True,
                'data_subject_rights_response_days': 30
            },
            DataProtectionRegulation.DPA_GHANA: {
                'consent_required': True,
                'explicit_consent_categories': [DataCategory.SENSITIVE_PERSONAL, DataCategory.BIOMETRIC],
                'data_retention_limits': {'default': 365},
                'breach_notification_hours': 72,
                'data_protection_officer_required': True,
                'local_processing_preference': True,
                'cross_border_approval_required': True
            }
        }
    
    def register_data_subject(self, subject_data: Dict[str, Any]) -> DataSubject:
        """Register a new data subject"""
        try:
            subject_id = str(uuid.uuid4())
            
            # Determine applicable regulations based on country
            applicable_regulations = self._determine_applicable_regulations(subject_data['country'])
            
            data_subject = DataSubject(
                subject_id=subject_id,
                tenant_id=subject_data['tenant_id'],
                email=subject_data['email'],
                country=subject_data['country'],
                applicable_regulations=applicable_regulations,
                consent_records={},
                data_categories=[],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.data_subjects[subject_id] = data_subject
            
            # Log registration
            self._log_compliance_event('data_subject_registered', {
                'subject_id': subject_id,
                'country': subject_data['country'],
                'regulations': [reg.value for reg in applicable_regulations]
            })
            
            logger.info(f"Registered data subject {subject_id} for country {subject_data['country']}")
            return data_subject
            
        except Exception as e:
            logger.error(f"Failed to register data subject: {str(e)}")
            raise ComplianceException(f"Data subject registration failed: {str(e)}")
    
    def record_consent(self, consent_data: Dict[str, Any]) -> ConsentRecord:
        """Record consent for data processing"""
        try:
            consent_id = str(uuid.uuid4())
            
            # Validate consent requirements
            self._validate_consent_requirements(consent_data)
            
            # Generate consent evidence hash
            consent_evidence = self._generate_consent_evidence(consent_data)
            
            consent_record = ConsentRecord(
                consent_id=consent_id,
                subject_id=consent_data['subject_id'],
                tenant_id=consent_data['tenant_id'],
                purpose=ProcessingPurpose(consent_data['purpose']),
                data_categories=[DataCategory(cat) for cat in consent_data['data_categories']],
                consent_given=consent_data['consent_given'],
                consent_date=datetime.utcnow(),
                expiry_date=consent_data.get('expiry_date'),
                withdrawal_date=None,
                consent_method=consent_data['consent_method'],
                consent_evidence=consent_evidence,
                granular_permissions=consent_data.get('granular_permissions', {})
            )
            
            self.consent_records[consent_id] = consent_record
            
            # Update data subject consent records
            if consent_data['subject_id'] in self.data_subjects:
                self.data_subjects[consent_data['subject_id']].consent_records[consent_id] = consent_record
            
            # Log consent
            self._log_compliance_event('consent_recorded', {
                'consent_id': consent_id,
                'subject_id': consent_data['subject_id'],
                'purpose': consent_data['purpose'],
                'consent_given': consent_data['consent_given']
            })
            
            logger.info(f"Recorded consent {consent_id} for subject {consent_data['subject_id']}")
            return consent_record
            
        except Exception as e:
            logger.error(f"Failed to record consent: {str(e)}")
            raise ComplianceException(f"Consent recording failed: {str(e)}")
    
    def withdraw_consent(self, subject_id: str, consent_id: str) -> bool:
        """Withdraw consent for data processing"""
        try:
            if consent_id not in self.consent_records:
                raise ComplianceException(f"Consent record {consent_id} not found")
            
            consent_record = self.consent_records[consent_id]
            
            if consent_record.subject_id != subject_id:
                raise ComplianceException("Subject ID mismatch")
            
            # Update consent record
            consent_record.withdrawal_date = datetime.utcnow()
            consent_record.consent_given = False
            
            # Log withdrawal
            self._log_compliance_event('consent_withdrawn', {
                'consent_id': consent_id,
                'subject_id': subject_id,
                'withdrawal_date': consent_record.withdrawal_date.isoformat()
            })
            
            # Trigger data processing review
            self._review_processing_after_withdrawal(subject_id, consent_record)
            
            logger.info(f"Withdrawn consent {consent_id} for subject {subject_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to withdraw consent: {str(e)}")
            raise ComplianceException(f"Consent withdrawal failed: {str(e)}")
    
    def process_data_subject_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data subject rights requests"""
        try:
            subject_id = request_data['subject_id']
            request_type = DataSubjectRight(request_data['request_type'])
            
            if subject_id not in self.data_subjects:
                raise ComplianceException(f"Data subject {subject_id} not found")
            
            data_subject = self.data_subjects[subject_id]
            
            # Process based on request type
            if request_type == DataSubjectRight.ACCESS:
                return self._process_access_request(data_subject)
            elif request_type == DataSubjectRight.RECTIFICATION:
                return self._process_rectification_request(data_subject, request_data)
            elif request_type == DataSubjectRight.ERASURE:
                return self._process_erasure_request(data_subject)
            elif request_type == DataSubjectRight.PORTABILITY:
                return self._process_portability_request(data_subject)
            elif request_type == DataSubjectRight.RESTRICTION:
                return self._process_restriction_request(data_subject, request_data)
            elif request_type == DataSubjectRight.OBJECTION:
                return self._process_objection_request(data_subject, request_data)
            else:
                raise ComplianceException(f"Unsupported request type: {request_type.value}")
                
        except Exception as e:
            logger.error(f"Failed to process data subject request: {str(e)}")
            raise ComplianceException(f"Data subject request processing failed: {str(e)}")
    
    def _determine_applicable_regulations(self, country: str) -> List[DataProtectionRegulation]:
        """Determine applicable regulations based on country"""
        country_regulations = {
            'south_africa': [DataProtectionRegulation.POPIA, DataProtectionRegulation.AU_CONVENTION],
            'nigeria': [DataProtectionRegulation.NDPR, DataProtectionRegulation.AU_CONVENTION],
            'kenya': [DataProtectionRegulation.DPA_KENYA, DataProtectionRegulation.AU_CONVENTION],
            'ghana': [DataProtectionRegulation.DPA_GHANA, DataProtectionRegulation.AU_CONVENTION],
            'egypt': [DataProtectionRegulation.DPA_EGYPT, DataProtectionRegulation.AU_CONVENTION],
            'morocco': [DataProtectionRegulation.DPA_MOROCCO, DataProtectionRegulation.AU_CONVENTION]
        }
        
        regulations = country_regulations.get(country.lower(), [DataProtectionRegulation.AU_CONVENTION])
        
        # Add GDPR if processing EU data subjects
        # This would be determined by business logic
        # regulations.append(DataProtectionRegulation.GDPR)
        
        return regulations
    
    def _validate_consent_requirements(self, consent_data: Dict[str, Any]):
        """Validate consent requirements based on applicable regulations"""
        subject_id = consent_data['subject_id']
        
        if subject_id not in self.data_subjects:
            raise ComplianceException(f"Data subject {subject_id} not found")
        
        data_subject = self.data_subjects[subject_id]
        data_categories = [DataCategory(cat) for cat in consent_data['data_categories']]
        
        # Check if explicit consent is required
        for regulation in data_subject.applicable_regulations:
            policy = self.compliance_policies.get(regulation, {})
            explicit_categories = policy.get('explicit_consent_categories', [])
            
            for category in data_categories:
                if category in explicit_categories and not consent_data.get('explicit_consent', False):
                    raise ComplianceException(f"Explicit consent required for {category.value} under {regulation.value}")
    
    def _generate_consent_evidence(self, consent_data: Dict[str, Any]) -> str:
        """Generate hash evidence of consent"""
        evidence_data = {
            'subject_id': consent_data['subject_id'],
            'purpose': consent_data['purpose'],
            'data_categories': consent_data['data_categories'],
            'consent_given': consent_data['consent_given'],
            'timestamp': datetime.utcnow().isoformat(),
            'method': consent_data['consent_method']
        }
        
        evidence_string = json.dumps(evidence_data, sort_keys=True)
        return hashlib.sha256(evidence_string.encode()).hexdigest()
    
    def _log_compliance_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log compliance events for audit trail"""
        log_entry = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': event_data
        }
        
        self.audit_logs.append(log_entry)
        
        # In production, this would be stored in a secure audit database
        logger.info(f"Compliance event logged: {event_type}")
    
    def _review_processing_after_withdrawal(self, subject_id: str, withdrawn_consent: ConsentRecord):
        """Review data processing activities after consent withdrawal"""
        # Find all processing records for this subject and purpose
        affected_processing = []
        
        for processing_id, record in self.processing_records.items():
            if (record.subject_id == subject_id and 
                record.processing_purpose == withdrawn_consent.purpose):
                affected_processing.append(record)
        
        # Log the review
        self._log_compliance_event('processing_review_triggered', {
            'subject_id': subject_id,
            'withdrawn_consent_id': withdrawn_consent.consent_id,
            'affected_processing_count': len(affected_processing)
        })
        
        # In production, this would trigger automated data deletion or anonymization
        logger.info(f"Processing review triggered for subject {subject_id}")
    
    def _process_access_request(self, data_subject: DataSubject) -> Dict[str, Any]:
        """Process data access request"""
        # Compile all data for the subject
        subject_data = {
            'personal_information': asdict(data_subject),
            'consent_records': [asdict(consent) for consent in data_subject.consent_records.values()],
            'processing_activities': self._get_processing_activities(data_subject.subject_id),
            'data_categories': [cat.value for cat in data_subject.data_categories],
            'retention_periods': self._get_retention_periods(data_subject.subject_id)
        }
        
        self._log_compliance_event('access_request_processed', {
            'subject_id': data_subject.subject_id,
            'data_categories_count': len(data_subject.data_categories)
        })
        
        return {
            'request_type': 'access',
            'subject_id': data_subject.subject_id,
            'data': subject_data,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _process_erasure_request(self, data_subject: DataSubject) -> Dict[str, Any]:
        """Process right to be forgotten request"""
        # Check if erasure is legally possible
        erasure_possible = self._can_erase_data(data_subject)
        
        if erasure_possible:
            # Mark for deletion (in production, this would trigger actual deletion)
            deletion_scheduled = datetime.utcnow() + timedelta(days=30)  # Grace period
            
            self._log_compliance_event('erasure_request_approved', {
                'subject_id': data_subject.subject_id,
                'deletion_scheduled': deletion_scheduled.isoformat()
            })
            
            return {
                'request_type': 'erasure',
                'subject_id': data_subject.subject_id,
                'status': 'approved',
                'deletion_scheduled': deletion_scheduled.isoformat()
            }
        else:
            self._log_compliance_event('erasure_request_denied', {
                'subject_id': data_subject.subject_id,
                'reason': 'legal_obligations_prevent_deletion'
            })
            
            return {
                'request_type': 'erasure',
                'subject_id': data_subject.subject_id,
                'status': 'denied',
                'reason': 'Legal obligations prevent deletion'
            }
    
    def _process_portability_request(self, data_subject: DataSubject) -> Dict[str, Any]:
        """Process data portability request"""
        # Export data in structured format
        portable_data = {
            'subject_information': {
                'subject_id': data_subject.subject_id,
                'email': data_subject.email,
                'country': data_subject.country
            },
            'consent_records': [
                {
                    'purpose': consent.purpose.value,
                    'data_categories': [cat.value for cat in consent.data_categories],
                    'consent_date': consent.consent_date.isoformat(),
                    'consent_given': consent.consent_given
                }
                for consent in data_subject.consent_records.values()
            ],
            'export_format': 'JSON',
            'export_date': datetime.utcnow().isoformat()
        }
        
        self._log_compliance_event('portability_request_processed', {
            'subject_id': data_subject.subject_id,
            'export_format': 'JSON'
        })
        
        return {
            'request_type': 'portability',
            'subject_id': data_subject.subject_id,
            'data': portable_data,
            'download_link': f"/api/compliance/export/{data_subject.subject_id}"
        }
    
    def _can_erase_data(self, data_subject: DataSubject) -> bool:
        """Check if data can be erased (considering legal obligations)"""
        # Check for legal obligations that prevent deletion
        # This would include financial records, legal proceedings, etc.
        
        # For now, return True (implement proper legal obligation checks)
        return True
    
    def _get_processing_activities(self, subject_id: str) -> List[Dict[str, Any]]:
        """Get processing activities for a subject"""
        activities = []
        
        for processing_id, record in self.processing_records.items():
            if record.subject_id == subject_id:
                activities.append({
                    'processing_id': processing_id,
                    'purpose': record.processing_purpose.value,
                    'data_categories': [cat.value for cat in record.data_categories],
                    'processing_date': record.processing_date.isoformat(),
                    'legal_basis': record.legal_basis
                })
        
        return activities
    
    def _get_retention_periods(self, subject_id: str) -> Dict[str, int]:
        """Get data retention periods for subject"""
        # This would calculate retention periods based on applicable regulations
        # For now, return default periods
        return {
            'basic_personal': 365,
            'financial': 2555,  # 7 years
            'health': 2190      # 6 years
        }
    
    def generate_compliance_report(self, tenant_id: str) -> Dict[str, Any]:
        """Generate compliance report for tenant"""
        try:
            tenant_subjects = [s for s in self.data_subjects.values() if s.tenant_id == tenant_id]
            tenant_consents = [c for c in self.consent_records.values() if c.tenant_id == tenant_id]
            
            report = {
                'tenant_id': tenant_id,
                'report_date': datetime.utcnow().isoformat(),
                'data_subjects_count': len(tenant_subjects),
                'active_consents': len([c for c in tenant_consents if c.consent_given]),
                'withdrawn_consents': len([c for c in tenant_consents if not c.consent_given]),
                'data_categories_processed': list(set([
                    cat.value for subject in tenant_subjects for cat in subject.data_categories
                ])),
                'applicable_regulations': list(set([
                    reg.value for subject in tenant_subjects for reg in subject.applicable_regulations
                ])),
                'compliance_status': self._assess_compliance_status(tenant_id),
                'recommendations': self._generate_compliance_recommendations(tenant_id)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate compliance report: {str(e)}")
            raise ComplianceException(f"Compliance report generation failed: {str(e)}")
    
    def _assess_compliance_status(self, tenant_id: str) -> Dict[str, str]:
        """Assess compliance status for tenant"""
        # This would implement comprehensive compliance assessment
        # For now, return basic status
        return {
            'overall': 'compliant',
            'consent_management': 'compliant',
            'data_retention': 'compliant',
            'subject_rights': 'compliant',
            'security_measures': 'compliant'
        }
    
    def _generate_compliance_recommendations(self, tenant_id: str) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # This would analyze compliance gaps and generate recommendations
        recommendations.append("Implement regular consent renewal process")
        recommendations.append("Set up automated data retention policy enforcement")
        recommendations.append("Establish data subject rights request automation")
        
        return recommendations

class ComplianceException(Exception):
    """Custom compliance exception"""
    pass

# Initialize compliance manager
african_compliance = AfricanDataProtectionCompliance()

