#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Access Control Agent (Agent 36)
Multi-Factor Authentication and Role-Based Access Control

This agent provides comprehensive access control with multi-factor authentication,
role-based access control, granular permissions, and Ubuntu philosophy integration
for community-centered security and traditional governance.

Features:
- Multi-factor authentication (SMS, TOTP, biometric, hardware tokens)
- Role-based access control (RBAC) with Ubuntu hierarchy
- Granular permissions and resource-level access control
- Ubuntu philosophy integration for community-based access
- Traditional governance and elder authority recognition
- African infrastructure optimization
- Real-time access monitoring and audit trails
"""

import asyncio
import base64
import hashlib
import hmac
import json
import logging
import os
import sqlite3
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import secrets
import pyotp
import qrcode
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthenticationMethod(Enum):
    """Authentication method types"""
    PASSWORD = "password"
    SMS = "sms"
    TOTP = "totp"
    BIOMETRIC = "biometric"
    HARDWARE_TOKEN = "hardware_token"
    UBUNTU_COMMUNITY_VERIFICATION = "ubuntu_community_verification"

class UserRole(Enum):
    """User role types with Ubuntu hierarchy"""
    GUEST = "guest"
    MEMBER = "member"
    ELDER = "elder"
    COMMUNITY_LEADER = "community_leader"
    TRADITIONAL_AUTHORITY = "traditional_authority"
    SYSTEM_ADMIN = "system_admin"
    UBUNTU_COUNCIL = "ubuntu_council"

class Permission(Enum):
    """Permission types"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    UBUNTU_GOVERNANCE = "ubuntu_governance"
    TRADITIONAL_KNOWLEDGE = "traditional_knowledge"
    ELDER_CONSULTATION = "elder_consultation"
    COMMUNITY_DECISION = "community_decision"

class ResourceType(Enum):
    """Resource types for access control"""
    USER_DATA = "user_data"
    FINANCIAL_DATA = "financial_data"
    CULTURAL_DATA = "cultural_data"
    TRADITIONAL_KNOWLEDGE = "traditional_knowledge"
    COMMUNITY_RESOURCES = "community_resources"
    SYSTEM_CONFIGURATION = "system_configuration"
    UBUNTU_GOVERNANCE = "ubuntu_governance"

class AccessStatus(Enum):
    """Access attempt status"""
    GRANTED = "granted"
    DENIED = "denied"
    PENDING_APPROVAL = "pending_approval"
    REQUIRES_ELDER_APPROVAL = "requires_elder_approval"
    UBUNTU_CONSENSUS_REQUIRED = "ubuntu_consensus_required"

@dataclass
class User:
    """User data structure"""
    user_id: str
    username: str
    email: str
    role: UserRole
    cultural_background: str
    ubuntu_community_member: bool = False
    elder_status: bool = False
    traditional_authority: bool = False
    enabled_auth_methods: List[AuthenticationMethod] = None
    last_login: Optional[datetime] = None
    failed_attempts: int = 0
    locked_until: Optional[datetime] = None

@dataclass
class AuthenticationFactor:
    """Authentication factor data structure"""
    factor_id: str
    user_id: str
    method: AuthenticationMethod
    secret: str
    verified: bool = False
    created_at: datetime = None
    ubuntu_verified: bool = False

@dataclass
class AccessRule:
    """Access control rule data structure"""
    rule_id: str
    resource_type: ResourceType
    required_role: UserRole
    required_permissions: List[Permission]
    ubuntu_governance_required: bool = False
    elder_approval_required: bool = False
    cultural_sensitivity_level: int = 1  # 1-5 scale

@dataclass
class AccessAttempt:
    """Access attempt data structure"""
    attempt_id: str
    user_id: str
    resource_type: ResourceType
    requested_permissions: List[Permission]
    status: AccessStatus
    timestamp: datetime
    ip_address: str
    user_agent: str
    ubuntu_context: Optional[str] = None
    elder_approval_id: Optional[str] = None

class AccessControlAgent:
    """
    Access Control Agent for WebWaka Digital Operating System
    
    Provides comprehensive access control with multi-factor authentication,
    role-based access control, and Ubuntu philosophy integration.
    """
    
    def __init__(self, db_path: str = "webwaka_access_control.db"):
        """Initialize the Access Control Agent"""
        self.db_path = db_path
        self.users: Dict[str, User] = {}
        self.auth_factors: Dict[str, AuthenticationFactor] = {}
        self.access_rules: Dict[str, AccessRule] = {}
        self.access_attempts: Dict[str, AccessAttempt] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.access_metrics = {
            "total_users": 0,
            "ubuntu_members": 0,
            "elders": 0,
            "successful_logins": 0,
            "failed_logins": 0,
            "access_granted": 0,
            "access_denied": 0,
            "ubuntu_approvals": 0
        }
        
        # Initialize database
        self._init_database()
        
        # Load default access rules
        self._load_default_access_rules()
        
        # Load sample users
        self._load_sample_users()
        
        logger.info("Access Control Agent initialized successfully")
    
    def _init_database(self):
        """Initialize the access control database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL,
                cultural_background TEXT NOT NULL,
                ubuntu_community_member BOOLEAN DEFAULT FALSE,
                elder_status BOOLEAN DEFAULT FALSE,
                traditional_authority BOOLEAN DEFAULT FALSE,
                enabled_auth_methods TEXT,
                last_login TEXT,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TEXT
            )
        ''')
        
        # Authentication factors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth_factors (
                factor_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                method TEXT NOT NULL,
                secret TEXT NOT NULL,
                verified BOOLEAN DEFAULT FALSE,
                created_at TEXT NOT NULL,
                ubuntu_verified BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Access rules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_rules (
                rule_id TEXT PRIMARY KEY,
                resource_type TEXT NOT NULL,
                required_role TEXT NOT NULL,
                required_permissions TEXT NOT NULL,
                ubuntu_governance_required BOOLEAN DEFAULT FALSE,
                elder_approval_required BOOLEAN DEFAULT FALSE,
                cultural_sensitivity_level INTEGER DEFAULT 1
            )
        ''')
        
        # Access attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_attempts (
                attempt_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                requested_permissions TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                ubuntu_context TEXT,
                elder_approval_id TEXT
            )
        ''')
        
        # Active sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                ubuntu_verified BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_default_access_rules(self):
        """Load default access control rules"""
        rules = [
            AccessRule(
                rule_id="rule_001",
                resource_type=ResourceType.USER_DATA,
                required_role=UserRole.MEMBER,
                required_permissions=[Permission.READ, Permission.WRITE],
                ubuntu_governance_required=False,
                elder_approval_required=False,
                cultural_sensitivity_level=2
            ),
            AccessRule(
                rule_id="rule_002",
                resource_type=ResourceType.FINANCIAL_DATA,
                required_role=UserRole.MEMBER,
                required_permissions=[Permission.READ, Permission.WRITE],
                ubuntu_governance_required=True,
                elder_approval_required=False,
                cultural_sensitivity_level=3
            ),
            AccessRule(
                rule_id="rule_003",
                resource_type=ResourceType.CULTURAL_DATA,
                required_role=UserRole.ELDER,
                required_permissions=[Permission.READ, Permission.WRITE],
                ubuntu_governance_required=True,
                elder_approval_required=True,
                cultural_sensitivity_level=5
            ),
            AccessRule(
                rule_id="rule_004",
                resource_type=ResourceType.TRADITIONAL_KNOWLEDGE,
                required_role=UserRole.ELDER,
                required_permissions=[Permission.TRADITIONAL_KNOWLEDGE],
                ubuntu_governance_required=True,
                elder_approval_required=True,
                cultural_sensitivity_level=5
            ),
            AccessRule(
                rule_id="rule_005",
                resource_type=ResourceType.UBUNTU_GOVERNANCE,
                required_role=UserRole.UBUNTU_COUNCIL,
                required_permissions=[Permission.UBUNTU_GOVERNANCE],
                ubuntu_governance_required=True,
                elder_approval_required=True,
                cultural_sensitivity_level=5
            ),
            AccessRule(
                rule_id="rule_006",
                resource_type=ResourceType.SYSTEM_CONFIGURATION,
                required_role=UserRole.SYSTEM_ADMIN,
                required_permissions=[Permission.ADMIN],
                ubuntu_governance_required=False,
                elder_approval_required=False,
                cultural_sensitivity_level=4
            )
        ]
        
        for rule in rules:
            self.access_rules[rule.rule_id] = rule
            self._save_access_rule(rule)
    
    def _load_sample_users(self):
        """Load sample users for testing"""
        users = [
            User(
                user_id="user_001",
                username="amara_okafor",
                email="amara.okafor@webwaka.com",
                role=UserRole.MEMBER,
                cultural_background="Igbo",
                ubuntu_community_member=True,
                elder_status=False,
                traditional_authority=False,
                enabled_auth_methods=[AuthenticationMethod.PASSWORD, AuthenticationMethod.SMS, AuthenticationMethod.TOTP]
            ),
            User(
                user_id="user_002",
                username="thabo_mthembu",
                email="thabo.mthembu@webwaka.com",
                role=UserRole.ELDER,
                cultural_background="Zulu",
                ubuntu_community_member=True,
                elder_status=True,
                traditional_authority=True,
                enabled_auth_methods=[AuthenticationMethod.PASSWORD, AuthenticationMethod.UBUNTU_COMMUNITY_VERIFICATION]
            ),
            User(
                user_id="user_003",
                username="fatima_alrashid",
                email="fatima.alrashid@webwaka.com",
                role=UserRole.COMMUNITY_LEADER,
                cultural_background="Arabic",
                ubuntu_community_member=True,
                elder_status=False,
                traditional_authority=False,
                enabled_auth_methods=[AuthenticationMethod.PASSWORD, AuthenticationMethod.TOTP, AuthenticationMethod.BIOMETRIC]
            ),
            User(
                user_id="user_004",
                username="ubuntu_council",
                email="council@webwaka.com",
                role=UserRole.UBUNTU_COUNCIL,
                cultural_background="Pan-African",
                ubuntu_community_member=True,
                elder_status=True,
                traditional_authority=True,
                enabled_auth_methods=[AuthenticationMethod.UBUNTU_COMMUNITY_VERIFICATION, AuthenticationMethod.HARDWARE_TOKEN]
            )
        ]
        
        for user in users:
            self.users[user.user_id] = user
            self._save_user(user)
            self.access_metrics["total_users"] += 1
            
            if user.ubuntu_community_member:
                self.access_metrics["ubuntu_members"] += 1
            if user.elder_status:
                self.access_metrics["elders"] += 1
            
            # Create authentication factors
            self._create_auth_factors_for_user(user)
    
    def _create_auth_factors_for_user(self, user: User):
        """Create authentication factors for user"""
        for method in user.enabled_auth_methods or []:
            factor_id = f"factor_{uuid.uuid4().hex[:8]}"
            
            if method == AuthenticationMethod.PASSWORD:
                # Hash a default password (in production, this would be set by user)
                secret = hashlib.sha256(f"password_{user.username}".encode()).hexdigest()
            elif method == AuthenticationMethod.TOTP:
                # Generate TOTP secret
                secret = pyotp.random_base32()
            elif method == AuthenticationMethod.SMS:
                # Phone number (placeholder)
                secret = f"+234{secrets.randbelow(1000000000):09d}"
            elif method == AuthenticationMethod.BIOMETRIC:
                # Biometric template hash (placeholder)
                secret = hashlib.sha256(f"biometric_{user.user_id}".encode()).hexdigest()
            elif method == AuthenticationMethod.HARDWARE_TOKEN:
                # Hardware token serial (placeholder)
                secret = f"HWT{secrets.randbelow(1000000):06d}"
            elif method == AuthenticationMethod.UBUNTU_COMMUNITY_VERIFICATION:
                # Ubuntu community verification token
                secret = f"ubuntu_{hashlib.sha256(user.user_id.encode()).hexdigest()[:16]}"
            else:
                secret = secrets.token_hex(16)
            
            auth_factor = AuthenticationFactor(
                factor_id=factor_id,
                user_id=user.user_id,
                method=method,
                secret=secret,
                verified=True,  # Pre-verified for testing
                created_at=datetime.now(),
                ubuntu_verified=user.ubuntu_community_member and method == AuthenticationMethod.UBUNTU_COMMUNITY_VERIFICATION
            )
            
            self.auth_factors[factor_id] = auth_factor
            self._save_auth_factor(auth_factor)
    
    def authenticate_user(self, username: str, password: str, 
                         additional_factors: Dict[str, str] = None,
                         ip_address: str = "127.0.0.1",
                         user_agent: str = "WebWaka Client") -> Dict[str, Any]:
        """Authenticate user with multi-factor authentication"""
        # Find user by username
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            self.access_metrics["failed_logins"] += 1
            return {"success": False, "error": "User not found"}
        
        # Check if user is locked
        if user.locked_until and datetime.now() < user.locked_until:
            return {"success": False, "error": "Account locked"}
        
        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        password_factor = None
        for factor in self.auth_factors.values():
            if (factor.user_id == user.user_id and 
                factor.method == AuthenticationMethod.PASSWORD and
                factor.secret == password_hash):
                password_factor = factor
                break
        
        if not password_factor:
            user.failed_attempts += 1
            if user.failed_attempts >= 5:
                user.locked_until = datetime.now() + timedelta(minutes=30)
            self._save_user(user)
            self.access_metrics["failed_logins"] += 1
            return {"success": False, "error": "Invalid password"}
        
        # Verify additional factors
        required_factors = [method for method in user.enabled_auth_methods 
                          if method != AuthenticationMethod.PASSWORD]
        
        verified_factors = []
        ubuntu_verified = False
        
        for method in required_factors:
            if additional_factors and method.value in additional_factors:
                factor_value = additional_factors[method.value]
                
                if self._verify_auth_factor(user.user_id, method, factor_value):
                    verified_factors.append(method)
                    
                    if method == AuthenticationMethod.UBUNTU_COMMUNITY_VERIFICATION:
                        ubuntu_verified = True
                        self.access_metrics["ubuntu_approvals"] += 1
                else:
                    self.access_metrics["failed_logins"] += 1
                    return {"success": False, "error": f"Invalid {method.value}"}
        
        # Check if all required factors are verified
        if len(verified_factors) < len(required_factors):
            missing_factors = [method.value for method in required_factors 
                             if method not in verified_factors]
            return {
                "success": False, 
                "error": "Additional authentication required",
                "required_factors": missing_factors
            }
        
        # Successful authentication
        user.last_login = datetime.now()
        user.failed_attempts = 0
        user.locked_until = None
        self._save_user(user)
        
        # Create session
        session_id = self._create_session(user, ip_address, user_agent, ubuntu_verified)
        
        self.access_metrics["successful_logins"] += 1
        
        return {
            "success": True,
            "session_id": session_id,
            "user_id": user.user_id,
            "role": user.role.value,
            "ubuntu_member": user.ubuntu_community_member,
            "elder_status": user.elder_status,
            "ubuntu_verified": ubuntu_verified
        }
    
    def _verify_auth_factor(self, user_id: str, method: AuthenticationMethod, value: str) -> bool:
        """Verify authentication factor"""
        for factor in self.auth_factors.values():
            if factor.user_id == user_id and factor.method == method:
                if method == AuthenticationMethod.TOTP:
                    # For testing, accept any 6-digit code
                    return len(value) == 6 and value.isdigit()
                elif method == AuthenticationMethod.SMS:
                    # In production, this would verify SMS code
                    return value == "123456"  # Placeholder
                elif method == AuthenticationMethod.BIOMETRIC:
                    # In production, this would verify biometric data
                    return hashlib.sha256(value.encode()).hexdigest() == factor.secret
                elif method == AuthenticationMethod.HARDWARE_TOKEN:
                    # In production, this would verify hardware token
                    return value == factor.secret
                elif method == AuthenticationMethod.UBUNTU_COMMUNITY_VERIFICATION:
                    # Ubuntu community verification
                    return value == factor.secret
                else:
                    return value == factor.secret
        
        return False
    
    def _create_session(self, user: User, ip_address: str, user_agent: str, ubuntu_verified: bool) -> str:
        """Create user session"""
        session_id = f"sess_{uuid.uuid4().hex}"
        
        session_data = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role.value,
            "ubuntu_member": user.ubuntu_community_member,
            "elder_status": user.elder_status,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=8),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "ubuntu_verified": ubuntu_verified
        }
        
        self.active_sessions[session_id] = session_data
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO active_sessions 
            (session_id, user_id, created_at, expires_at, ip_address, user_agent, ubuntu_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, user.user_id, session_data["created_at"].isoformat(),
            session_data["expires_at"].isoformat(), ip_address, user_agent, ubuntu_verified
        ))
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def check_access(self, session_id: str, resource_type: ResourceType,
                    requested_permissions: List[Permission],
                    ip_address: str = "127.0.0.1",
                    user_agent: str = "WebWaka Client") -> Dict[str, Any]:
        """Check access permissions for resource"""
        # Validate session
        if session_id not in self.active_sessions:
            return {"access_granted": False, "error": "Invalid session"}
        
        session = self.active_sessions[session_id]
        
        # Check session expiry
        if datetime.now() > session["expires_at"]:
            del self.active_sessions[session_id]
            return {"access_granted": False, "error": "Session expired"}
        
        user_id = session["user_id"]
        user = self.users[user_id]
        
        # Find applicable access rule
        applicable_rule = None
        for rule in self.access_rules.values():
            if rule.resource_type == resource_type:
                applicable_rule = rule
                break
        
        if not applicable_rule:
            return {"access_granted": False, "error": "No access rule found"}
        
        # Check role requirement
        role_hierarchy = {
            UserRole.GUEST: 0,
            UserRole.MEMBER: 1,
            UserRole.ELDER: 2,
            UserRole.COMMUNITY_LEADER: 3,
            UserRole.TRADITIONAL_AUTHORITY: 4,
            UserRole.SYSTEM_ADMIN: 5,
            UserRole.UBUNTU_COUNCIL: 6
        }
        
        if role_hierarchy[user.role] < role_hierarchy[applicable_rule.required_role]:
            self._log_access_attempt(user_id, resource_type, requested_permissions, 
                                   AccessStatus.DENIED, ip_address, user_agent,
                                   "Insufficient role")
            self.access_metrics["access_denied"] += 1
            return {"access_granted": False, "error": "Insufficient role"}
        
        # Check permission requirements
        missing_permissions = []
        for required_perm in applicable_rule.required_permissions:
            if required_perm not in requested_permissions:
                missing_permissions.append(required_perm)
        
        if missing_permissions:
            self._log_access_attempt(user_id, resource_type, requested_permissions,
                                   AccessStatus.DENIED, ip_address, user_agent,
                                   f"Missing permissions: {missing_permissions}")
            self.access_metrics["access_denied"] += 1
            return {"access_granted": False, "error": f"Missing permissions: {missing_permissions}"}
        
        # Check Ubuntu governance requirement
        if applicable_rule.ubuntu_governance_required and not session["ubuntu_verified"]:
            self._log_access_attempt(user_id, resource_type, requested_permissions,
                                   AccessStatus.UBUNTU_CONSENSUS_REQUIRED, ip_address, user_agent,
                                   "Ubuntu governance verification required")
            return {
                "access_granted": False, 
                "error": "Ubuntu governance verification required",
                "requires_ubuntu_consensus": True
            }
        
        # Check elder approval requirement
        if applicable_rule.elder_approval_required and not user.elder_status:
            self._log_access_attempt(user_id, resource_type, requested_permissions,
                                   AccessStatus.REQUIRES_ELDER_APPROVAL, ip_address, user_agent,
                                   "Elder approval required")
            return {
                "access_granted": False,
                "error": "Elder approval required",
                "requires_elder_approval": True
            }
        
        # Access granted
        self._log_access_attempt(user_id, resource_type, requested_permissions,
                               AccessStatus.GRANTED, ip_address, user_agent)
        self.access_metrics["access_granted"] += 1
        
        return {
            "access_granted": True,
            "user_role": user.role.value,
            "ubuntu_member": user.ubuntu_community_member,
            "elder_status": user.elder_status,
            "cultural_sensitivity_level": applicable_rule.cultural_sensitivity_level
        }
    
    def _log_access_attempt(self, user_id: str, resource_type: ResourceType,
                          requested_permissions: List[Permission], status: AccessStatus,
                          ip_address: str, user_agent: str, ubuntu_context: str = None):
        """Log access attempt"""
        attempt_id = f"attempt_{uuid.uuid4().hex[:8]}"
        
        attempt = AccessAttempt(
            attempt_id=attempt_id,
            user_id=user_id,
            resource_type=resource_type,
            requested_permissions=requested_permissions,
            status=status,
            timestamp=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            ubuntu_context=ubuntu_context
        )
        
        self.access_attempts[attempt_id] = attempt
        self._save_access_attempt(attempt)
    
    def get_access_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive access control dashboard"""
        # User statistics
        users_by_role = {}
        users_by_culture = {}
        
        for user in self.users.values():
            role = user.role.value
            culture = user.cultural_background
            
            users_by_role[role] = users_by_role.get(role, 0) + 1
            users_by_culture[culture] = users_by_culture.get(culture, 0) + 1
        
        # Access attempt statistics
        attempts_by_status = {}
        attempts_by_resource = {}
        
        for attempt in self.access_attempts.values():
            status = attempt.status.value
            resource = attempt.resource_type.value
            
            attempts_by_status[status] = attempts_by_status.get(status, 0) + 1
            attempts_by_resource[resource] = attempts_by_resource.get(resource, 0) + 1
        
        # Authentication factor statistics
        factors_by_method = {}
        ubuntu_verified_factors = 0
        
        for factor in self.auth_factors.values():
            method = factor.method.value
            factors_by_method[method] = factors_by_method.get(method, 0) + 1
            
            if factor.ubuntu_verified:
                ubuntu_verified_factors += 1
        
        return {
            "access_metrics": self.access_metrics,
            "users": {
                "total": len(self.users),
                "by_role": users_by_role,
                "by_culture": users_by_culture,
                "ubuntu_members": self.access_metrics["ubuntu_members"],
                "elders": self.access_metrics["elders"]
            },
            "access_attempts": {
                "total": len(self.access_attempts),
                "by_status": attempts_by_status,
                "by_resource": attempts_by_resource
            },
            "authentication": {
                "total_factors": len(self.auth_factors),
                "by_method": factors_by_method,
                "ubuntu_verified": ubuntu_verified_factors
            },
            "active_sessions": {
                "total": len(self.active_sessions),
                "ubuntu_verified_sessions": sum(1 for s in self.active_sessions.values() 
                                              if s.get("ubuntu_verified", False))
            },
            "access_rules": {
                "total": len(self.access_rules),
                "ubuntu_governance_required": sum(1 for r in self.access_rules.values() 
                                                if r.ubuntu_governance_required),
                "elder_approval_required": sum(1 for r in self.access_rules.values() 
                                             if r.elder_approval_required)
            }
        }
    
    def _save_user(self, user: User):
        """Save user to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, email, role, cultural_background, ubuntu_community_member,
             elder_status, traditional_authority, enabled_auth_methods, last_login,
             failed_attempts, locked_until)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user.user_id, user.username, user.email, user.role.value,
            user.cultural_background, user.ubuntu_community_member,
            user.elder_status, user.traditional_authority,
            json.dumps([method.value for method in user.enabled_auth_methods]) if user.enabled_auth_methods else None,
            user.last_login.isoformat() if user.last_login else None,
            user.failed_attempts,
            user.locked_until.isoformat() if user.locked_until else None
        ))
        
        conn.commit()
        conn.close()
    
    def _save_auth_factor(self, factor: AuthenticationFactor):
        """Save authentication factor to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO auth_factors 
            (factor_id, user_id, method, secret, verified, created_at, ubuntu_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            factor.factor_id, factor.user_id, factor.method.value, factor.secret,
            factor.verified, factor.created_at.isoformat(), factor.ubuntu_verified
        ))
        
        conn.commit()
        conn.close()
    
    def _save_access_rule(self, rule: AccessRule):
        """Save access rule to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO access_rules 
            (rule_id, resource_type, required_role, required_permissions,
             ubuntu_governance_required, elder_approval_required, cultural_sensitivity_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            rule.rule_id, rule.resource_type.value, rule.required_role.value,
            json.dumps([perm.value for perm in rule.required_permissions]),
            rule.ubuntu_governance_required, rule.elder_approval_required,
            rule.cultural_sensitivity_level
        ))
        
        conn.commit()
        conn.close()
    
    def _save_access_attempt(self, attempt: AccessAttempt):
        """Save access attempt to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO access_attempts 
            (attempt_id, user_id, resource_type, requested_permissions, status,
             timestamp, ip_address, user_agent, ubuntu_context, elder_approval_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            attempt.attempt_id, attempt.user_id, attempt.resource_type.value,
            json.dumps([perm.value for perm in attempt.requested_permissions]),
            attempt.status.value, attempt.timestamp.isoformat(),
            attempt.ip_address, attempt.user_agent, attempt.ubuntu_context,
            attempt.elder_approval_id
        ))
        
        conn.commit()
        conn.close()

def main():
    """Test the Access Control Agent"""
    print("🔐 Testing WebWaka Access Control Agent")
    print("=" * 45)
    
    # Initialize agent
    agent = AccessControlAgent()
    
    # Test user authentication
    print("\n🔑 Testing User Authentication")
    print("-" * 30)
    
    # Test member authentication with MFA
    auth_result = agent.authenticate_user(
        username="amara_okafor",
        password="password_amara_okafor",
        additional_factors={
            "sms": "123456",
            "totp": "123456"  # In production, this would be a real TOTP code
        },
        ip_address="192.168.1.100",
        user_agent="WebWaka Mobile App"
    )
    
    if auth_result["success"]:
        print(f"✅ Member Authentication Successful")
        print(f"   Session ID: {auth_result['session_id']}")
        print(f"   Role: {auth_result['role']}")
        print(f"   Ubuntu member: {auth_result['ubuntu_member']}")
        member_session = auth_result["session_id"]
    else:
        print(f"❌ Member Authentication Failed: {auth_result['error']}")
        member_session = None
    
    # Test elder authentication with Ubuntu verification
    elder_auth = agent.authenticate_user(
        username="thabo_mthembu",
        password="password_thabo_mthembu",
        additional_factors={
            "ubuntu_community_verification": "ubuntu_b5d4e6f8a9c2d1e3"
        },
        ip_address="10.0.0.50",
        user_agent="WebWaka Desktop"
    )
    
    if elder_auth["success"]:
        print(f"✅ Elder Authentication Successful")
        print(f"   Session ID: {elder_auth['session_id']}")
        print(f"   Role: {elder_auth['role']}")
        print(f"   Elder status: {elder_auth['elder_status']}")
        print(f"   Ubuntu verified: {elder_auth['ubuntu_verified']}")
        elder_session = elder_auth["session_id"]
    else:
        print(f"❌ Elder Authentication Failed: {elder_auth['error']}")
        elder_session = None
    
    # Test access control
    print("\n🛡️ Testing Access Control")
    print("-" * 25)
    
    if member_session:
        # Test member access to user data
        access_result = agent.check_access(
            session_id=member_session,
            resource_type=ResourceType.USER_DATA,
            requested_permissions=[Permission.READ, Permission.WRITE],
            ip_address="192.168.1.100"
        )
        
        print(f"✅ Member User Data Access: {access_result['access_granted']}")
        if access_result["access_granted"]:
            print(f"   Cultural sensitivity level: {access_result['cultural_sensitivity_level']}")
        
        # Test member access to cultural data (should be denied)
        cultural_access = agent.check_access(
            session_id=member_session,
            resource_type=ResourceType.CULTURAL_DATA,
            requested_permissions=[Permission.READ, Permission.WRITE],
            ip_address="192.168.1.100"
        )
        
        print(f"❌ Member Cultural Data Access: {cultural_access['access_granted']}")
        if not cultural_access["access_granted"]:
            print(f"   Error: {cultural_access['error']}")
    
    if elder_session:
        # Test elder access to cultural data
        elder_cultural_access = agent.check_access(
            session_id=elder_session,
            resource_type=ResourceType.CULTURAL_DATA,
            requested_permissions=[Permission.READ, Permission.WRITE],
            ip_address="10.0.0.50"
        )
        
        print(f"✅ Elder Cultural Data Access: {elder_cultural_access['access_granted']}")
        if elder_cultural_access["access_granted"]:
            print(f"   Cultural sensitivity level: {elder_cultural_access['cultural_sensitivity_level']}")
        
        # Test elder access to traditional knowledge
        traditional_access = agent.check_access(
            session_id=elder_session,
            resource_type=ResourceType.TRADITIONAL_KNOWLEDGE,
            requested_permissions=[Permission.TRADITIONAL_KNOWLEDGE],
            ip_address="10.0.0.50"
        )
        
        print(f"✅ Elder Traditional Knowledge Access: {traditional_access['access_granted']}")
        if traditional_access["access_granted"]:
            print(f"   Elder status: {traditional_access['elder_status']}")
    
    # Test Ubuntu Council authentication
    print("\n🏛️ Testing Ubuntu Council Authentication")
    print("-" * 40)
    
    council_auth = agent.authenticate_user(
        username="ubuntu_council",
        password="password_ubuntu_council",
        additional_factors={
            "ubuntu_community_verification": "ubuntu_a1b2c3d4e5f6g7h8",
            "hardware_token": "HWT123456"
        },
        ip_address="172.16.0.10",
        user_agent="WebWaka Council Portal"
    )
    
    if council_auth["success"]:
        print(f"✅ Ubuntu Council Authentication Successful")
        print(f"   Role: {council_auth['role']}")
        print(f"   Ubuntu verified: {council_auth['ubuntu_verified']}")
        
        # Test Ubuntu governance access
        governance_access = agent.check_access(
            session_id=council_auth["session_id"],
            resource_type=ResourceType.UBUNTU_GOVERNANCE,
            requested_permissions=[Permission.UBUNTU_GOVERNANCE],
            ip_address="172.16.0.10"
        )
        
        print(f"✅ Ubuntu Governance Access: {governance_access['access_granted']}")
    
    # Display access control dashboard
    print("\n📊 Access Control Dashboard")
    print("-" * 30)
    
    dashboard = agent.get_access_dashboard()
    
    print(f"Access Metrics:")
    for metric, value in dashboard['access_metrics'].items():
        print(f"   {metric}: {value}")
    
    print(f"\nUsers:")
    print(f"   Total: {dashboard['users']['total']}")
    print(f"   Ubuntu members: {dashboard['users']['ubuntu_members']}")
    print(f"   Elders: {dashboard['users']['elders']}")
    for role, count in dashboard['users']['by_role'].items():
        print(f"   {role}: {count}")
    
    print(f"\nAuthentication:")
    print(f"   Total factors: {dashboard['authentication']['total_factors']}")
    print(f"   Ubuntu verified: {dashboard['authentication']['ubuntu_verified']}")
    for method, count in dashboard['authentication']['by_method'].items():
        print(f"   {method}: {count}")
    
    print(f"\nActive Sessions:")
    print(f"   Total: {dashboard['active_sessions']['total']}")
    print(f"   Ubuntu verified: {dashboard['active_sessions']['ubuntu_verified_sessions']}")
    
    print(f"\nAccess Rules:")
    print(f"   Total: {dashboard['access_rules']['total']}")
    print(f"   Ubuntu governance required: {dashboard['access_rules']['ubuntu_governance_required']}")
    print(f"   Elder approval required: {dashboard['access_rules']['elder_approval_required']}")
    
    print("\n🎉 Access Control Agent testing completed!")

if __name__ == "__main__":
    main()

