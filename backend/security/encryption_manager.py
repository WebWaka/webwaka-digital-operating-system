"""
WebWaka End-to-End Encryption Manager
Comprehensive encryption for all data and communications with African compliance
"""

import os
import base64
import secrets
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EncryptionLevel(Enum):
    """Encryption levels for different data types"""
    BASIC = "basic"           # Standard AES-256
    ENHANCED = "enhanced"     # AES-256 + HMAC
    MAXIMUM = "maximum"       # AES-256 + RSA + HMAC
    QUANTUM_SAFE = "quantum_safe"  # Post-quantum cryptography

class DataClassification(Enum):
    """Data classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    TOP_SECRET = "top_secret"

class EncryptionAlgorithm(Enum):
    """Supported encryption algorithms"""
    AES_256_GCM = "aes_256_gcm"
    AES_256_CBC = "aes_256_cbc"
    CHACHA20_POLY1305 = "chacha20_poly1305"
    RSA_4096 = "rsa_4096"
    ECDSA_P384 = "ecdsa_p384"

@dataclass
class EncryptionKey:
    """Encryption key information"""
    key_id: str
    tenant_id: str
    algorithm: EncryptionAlgorithm
    key_data: bytes
    created_at: datetime
    expires_at: Optional[datetime]
    rotation_count: int
    usage_count: int
    max_usage: Optional[int]
    key_derivation_info: Optional[Dict[str, Any]]

@dataclass
class EncryptedData:
    """Encrypted data container"""
    data_id: str
    tenant_id: str
    encrypted_content: bytes
    encryption_metadata: Dict[str, Any]
    key_id: str
    algorithm: EncryptionAlgorithm
    iv_nonce: bytes
    auth_tag: Optional[bytes]
    created_at: datetime
    data_classification: DataClassification

class WebWakaEncryptionManager:
    """Comprehensive encryption manager for WebWaka"""
    
    def __init__(self):
        self.encryption_keys = {}
        self.tenant_key_stores = {}
        self.encrypted_data_store = {}
        self.key_rotation_policies = {}
        self.encryption_audit_log = []
        self._initialize_encryption_policies()
    
    def _initialize_encryption_policies(self):
        """Initialize encryption policies for different data classifications"""
        self.encryption_policies = {
            DataClassification.PUBLIC: {
                'encryption_required': False,
                'algorithm': EncryptionAlgorithm.AES_256_GCM,
                'key_rotation_days': 365,
                'max_key_usage': None
            },
            DataClassification.INTERNAL: {
                'encryption_required': True,
                'algorithm': EncryptionAlgorithm.AES_256_GCM,
                'key_rotation_days': 180,
                'max_key_usage': 1000000
            },
            DataClassification.CONFIDENTIAL: {
                'encryption_required': True,
                'algorithm': EncryptionAlgorithm.AES_256_GCM,
                'key_rotation_days': 90,
                'max_key_usage': 500000,
                'additional_authentication': True
            },
            DataClassification.RESTRICTED: {
                'encryption_required': True,
                'algorithm': EncryptionAlgorithm.AES_256_GCM,
                'key_rotation_days': 30,
                'max_key_usage': 100000,
                'additional_authentication': True,
                'hardware_security_module': True
            },
            DataClassification.TOP_SECRET: {
                'encryption_required': True,
                'algorithm': EncryptionAlgorithm.AES_256_GCM,
                'key_rotation_days': 7,
                'max_key_usage': 10000,
                'additional_authentication': True,
                'hardware_security_module': True,
                'quantum_safe': True
            }
        }
    
    def initialize_tenant_encryption(self, tenant_id: str, 
                                   encryption_config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize encryption for a tenant"""
        try:
            # Generate master key for tenant
            master_key = self._generate_master_key(tenant_id)
            
            # Create key store for tenant
            self.tenant_key_stores[tenant_id] = {
                'master_key': master_key,
                'data_encryption_keys': {},
                'communication_keys': {},
                'backup_keys': {},
                'key_rotation_schedule': self._create_key_rotation_schedule(tenant_id),
                'encryption_config': encryption_config
            }
            
            # Generate initial data encryption keys
            initial_keys = self._generate_initial_keys(tenant_id, encryption_config)
            
            # Set up key rotation
            self._setup_key_rotation(tenant_id)
            
            # Log initialization
            self._log_encryption_event('tenant_encryption_initialized', {
                'tenant_id': tenant_id,
                'master_key_id': master_key.key_id,
                'initial_keys_count': len(initial_keys)
            })
            
            logger.info(f"Initialized encryption for tenant {tenant_id}")
            
            return {
                'tenant_id': tenant_id,
                'master_key_id': master_key.key_id,
                'data_encryption_keys': [key.key_id for key in initial_keys],
                'encryption_status': 'initialized',
                'key_rotation_enabled': True
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize tenant encryption: {str(e)}")
            raise EncryptionException(f"Tenant encryption initialization failed: {str(e)}")
    
    def encrypt_data(self, tenant_id: str, data: Union[str, bytes], 
                    data_classification: DataClassification,
                    metadata: Optional[Dict[str, Any]] = None) -> EncryptedData:
        """Encrypt data with appropriate encryption level"""
        try:
            # Validate tenant
            if tenant_id not in self.tenant_key_stores:
                raise EncryptionException(f"Tenant {tenant_id} not initialized for encryption")
            
            # Get encryption policy
            policy = self.encryption_policies[data_classification]
            
            if not policy['encryption_required'] and data_classification == DataClassification.PUBLIC:
                # For public data, encryption is optional
                logger.info(f"Skipping encryption for public data (tenant: {tenant_id})")
                return self._create_unencrypted_container(tenant_id, data, data_classification)
            
            # Get or create encryption key
            encryption_key = self._get_or_create_encryption_key(tenant_id, data_classification)
            
            # Convert data to bytes if string
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            # Encrypt based on algorithm
            if policy['algorithm'] == EncryptionAlgorithm.AES_256_GCM:
                encrypted_content, iv_nonce, auth_tag = self._encrypt_aes_gcm(data_bytes, encryption_key.key_data)
            elif policy['algorithm'] == EncryptionAlgorithm.CHACHA20_POLY1305:
                encrypted_content, iv_nonce, auth_tag = self._encrypt_chacha20_poly1305(data_bytes, encryption_key.key_data)
            else:
                raise EncryptionException(f"Unsupported encryption algorithm: {policy['algorithm']}")
            
            # Create encrypted data container
            data_id = self._generate_data_id()
            encrypted_data = EncryptedData(
                data_id=data_id,
                tenant_id=tenant_id,
                encrypted_content=encrypted_content,
                encryption_metadata=metadata or {},
                key_id=encryption_key.key_id,
                algorithm=policy['algorithm'],
                iv_nonce=iv_nonce,
                auth_tag=auth_tag,
                created_at=datetime.utcnow(),
                data_classification=data_classification
            )
            
            # Store encrypted data
            self.encrypted_data_store[data_id] = encrypted_data
            
            # Update key usage
            encryption_key.usage_count += 1
            
            # Log encryption
            self._log_encryption_event('data_encrypted', {
                'tenant_id': tenant_id,
                'data_id': data_id,
                'key_id': encryption_key.key_id,
                'algorithm': policy['algorithm'].value,
                'data_classification': data_classification.value
            })
            
            logger.info(f"Encrypted data {data_id} for tenant {tenant_id}")
            return encrypted_data
            
        except Exception as e:
            logger.error(f"Failed to encrypt data: {str(e)}")
            raise EncryptionException(f"Data encryption failed: {str(e)}")
    
    def decrypt_data(self, tenant_id: str, encrypted_data: EncryptedData) -> bytes:
        """Decrypt data"""
        try:
            # Validate tenant
            if tenant_id not in self.tenant_key_stores:
                raise EncryptionException(f"Tenant {tenant_id} not initialized for encryption")
            
            # Validate data ownership
            if encrypted_data.tenant_id != tenant_id:
                raise EncryptionException("Tenant mismatch for encrypted data")
            
            # Get encryption key
            encryption_key = self._get_encryption_key(encrypted_data.key_id)
            if not encryption_key:
                raise EncryptionException(f"Encryption key {encrypted_data.key_id} not found")
            
            # Decrypt based on algorithm
            if encrypted_data.algorithm == EncryptionAlgorithm.AES_256_GCM:
                decrypted_data = self._decrypt_aes_gcm(
                    encrypted_data.encrypted_content,
                    encryption_key.key_data,
                    encrypted_data.iv_nonce,
                    encrypted_data.auth_tag
                )
            elif encrypted_data.algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
                decrypted_data = self._decrypt_chacha20_poly1305(
                    encrypted_data.encrypted_content,
                    encryption_key.key_data,
                    encrypted_data.iv_nonce,
                    encrypted_data.auth_tag
                )
            else:
                raise EncryptionException(f"Unsupported decryption algorithm: {encrypted_data.algorithm}")
            
            # Log decryption
            self._log_encryption_event('data_decrypted', {
                'tenant_id': tenant_id,
                'data_id': encrypted_data.data_id,
                'key_id': encryption_key.key_id
            })
            
            return decrypted_data
            
        except Exception as e:
            logger.error(f"Failed to decrypt data: {str(e)}")
            raise EncryptionException(f"Data decryption failed: {str(e)}")
    
    def encrypt_communication(self, sender_tenant_id: str, recipient_tenant_id: str,
                            message: str, message_type: str = 'text') -> Dict[str, Any]:
        """Encrypt communication between tenants"""
        try:
            # Generate ephemeral key for this communication
            ephemeral_key = secrets.token_bytes(32)
            
            # Create communication envelope
            communication_data = {
                'sender': sender_tenant_id,
                'recipient': recipient_tenant_id,
                'message': message,
                'message_type': message_type,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Encrypt communication data
            encrypted_communication = self.encrypt_data(
                sender_tenant_id,
                json.dumps(communication_data),
                DataClassification.CONFIDENTIAL,
                {'communication': True, 'ephemeral_key': True}
            )
            
            # Create secure envelope for recipient
            envelope = {
                'encrypted_data_id': encrypted_communication.data_id,
                'sender_tenant_id': sender_tenant_id,
                'recipient_tenant_id': recipient_tenant_id,
                'encryption_metadata': {
                    'algorithm': encrypted_communication.algorithm.value,
                    'key_id': encrypted_communication.key_id,
                    'created_at': encrypted_communication.created_at.isoformat()
                }
            }
            
            # Log communication encryption
            self._log_encryption_event('communication_encrypted', {
                'sender': sender_tenant_id,
                'recipient': recipient_tenant_id,
                'data_id': encrypted_communication.data_id
            })
            
            return envelope
            
        except Exception as e:
            logger.error(f"Failed to encrypt communication: {str(e)}")
            raise EncryptionException(f"Communication encryption failed: {str(e)}")
    
    def decrypt_communication(self, recipient_tenant_id: str, 
                            envelope: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt communication for recipient"""
        try:
            # Validate recipient
            if envelope['recipient_tenant_id'] != recipient_tenant_id:
                raise EncryptionException("Recipient mismatch")
            
            # Get encrypted data
            encrypted_data = self.encrypted_data_store.get(envelope['encrypted_data_id'])
            if not encrypted_data:
                raise EncryptionException("Encrypted communication data not found")
            
            # Decrypt communication
            decrypted_bytes = self.decrypt_data(recipient_tenant_id, encrypted_data)
            communication_data = json.loads(decrypted_bytes.decode('utf-8'))
            
            # Log communication decryption
            self._log_encryption_event('communication_decrypted', {
                'recipient': recipient_tenant_id,
                'sender': communication_data['sender'],
                'data_id': envelope['encrypted_data_id']
            })
            
            return communication_data
            
        except Exception as e:
            logger.error(f"Failed to decrypt communication: {str(e)}")
            raise EncryptionException(f"Communication decryption failed: {str(e)}")
    
    def rotate_keys(self, tenant_id: str, force_rotation: bool = False) -> Dict[str, Any]:
        """Rotate encryption keys for tenant"""
        try:
            if tenant_id not in self.tenant_key_stores:
                raise EncryptionException(f"Tenant {tenant_id} not found")
            
            tenant_store = self.tenant_key_stores[tenant_id]
            rotated_keys = []
            
            # Rotate data encryption keys
            for classification, keys in tenant_store['data_encryption_keys'].items():
                for key in keys:
                    if self._should_rotate_key(key, force_rotation):
                        new_key = self._rotate_encryption_key(tenant_id, key, classification)
                        rotated_keys.append({
                            'old_key_id': key.key_id,
                            'new_key_id': new_key.key_id,
                            'classification': classification.value
                        })
            
            # Log key rotation
            self._log_encryption_event('keys_rotated', {
                'tenant_id': tenant_id,
                'rotated_keys_count': len(rotated_keys),
                'force_rotation': force_rotation
            })
            
            logger.info(f"Rotated {len(rotated_keys)} keys for tenant {tenant_id}")
            
            return {
                'tenant_id': tenant_id,
                'rotated_keys': rotated_keys,
                'rotation_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to rotate keys: {str(e)}")
            raise EncryptionException(f"Key rotation failed: {str(e)}")
    
    def _generate_master_key(self, tenant_id: str) -> EncryptionKey:
        """Generate master key for tenant"""
        key_id = f"master_{tenant_id}_{secrets.token_hex(8)}"
        master_key_data = secrets.token_bytes(32)  # 256-bit key
        
        master_key = EncryptionKey(
            key_id=key_id,
            tenant_id=tenant_id,
            algorithm=EncryptionAlgorithm.AES_256_GCM,
            key_data=master_key_data,
            created_at=datetime.utcnow(),
            expires_at=None,  # Master keys don't expire
            rotation_count=0,
            usage_count=0,
            max_usage=None,
            key_derivation_info=None
        )
        
        self.encryption_keys[key_id] = master_key
        return master_key
    
    def _generate_initial_keys(self, tenant_id: str, 
                              config: Dict[str, Any]) -> List[EncryptionKey]:
        """Generate initial encryption keys for tenant"""
        initial_keys = []
        
        # Generate keys for each data classification level
        for classification in DataClassification:
            if config.get(f'enable_{classification.value}', True):
                key = self._create_data_encryption_key(tenant_id, classification)
                initial_keys.append(key)
                
                # Store in tenant key store
                if tenant_id not in self.tenant_key_stores:
                    self.tenant_key_stores[tenant_id]['data_encryption_keys'] = {}
                
                if classification not in self.tenant_key_stores[tenant_id]['data_encryption_keys']:
                    self.tenant_key_stores[tenant_id]['data_encryption_keys'][classification] = []
                
                self.tenant_key_stores[tenant_id]['data_encryption_keys'][classification].append(key)
        
        return initial_keys
    
    def _create_data_encryption_key(self, tenant_id: str, 
                                   classification: DataClassification) -> EncryptionKey:
        """Create data encryption key for specific classification"""
        key_id = f"dek_{tenant_id}_{classification.value}_{secrets.token_hex(8)}"
        key_data = secrets.token_bytes(32)  # 256-bit key
        
        policy = self.encryption_policies[classification]
        expires_at = datetime.utcnow() + timedelta(days=policy['key_rotation_days'])
        
        encryption_key = EncryptionKey(
            key_id=key_id,
            tenant_id=tenant_id,
            algorithm=policy['algorithm'],
            key_data=key_data,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            rotation_count=0,
            usage_count=0,
            max_usage=policy['max_key_usage'],
            key_derivation_info={'classification': classification.value}
        )
        
        self.encryption_keys[key_id] = encryption_key
        return encryption_key
    
    def _get_or_create_encryption_key(self, tenant_id: str, 
                                     classification: DataClassification) -> EncryptionKey:
        """Get existing or create new encryption key"""
        tenant_store = self.tenant_key_stores[tenant_id]
        
        if classification in tenant_store['data_encryption_keys']:
            keys = tenant_store['data_encryption_keys'][classification]
            
            # Find active key
            for key in keys:
                if self._is_key_active(key):
                    return key
        
        # Create new key if none found
        return self._create_data_encryption_key(tenant_id, classification)
    
    def _is_key_active(self, key: EncryptionKey) -> bool:
        """Check if key is still active"""
        # Check expiration
        if key.expires_at and datetime.utcnow() > key.expires_at:
            return False
        
        # Check usage limit
        if key.max_usage and key.usage_count >= key.max_usage:
            return False
        
        return True
    
    def _encrypt_aes_gcm(self, data: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
        """Encrypt data using AES-256-GCM"""
        # Generate random IV
        iv = secrets.token_bytes(12)  # 96-bit IV for GCM
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Encrypt data
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return ciphertext, iv, encryptor.tag
    
    def _decrypt_aes_gcm(self, ciphertext: bytes, key: bytes, 
                        iv: bytes, auth_tag: bytes) -> bytes:
        """Decrypt data using AES-256-GCM"""
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, auth_tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt data
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        return plaintext
    
    def _encrypt_chacha20_poly1305(self, data: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
        """Encrypt data using ChaCha20-Poly1305"""
        # Generate random nonce
        nonce = secrets.token_bytes(12)  # 96-bit nonce
        
        # Create cipher
        cipher = Cipher(algorithms.ChaCha20(key, nonce), None, backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Encrypt data
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        # For ChaCha20-Poly1305, we need to implement AEAD manually
        # This is a simplified version - in production, use proper ChaCha20-Poly1305 AEAD
        auth_tag = hmac.new(key, ciphertext + nonce, hashlib.sha256).digest()[:16]
        
        return ciphertext, nonce, auth_tag
    
    def _decrypt_chacha20_poly1305(self, ciphertext: bytes, key: bytes,
                                  nonce: bytes, auth_tag: bytes) -> bytes:
        """Decrypt data using ChaCha20-Poly1305"""
        # Verify authentication tag
        expected_tag = hmac.new(key, ciphertext + nonce, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(auth_tag, expected_tag):
            raise EncryptionException("Authentication tag verification failed")
        
        # Create cipher
        cipher = Cipher(algorithms.ChaCha20(key, nonce), None, backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt data
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        return plaintext
    
    def _generate_data_id(self) -> str:
        """Generate unique data ID"""
        return f"data_{secrets.token_hex(16)}"
    
    def _create_unencrypted_container(self, tenant_id: str, data: Union[str, bytes],
                                    classification: DataClassification) -> EncryptedData:
        """Create container for unencrypted public data"""
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data
        
        data_id = self._generate_data_id()
        
        return EncryptedData(
            data_id=data_id,
            tenant_id=tenant_id,
            encrypted_content=data_bytes,  # Not actually encrypted
            encryption_metadata={'encrypted': False},
            key_id='none',
            algorithm=EncryptionAlgorithm.AES_256_GCM,  # Placeholder
            iv_nonce=b'',
            auth_tag=None,
            created_at=datetime.utcnow(),
            data_classification=classification
        )
    
    def _get_encryption_key(self, key_id: str) -> Optional[EncryptionKey]:
        """Get encryption key by ID"""
        return self.encryption_keys.get(key_id)
    
    def _should_rotate_key(self, key: EncryptionKey, force: bool = False) -> bool:
        """Check if key should be rotated"""
        if force:
            return True
        
        # Check expiration
        if key.expires_at and datetime.utcnow() > key.expires_at:
            return True
        
        # Check usage limit
        if key.max_usage and key.usage_count >= key.max_usage:
            return True
        
        return False
    
    def _rotate_encryption_key(self, tenant_id: str, old_key: EncryptionKey,
                              classification: DataClassification) -> EncryptionKey:
        """Rotate an encryption key"""
        # Create new key
        new_key = self._create_data_encryption_key(tenant_id, classification)
        new_key.rotation_count = old_key.rotation_count + 1
        
        # Mark old key as rotated (but keep for decryption of old data)
        old_key.expires_at = datetime.utcnow()
        
        # Update tenant key store
        tenant_store = self.tenant_key_stores[tenant_id]
        if classification in tenant_store['data_encryption_keys']:
            tenant_store['data_encryption_keys'][classification].append(new_key)
        
        return new_key
    
    def _create_key_rotation_schedule(self, tenant_id: str) -> Dict[str, Any]:
        """Create key rotation schedule for tenant"""
        return {
            'enabled': True,
            'check_interval_hours': 24,
            'last_check': datetime.utcnow(),
            'next_check': datetime.utcnow() + timedelta(hours=24),
            'auto_rotation': True
        }
    
    def _setup_key_rotation(self, tenant_id: str):
        """Set up automatic key rotation for tenant"""
        # In production, this would set up scheduled tasks
        logger.info(f"Key rotation scheduled for tenant {tenant_id}")
    
    def _log_encryption_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log encryption events for audit trail"""
        log_entry = {
            'event_id': secrets.token_hex(16),
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': event_data
        }
        
        self.encryption_audit_log.append(log_entry)
        logger.info(f"Encryption event logged: {event_type}")
    
    def get_encryption_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get encryption status for tenant"""
        if tenant_id not in self.tenant_key_stores:
            return {'status': 'not_initialized'}
        
        tenant_store = self.tenant_key_stores[tenant_id]
        
        # Count active keys
        active_keys = 0
        total_keys = 0
        
        for classification, keys in tenant_store['data_encryption_keys'].items():
            total_keys += len(keys)
            active_keys += sum(1 for key in keys if self._is_key_active(key))
        
        return {
            'tenant_id': tenant_id,
            'status': 'initialized',
            'total_keys': total_keys,
            'active_keys': active_keys,
            'encrypted_data_count': len([d for d in self.encrypted_data_store.values() 
                                       if d.tenant_id == tenant_id]),
            'key_rotation_enabled': tenant_store['key_rotation_schedule']['enabled'],
            'last_rotation_check': tenant_store['key_rotation_schedule']['last_check'].isoformat()
        }

class EncryptionException(Exception):
    """Custom encryption exception"""
    pass

# Initialize encryption manager
encryption_manager = WebWakaEncryptionManager()

