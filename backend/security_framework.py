#!/usr/bin/env python3
"""
WebWaka Security Framework - Agent 2
Comprehensive security hardening with African compliance and enterprise-grade protection
"""

import os
import json
import logging
import hashlib
import secrets
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import ipaddress
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different data types"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    TOP_SECRET = "top_secret"

class ThreatLevel(Enum):
    """Threat assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityEvent:
    """Security event for audit trail"""
    event_id: str
    event_type: str
    user_id: str
    ip_address: str
    user_agent: str
    timestamp: datetime
    severity: ThreatLevel
    description: str
    metadata: Dict[str, Any]

class EncryptionManager:
    """Advanced encryption manager for data protection"""
    
    def __init__(self, master_key: str = None):
        self.master_key = master_key or os.getenv('WEBWAKA_MASTER_KEY', self._generate_master_key())
        self.fernet = self._create_fernet_instance()
        
    def _generate_master_key(self) -> str:
        """Generate a secure master key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    
    def _create_fernet_instance(self) -> Fernet:
        """Create Fernet encryption instance"""
        try:
            # If master_key is already base64 encoded, use it directly
            return Fernet(self.master_key.encode())
        except:
            # If not, decode it first
            key = base64.urlsafe_b64decode(self.master_key.encode())
            return Fernet(key)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt"""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False

class AuthenticationManager:
    """Advanced authentication with African cultural considerations"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        self.encryption_manager = EncryptionManager()
        self.failed_attempts = {}  # Track failed login attempts
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        
    def generate_jwt_token(self, user_id: str, user_data: Dict[str, Any], 
                          expires_in: timedelta = timedelta(hours=24)) -> str:
        """Generate JWT token with user data"""
        try:
            payload = {
                'user_id': user_id,
                'user_data': user_data,
                'exp': datetime.utcnow() + expires_in,
                'iat': datetime.utcnow(),
                'iss': 'webwaka-dos'
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            logger.info(f"JWT token generated for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"JWT token generation failed: {e}")
            raise
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.error(f"JWT token verification failed: {e}")
            return None
    
    def is_account_locked(self, identifier: str) -> bool:
        """Check if account is locked due to failed attempts"""
        if identifier not in self.failed_attempts:
            return False
        
        attempts_data = self.failed_attempts[identifier]
        if attempts_data['count'] >= self.max_attempts:
            if datetime.now() - attempts_data['last_attempt'] < self.lockout_duration:
                return True
            else:
                # Reset after lockout period
                del self.failed_attempts[identifier]
                return False
        
        return False
    
    def record_failed_attempt(self, identifier: str):
        """Record failed authentication attempt"""
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = {'count': 0, 'last_attempt': datetime.now()}
        
        self.failed_attempts[identifier]['count'] += 1
        self.failed_attempts[identifier]['last_attempt'] = datetime.now()
        
        logger.warning(f"Failed authentication attempt for {identifier} (count: {self.failed_attempts[identifier]['count']})")
    
    def reset_failed_attempts(self, identifier: str):
        """Reset failed attempts after successful authentication"""
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]

class AccessControlManager:
    """Role-based access control with African cultural hierarchy"""
    
    def __init__(self):
        self.roles = {
            'super_admin': {
                'permissions': ['*'],  # All permissions
                'description': 'System administrator with full access'
            },
            'business_owner': {
                'permissions': ['manage_business', 'view_analytics', 'manage_users', 'manage_inventory'],
                'description': 'Business owner with management permissions'
            },
            'manager': {
                'permissions': ['view_analytics', 'manage_inventory', 'manage_staff'],
                'description': 'Manager with operational permissions'
            },
            'staff': {
                'permissions': ['use_pos', 'view_inventory', 'process_orders'],
                'description': 'Staff member with operational permissions'
            },
            'customer': {
                'permissions': ['view_products', 'place_orders', 'view_order_history'],
                'description': 'Customer with basic permissions'
            },
            'elder': {
                'permissions': ['advisory_access', 'cultural_guidance', 'community_oversight'],
                'description': 'Community elder with advisory permissions (Ubuntu philosophy)'
            }
        }
        
        self.cultural_permissions = {
            'ubuntu_consultation': ['elder', 'business_owner'],
            'community_decisions': ['elder', 'business_owner', 'manager'],
            'traditional_practices': ['elder', 'business_owner'],
            'cultural_adaptation': ['elder', 'business_owner', 'manager']
        }
    
    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """Check if user role has required permission"""
        try:
            if user_role not in self.roles:
                logger.warning(f"Unknown role: {user_role}")
                return False
            
            role_permissions = self.roles[user_role]['permissions']
            
            # Super admin has all permissions
            if '*' in role_permissions:
                return True
            
            # Check specific permission
            if required_permission in role_permissions:
                return True
            
            # Check cultural permissions
            if required_permission in self.cultural_permissions:
                return user_role in self.cultural_permissions[required_permission]
            
            return False
            
        except Exception as e:
            logger.error(f"Permission check failed: {e}")
            return False
    
    def get_user_permissions(self, user_role: str) -> List[str]:
        """Get all permissions for a user role"""
        try:
            if user_role not in self.roles:
                return []
            
            permissions = self.roles[user_role]['permissions'].copy()
            
            # Add cultural permissions
            for cultural_perm, allowed_roles in self.cultural_permissions.items():
                if user_role in allowed_roles:
                    permissions.append(cultural_perm)
            
            return permissions
            
        except Exception as e:
            logger.error(f"Failed to get user permissions: {e}")
            return []

class ThreatDetectionSystem:
    """Advanced threat detection with African context awareness"""
    
    def __init__(self):
        self.threat_patterns = {
            'sql_injection': [
                r"(\bUNION\b.*\bSELECT\b)",
                r"(\bDROP\b.*\bTABLE\b)",
                r"(\bINSERT\b.*\bINTO\b.*\bVALUES\b)",
                r"(\bDELETE\b.*\bFROM\b)",
                r"(\bUPDATE\b.*\bSET\b)"
            ],
            'xss_attack': [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>.*?</iframe>"
            ],
            'brute_force': [
                r"(.{1,3})\1{10,}",  # Repeated patterns
                r"^(admin|root|administrator|test|guest)$"  # Common usernames
            ],
            'data_exfiltration': [
                r"(password|secret|key|token|api)",
                r"(credit.*card|bank.*account|financial)",
                r"(personal.*data|private.*info)"
            ]
        }
        
        self.suspicious_ips = set()
        self.rate_limits = {}
        self.max_requests_per_minute = 60
        
    def analyze_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze request for security threats"""
        try:
            threat_assessment = {
                'threat_level': ThreatLevel.LOW,
                'threats_detected': [],
                'risk_score': 0.0,
                'recommendations': []
            }
            
            # Analyze request content
            content = str(request_data.get('content', ''))
            
            # Check for SQL injection
            for pattern in self.threat_patterns['sql_injection']:
                if re.search(pattern, content, re.IGNORECASE):
                    threat_assessment['threats_detected'].append('sql_injection')
                    threat_assessment['risk_score'] += 0.8
            
            # Check for XSS attacks
            for pattern in self.threat_patterns['xss_attack']:
                if re.search(pattern, content, re.IGNORECASE):
                    threat_assessment['threats_detected'].append('xss_attack')
                    threat_assessment['risk_score'] += 0.7
            
            # Check for data exfiltration attempts
            for pattern in self.threat_patterns['data_exfiltration']:
                if re.search(pattern, content, re.IGNORECASE):
                    threat_assessment['threats_detected'].append('data_exfiltration')
                    threat_assessment['risk_score'] += 0.6
            
            # Rate limiting check
            ip_address = request_data.get('ip_address', 'unknown')
            if self._check_rate_limit(ip_address):
                threat_assessment['threats_detected'].append('rate_limit_exceeded')
                threat_assessment['risk_score'] += 0.5
            
            # Determine overall threat level
            if threat_assessment['risk_score'] >= 1.5:
                threat_assessment['threat_level'] = ThreatLevel.CRITICAL
            elif threat_assessment['risk_score'] >= 1.0:
                threat_assessment['threat_level'] = ThreatLevel.HIGH
            elif threat_assessment['risk_score'] >= 0.5:
                threat_assessment['threat_level'] = ThreatLevel.MEDIUM
            
            # Generate recommendations
            if threat_assessment['threats_detected']:
                threat_assessment['recommendations'] = self._generate_recommendations(threat_assessment['threats_detected'])
            
            return threat_assessment
            
        except Exception as e:
            logger.error(f"Threat analysis failed: {e}")
            return {
                'threat_level': ThreatLevel.HIGH,
                'threats_detected': ['analysis_error'],
                'risk_score': 1.0,
                'error': str(e)
            }
    
    def _check_rate_limit(self, ip_address: str) -> bool:
        """Check if IP address exceeds rate limit"""
        try:
            current_time = datetime.now()
            minute_key = current_time.strftime("%Y-%m-%d %H:%M")
            rate_key = f"{ip_address}:{minute_key}"
            
            if rate_key not in self.rate_limits:
                self.rate_limits[rate_key] = 0
            
            self.rate_limits[rate_key] += 1
            
            # Clean old entries
            self._cleanup_rate_limits()
            
            return self.rate_limits[rate_key] > self.max_requests_per_minute
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return False
    
    def _cleanup_rate_limits(self):
        """Clean up old rate limit entries"""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(minutes=5)
            
            keys_to_remove = []
            for key in self.rate_limits:
                try:
                    time_part = key.split(':', 1)[1]
                    entry_time = datetime.strptime(time_part, "%Y-%m-%d %H:%M")
                    if entry_time < cutoff_time:
                        keys_to_remove.append(key)
                except:
                    keys_to_remove.append(key)  # Remove malformed keys
            
            for key in keys_to_remove:
                del self.rate_limits[key]
                
        except Exception as e:
            logger.error(f"Rate limit cleanup failed: {e}")
    
    def _generate_recommendations(self, threats: List[str]) -> List[str]:
        """Generate security recommendations based on detected threats"""
        recommendations = []
        
        if 'sql_injection' in threats:
            recommendations.append("Implement parameterized queries and input validation")
        
        if 'xss_attack' in threats:
            recommendations.append("Sanitize user input and implement Content Security Policy")
        
        if 'data_exfiltration' in threats:
            recommendations.append("Review data access patterns and implement data loss prevention")
        
        if 'rate_limit_exceeded' in threats:
            recommendations.append("Implement CAPTCHA or temporary IP blocking")
        
        return recommendations

class ComplianceManager:
    """African data protection and compliance manager"""
    
    def __init__(self):
        self.compliance_frameworks = {
            'gdpr': {
                'name': 'General Data Protection Regulation',
                'applicable_regions': ['all'],
                'requirements': [
                    'data_minimization',
                    'consent_management',
                    'right_to_erasure',
                    'data_portability',
                    'privacy_by_design'
                ]
            },
            'popia': {
                'name': 'Protection of Personal Information Act (South Africa)',
                'applicable_regions': ['southern_africa'],
                'requirements': [
                    'lawful_processing',
                    'data_subject_rights',
                    'security_safeguards',
                    'cross_border_transfers'
                ]
            },
            'ndpr': {
                'name': 'Nigeria Data Protection Regulation',
                'applicable_regions': ['west_africa'],
                'requirements': [
                    'consent_requirements',
                    'data_breach_notification',
                    'privacy_impact_assessment',
                    'data_protection_officer'
                ]
            },
            'african_union': {
                'name': 'African Union Convention on Cyber Security',
                'applicable_regions': ['all'],
                'requirements': [
                    'cybersecurity_measures',
                    'data_localization',
                    'cross_border_cooperation',
                    'capacity_building'
                ]
            }
        }
        
        self.cultural_considerations = {
            'ubuntu_philosophy': {
                'principles': ['community_consent', 'collective_responsibility', 'shared_benefits'],
                'implementation': 'Community-based data governance with elder consultation'
            },
            'traditional_authority': {
                'principles': ['hierarchical_approval', 'elder_wisdom', 'community_validation'],
                'implementation': 'Traditional authority integration in data decisions'
            },
            'communal_ownership': {
                'principles': ['shared_resources', 'collective_benefit', 'community_control'],
                'implementation': 'Community ownership models for data and benefits'
            }
        }
    
    def check_compliance(self, data_operation: Dict[str, Any], region: str) -> Dict[str, Any]:
        """Check compliance with applicable frameworks"""
        try:
            compliance_status = {
                'compliant': True,
                'applicable_frameworks': [],
                'requirements_met': [],
                'requirements_missing': [],
                'cultural_considerations': [],
                'recommendations': []
            }
            
            # Check applicable frameworks
            for framework_id, framework in self.compliance_frameworks.items():
                if region in framework['applicable_regions'] or 'all' in framework['applicable_regions']:
                    compliance_status['applicable_frameworks'].append(framework_id)
                    
                    # Check requirements (simplified for demo)
                    for requirement in framework['requirements']:
                        if self._check_requirement(data_operation, requirement):
                            compliance_status['requirements_met'].append(f"{framework_id}:{requirement}")
                        else:
                            compliance_status['requirements_missing'].append(f"{framework_id}:{requirement}")
                            compliance_status['compliant'] = False
            
            # Check cultural considerations
            for cultural_aspect, details in self.cultural_considerations.items():
                if self._check_cultural_compliance(data_operation, cultural_aspect):
                    compliance_status['cultural_considerations'].append(cultural_aspect)
            
            # Generate recommendations
            if compliance_status['requirements_missing']:
                compliance_status['recommendations'] = self._generate_compliance_recommendations(
                    compliance_status['requirements_missing']
                )
            
            return compliance_status
            
        except Exception as e:
            logger.error(f"Compliance check failed: {e}")
            return {
                'compliant': False,
                'error': str(e),
                'recommendations': ['Review compliance framework implementation']
            }
    
    def _check_requirement(self, operation: Dict[str, Any], requirement: str) -> bool:
        """Check if specific compliance requirement is met"""
        # Simplified compliance checking (would be more comprehensive in production)
        requirement_checks = {
            'data_minimization': lambda op: op.get('data_scope') == 'minimal',
            'consent_management': lambda op: op.get('consent_obtained', False),
            'right_to_erasure': lambda op: op.get('deletion_capability', False),
            'data_portability': lambda op: op.get('export_capability', False),
            'privacy_by_design': lambda op: op.get('privacy_built_in', False),
            'lawful_processing': lambda op: op.get('legal_basis') is not None,
            'security_safeguards': lambda op: op.get('encryption_enabled', False),
            'data_breach_notification': lambda op: op.get('breach_notification_system', False)
        }
        
        check_function = requirement_checks.get(requirement, lambda op: True)
        return check_function(operation)
    
    def _check_cultural_compliance(self, operation: Dict[str, Any], cultural_aspect: str) -> bool:
        """Check cultural compliance aspects"""
        cultural_checks = {
            'ubuntu_philosophy': lambda op: op.get('community_benefit', False),
            'traditional_authority': lambda op: op.get('elder_approval', False),
            'communal_ownership': lambda op: op.get('shared_ownership', False)
        }
        
        check_function = cultural_checks.get(cultural_aspect, lambda op: False)
        return check_function(operation)
    
    def _generate_compliance_recommendations(self, missing_requirements: List[str]) -> List[str]:
        """Generate recommendations for missing compliance requirements"""
        recommendations = []
        
        for requirement in missing_requirements:
            if 'consent' in requirement:
                recommendations.append("Implement comprehensive consent management system")
            elif 'encryption' in requirement or 'security' in requirement:
                recommendations.append("Enable end-to-end encryption for all data")
            elif 'erasure' in requirement or 'deletion' in requirement:
                recommendations.append("Implement data deletion and right to be forgotten")
            elif 'cultural' in requirement:
                recommendations.append("Integrate traditional authority consultation process")
        
        return list(set(recommendations))  # Remove duplicates

class SecurityFramework:
    """Comprehensive security framework orchestrator"""
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.auth_manager = AuthenticationManager()
        self.access_control = AccessControlManager()
        self.threat_detection = ThreatDetectionSystem()
        self.compliance_manager = ComplianceManager()
        
        self.security_events = []
        self.max_events = 10000
        
    async def secure_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive request security processing"""
        try:
            security_result = {
                'allowed': True,
                'security_level': SecurityLevel.PUBLIC,
                'threat_assessment': {},
                'compliance_status': {},
                'security_headers': {},
                'audit_trail': []
            }
            
            # Threat detection
            threat_assessment = self.threat_detection.analyze_request(request_data)
            security_result['threat_assessment'] = threat_assessment
            
            # Block high-risk requests
            if threat_assessment['threat_level'] in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                security_result['allowed'] = False
                security_result['reason'] = 'High threat level detected'
                
                # Log security event
                await self._log_security_event(
                    event_type='threat_blocked',
                    user_id=request_data.get('user_id', 'anonymous'),
                    ip_address=request_data.get('ip_address', 'unknown'),
                    severity=threat_assessment['threat_level'],
                    description=f"Blocked request due to threats: {threat_assessment['threats_detected']}"
                )
            
            # Compliance check
            region = request_data.get('region', 'west_africa')
            compliance_status = self.compliance_manager.check_compliance(request_data, region)
            security_result['compliance_status'] = compliance_status
            
            # Generate security headers
            security_result['security_headers'] = self._generate_security_headers()
            
            return security_result
            
        except Exception as e:
            logger.error(f"Security processing failed: {e}")
            return {
                'allowed': False,
                'error': str(e),
                'security_level': SecurityLevel.RESTRICTED
            }
    
    async def _log_security_event(self, event_type: str, user_id: str, ip_address: str,
                                 severity: ThreatLevel, description: str, 
                                 metadata: Dict[str, Any] = None):
        """Log security event for audit trail"""
        try:
            event = SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=metadata.get('user_agent', 'unknown') if metadata else 'unknown',
                timestamp=datetime.now(),
                severity=severity,
                description=description,
                metadata=metadata or {}
            )
            
            self.security_events.append(event)
            
            # Rotate events if too many
            if len(self.security_events) > self.max_events:
                self.security_events = self.security_events[-self.max_events:]
            
            logger.info(f"Security event logged: {event_type} - {severity.value}")
            
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
    
    def _generate_security_headers(self) -> Dict[str, str]:
        """Generate security headers for responses"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }
    
    async def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status"""
        try:
            status = {
                'overall_status': 'secure',
                'encryption': {
                    'status': 'active',
                    'algorithm': 'Fernet (AES 128)',
                    'key_rotation': 'manual'
                },
                'authentication': {
                    'status': 'active',
                    'method': 'JWT + bcrypt',
                    'session_timeout': '24 hours'
                },
                'threat_detection': {
                    'status': 'active',
                    'patterns_loaded': len(self.threat_detection.threat_patterns),
                    'events_logged': len(self.security_events)
                },
                'compliance': {
                    'frameworks': list(self.compliance_manager.compliance_frameworks.keys()),
                    'cultural_integration': list(self.compliance_manager.cultural_considerations.keys())
                },
                'recent_events': [
                    {
                        'type': event.event_type,
                        'severity': event.severity.value,
                        'timestamp': event.timestamp.isoformat()
                    }
                    for event in self.security_events[-10:]  # Last 10 events
                ]
            }
            
            # Assess overall security health
            critical_events = [e for e in self.security_events[-100:] if e.severity == ThreatLevel.CRITICAL]
            if len(critical_events) > 5:
                status['overall_status'] = 'at_risk'
            elif len(critical_events) > 0:
                status['overall_status'] = 'monitoring'
            
            return status
            
        except Exception as e:
            logger.error(f"Security status check failed: {e}")
            return {
                'overall_status': 'error',
                'error': str(e)
            }

# Global security framework instance
security_framework = SecurityFramework()

# Utility functions
async def initialize_security() -> bool:
    """Initialize security framework"""
    try:
        logger.info("Security framework initialized")
        return True
    except Exception as e:
        logger.error(f"Security initialization failed: {e}")
        return False

async def secure_data(data: str, security_level: SecurityLevel = SecurityLevel.CONFIDENTIAL) -> str:
    """Encrypt data based on security level"""
    if security_level in [SecurityLevel.CONFIDENTIAL, SecurityLevel.RESTRICTED, SecurityLevel.TOP_SECRET]:
        return security_framework.encryption_manager.encrypt_data(data)
    return data

async def authenticate_user(token: str) -> Optional[Dict[str, Any]]:
    """Authenticate user with JWT token"""
    return security_framework.auth_manager.verify_jwt_token(token)

async def check_user_permission(user_role: str, permission: str) -> bool:
    """Check if user has required permission"""
    return security_framework.access_control.check_permission(user_role, permission)

async def analyze_security_threat(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze request for security threats"""
    return security_framework.threat_detection.analyze_request(request_data)

async def validate_compliance(operation: Dict[str, Any], region: str) -> Dict[str, Any]:
    """Validate operation compliance"""
    return security_framework.compliance_manager.check_compliance(operation, region)

async def get_security_health() -> Dict[str, Any]:
    """Get security framework health status"""
    return await security_framework.get_security_status()

# Export main components
__all__ = [
    'SecurityFramework', 'EncryptionManager', 'AuthenticationManager', 
    'AccessControlManager', 'ThreatDetectionSystem', 'ComplianceManager',
    'SecurityLevel', 'ThreatLevel', 'SecurityEvent',
    'security_framework', 'initialize_security', 'secure_data',
    'authenticate_user', 'check_user_permission', 'analyze_security_threat',
    'validate_compliance', 'get_security_health'
]

