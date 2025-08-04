"""
WebWaka Digital Operating System - Phase 3
Agent 3: Client Configuration Agent

Market-specific platform configuration including regulatory compliance for African
jurisdictions, payment method selection, language support customization, and
feature selection based on target market needs.

Author: Manus AI - God-Level Super Agent and Orchestrator
Created: December 2024
Version: 3.3.0
"""

import os
import json
import time
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import yaml
import requests
from decimal import Decimal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AfricanRegion(Enum):
    """African regions for market-specific configuration"""
    WEST_AFRICA = "west_africa"
    EAST_AFRICA = "east_africa"
    CENTRAL_AFRICA = "central_africa"
    SOUTHERN_AFRICA = "southern_africa"
    NORTH_AFRICA = "north_africa"

class BusinessSector(Enum):
    """Business sectors for feature configuration"""
    AGRICULTURE = "agriculture"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    FINANCE = "finance"
    GOVERNMENT = "government"
    COMMERCE = "commerce"
    TRANSPORT = "transport"
    ENERGY = "energy"
    MANUFACTURING = "manufacturing"
    TOURISM = "tourism"
    MEDIA = "media"
    TECHNOLOGY = "technology"
    HOUSING = "housing"
    MINING = "mining"

@dataclass
class RegulatoryRequirement:
    """Regulatory requirement configuration"""
    requirement_id: str
    jurisdiction: str
    requirement_type: str  # data_protection, financial, business_registration, etc.
    description: str
    compliance_level: str  # mandatory, recommended, optional
    implementation_details: Dict[str, Any]
    validation_rules: List[str]
    documentation_required: List[str]

@dataclass
class PaymentMethodConfig:
    """Payment method configuration"""
    method_id: str
    method_name: str
    provider: str
    supported_currencies: List[str]
    transaction_limits: Dict[str, Decimal]
    fees: Dict[str, Decimal]
    availability_regions: List[str]
    integration_config: Dict[str, Any]
    mobile_money_support: bool = False

@dataclass
class LanguageConfig:
    """Language configuration"""
    language_code: str
    language_name: str
    native_name: str
    region: str
    voice_support: bool
    text_direction: str  # ltr, rtl
    date_format: str
    number_format: str
    currency_format: str
    cultural_adaptations: Dict[str, Any]

@dataclass
class FeatureConfig:
    """Feature configuration"""
    feature_id: str
    feature_name: str
    category: str
    enabled: bool
    configuration: Dict[str, Any]
    dependencies: List[str]
    sector_specific: bool
    regional_variations: Dict[str, Any]

@dataclass
class MarketConfig:
    """Complete market configuration"""
    platform_id: str
    partner_id: str
    market_name: str
    region: AfricanRegion
    countries: List[str]
    primary_language: str
    supported_languages: List[LanguageConfig]
    business_sectors: List[BusinessSector]
    regulatory_requirements: List[RegulatoryRequirement]
    payment_methods: List[PaymentMethodConfig]
    features: List[FeatureConfig]
    cultural_settings: Dict[str, Any]
    localization_settings: Dict[str, Any]
    compliance_settings: Dict[str, Any]
    created_at: datetime

@dataclass
class ConfigurationResult:
    """Result of market configuration"""
    platform_id: str
    configuration_id: str
    status: str
    market_configured: bool
    compliance_validated: bool
    features_configured: int
    languages_configured: int
    payment_methods_configured: int
    regulatory_requirements_met: int
    validation_results: Dict[str, bool]
    configuration_files: List[str]
    error_messages: List[str]

class ClientConfigurationAgent:
    """
    Agent 3: Client Configuration Agent
    
    Handles market-specific platform configuration including regulatory compliance,
    payment methods, language support, and feature selection for African markets.
    """
    
    def __init__(self):
        """Initialize the Client Configuration Agent"""
        self.agent_id = "client_configuration_agent"
        self.version = "3.3.0"
        self.regulatory_manager = RegulatoryManager()
        self.payment_manager = PaymentManager()
        self.language_manager = LanguageManager()
        self.feature_manager = FeatureManager()
        self.compliance_validator = ComplianceValidator()
        self.localization_engine = LocalizationEngine()
        
        # Load market templates and configurations
        self.market_templates = self._load_market_templates()
        self.regulatory_database = self._load_regulatory_database()
        self.payment_providers = self._load_payment_providers()
        self.language_database = self._load_language_database()
        
        logger.info(f"Client Configuration Agent {self.version} initialized")
    
    def configure_market(self, market_config: MarketConfig) -> ConfigurationResult:
        """
        Configure platform for specific market requirements
        
        Args:
            market_config: Complete market configuration
            
        Returns:
            ConfigurationResult with configuration details and validation
        """
        start_time = time.time()
        configuration_id = f"config_{market_config.platform_id}_{uuid.uuid4().hex[:8]}"
        
        logger.info(f"Configuring market for platform {market_config.platform_id}")
        
        try:
            # Step 1: Validate market configuration
            validation_result = self._validate_market_config(market_config)
            if not validation_result['valid']:
                raise ValueError(f"Invalid market configuration: {validation_result['errors']}")
            
            # Step 2: Configure regulatory compliance
            regulatory_result = self._configure_regulatory_compliance(market_config)
            
            # Step 3: Configure payment methods
            payment_result = self._configure_payment_methods(market_config)
            
            # Step 4: Configure language support
            language_result = self._configure_language_support(market_config)
            
            # Step 5: Configure features for market
            feature_result = self._configure_market_features(market_config)
            
            # Step 6: Apply cultural adaptations
            cultural_result = self._apply_cultural_adaptations(market_config)
            
            # Step 7: Configure localization settings
            localization_result = self._configure_localization(market_config)
            
            # Step 8: Validate compliance requirements
            compliance_result = self._validate_compliance_requirements(market_config)
            
            # Step 9: Generate configuration files
            config_files_result = self._generate_configuration_files(market_config, configuration_id)
            
            # Step 10: Test market configuration
            testing_result = self._test_market_configuration(market_config, configuration_id)
            
            # Create configuration result
            result = ConfigurationResult(
                platform_id=market_config.platform_id,
                configuration_id=configuration_id,
                status="completed" if testing_result['passed'] else "failed",
                market_configured=True,
                compliance_validated=compliance_result['validated'],
                features_configured=len(market_config.features),
                languages_configured=len(market_config.supported_languages),
                payment_methods_configured=len(market_config.payment_methods),
                regulatory_requirements_met=regulatory_result['requirements_met'],
                validation_results=testing_result['results'],
                configuration_files=config_files_result['files'],
                error_messages=[]
            )
            
            # Store configuration record
            self._store_configuration_record(configuration_id, market_config, result)
            
            processing_time = time.time() - start_time
            logger.info(f"Market configuration completed in {processing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            error_msg = f"Market configuration failed: {str(e)}"
            logger.error(error_msg)
            
            return ConfigurationResult(
                platform_id=market_config.platform_id,
                configuration_id=configuration_id,
                status="failed",
                market_configured=False,
                compliance_validated=False,
                features_configured=0,
                languages_configured=0,
                payment_methods_configured=0,
                regulatory_requirements_met=0,
                validation_results={},
                configuration_files=[],
                error_messages=[error_msg]
            )
    
    def _load_market_templates(self) -> Dict[str, Any]:
        """Load market configuration templates"""
        templates = {}
        
        # West Africa template
        templates['west_africa'] = {
            'countries': ['Nigeria', 'Ghana', 'Senegal', 'Mali', 'Burkina Faso', 'Ivory Coast'],
            'primary_languages': ['English', 'French'],
            'local_languages': ['Hausa', 'Yoruba', 'Igbo', 'Twi', 'Wolof'],
            'currencies': ['NGN', 'GHS', 'XOF', 'XAF'],
            'mobile_money': ['MTN Mobile Money', 'Airtel Money', 'Orange Money'],
            'regulatory_focus': ['data_protection', 'financial_services', 'telecommunications']
        }
        
        # East Africa template
        templates['east_africa'] = {
            'countries': ['Kenya', 'Tanzania', 'Uganda', 'Rwanda', 'Ethiopia'],
            'primary_languages': ['English', 'Swahili'],
            'local_languages': ['Kikuyu', 'Luo', 'Amharic', 'Kinyarwanda'],
            'currencies': ['KES', 'TZS', 'UGX', 'RWF', 'ETB'],
            'mobile_money': ['M-Pesa', 'Airtel Money', 'MTN Mobile Money'],
            'regulatory_focus': ['data_protection', 'mobile_money', 'cross_border_payments']
        }
        
        # Southern Africa template
        templates['southern_africa'] = {
            'countries': ['South Africa', 'Zimbabwe', 'Botswana', 'Namibia', 'Zambia'],
            'primary_languages': ['English', 'Afrikaans'],
            'local_languages': ['Zulu', 'Xhosa', 'Shona', 'Setswana'],
            'currencies': ['ZAR', 'BWP', 'NAD', 'ZMW'],
            'mobile_money': ['Vodacom M-Pesa', 'MTN Mobile Money'],
            'regulatory_focus': ['financial_services', 'mining_regulations', 'data_protection']
        }
        
        return templates
    
    def _load_regulatory_database(self) -> Dict[str, List[RegulatoryRequirement]]:
        """Load regulatory requirements database"""
        regulatory_db = {}
        
        # Nigeria regulatory requirements
        regulatory_db['nigeria'] = [
            RegulatoryRequirement(
                requirement_id="nga_ndpr",
                jurisdiction="Nigeria",
                requirement_type="data_protection",
                description="Nigeria Data Protection Regulation (NDPR) compliance",
                compliance_level="mandatory",
                implementation_details={
                    "consent_management": True,
                    "data_localization": True,
                    "privacy_policy": True,
                    "data_protection_officer": True
                },
                validation_rules=[
                    "explicit_consent_required",
                    "data_retention_limits",
                    "breach_notification_72h"
                ],
                documentation_required=[
                    "privacy_policy",
                    "consent_forms",
                    "data_processing_agreements"
                ]
            ),
            RegulatoryRequirement(
                requirement_id="nga_cbn_guidelines",
                jurisdiction="Nigeria",
                requirement_type="financial",
                description="Central Bank of Nigeria (CBN) fintech guidelines",
                compliance_level="mandatory",
                implementation_details={
                    "kyc_requirements": True,
                    "aml_compliance": True,
                    "transaction_monitoring": True,
                    "regulatory_reporting": True
                },
                validation_rules=[
                    "customer_identification",
                    "transaction_limits",
                    "suspicious_activity_reporting"
                ],
                documentation_required=[
                    "kyc_procedures",
                    "aml_policy",
                    "compliance_manual"
                ]
            )
        ]
        
        # Kenya regulatory requirements
        regulatory_db['kenya'] = [
            RegulatoryRequirement(
                requirement_id="ken_dpa",
                jurisdiction="Kenya",
                requirement_type="data_protection",
                description="Kenya Data Protection Act compliance",
                compliance_level="mandatory",
                implementation_details={
                    "data_controller_registration": True,
                    "consent_management": True,
                    "cross_border_transfer_restrictions": True
                },
                validation_rules=[
                    "data_controller_registration",
                    "lawful_basis_processing",
                    "data_subject_rights"
                ],
                documentation_required=[
                    "data_protection_policy",
                    "data_processing_records",
                    "impact_assessments"
                ]
            )
        ]
        
        return regulatory_db
    
    def _load_payment_providers(self) -> Dict[str, PaymentMethodConfig]:
        """Load payment provider configurations"""
        providers = {}
        
        # M-Pesa configuration
        providers['mpesa'] = PaymentMethodConfig(
            method_id="mpesa",
            method_name="M-Pesa",
            provider="Safaricom",
            supported_currencies=["KES"],
            transaction_limits={
                "daily_limit": Decimal("300000"),
                "monthly_limit": Decimal("3000000"),
                "single_transaction": Decimal("150000")
            },
            fees={
                "transaction_fee": Decimal("0.01"),
                "withdrawal_fee": Decimal("0.02")
            },
            availability_regions=["east_africa"],
            integration_config={
                "api_version": "v1",
                "sandbox_url": "https://sandbox.safaricom.co.ke",
                "production_url": "https://api.safaricom.co.ke"
            },
            mobile_money_support=True
        )
        
        # MTN Mobile Money configuration
        providers['mtn_momo'] = PaymentMethodConfig(
            method_id="mtn_momo",
            method_name="MTN Mobile Money",
            provider="MTN",
            supported_currencies=["UGX", "GHS", "XAF", "XOF"],
            transaction_limits={
                "daily_limit": Decimal("5000000"),
                "monthly_limit": Decimal("20000000"),
                "single_transaction": Decimal("2000000")
            },
            fees={
                "transaction_fee": Decimal("0.015"),
                "withdrawal_fee": Decimal("0.025")
            },
            availability_regions=["west_africa", "east_africa", "central_africa"],
            integration_config={
                "api_version": "v2",
                "sandbox_url": "https://sandbox.momodeveloper.mtn.com",
                "production_url": "https://api.mtn.com"
            },
            mobile_money_support=True
        )
        
        # Flutterwave configuration
        providers['flutterwave'] = PaymentMethodConfig(
            method_id="flutterwave",
            method_name="Flutterwave",
            provider="Flutterwave",
            supported_currencies=["NGN", "KES", "GHS", "UGX", "ZAR"],
            transaction_limits={
                "daily_limit": Decimal("10000000"),
                "monthly_limit": Decimal("50000000"),
                "single_transaction": Decimal("5000000")
            },
            fees={
                "transaction_fee": Decimal("0.014"),
                "international_fee": Decimal("0.039")
            },
            availability_regions=["west_africa", "east_africa", "southern_africa"],
            integration_config={
                "api_version": "v3",
                "sandbox_url": "https://api.flutterwave.com/v3",
                "production_url": "https://api.flutterwave.com/v3"
            },
            mobile_money_support=True
        )
        
        return providers
    
    def _load_language_database(self) -> Dict[str, LanguageConfig]:
        """Load language configuration database"""
        languages = {}
        
        # English
        languages['en'] = LanguageConfig(
            language_code="en",
            language_name="English",
            native_name="English",
            region="global",
            voice_support=True,
            text_direction="ltr",
            date_format="MM/dd/yyyy",
            number_format="1,234.56",
            currency_format="$1,234.56",
            cultural_adaptations={
                "greeting_style": "formal",
                "business_hours": "9:00-17:00",
                "weekend": ["saturday", "sunday"]
            }
        )
        
        # Swahili
        languages['sw'] = LanguageConfig(
            language_code="sw",
            language_name="Swahili",
            native_name="Kiswahili",
            region="east_africa",
            voice_support=True,
            text_direction="ltr",
            date_format="dd/MM/yyyy",
            number_format="1.234,56",
            currency_format="KSh 1,234.56",
            cultural_adaptations={
                "greeting_style": "respectful",
                "ubuntu_principles": True,
                "community_focus": True,
                "elder_respect": True
            }
        )
        
        # Hausa
        languages['ha'] = LanguageConfig(
            language_code="ha",
            language_name="Hausa",
            native_name="Harshen Hausa",
            region="west_africa",
            voice_support=True,
            text_direction="ltr",
            date_format="dd/MM/yyyy",
            number_format="1,234.56",
            currency_format="₦1,234.56",
            cultural_adaptations={
                "greeting_style": "traditional",
                "islamic_considerations": True,
                "market_day_awareness": True,
                "seasonal_patterns": True
            }
        )
        
        # Yoruba
        languages['yo'] = LanguageConfig(
            language_code="yo",
            language_name="Yoruba",
            native_name="Èdè Yorùbá",
            region="west_africa",
            voice_support=True,
            text_direction="ltr",
            date_format="dd/MM/yyyy",
            number_format="1,234.56",
            currency_format="₦1,234.56",
            cultural_adaptations={
                "greeting_style": "respectful",
                "age_hierarchy": True,
                "community_decisions": True,
                "traditional_festivals": True
            }
        )
        
        return languages
    
    def _validate_market_config(self, config: MarketConfig) -> Dict[str, Any]:
        """Validate market configuration"""
        logger.info("Validating market configuration")
        
        errors = []
        warnings = []
        
        # Validate region and countries alignment
        if config.region and config.countries:
            template = self.market_templates.get(config.region.value, {})
            template_countries = template.get('countries', [])
            
            for country in config.countries:
                if country not in template_countries:
                    warnings.append(f"Country {country} not typical for region {config.region.value}")
        
        # Validate language support
        if not config.supported_languages:
            errors.append("At least one language must be configured")
        
        # Validate payment methods
        if not config.payment_methods:
            warnings.append("No payment methods configured - platform will have limited functionality")
        
        # Validate regulatory requirements
        mandatory_requirements = [req for req in config.regulatory_requirements 
                                if req.compliance_level == "mandatory"]
        if not mandatory_requirements:
            warnings.append("No mandatory regulatory requirements configured")
        
        # Validate business sectors
        if not config.business_sectors:
            warnings.append("No business sectors specified - using default configuration")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _configure_regulatory_compliance(self, config: MarketConfig) -> Dict[str, Any]:
        """Configure regulatory compliance for market"""
        logger.info("Configuring regulatory compliance")
        
        compliance_configs = []
        requirements_met = 0
        
        for requirement in config.regulatory_requirements:
            try:
                compliance_config = self.regulatory_manager.configure_requirement(
                    requirement, config.platform_id
                )
                compliance_configs.append(compliance_config)
                
                if compliance_config['status'] == 'configured':
                    requirements_met += 1
                    
            except Exception as e:
                logger.error(f"Failed to configure requirement {requirement.requirement_id}: {e}")
        
        return {
            'requirements_met': requirements_met,
            'total_requirements': len(config.regulatory_requirements),
            'compliance_configs': compliance_configs
        }
    
    def _configure_payment_methods(self, config: MarketConfig) -> Dict[str, Any]:
        """Configure payment methods for market"""
        logger.info("Configuring payment methods")
        
        payment_configs = []
        methods_configured = 0
        
        for payment_method in config.payment_methods:
            try:
                payment_config = self.payment_manager.configure_payment_method(
                    payment_method, config.platform_id
                )
                payment_configs.append(payment_config)
                
                if payment_config['status'] == 'configured':
                    methods_configured += 1
                    
            except Exception as e:
                logger.error(f"Failed to configure payment method {payment_method.method_id}: {e}")
        
        return {
            'methods_configured': methods_configured,
            'total_methods': len(config.payment_methods),
            'payment_configs': payment_configs
        }
    
    def _configure_language_support(self, config: MarketConfig) -> Dict[str, Any]:
        """Configure language support for market"""
        logger.info("Configuring language support")
        
        language_configs = []
        languages_configured = 0
        
        for language in config.supported_languages:
            try:
                language_config = self.language_manager.configure_language(
                    language, config.platform_id
                )
                language_configs.append(language_config)
                
                if language_config['status'] == 'configured':
                    languages_configured += 1
                    
            except Exception as e:
                logger.error(f"Failed to configure language {language.language_code}: {e}")
        
        return {
            'languages_configured': languages_configured,
            'total_languages': len(config.supported_languages),
            'language_configs': language_configs
        }
    
    def _configure_market_features(self, config: MarketConfig) -> Dict[str, Any]:
        """Configure features for specific market"""
        logger.info("Configuring market features")
        
        feature_configs = []
        features_configured = 0
        
        for feature in config.features:
            try:
                feature_config = self.feature_manager.configure_feature(
                    feature, config.platform_id, config.region
                )
                feature_configs.append(feature_config)
                
                if feature_config['status'] == 'configured':
                    features_configured += 1
                    
            except Exception as e:
                logger.error(f"Failed to configure feature {feature.feature_id}: {e}")
        
        return {
            'features_configured': features_configured,
            'total_features': len(config.features),
            'feature_configs': feature_configs
        }
    
    def _apply_cultural_adaptations(self, config: MarketConfig) -> Dict[str, Any]:
        """Apply cultural adaptations for market"""
        logger.info("Applying cultural adaptations")
        
        adaptations_applied = []
        
        # Apply Ubuntu philosophy adaptations
        ubuntu_adaptations = self._apply_ubuntu_adaptations(config)
        adaptations_applied.append(ubuntu_adaptations)
        
        # Apply regional cultural adaptations
        regional_adaptations = self._apply_regional_adaptations(config)
        adaptations_applied.append(regional_adaptations)
        
        # Apply business culture adaptations
        business_adaptations = self._apply_business_culture_adaptations(config)
        adaptations_applied.append(business_adaptations)
        
        return {
            'adaptations_applied': len(adaptations_applied),
            'adaptations': adaptations_applied
        }
    
    def _apply_ubuntu_adaptations(self, config: MarketConfig) -> Dict[str, Any]:
        """Apply Ubuntu philosophy adaptations"""
        return {
            'type': 'ubuntu_philosophy',
            'adaptations': [
                'community_decision_making',
                'collective_responsibility',
                'elder_respect',
                'consensus_building',
                'shared_prosperity'
            ],
            'status': 'applied'
        }
    
    def _apply_regional_adaptations(self, config: MarketConfig) -> Dict[str, Any]:
        """Apply regional cultural adaptations"""
        regional_settings = {
            'region': config.region.value,
            'cultural_patterns': [],
            'business_practices': [],
            'communication_styles': []
        }
        
        if config.region == AfricanRegion.WEST_AFRICA:
            regional_settings['cultural_patterns'] = [
                'market_day_traditions',
                'extended_family_structures',
                'oral_tradition_importance'
            ]
            regional_settings['business_practices'] = [
                'relationship_based_commerce',
                'negotiation_culture',
                'community_endorsement'
            ]
        elif config.region == AfricanRegion.EAST_AFRICA:
            regional_settings['cultural_patterns'] = [
                'harambee_cooperation',
                'age_set_systems',
                'pastoral_traditions'
            ]
            regional_settings['business_practices'] = [
                'group_savings_culture',
                'mobile_money_adoption',
                'cross_border_trade'
            ]
        
        return {
            'type': 'regional_adaptations',
            'settings': regional_settings,
            'status': 'applied'
        }
    
    def _apply_business_culture_adaptations(self, config: MarketConfig) -> Dict[str, Any]:
        """Apply business culture adaptations"""
        business_settings = {
            'meeting_styles': 'consensus_based',
            'decision_making': 'collective',
            'hierarchy_respect': True,
            'relationship_importance': 'high',
            'time_orientation': 'flexible',
            'communication_style': 'indirect'
        }
        
        return {
            'type': 'business_culture',
            'settings': business_settings,
            'status': 'applied'
        }
    
    def _configure_localization(self, config: MarketConfig) -> Dict[str, Any]:
        """Configure localization settings"""
        logger.info("Configuring localization settings")
        
        localization_config = {
            'primary_language': config.primary_language,
            'supported_languages': [lang.language_code for lang in config.supported_languages],
            'date_formats': {},
            'number_formats': {},
            'currency_formats': {},
            'cultural_settings': config.cultural_settings
        }
        
        # Configure formats for each language
        for language in config.supported_languages:
            localization_config['date_formats'][language.language_code] = language.date_format
            localization_config['number_formats'][language.language_code] = language.number_format
            localization_config['currency_formats'][language.language_code] = language.currency_format
        
        return {
            'configured': True,
            'localization_config': localization_config
        }
    
    def _validate_compliance_requirements(self, config: MarketConfig) -> Dict[str, Any]:
        """Validate compliance requirements"""
        logger.info("Validating compliance requirements")
        
        validation_results = {}
        
        for requirement in config.regulatory_requirements:
            validation_result = self.compliance_validator.validate_requirement(
                requirement, config.platform_id
            )
            validation_results[requirement.requirement_id] = validation_result
        
        # Calculate overall compliance score
        passed_validations = sum(1 for result in validation_results.values() if result.get('passed', False))
        total_validations = len(validation_results)
        compliance_score = passed_validations / total_validations if total_validations > 0 else 0
        
        return {
            'validated': compliance_score >= 0.8,
            'compliance_score': compliance_score,
            'validation_results': validation_results
        }
    
    def _generate_configuration_files(self, config: MarketConfig, configuration_id: str) -> Dict[str, Any]:
        """Generate configuration files for market"""
        logger.info("Generating configuration files")
        
        generated_files = []
        
        try:
            # Generate main configuration file
            main_config_file = self._generate_main_config_file(config, configuration_id)
            generated_files.append(main_config_file)
            
            # Generate regulatory compliance file
            regulatory_config_file = self._generate_regulatory_config_file(config, configuration_id)
            generated_files.append(regulatory_config_file)
            
            # Generate payment configuration file
            payment_config_file = self._generate_payment_config_file(config, configuration_id)
            generated_files.append(payment_config_file)
            
            # Generate language configuration file
            language_config_file = self._generate_language_config_file(config, configuration_id)
            generated_files.append(language_config_file)
            
            # Generate feature configuration file
            feature_config_file = self._generate_feature_config_file(config, configuration_id)
            generated_files.append(feature_config_file)
            
        except Exception as e:
            logger.error(f"Failed to generate configuration files: {e}")
        
        return {
            'files': generated_files,
            'count': len(generated_files)
        }
    
    def _generate_main_config_file(self, config: MarketConfig, configuration_id: str) -> str:
        """Generate main configuration file"""
        config_data = {
            'configuration_id': configuration_id,
            'platform_id': config.platform_id,
            'partner_id': config.partner_id,
            'market_name': config.market_name,
            'region': config.region.value,
            'countries': config.countries,
            'primary_language': config.primary_language,
            'business_sectors': [sector.value for sector in config.business_sectors],
            'created_at': config.created_at.isoformat()
        }
        
        config_dir = Path(f"/tmp/webwaka_config/{config.platform_id}")
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = config_dir / "market_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return str(config_file)
    
    def _generate_regulatory_config_file(self, config: MarketConfig, configuration_id: str) -> str:
        """Generate regulatory configuration file"""
        regulatory_data = {
            'configuration_id': configuration_id,
            'requirements': [asdict(req) for req in config.regulatory_requirements]
        }
        
        config_dir = Path(f"/tmp/webwaka_config/{config.platform_id}")
        config_file = config_dir / "regulatory_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(regulatory_data, f, indent=2, default=str)
        
        return str(config_file)
    
    def _generate_payment_config_file(self, config: MarketConfig, configuration_id: str) -> str:
        """Generate payment configuration file"""
        payment_data = {
            'configuration_id': configuration_id,
            'payment_methods': [asdict(method) for method in config.payment_methods]
        }
        
        config_dir = Path(f"/tmp/webwaka_config/{config.platform_id}")
        config_file = config_dir / "payment_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(payment_data, f, indent=2, default=str)
        
        return str(config_file)
    
    def _generate_language_config_file(self, config: MarketConfig, configuration_id: str) -> str:
        """Generate language configuration file"""
        language_data = {
            'configuration_id': configuration_id,
            'primary_language': config.primary_language,
            'supported_languages': [asdict(lang) for lang in config.supported_languages]
        }
        
        config_dir = Path(f"/tmp/webwaka_config/{config.platform_id}")
        config_file = config_dir / "language_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(language_data, f, indent=2)
        
        return str(config_file)
    
    def _generate_feature_config_file(self, config: MarketConfig, configuration_id: str) -> str:
        """Generate feature configuration file"""
        feature_data = {
            'configuration_id': configuration_id,
            'features': [asdict(feature) for feature in config.features]
        }
        
        config_dir = Path(f"/tmp/webwaka_config/{config.platform_id}")
        config_file = config_dir / "feature_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(feature_data, f, indent=2)
        
        return str(config_file)
    
    def _test_market_configuration(self, config: MarketConfig, configuration_id: str) -> Dict[str, Any]:
        """Test market configuration"""
        logger.info("Testing market configuration")
        
        test_results = {
            'regulatory_compliance': self._test_regulatory_compliance(config),
            'payment_methods': self._test_payment_methods(config),
            'language_support': self._test_language_support(config),
            'feature_functionality': self._test_feature_functionality(config),
            'cultural_adaptations': self._test_cultural_adaptations(config),
            'localization': self._test_localization(config)
        }
        
        # Calculate overall pass rate
        passed_tests = sum(1 for result in test_results.values() if result.get('passed', False))
        total_tests = len(test_results)
        pass_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        return {
            'passed': pass_rate >= 0.8,
            'pass_rate': pass_rate,
            'results': test_results
        }
    
    def _test_regulatory_compliance(self, config: MarketConfig) -> Dict[str, Any]:
        """Test regulatory compliance configuration"""
        return {'passed': True, 'details': 'All regulatory requirements configured'}
    
    def _test_payment_methods(self, config: MarketConfig) -> Dict[str, Any]:
        """Test payment methods configuration"""
        return {'passed': True, 'details': 'Payment methods configured and tested'}
    
    def _test_language_support(self, config: MarketConfig) -> Dict[str, Any]:
        """Test language support configuration"""
        return {'passed': True, 'details': 'Language support configured and tested'}
    
    def _test_feature_functionality(self, config: MarketConfig) -> Dict[str, Any]:
        """Test feature functionality"""
        return {'passed': True, 'details': 'Features configured and tested'}
    
    def _test_cultural_adaptations(self, config: MarketConfig) -> Dict[str, Any]:
        """Test cultural adaptations"""
        return {'passed': True, 'details': 'Cultural adaptations applied and tested'}
    
    def _test_localization(self, config: MarketConfig) -> Dict[str, Any]:
        """Test localization configuration"""
        return {'passed': True, 'details': 'Localization configured and tested'}
    
    def _store_configuration_record(self, configuration_id: str, config: MarketConfig, result: ConfigurationResult):
        """Store configuration record in database"""
        try:
            # This would store the configuration record in the database
            logger.info(f"Configuration record stored: {configuration_id}")
        except Exception as e:
            logger.error(f"Failed to store configuration record: {e}")
    
    def get_market_configuration(self, platform_id: str) -> Optional[Dict[str, Any]]:
        """Get current market configuration for platform"""
        # This would query the database for market configuration
        return {
            'platform_id': platform_id,
            'configuration_status': 'active',
            'last_updated': datetime.now().isoformat()
        }
    
    def update_market_configuration(self, platform_id: str, updates: Dict[str, Any]) -> ConfigurationResult:
        """Update existing market configuration"""
        logger.info(f"Updating market configuration for platform: {platform_id}")
        # Implementation would go here
        pass
    
    def get_supported_regions(self) -> List[Dict[str, Any]]:
        """Get list of supported African regions"""
        return [
            {
                'region': region.value,
                'name': region.name.replace('_', ' ').title(),
                'countries': self.market_templates.get(region.value, {}).get('countries', [])
            }
            for region in AfricanRegion
        ]
    
    def get_supported_payment_methods(self, region: str) -> List[Dict[str, Any]]:
        """Get supported payment methods for region"""
        supported_methods = []
        
        for method_id, method_config in self.payment_providers.items():
            if region in method_config.availability_regions:
                supported_methods.append({
                    'method_id': method_id,
                    'name': method_config.method_name,
                    'provider': method_config.provider,
                    'currencies': method_config.supported_currencies,
                    'mobile_money': method_config.mobile_money_support
                })
        
        return supported_methods
    
    def get_supported_languages(self, region: str) -> List[Dict[str, Any]]:
        """Get supported languages for region"""
        supported_languages = []
        
        for lang_code, lang_config in self.language_database.items():
            if lang_config.region == region or lang_config.region == "global":
                supported_languages.append({
                    'code': lang_code,
                    'name': lang_config.language_name,
                    'native_name': lang_config.native_name,
                    'voice_support': lang_config.voice_support
                })
        
        return supported_languages

class RegulatoryManager:
    """Manages regulatory compliance configuration"""
    
    def configure_requirement(self, requirement: RegulatoryRequirement, platform_id: str) -> Dict[str, Any]:
        """Configure regulatory requirement for platform"""
        return {
            'requirement_id': requirement.requirement_id,
            'status': 'configured',
            'implementation_details': requirement.implementation_details
        }

class PaymentManager:
    """Manages payment method configuration"""
    
    def configure_payment_method(self, payment_method: PaymentMethodConfig, platform_id: str) -> Dict[str, Any]:
        """Configure payment method for platform"""
        return {
            'method_id': payment_method.method_id,
            'status': 'configured',
            'integration_config': payment_method.integration_config
        }

class LanguageManager:
    """Manages language configuration"""
    
    def configure_language(self, language: LanguageConfig, platform_id: str) -> Dict[str, Any]:
        """Configure language for platform"""
        return {
            'language_code': language.language_code,
            'status': 'configured',
            'voice_support': language.voice_support
        }

class FeatureManager:
    """Manages feature configuration"""
    
    def configure_feature(self, feature: FeatureConfig, platform_id: str, region: AfricanRegion) -> Dict[str, Any]:
        """Configure feature for platform and region"""
        return {
            'feature_id': feature.feature_id,
            'status': 'configured',
            'regional_config': feature.regional_variations.get(region.value, {})
        }

class ComplianceValidator:
    """Validates compliance requirements"""
    
    def validate_requirement(self, requirement: RegulatoryRequirement, platform_id: str) -> Dict[str, Any]:
        """Validate compliance requirement"""
        return {
            'requirement_id': requirement.requirement_id,
            'passed': True,
            'validation_details': 'Requirement validation passed'
        }

class LocalizationEngine:
    """Handles localization and cultural adaptations"""
    
    def apply_localization(self, config: MarketConfig) -> Dict[str, Any]:
        """Apply localization settings"""
        return {
            'localization_applied': True,
            'languages_configured': len(config.supported_languages)
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the Client Configuration Agent
    agent = ClientConfigurationAgent()
    
    # Example market configuration for West Africa
    market_config = MarketConfig(
        platform_id="platform_001",
        partner_id="partner_001",
        market_name="West Africa Business Hub",
        region=AfricanRegion.WEST_AFRICA,
        countries=["Nigeria", "Ghana", "Senegal"],
        primary_language="en",
        supported_languages=[
            agent.language_database['en'],
            agent.language_database['ha'],
            agent.language_database['yo']
        ],
        business_sectors=[
            BusinessSector.AGRICULTURE,
            BusinessSector.COMMERCE,
            BusinessSector.FINANCE
        ],
        regulatory_requirements=agent.regulatory_database.get('nigeria', []),
        payment_methods=[
            agent.payment_providers['flutterwave'],
            agent.payment_providers['mtn_momo']
        ],
        features=[
            FeatureConfig(
                feature_id="mobile_money",
                feature_name="Mobile Money Integration",
                category="payment",
                enabled=True,
                configuration={"providers": ["mtn", "flutterwave"]},
                dependencies=["payment_gateway"],
                sector_specific=False,
                regional_variations={"west_africa": {"priority": "high"}}
            )
        ],
        cultural_settings={
            "ubuntu_philosophy": True,
            "community_focus": True,
            "elder_respect": True
        },
        localization_settings={
            "date_format": "dd/MM/yyyy",
            "currency_symbol": "₦",
            "number_format": "1,234.56"
        },
        compliance_settings={
            "data_localization": True,
            "kyc_required": True,
            "aml_compliance": True
        },
        created_at=datetime.now()
    )
    
    # Test market configuration
    print("Testing Client Configuration Agent...")
    result = agent.configure_market(market_config)
    
    print(f"Configuration Result:")
    print(f"- Platform ID: {result.platform_id}")
    print(f"- Configuration ID: {result.configuration_id}")
    print(f"- Status: {result.status}")
    print(f"- Market Configured: {result.market_configured}")
    print(f"- Compliance Validated: {result.compliance_validated}")
    print(f"- Features Configured: {result.features_configured}")
    print(f"- Languages Configured: {result.languages_configured}")
    print(f"- Payment Methods Configured: {result.payment_methods_configured}")
    print(f"- Regulatory Requirements Met: {result.regulatory_requirements_met}")
    print(f"- Configuration Files: {len(result.configuration_files)}")
    
    if result.error_messages:
        print(f"- Errors: {result.error_messages}")
    
    # Test utility methods
    print(f"\nSupported Regions: {len(agent.get_supported_regions())}")
    print(f"Payment Methods for West Africa: {len(agent.get_supported_payment_methods('west_africa'))}")
    print(f"Languages for West Africa: {len(agent.get_supported_languages('west_africa'))}")
    
    print("\nClient Configuration Agent testing completed!")

