"""
WebWaka Multi-Tenant Security Architecture
Cellular-level isolation with enterprise-grade security
"""

import hashlib
import secrets
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from functools import wraps
import redis
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations"""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    AUTHORIZED = "authorized"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class TenantType(Enum):
    """Types of tenants in the system"""
    INDIVIDUAL = "individual"
    SMALL_BUSINESS = "small_business"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"
    NGO = "ngo"
    COOPERATIVE = "cooperative"

@dataclass
class SecurityContext:
    """Security context for requests"""
    tenant_id: str
    user_id: str
    role: str
    permissions: List[str]
    security_level: SecurityLevel
    session_id: str
    ip_address: str
    user_agent: str
    timestamp: datetime

@dataclass
class TenantConfiguration:
    """Tenant-specific security configuration"""
    tenant_id: str
    tenant_type: TenantType
    security_level: SecurityLevel
    encryption_key: str
    data_residency: str  # African country/region
    compliance_requirements: List[str]
    cellular_modules: List[str]
    max_users: int
    storage_quota: int
    api_rate_limit: int

class CellularSecurityManager:
    """Manages cellular-level security isolation"""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        self.tenant_configs = {}
        self.active_sessions = {}
        self.security_policies = {}
        
    def initialize_tenant_security(self, tenant_config: TenantConfiguration) -> Dict[str, Any]:
        """Initialize security for a new tenant"""
        try:
            # Generate tenant-specific encryption keys
            tenant_key = self._generate_tenant_key(tenant_config.tenant_id)
            
            # Create cellular security boundaries
            cellular_boundaries = self._create_cellular_boundaries(
                tenant_config.tenant_id, 
                tenant_config.cellular_modules
            )
            
            # Set up data isolation
            data_isolation = self._setup_data_isolation(tenant_config)
            
            # Configure security policies
            security_policies = self._configure_security_policies(tenant_config)
            
            # Store tenant configuration
            self.tenant_configs[tenant_config.tenant_id] = tenant_config
            
            # Cache in Redis for fast access
            self.redis_client.setex(
                f"tenant_config:{tenant_config.tenant_id}",
                3600,  # 1 hour TTL
                json.dumps({
                    'tenant_id': tenant_config.tenant_id,
                    'tenant_type': tenant_config.tenant_type.value,
                    'security_level': tenant_config.security_level.value,
                    'cellular_modules': tenant_config.cellular_modules,
                    'compliance_requirements': tenant_config.compliance_requirements
                })
            )
            
            logger.info(f"Initialized security for tenant {tenant_config.tenant_id}")
            
            return {
                'tenant_id': tenant_config.tenant_id,
                'tenant_key': tenant_key,
                'cellular_boundaries': cellular_boundaries,
                'data_isolation': data_isolation,
                'security_policies': security_policies,
                'status': 'initialized'
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize tenant security: {str(e)}")
            raise SecurityException(f"Tenant security initialization failed: {str(e)}")
    
    def _generate_tenant_key(self, tenant_id: str) -> str:
        """Generate unique encryption key for tenant"""
        # Combine tenant ID with system secret and timestamp
        system_secret = secrets.token_hex(32)
        timestamp = str(datetime.utcnow().timestamp())
        
        key_material = f"{tenant_id}:{system_secret}:{timestamp}"
        tenant_key = hashlib.sha256(key_material.encode()).hexdigest()
        
        # Store key securely (in production, use HSM or key management service)
        self.redis_client.setex(
            f"tenant_key:{tenant_id}",
            86400,  # 24 hours TTL
            tenant_key
        )
        
        return tenant_key
    
    def _create_cellular_boundaries(self, tenant_id: str, cellular_modules: List[str]) -> Dict[str, Any]:
        """Create security boundaries for cellular modules"""
        boundaries = {}
        
        for module in cellular_modules:
            # Create module-specific security boundary
            module_boundary = {
                'module_id': module,
                'tenant_id': tenant_id,
                'namespace': f"{tenant_id}:{module}",
                'access_controls': self._generate_module_access_controls(module),
                'data_encryption': True,
                'audit_logging': True,
                'rate_limiting': self._get_module_rate_limits(module)
            }
            
            boundaries[module] = module_boundary
            
            # Cache module boundary
            self.redis_client.setex(
                f"module_boundary:{tenant_id}:{module}",
                3600,
                json.dumps(module_boundary)
            )
        
        return boundaries
    
    def _setup_data_isolation(self, tenant_config: TenantConfiguration) -> Dict[str, Any]:
        """Set up data isolation for tenant"""
        isolation_config = {
            'tenant_id': tenant_config.tenant_id,
            'database_schema': f"tenant_{tenant_config.tenant_id}",
            'storage_prefix': f"data/{tenant_config.tenant_id}/",
            'cache_namespace': f"cache:{tenant_config.tenant_id}:",
            'encryption_at_rest': True,
            'encryption_in_transit': True,
            'data_residency': tenant_config.data_residency,
            'backup_encryption': True,
            'cross_tenant_access': False
        }
        
        # African data residency compliance
        if tenant_config.data_residency in ['south_africa', 'nigeria', 'kenya', 'ghana', 'egypt']:
            isolation_config['local_data_processing'] = True
            isolation_config['cross_border_restrictions'] = True
        
        return isolation_config
    
    def _configure_security_policies(self, tenant_config: TenantConfiguration) -> Dict[str, Any]:
        """Configure security policies for tenant"""
        policies = {
            'authentication': {
                'multi_factor_required': tenant_config.security_level in [SecurityLevel.ADMIN, SecurityLevel.SUPER_ADMIN],
                'password_complexity': self._get_password_policy(tenant_config.security_level),
                'session_timeout': self._get_session_timeout(tenant_config.tenant_type),
                'concurrent_sessions': self._get_concurrent_session_limit(tenant_config.tenant_type)
            },
            'authorization': {
                'role_based_access': True,
                'cellular_permissions': True,
                'resource_level_permissions': True,
                'time_based_access': False
            },
            'data_protection': {
                'encryption_algorithm': 'AES-256-GCM',
                'key_rotation_interval': 90,  # days
                'data_classification': True,
                'pii_detection': True,
                'data_masking': True
            },
            'audit_logging': {
                'all_access_logged': True,
                'data_changes_logged': True,
                'admin_actions_logged': True,
                'log_retention_days': 2555,  # 7 years for compliance
                'log_encryption': True
            },
            'threat_protection': {
                'rate_limiting': True,
                'ddos_protection': True,
                'intrusion_detection': True,
                'malware_scanning': True,
                'vulnerability_scanning': True
            }
        }
        
        # Add compliance-specific policies
        if 'GDPR' in tenant_config.compliance_requirements:
            policies['gdpr_compliance'] = {
                'right_to_be_forgotten': True,
                'data_portability': True,
                'consent_management': True,
                'privacy_by_design': True
            }
        
        if 'POPIA' in tenant_config.compliance_requirements:  # South Africa
            policies['popia_compliance'] = {
                'data_minimization': True,
                'purpose_limitation': True,
                'storage_limitation': True,
                'data_subject_rights': True
            }
        
        return policies
    
    def _generate_module_access_controls(self, module: str) -> Dict[str, Any]:
        """Generate access controls for cellular module"""
        # Define module-specific access patterns
        module_access_patterns = {
            'customer_management': ['read', 'write', 'update', 'delete'],
            'inventory': ['read', 'write', 'update', 'stock_adjust'],
            'billing': ['read', 'write', 'payment_process', 'refund'],
            'analytics': ['read', 'export', 'dashboard_access'],
            'user_management': ['read', 'write', 'role_assign', 'permission_grant']
        }
        
        base_permissions = module_access_patterns.get(module, ['read', 'write'])
        
        return {
            'permissions': base_permissions,
            'resource_filters': True,
            'field_level_security': True,
            'time_based_restrictions': False,
            'ip_restrictions': False,
            'device_restrictions': False
        }
    
    def _get_module_rate_limits(self, module: str) -> Dict[str, int]:
        """Get rate limits for cellular module"""
        # Define module-specific rate limits (requests per minute)
        rate_limits = {
            'customer_management': {'read': 1000, 'write': 100},
            'inventory': {'read': 500, 'write': 200, 'stock_adjust': 50},
            'billing': {'read': 300, 'write': 100, 'payment_process': 10},
            'analytics': {'read': 200, 'export': 5},
            'user_management': {'read': 100, 'write': 20}
        }
        
        return rate_limits.get(module, {'read': 100, 'write': 50})
    
    def _get_password_policy(self, security_level: SecurityLevel) -> Dict[str, Any]:
        """Get password policy based on security level"""
        policies = {
            SecurityLevel.PUBLIC: {
                'min_length': 8,
                'require_uppercase': True,
                'require_lowercase': True,
                'require_numbers': True,
                'require_symbols': False,
                'max_age_days': 180
            },
            SecurityLevel.AUTHENTICATED: {
                'min_length': 10,
                'require_uppercase': True,
                'require_lowercase': True,
                'require_numbers': True,
                'require_symbols': True,
                'max_age_days': 90
            },
            SecurityLevel.ADMIN: {
                'min_length': 12,
                'require_uppercase': True,
                'require_lowercase': True,
                'require_numbers': True,
                'require_symbols': True,
                'max_age_days': 60,
                'prevent_reuse': 12
            }
        }
        
        return policies.get(security_level, policies[SecurityLevel.AUTHENTICATED])
    
    def _get_session_timeout(self, tenant_type: TenantType) -> int:
        """Get session timeout based on tenant type (minutes)"""
        timeouts = {
            TenantType.INDIVIDUAL: 120,      # 2 hours
            TenantType.SMALL_BUSINESS: 240,  # 4 hours
            TenantType.ENTERPRISE: 480,      # 8 hours
            TenantType.GOVERNMENT: 60,       # 1 hour (more secure)
            TenantType.NGO: 180             # 3 hours
        }
        
        return timeouts.get(tenant_type, 120)
    
    def _get_concurrent_session_limit(self, tenant_type: TenantType) -> int:
        """Get concurrent session limit based on tenant type"""
        limits = {
            TenantType.INDIVIDUAL: 3,
            TenantType.SMALL_BUSINESS: 10,
            TenantType.ENTERPRISE: 100,
            TenantType.GOVERNMENT: 50,
            TenantType.NGO: 20
        }
        
        return limits.get(tenant_type, 3)

class SecurityContextManager:
    """Manages security context for requests"""
    
    def __init__(self, cellular_security: CellularSecurityManager):
        self.cellular_security = cellular_security
        self.jwt_secret = secrets.token_hex(32)
    
    def create_security_context(self, tenant_id: str, user_id: str, 
                              request_data: Dict[str, Any]) -> SecurityContext:
        """Create security context for request"""
        try:
            # Get tenant configuration
            tenant_config = self._get_tenant_config(tenant_id)
            if not tenant_config:
                raise SecurityException(f"Tenant {tenant_id} not found")
            
            # Get user permissions
            user_permissions = self._get_user_permissions(tenant_id, user_id)
            
            # Determine security level
            security_level = self._determine_security_level(user_permissions)
            
            # Create session
            session_id = self._create_session(tenant_id, user_id)
            
            context = SecurityContext(
                tenant_id=tenant_id,
                user_id=user_id,
                role=user_permissions.get('role', 'user'),
                permissions=user_permissions.get('permissions', []),
                security_level=security_level,
                session_id=session_id,
                ip_address=request_data.get('ip_address', ''),
                user_agent=request_data.get('user_agent', ''),
                timestamp=datetime.utcnow()
            )
            
            # Cache security context
            self._cache_security_context(context)
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to create security context: {str(e)}")
            raise SecurityException(f"Security context creation failed: {str(e)}")
    
    def validate_security_context(self, context: SecurityContext) -> bool:
        """Validate security context"""
        try:
            # Check session validity
            if not self._is_session_valid(context.session_id):
                return False
            
            # Check tenant access
            if not self._can_access_tenant(context.user_id, context.tenant_id):
                return False
            
            # Check security level
            if not self._validate_security_level(context):
                return False
            
            # Update last activity
            self._update_session_activity(context.session_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Security context validation failed: {str(e)}")
            return False
    
    def _get_tenant_config(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get tenant configuration"""
        # Try cache first
        cached_config = self.cellular_security.redis_client.get(f"tenant_config:{tenant_id}")
        if cached_config:
            return json.loads(cached_config)
        
        # Fallback to in-memory
        return self.cellular_security.tenant_configs.get(tenant_id)
    
    def _get_user_permissions(self, tenant_id: str, user_id: str) -> Dict[str, Any]:
        """Get user permissions for tenant"""
        # This would typically query a database
        # For now, return mock permissions
        return {
            'role': 'admin',
            'permissions': ['read', 'write', 'delete', 'admin'],
            'cellular_modules': ['customer_management', 'inventory', 'billing']
        }
    
    def _determine_security_level(self, permissions: Dict[str, Any]) -> SecurityLevel:
        """Determine security level based on permissions"""
        role = permissions.get('role', 'user')
        
        if role == 'super_admin':
            return SecurityLevel.SUPER_ADMIN
        elif role == 'admin':
            return SecurityLevel.ADMIN
        elif 'admin' in permissions.get('permissions', []):
            return SecurityLevel.AUTHORIZED
        elif permissions.get('permissions'):
            return SecurityLevel.AUTHENTICATED
        else:
            return SecurityLevel.PUBLIC
    
    def _create_session(self, tenant_id: str, user_id: str) -> str:
        """Create new session"""
        session_id = secrets.token_hex(32)
        session_data = {
            'tenant_id': tenant_id,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'active': True
        }
        
        # Store session with TTL
        self.cellular_security.redis_client.setex(
            f"session:{session_id}",
            7200,  # 2 hours
            json.dumps(session_data)
        )
        
        return session_id
    
    def _cache_security_context(self, context: SecurityContext):
        """Cache security context"""
        context_data = {
            'tenant_id': context.tenant_id,
            'user_id': context.user_id,
            'role': context.role,
            'permissions': context.permissions,
            'security_level': context.security_level.value,
            'session_id': context.session_id
        }
        
        self.cellular_security.redis_client.setex(
            f"security_context:{context.session_id}",
            3600,  # 1 hour
            json.dumps(context_data)
        )
    
    def _is_session_valid(self, session_id: str) -> bool:
        """Check if session is valid"""
        session_data = self.cellular_security.redis_client.get(f"session:{session_id}")
        if not session_data:
            return False
        
        session = json.loads(session_data)
        return session.get('active', False)
    
    def _can_access_tenant(self, user_id: str, tenant_id: str) -> bool:
        """Check if user can access tenant"""
        # This would typically query user-tenant relationships
        # For now, return True (implement proper access control)
        return True
    
    def _validate_security_level(self, context: SecurityContext) -> bool:
        """Validate security level requirements"""
        # Implement security level validation logic
        return True
    
    def _update_session_activity(self, session_id: str):
        """Update session last activity"""
        session_data = self.cellular_security.redis_client.get(f"session:{session_id}")
        if session_data:
            session = json.loads(session_data)
            session['last_activity'] = datetime.utcnow().isoformat()
            
            self.cellular_security.redis_client.setex(
                f"session:{session_id}",
                7200,  # 2 hours
                json.dumps(session)
            )

class SecurityException(Exception):
    """Custom security exception"""
    pass

def require_security_level(required_level: SecurityLevel):
    """Decorator to require specific security level"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get security context from request
            context = kwargs.get('security_context')
            if not context or context.security_level.value < required_level.value:
                raise SecurityException(f"Insufficient security level. Required: {required_level.value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_cellular_permission(module: str, permission: str):
    """Decorator to require specific cellular module permission"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context = kwargs.get('security_context')
            if not context:
                raise SecurityException("Security context required")
            
            # Check if user has permission for cellular module
            if not has_cellular_permission(context, module, permission):
                raise SecurityException(f"Permission denied for {module}:{permission}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def has_cellular_permission(context: SecurityContext, module: str, permission: str) -> bool:
    """Check if user has permission for cellular module"""
    # This would implement the actual permission checking logic
    # For now, return True if user has any permissions
    return len(context.permissions) > 0

# Initialize security managers
cellular_security = CellularSecurityManager()
security_context_manager = SecurityContextManager(cellular_security)

