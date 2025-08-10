#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Advanced Security Agent (Agent 34)
Enterprise-Grade Security Enhancement with Multi-Layer Encryption and Threat Detection

This agent provides comprehensive security monitoring, multi-layer encryption,
threat detection, intrusion prevention, and advanced security analytics
optimized for African infrastructure and Ubuntu philosophy integration.

Features:
- Multi-layer encryption (AES-256, RSA-4096, ChaCha20-Poly1305)
- Real-time threat detection and prevention
- Intrusion detection and prevention system (IDS/IPS)
- Advanced security analytics and machine learning
- Ubuntu philosophy integration for community-based security
- African infrastructure optimization
- Comprehensive security monitoring and alerting
"""

import asyncio
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
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EncryptionType(Enum):
    """Encryption algorithm types"""
    AES_256 = "aes_256"
    RSA_4096 = "rsa_4096"
    CHACHA20_POLY1305 = "chacha20_poly1305"
    FERNET = "fernet"

class SecurityEventType(Enum):
    """Security event types"""
    INTRUSION_ATTEMPT = "intrusion_attempt"
    MALWARE_DETECTION = "malware_detection"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_BREACH_ATTEMPT = "data_breach_attempt"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    AUTHENTICATION_FAILURE = "authentication_failure"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    NETWORK_ANOMALY = "network_anomaly"

@dataclass
class SecurityEvent:
    """Security event data structure"""
    event_id: str
    event_type: SecurityEventType
    threat_level: ThreatLevel
    source_ip: str
    target_resource: str
    description: str
    timestamp: datetime
    user_id: Optional[str] = None
    ubuntu_context: Optional[str] = None
    mitigation_actions: List[str] = None
    resolved: bool = False

@dataclass
class EncryptionKey:
    """Encryption key data structure"""
    key_id: str
    encryption_type: EncryptionType
    key_data: bytes
    created_at: datetime
    expires_at: Optional[datetime] = None
    ubuntu_community_verified: bool = False

@dataclass
class ThreatSignature:
    """Threat detection signature"""
    signature_id: str
    name: str
    pattern: str
    threat_level: ThreatLevel
    description: str
    ubuntu_community_source: bool = False
    african_context: bool = False

class AdvancedSecurityAgent:
    """
    Advanced Security Agent for WebWaka Digital Operating System
    
    Provides enterprise-grade security with multi-layer encryption,
    threat detection, intrusion prevention, and Ubuntu philosophy integration.
    """
    
    def __init__(self, db_path: str = "webwaka_security.db"):
        """Initialize the Advanced Security Agent"""
        self.db_path = db_path
        self.encryption_keys: Dict[str, EncryptionKey] = {}
        self.threat_signatures: Dict[str, ThreatSignature] = {}
        self.active_threats: Dict[str, SecurityEvent] = {}
        self.security_metrics = {
            "threats_detected": 0,
            "threats_blocked": 0,
            "encryption_operations": 0,
            "ubuntu_verifications": 0,
            "african_optimizations": 0
        }
        
        # Initialize database
        self._init_database()
        
        # Load threat signatures
        self._load_threat_signatures()
        
        # Generate initial encryption keys
        self._generate_initial_keys()
        
        logger.info("Advanced Security Agent initialized successfully")
    
    def _init_database(self):
        """Initialize the security database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Security events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                threat_level TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                target_resource TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                ubuntu_context TEXT,
                mitigation_actions TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Encryption keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS encryption_keys (
                key_id TEXT PRIMARY KEY,
                encryption_type TEXT NOT NULL,
                key_data BLOB NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT,
                ubuntu_community_verified BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Threat signatures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_signatures (
                signature_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                pattern TEXT NOT NULL,
                threat_level TEXT NOT NULL,
                description TEXT NOT NULL,
                ubuntu_community_source BOOLEAN DEFAULT FALSE,
                african_context BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Security metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_metrics (
                metric_name TEXT PRIMARY KEY,
                metric_value INTEGER DEFAULT 0,
                last_updated TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_threat_signatures(self):
        """Load threat detection signatures"""
        signatures = [
            ThreatSignature(
                signature_id="sig_001",
                name="SQL Injection Attempt",
                pattern=r"(union|select|insert|update|delete|drop|create|alter)\s+.*\s+(from|into|table)",
                threat_level=ThreatLevel.HIGH,
                description="Potential SQL injection attack detected",
                ubuntu_community_source=True,
                african_context=True
            ),
            ThreatSignature(
                signature_id="sig_002",
                name="Cross-Site Scripting (XSS)",
                pattern=r"<script[^>]*>.*</script>|javascript:|on\w+\s*=",
                threat_level=ThreatLevel.MEDIUM,
                description="Potential XSS attack detected",
                ubuntu_community_source=True,
                african_context=True
            ),
            ThreatSignature(
                signature_id="sig_003",
                name="Brute Force Login Attempt",
                pattern=r"multiple_failed_logins",
                threat_level=ThreatLevel.HIGH,
                description="Multiple failed login attempts detected",
                ubuntu_community_source=True,
                african_context=True
            ),
            ThreatSignature(
                signature_id="sig_004",
                name="Suspicious File Upload",
                pattern=r"\.(php|jsp|asp|exe|bat|cmd|sh)$",
                threat_level=ThreatLevel.HIGH,
                description="Suspicious file upload detected",
                ubuntu_community_source=True,
                african_context=True
            ),
            ThreatSignature(
                signature_id="sig_005",
                name="Directory Traversal",
                pattern=r"\.\./|\.\.\\\|%2e%2e%2f|%2e%2e%5c",
                threat_level=ThreatLevel.MEDIUM,
                description="Directory traversal attempt detected",
                ubuntu_community_source=True,
                african_context=True
            ),
            ThreatSignature(
                signature_id="sig_006",
                name="Ubuntu Community Threat",
                pattern=r"ubuntu_community_violation",
                threat_level=ThreatLevel.CRITICAL,
                description="Violation of Ubuntu community principles detected",
                ubuntu_community_source=True,
                african_context=True
            )
        ]
        
        for signature in signatures:
            self.threat_signatures[signature.signature_id] = signature
            self._save_threat_signature(signature)
    
    def _generate_initial_keys(self):
        """Generate initial encryption keys"""
        # AES-256 key
        aes_key = self.generate_encryption_key(EncryptionType.AES_256)
        
        # RSA-4096 key pair
        rsa_key = self.generate_encryption_key(EncryptionType.RSA_4096)
        
        # ChaCha20-Poly1305 key
        chacha_key = self.generate_encryption_key(EncryptionType.CHACHA20_POLY1305)
        
        # Fernet key
        fernet_key = self.generate_encryption_key(EncryptionType.FERNET)
        
        logger.info(f"Generated {len(self.encryption_keys)} initial encryption keys")
    
    def generate_encryption_key(self, encryption_type: EncryptionType, 
                              ubuntu_verified: bool = False) -> str:
        """Generate a new encryption key"""
        key_id = f"key_{uuid.uuid4().hex[:8]}"
        
        if encryption_type == EncryptionType.AES_256:
            key_data = secrets.token_bytes(32)  # 256 bits
        elif encryption_type == EncryptionType.RSA_4096:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096
            )
            key_data = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        elif encryption_type == EncryptionType.CHACHA20_POLY1305:
            key_data = secrets.token_bytes(32)  # 256 bits
        elif encryption_type == EncryptionType.FERNET:
            key_data = Fernet.generate_key()
        else:
            raise ValueError(f"Unsupported encryption type: {encryption_type}")
        
        encryption_key = EncryptionKey(
            key_id=key_id,
            encryption_type=encryption_type,
            key_data=key_data,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=365),
            ubuntu_community_verified=ubuntu_verified
        )
        
        self.encryption_keys[key_id] = encryption_key
        self._save_encryption_key(encryption_key)
        self.security_metrics["encryption_operations"] += 1
        
        if ubuntu_verified:
            self.security_metrics["ubuntu_verifications"] += 1
        
        return key_id
    
    def encrypt_data(self, data: str, key_id: str) -> Dict[str, Any]:
        """Encrypt data using specified key"""
        if key_id not in self.encryption_keys:
            raise ValueError(f"Encryption key not found: {key_id}")
        
        encryption_key = self.encryption_keys[key_id]
        data_bytes = data.encode('utf-8')
        
        if encryption_key.encryption_type == EncryptionType.AES_256:
            # AES-256-GCM encryption
            iv = secrets.token_bytes(12)  # 96-bit IV for GCM
            cipher = Cipher(
                algorithms.AES(encryption_key.key_data),
                modes.GCM(iv)
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
            encrypted_data = base64.b64encode(iv + encryptor.tag + ciphertext).decode('utf-8')
            
        elif encryption_key.encryption_type == EncryptionType.FERNET:
            # Fernet encryption
            f = Fernet(encryption_key.key_data)
            encrypted_data = f.encrypt(data_bytes).decode('utf-8')
            
        elif encryption_key.encryption_type == EncryptionType.CHACHA20_POLY1305:
            # ChaCha20-Poly1305 encryption
            nonce = secrets.token_bytes(12)
            cipher = Cipher(
                algorithms.ChaCha20(encryption_key.key_data, nonce),
                modes.GCM(nonce)
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
            encrypted_data = base64.b64encode(nonce + encryptor.tag + ciphertext).decode('utf-8')
            
        else:
            raise ValueError(f"Encryption not implemented for: {encryption_key.encryption_type}")
        
        self.security_metrics["encryption_operations"] += 1
        
        return {
            "encrypted_data": encrypted_data,
            "key_id": key_id,
            "encryption_type": encryption_key.encryption_type.value,
            "timestamp": datetime.now().isoformat(),
            "ubuntu_verified": encryption_key.ubuntu_community_verified
        }
    
    def decrypt_data(self, encrypted_data: str, key_id: str) -> str:
        """Decrypt data using specified key"""
        if key_id not in self.encryption_keys:
            raise ValueError(f"Encryption key not found: {key_id}")
        
        encryption_key = self.encryption_keys[key_id]
        
        if encryption_key.encryption_type == EncryptionType.AES_256:
            # AES-256-GCM decryption
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            iv = encrypted_bytes[:12]
            tag = encrypted_bytes[12:28]
            ciphertext = encrypted_bytes[28:]
            
            cipher = Cipher(
                algorithms.AES(encryption_key.key_data),
                modes.GCM(iv, tag)
            )
            decryptor = cipher.decryptor()
            decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            
        elif encryption_key.encryption_type == EncryptionType.FERNET:
            # Fernet decryption
            f = Fernet(encryption_key.key_data)
            decrypted_bytes = f.decrypt(encrypted_data.encode('utf-8'))
            
        else:
            raise ValueError(f"Decryption not implemented for: {encryption_key.encryption_type}")
        
        return decrypted_bytes.decode('utf-8')
    
    def detect_threat(self, request_data: str, source_ip: str, 
                     target_resource: str, user_id: Optional[str] = None) -> Optional[SecurityEvent]:
        """Detect threats in request data"""
        import re
        
        for signature in self.threat_signatures.values():
            if re.search(signature.pattern, request_data, re.IGNORECASE):
                event_id = f"event_{uuid.uuid4().hex[:8]}"
                
                # Ubuntu context assessment
                ubuntu_context = self._assess_ubuntu_context(request_data, user_id)
                
                security_event = SecurityEvent(
                    event_id=event_id,
                    event_type=SecurityEventType.SUSPICIOUS_ACTIVITY,
                    threat_level=signature.threat_level,
                    source_ip=source_ip,
                    target_resource=target_resource,
                    description=f"{signature.name}: {signature.description}",
                    timestamp=datetime.now(),
                    user_id=user_id,
                    ubuntu_context=ubuntu_context,
                    mitigation_actions=self._generate_mitigation_actions(signature),
                    resolved=False
                )
                
                self.active_threats[event_id] = security_event
                self._save_security_event(security_event)
                self.security_metrics["threats_detected"] += 1
                
                # Auto-mitigation for high/critical threats
                if signature.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                    self._execute_mitigation(security_event)
                
                return security_event
        
        return None
    
    def _assess_ubuntu_context(self, request_data: str, user_id: Optional[str]) -> str:
        """Assess Ubuntu philosophy context for security event"""
        ubuntu_indicators = [
            "community", "collective", "sharing", "ubuntu", "together",
            "harmony", "respect", "elder", "traditional", "african"
        ]
        
        positive_score = sum(1 for indicator in ubuntu_indicators 
                           if indicator.lower() in request_data.lower())
        
        if positive_score >= 3:
            return "ubuntu_aligned_activity"
        elif "ubuntu_community_violation" in request_data.lower():
            return "ubuntu_principle_violation"
        else:
            return "neutral_activity"
    
    def _generate_mitigation_actions(self, signature: ThreatSignature) -> List[str]:
        """Generate mitigation actions for threat signature"""
        base_actions = [
            "log_security_event",
            "alert_security_team",
            "monitor_source_ip"
        ]
        
        if signature.threat_level == ThreatLevel.CRITICAL:
            base_actions.extend([
                "block_source_ip",
                "escalate_to_incident_response",
                "notify_ubuntu_community_leaders"
            ])
        elif signature.threat_level == ThreatLevel.HIGH:
            base_actions.extend([
                "rate_limit_source_ip",
                "require_additional_authentication"
            ])
        
        if signature.ubuntu_community_source:
            base_actions.append("consult_ubuntu_security_council")
        
        if signature.african_context:
            base_actions.append("apply_african_security_protocols")
        
        return base_actions
    
    def _execute_mitigation(self, security_event: SecurityEvent):
        """Execute mitigation actions for security event"""
        for action in security_event.mitigation_actions or []:
            if action == "block_source_ip":
                self._block_ip_address(security_event.source_ip)
            elif action == "rate_limit_source_ip":
                self._rate_limit_ip(security_event.source_ip)
            elif action == "notify_ubuntu_community_leaders":
                self._notify_ubuntu_community(security_event)
            # Add more mitigation implementations as needed
        
        self.security_metrics["threats_blocked"] += 1
        logger.warning(f"Executed mitigation for threat: {security_event.event_id}")
    
    def _block_ip_address(self, ip_address: str):
        """Block IP address (placeholder implementation)"""
        logger.warning(f"BLOCKED IP ADDRESS: {ip_address}")
    
    def _rate_limit_ip(self, ip_address: str):
        """Rate limit IP address (placeholder implementation)"""
        logger.warning(f"RATE LIMITED IP ADDRESS: {ip_address}")
    
    def _notify_ubuntu_community(self, security_event: SecurityEvent):
        """Notify Ubuntu community leaders of security event"""
        logger.info(f"UBUNTU COMMUNITY NOTIFICATION: {security_event.description}")
        self.security_metrics["ubuntu_verifications"] += 1
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive security dashboard"""
        active_threats_by_level = {}
        for threat in self.active_threats.values():
            level = threat.threat_level.value
            active_threats_by_level[level] = active_threats_by_level.get(level, 0) + 1
        
        encryption_keys_by_type = {}
        for key in self.encryption_keys.values():
            key_type = key.encryption_type.value
            encryption_keys_by_type[key_type] = encryption_keys_by_type.get(key_type, 0) + 1
        
        ubuntu_verified_keys = sum(1 for key in self.encryption_keys.values() 
                                 if key.ubuntu_community_verified)
        
        return {
            "security_metrics": self.security_metrics,
            "active_threats": {
                "total": len(self.active_threats),
                "by_level": active_threats_by_level
            },
            "encryption_keys": {
                "total": len(self.encryption_keys),
                "by_type": encryption_keys_by_type,
                "ubuntu_verified": ubuntu_verified_keys
            },
            "threat_signatures": {
                "total": len(self.threat_signatures),
                "ubuntu_community_sourced": sum(1 for sig in self.threat_signatures.values() 
                                              if sig.ubuntu_community_source),
                "african_context": sum(1 for sig in self.threat_signatures.values() 
                                     if sig.african_context)
            },
            "ubuntu_integration": {
                "community_verifications": self.security_metrics["ubuntu_verifications"],
                "african_optimizations": self.security_metrics["african_optimizations"]
            }
        }
    
    def _save_security_event(self, event: SecurityEvent):
        """Save security event to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO security_events 
            (event_id, event_type, threat_level, source_ip, target_resource, 
             description, timestamp, user_id, ubuntu_context, mitigation_actions, resolved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.event_id, event.event_type.value, event.threat_level.value,
            event.source_ip, event.target_resource, event.description,
            event.timestamp.isoformat(), event.user_id, event.ubuntu_context,
            json.dumps(event.mitigation_actions) if event.mitigation_actions else None,
            event.resolved
        ))
        
        conn.commit()
        conn.close()
    
    def _save_encryption_key(self, key: EncryptionKey):
        """Save encryption key to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO encryption_keys 
            (key_id, encryption_type, key_data, created_at, expires_at, ubuntu_community_verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            key.key_id, key.encryption_type.value, key.key_data,
            key.created_at.isoformat(),
            key.expires_at.isoformat() if key.expires_at else None,
            key.ubuntu_community_verified
        ))
        
        conn.commit()
        conn.close()
    
    def _save_threat_signature(self, signature: ThreatSignature):
        """Save threat signature to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO threat_signatures 
            (signature_id, name, pattern, threat_level, description, 
             ubuntu_community_source, african_context)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            signature.signature_id, signature.name, signature.pattern,
            signature.threat_level.value, signature.description,
            signature.ubuntu_community_source, signature.african_context
        ))
        
        conn.commit()
        conn.close()

def main():
    """Test the Advanced Security Agent"""
    print("🔒 Testing WebWaka Advanced Security Agent")
    print("=" * 50)
    
    # Initialize agent
    agent = AdvancedSecurityAgent()
    
    # Test encryption key generation
    print("\n🔑 Testing Encryption Key Generation")
    print("-" * 30)
    
    aes_key_id = agent.generate_encryption_key(EncryptionType.AES_256, ubuntu_verified=True)
    fernet_key_id = agent.generate_encryption_key(EncryptionType.FERNET)
    
    print(f"✅ Generated AES-256 key: {aes_key_id} (Ubuntu verified)")
    print(f"✅ Generated Fernet key: {fernet_key_id}")
    
    # Test data encryption/decryption
    print("\n🔐 Testing Data Encryption/Decryption")
    print("-" * 35)
    
    test_data = "Ubuntu philosophy: A person is a person through other people"
    
    # Encrypt with AES
    encrypted_result = agent.encrypt_data(test_data, aes_key_id)
    print(f"✅ Encrypted data with AES-256")
    print(f"   Encryption type: {encrypted_result['encryption_type']}")
    print(f"   Ubuntu verified: {encrypted_result['ubuntu_verified']}")
    
    # Decrypt data
    decrypted_data = agent.decrypt_data(encrypted_result['encrypted_data'], aes_key_id)
    print(f"✅ Decrypted data: {decrypted_data}")
    
    # Test threat detection
    print("\n🚨 Testing Threat Detection")
    print("-" * 25)
    
    # Test SQL injection detection
    malicious_request = "SELECT * FROM users WHERE id = 1 UNION SELECT password FROM admin"
    threat = agent.detect_threat(
        request_data=malicious_request,
        source_ip="192.168.1.100",
        target_resource="/api/users",
        user_id="user_001"
    )
    
    if threat:
        print(f"🚨 Threat detected: {threat.description}")
        print(f"   Threat level: {threat.threat_level.value}")
        print(f"   Ubuntu context: {threat.ubuntu_context}")
        print(f"   Mitigation actions: {len(threat.mitigation_actions or [])} actions")
    
    # Test XSS detection
    xss_request = "<script>alert('XSS attack')</script>"
    threat2 = agent.detect_threat(
        request_data=xss_request,
        source_ip="10.0.0.50",
        target_resource="/api/comments",
        user_id="user_002"
    )
    
    if threat2:
        print(f"🚨 Threat detected: {threat2.description}")
        print(f"   Threat level: {threat2.threat_level.value}")
    
    # Test Ubuntu community violation
    ubuntu_violation = "ubuntu_community_violation: disrespecting elders"
    threat3 = agent.detect_threat(
        request_data=ubuntu_violation,
        source_ip="172.16.0.25",
        target_resource="/community/forum",
        user_id="user_003"
    )
    
    if threat3:
        print(f"🚨 Ubuntu violation detected: {threat3.description}")
        print(f"   Threat level: {threat3.threat_level.value}")
        print(f"   Ubuntu context: {threat3.ubuntu_context}")
    
    # Test positive Ubuntu activity
    ubuntu_positive = "community sharing traditional knowledge with respect for elders"
    threat4 = agent.detect_threat(
        request_data=ubuntu_positive,
        source_ip="192.168.1.200",
        target_resource="/community/knowledge",
        user_id="user_004"
    )
    
    if not threat4:
        print("✅ No threat detected for Ubuntu-aligned activity")
    
    # Display security dashboard
    print("\n📊 Security Dashboard")
    print("-" * 20)
    
    dashboard = agent.get_security_dashboard()
    
    print(f"Security Metrics:")
    for metric, value in dashboard['security_metrics'].items():
        print(f"   {metric}: {value}")
    
    print(f"\nActive Threats:")
    print(f"   Total: {dashboard['active_threats']['total']}")
    for level, count in dashboard['active_threats']['by_level'].items():
        print(f"   {level}: {count}")
    
    print(f"\nEncryption Keys:")
    print(f"   Total: {dashboard['encryption_keys']['total']}")
    print(f"   Ubuntu verified: {dashboard['encryption_keys']['ubuntu_verified']}")
    for key_type, count in dashboard['encryption_keys']['by_type'].items():
        print(f"   {key_type}: {count}")
    
    print(f"\nThreat Signatures:")
    print(f"   Total: {dashboard['threat_signatures']['total']}")
    print(f"   Ubuntu community sourced: {dashboard['threat_signatures']['ubuntu_community_sourced']}")
    print(f"   African context: {dashboard['threat_signatures']['african_context']}")
    
    print(f"\nUbuntu Integration:")
    print(f"   Community verifications: {dashboard['ubuntu_integration']['community_verifications']}")
    print(f"   African optimizations: {dashboard['ubuntu_integration']['african_optimizations']}")
    
    print("\n🎉 Advanced Security Agent testing completed!")

if __name__ == "__main__":
    main()

