"""
WebWaka AI Provider Expansion Module
Comprehensive integration with additional AI providers for enhanced capabilities
"""

import json
import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import os
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProviderType(Enum):
    """AI provider types"""
    LLM = "llm"
    SPEECH_TO_TEXT = "speech_to_text"
    TEXT_TO_SPEECH = "text_to_speech"
    IMAGE_GENERATION = "image_generation"
    IMAGE_ANALYSIS = "image_analysis"
    TRANSLATION = "translation"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    EMBEDDINGS = "embeddings"
    VECTOR_DATABASE = "vector_database"

class AIProviderStatus(Enum):
    """AI provider status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"
    MAINTENANCE = "maintenance"

@dataclass
class AIProviderConfig:
    """AI provider configuration"""
    provider_id: str
    name: str
    provider_type: AIProviderType
    api_key: str
    base_url: str
    model_name: Optional[str] = None
    max_requests_per_minute: int = 60
    max_tokens: Optional[int] = None
    temperature: float = 0.7
    timeout: int = 30
    retry_attempts: int = 3
    cost_per_request: float = 0.0
    supports_streaming: bool = False
    african_language_support: List[str] = None
    cultural_adaptation: bool = False

@dataclass
class AIProviderMetrics:
    """AI provider metrics"""
    provider_id: str
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    last_request_time: Optional[datetime] = None
    rate_limit_hits: int = 0
    uptime_percentage: float = 100.0

class AIProviderInterface(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, config: AIProviderConfig):
        self.config = config
        self.status = AIProviderStatus.INACTIVE
        self.metrics = AIProviderMetrics(provider_id=config.provider_id)
        self.session: Optional[aiohttp.ClientSession] = None
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the AI provider"""
        pass
    
    @abstractmethod
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process AI request"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check provider health"""
        pass
    
    async def shutdown(self):
        """Shutdown the provider"""
        if self.session:
            await self.session.close()
        self.status = AIProviderStatus.INACTIVE

class GoogleVertexAIProvider(AIProviderInterface):
    """Google Vertex AI provider for advanced LLM capabilities"""
    
    def __init__(self, config: AIProviderConfig):
        super().__init__(config)
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        self.location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        
    async def initialize(self) -> bool:
        """Initialize Google Vertex AI"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Test authentication
            auth_test = await self.health_check()
            if auth_test:
                self.status = AIProviderStatus.ACTIVE
                logger.info(f"Google Vertex AI provider {self.config.provider_id} initialized")
                return True
            else:
                self.status = AIProviderStatus.ERROR
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize Google Vertex AI: {e}")
            self.status = AIProviderStatus.ERROR
            return False
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process request with Google Vertex AI"""
        try:
            start_time = datetime.now()
            
            # Prepare request for Vertex AI
            endpoint = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.config.model_name}:predict"
            
            headers = {
                'Authorization': f'Bearer {self.config.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "instances": [
                    {
                        "prompt": request_data.get('prompt', ''),
                        "max_output_tokens": request_data.get('max_tokens', 1024),
                        "temperature": request_data.get('temperature', self.config.temperature)
                    }
                ]
            }
            
            async with self.session.post(endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Update metrics
                    processing_time = (datetime.now() - start_time).total_seconds()
                    self.metrics.successful_requests += 1
                    self.metrics.total_requests += 1
                    self.metrics.average_response_time = (
                        (self.metrics.average_response_time * (self.metrics.total_requests - 1) + processing_time) /
                        self.metrics.total_requests
                    )
                    self.metrics.last_request_time = datetime.now()
                    
                    return {
                        'success': True,
                        'response': result.get('predictions', [{}])[0].get('content', ''),
                        'provider': 'google_vertex_ai',
                        'processing_time': processing_time,
                        'tokens_used': result.get('metadata', {}).get('tokenMetadata', {}).get('outputTokenCount', 0)
                    }
                else:
                    error_text = await response.text()
                    self.metrics.failed_requests += 1
                    self.metrics.total_requests += 1
                    
                    return {
                        'success': False,
                        'error': f"HTTP {response.status}: {error_text}",
                        'provider': 'google_vertex_ai'
                    }
                    
        except Exception as e:
            logger.error(f"Google Vertex AI request failed: {e}")
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            
            return {
                'success': False,
                'error': str(e),
                'provider': 'google_vertex_ai'
            }
    
    async def health_check(self) -> bool:
        """Check Google Vertex AI health"""
        try:
            # Simple health check - list models
            endpoint = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models"
            
            headers = {
                'Authorization': f'Bearer {self.config.api_key}'
            }
            
            async with self.session.get(endpoint, headers=headers) as response:
                return response.status == 200
                
        except Exception as e:
            logger.error(f"Google Vertex AI health check failed: {e}")
            return False

class AWSBedrockProvider(AIProviderInterface):
    """AWS Bedrock provider for enterprise AI capabilities"""
    
    def __init__(self, config: AIProviderConfig):
        super().__init__(config)
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        
    async def initialize(self) -> bool:
        """Initialize AWS Bedrock"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Test authentication
            auth_test = await self.health_check()
            if auth_test:
                self.status = AIProviderStatus.ACTIVE
                logger.info(f"AWS Bedrock provider {self.config.provider_id} initialized")
                return True
            else:
                self.status = AIProviderStatus.ERROR
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock: {e}")
            self.status = AIProviderStatus.ERROR
            return False
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process request with AWS Bedrock"""
        try:
            start_time = datetime.now()
            
            # Prepare request for Bedrock
            endpoint = f"https://bedrock-runtime.{self.region}.amazonaws.com/model/{self.config.model_name}/invoke"
            
            headers = {
                'Authorization': f'AWS4-HMAC-SHA256 {self.config.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            payload = {
                "prompt": request_data.get('prompt', ''),
                "max_tokens_to_sample": request_data.get('max_tokens', 1024),
                "temperature": request_data.get('temperature', self.config.temperature),
                "stop_sequences": request_data.get('stop_sequences', [])
            }
            
            async with self.session.post(endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Update metrics
                    processing_time = (datetime.now() - start_time).total_seconds()
                    self.metrics.successful_requests += 1
                    self.metrics.total_requests += 1
                    self.metrics.average_response_time = (
                        (self.metrics.average_response_time * (self.metrics.total_requests - 1) + processing_time) /
                        self.metrics.total_requests
                    )
                    self.metrics.last_request_time = datetime.now()
                    
                    return {
                        'success': True,
                        'response': result.get('completion', ''),
                        'provider': 'aws_bedrock',
                        'processing_time': processing_time,
                        'tokens_used': result.get('usage', {}).get('output_tokens', 0)
                    }
                else:
                    error_text = await response.text()
                    self.metrics.failed_requests += 1
                    self.metrics.total_requests += 1
                    
                    return {
                        'success': False,
                        'error': f"HTTP {response.status}: {error_text}",
                        'provider': 'aws_bedrock'
                    }
                    
        except Exception as e:
            logger.error(f"AWS Bedrock request failed: {e}")
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            
            return {
                'success': False,
                'error': str(e),
                'provider': 'aws_bedrock'
            }
    
    async def health_check(self) -> bool:
        """Check AWS Bedrock health"""
        try:
            # Simple health check - list foundation models
            endpoint = f"https://bedrock.{self.region}.amazonaws.com/foundation-models"
            
            headers = {
                'Authorization': f'AWS4-HMAC-SHA256 {self.config.api_key}'
            }
            
            async with self.session.get(endpoint, headers=headers) as response:
                return response.status == 200
                
        except Exception as e:
            logger.error(f"AWS Bedrock health check failed: {e}")
            return False

class StabilityAIProvider(AIProviderInterface):
    """Stability AI provider for image generation"""
    
    async def initialize(self) -> bool:
        """Initialize Stability AI"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Test authentication
            auth_test = await self.health_check()
            if auth_test:
                self.status = AIProviderStatus.ACTIVE
                logger.info(f"Stability AI provider {self.config.provider_id} initialized")
                return True
            else:
                self.status = AIProviderStatus.ERROR
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize Stability AI: {e}")
            self.status = AIProviderStatus.ERROR
            return False
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process image generation request with Stability AI"""
        try:
            start_time = datetime.now()
            
            endpoint = f"{self.config.base_url}/v1/generation/{self.config.model_name}/text-to-image"
            
            headers = {
                'Authorization': f'Bearer {self.config.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            payload = {
                "text_prompts": [
                    {
                        "text": request_data.get('prompt', ''),
                        "weight": 1.0
                    }
                ],
                "cfg_scale": request_data.get('cfg_scale', 7),
                "height": request_data.get('height', 512),
                "width": request_data.get('width', 512),
                "samples": request_data.get('samples', 1),
                "steps": request_data.get('steps', 30)
            }
            
            async with self.session.post(endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Update metrics
                    processing_time = (datetime.now() - start_time).total_seconds()
                    self.metrics.successful_requests += 1
                    self.metrics.total_requests += 1
                    self.metrics.average_response_time = (
                        (self.metrics.average_response_time * (self.metrics.total_requests - 1) + processing_time) /
                        self.metrics.total_requests
                    )
                    self.metrics.last_request_time = datetime.now()
                    
                    return {
                        'success': True,
                        'images': result.get('artifacts', []),
                        'provider': 'stability_ai',
                        'processing_time': processing_time
                    }
                else:
                    error_text = await response.text()
                    self.metrics.failed_requests += 1
                    self.metrics.total_requests += 1
                    
                    return {
                        'success': False,
                        'error': f"HTTP {response.status}: {error_text}",
                        'provider': 'stability_ai'
                    }
                    
        except Exception as e:
            logger.error(f"Stability AI request failed: {e}")
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            
            return {
                'success': False,
                'error': str(e),
                'provider': 'stability_ai'
            }
    
    async def health_check(self) -> bool:
        """Check Stability AI health"""
        try:
            endpoint = f"{self.config.base_url}/v1/user/account"
            
            headers = {
                'Authorization': f'Bearer {self.config.api_key}'
            }
            
            async with self.session.get(endpoint, headers=headers) as response:
                return response.status == 200
                
        except Exception as e:
            logger.error(f"Stability AI health check failed: {e}")
            return False

class ElevenLabsProvider(AIProviderInterface):
    """ElevenLabs provider for advanced text-to-speech"""
    
    async def initialize(self) -> bool:
        """Initialize ElevenLabs"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Test authentication
            auth_test = await self.health_check()
            if auth_test:
                self.status = AIProviderStatus.ACTIVE
                logger.info(f"ElevenLabs provider {self.config.provider_id} initialized")
                return True
            else:
                self.status = AIProviderStatus.ERROR
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize ElevenLabs: {e}")
            self.status = AIProviderStatus.ERROR
            return False
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process text-to-speech request with ElevenLabs"""
        try:
            start_time = datetime.now()
            
            voice_id = request_data.get('voice_id', 'pNInz6obpgDQGcFmaJgB')  # Default voice
            endpoint = f"{self.config.base_url}/v1/text-to-speech/{voice_id}"
            
            headers = {
                'xi-api-key': self.config.api_key,
                'Content-Type': 'application/json',
                'Accept': 'audio/mpeg'
            }
            
            payload = {
                "text": request_data.get('text', ''),
                "model_id": request_data.get('model_id', 'eleven_monolingual_v1'),
                "voice_settings": {
                    "stability": request_data.get('stability', 0.5),
                    "similarity_boost": request_data.get('similarity_boost', 0.5)
                }
            }
            
            async with self.session.post(endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    
                    # Update metrics
                    processing_time = (datetime.now() - start_time).total_seconds()
                    self.metrics.successful_requests += 1
                    self.metrics.total_requests += 1
                    self.metrics.average_response_time = (
                        (self.metrics.average_response_time * (self.metrics.total_requests - 1) + processing_time) /
                        self.metrics.total_requests
                    )
                    self.metrics.last_request_time = datetime.now()
                    
                    return {
                        'success': True,
                        'audio_data': audio_data,
                        'provider': 'elevenlabs',
                        'processing_time': processing_time,
                        'content_type': 'audio/mpeg'
                    }
                else:
                    error_text = await response.text()
                    self.metrics.failed_requests += 1
                    self.metrics.total_requests += 1
                    
                    return {
                        'success': False,
                        'error': f"HTTP {response.status}: {error_text}",
                        'provider': 'elevenlabs'
                    }
                    
        except Exception as e:
            logger.error(f"ElevenLabs request failed: {e}")
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            
            return {
                'success': False,
                'error': str(e),
                'provider': 'elevenlabs'
            }
    
    async def health_check(self) -> bool:
        """Check ElevenLabs health"""
        try:
            endpoint = f"{self.config.base_url}/v1/user"
            
            headers = {
                'xi-api-key': self.config.api_key
            }
            
            async with self.session.get(endpoint, headers=headers) as response:
                return response.status == 200
                
        except Exception as e:
            logger.error(f"ElevenLabs health check failed: {e}")
            return False

class AssemblyAIProvider(AIProviderInterface):
    """AssemblyAI provider for advanced speech-to-text"""
    
    async def initialize(self) -> bool:
        """Initialize AssemblyAI"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
            
            # Test authentication
            auth_test = await self.health_check()
            if auth_test:
                self.status = AIProviderStatus.ACTIVE
                logger.info(f"AssemblyAI provider {self.config.provider_id} initialized")
                return True
            else:
                self.status = AIProviderStatus.ERROR
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize AssemblyAI: {e}")
            self.status = AIProviderStatus.ERROR
            return False
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process speech-to-text request with AssemblyAI"""
        try:
            start_time = datetime.now()
            
            # First upload audio file
            upload_endpoint = f"{self.config.base_url}/v2/upload"
            headers = {'authorization': self.config.api_key}
            
            audio_data = request_data.get('audio_data')
            if not audio_data:
                return {
                    'success': False,
                    'error': 'No audio data provided',
                    'provider': 'assemblyai'
                }
            
            # Upload audio
            async with self.session.post(upload_endpoint, data=audio_data, headers=headers) as upload_response:
                if upload_response.status != 200:
                    return {
                        'success': False,
                        'error': f'Audio upload failed: {upload_response.status}',
                        'provider': 'assemblyai'
                    }
                
                upload_result = await upload_response.json()
                audio_url = upload_result.get('upload_url')
            
            # Create transcription job
            transcript_endpoint = f"{self.config.base_url}/v2/transcript"
            transcript_payload = {
                "audio_url": audio_url,
                "language_detection": request_data.get('language_detection', True),
                "speaker_labels": request_data.get('speaker_labels', False),
                "punctuate": request_data.get('punctuate', True),
                "format_text": request_data.get('format_text', True)
            }
            
            async with self.session.post(transcript_endpoint, json=transcript_payload, headers=headers) as transcript_response:
                if transcript_response.status == 200:
                    transcript_result = await transcript_response.json()
                    transcript_id = transcript_result.get('id')
                    
                    # Poll for completion
                    status_endpoint = f"{self.config.base_url}/v2/transcript/{transcript_id}"
                    
                    while True:
                        await asyncio.sleep(2)  # Wait 2 seconds between polls
                        
                        async with self.session.get(status_endpoint, headers=headers) as status_response:
                            if status_response.status == 200:
                                status_result = await status_response.json()
                                status = status_result.get('status')
                                
                                if status == 'completed':
                                    # Update metrics
                                    processing_time = (datetime.now() - start_time).total_seconds()
                                    self.metrics.successful_requests += 1
                                    self.metrics.total_requests += 1
                                    self.metrics.average_response_time = (
                                        (self.metrics.average_response_time * (self.metrics.total_requests - 1) + processing_time) /
                                        self.metrics.total_requests
                                    )
                                    self.metrics.last_request_time = datetime.now()
                                    
                                    return {
                                        'success': True,
                                        'transcript': status_result.get('text', ''),
                                        'confidence': status_result.get('confidence', 0.0),
                                        'language': status_result.get('language_code'),
                                        'provider': 'assemblyai',
                                        'processing_time': processing_time
                                    }
                                elif status == 'error':
                                    self.metrics.failed_requests += 1
                                    self.metrics.total_requests += 1
                                    
                                    return {
                                        'success': False,
                                        'error': status_result.get('error', 'Transcription failed'),
                                        'provider': 'assemblyai'
                                    }
                            else:
                                break
                    
                    return {
                        'success': False,
                        'error': 'Failed to get transcription status',
                        'provider': 'assemblyai'
                    }
                else:
                    error_text = await transcript_response.text()
                    self.metrics.failed_requests += 1
                    self.metrics.total_requests += 1
                    
                    return {
                        'success': False,
                        'error': f"HTTP {transcript_response.status}: {error_text}",
                        'provider': 'assemblyai'
                    }
                    
        except Exception as e:
            logger.error(f"AssemblyAI request failed: {e}")
            self.metrics.failed_requests += 1
            self.metrics.total_requests += 1
            
            return {
                'success': False,
                'error': str(e),
                'provider': 'assemblyai'
            }
    
    async def health_check(self) -> bool:
        """Check AssemblyAI health"""
        try:
            endpoint = f"{self.config.base_url}/v2/transcript"
            
            headers = {
                'authorization': self.config.api_key
            }
            
            # Simple GET request to check API availability
            async with self.session.get(endpoint, headers=headers) as response:
                return response.status in [200, 400]  # 400 is expected for GET without parameters
                
        except Exception as e:
            logger.error(f"AssemblyAI health check failed: {e}")
            return False

class AIProviderManager:
    """Enhanced AI Provider Manager with expanded capabilities"""
    
    def __init__(self):
        self.providers: Dict[str, AIProviderInterface] = {}
        self.provider_configs: Dict[str, AIProviderConfig] = {}
        self.load_balancer_weights: Dict[str, float] = {}
        self.cost_tracker: Dict[str, float] = {}
        
    def register_provider(self, config: AIProviderConfig, provider_class: type):
        """Register a new AI provider"""
        try:
            provider = provider_class(config)
            self.providers[config.provider_id] = provider
            self.provider_configs[config.provider_id] = config
            self.load_balancer_weights[config.provider_id] = 1.0
            self.cost_tracker[config.provider_id] = 0.0
            
            logger.info(f"Registered AI provider: {config.provider_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register provider {config.provider_id}: {e}")
            return False
    
    async def initialize_all_providers(self) -> Dict[str, bool]:
        """Initialize all registered providers"""
        results = {}
        
        for provider_id, provider in self.providers.items():
            try:
                success = await provider.initialize()
                results[provider_id] = success
                
                if success:
                    logger.info(f"Successfully initialized provider: {provider_id}")
                else:
                    logger.error(f"Failed to initialize provider: {provider_id}")
                    
            except Exception as e:
                logger.error(f"Error initializing provider {provider_id}: {e}")
                results[provider_id] = False
        
        return results
    
    async def get_best_provider(self, provider_type: AIProviderType, 
                               requirements: Dict[str, Any] = None) -> Optional[str]:
        """Get the best provider for a specific type and requirements"""
        try:
            suitable_providers = []
            
            for provider_id, config in self.provider_configs.items():
                if config.provider_type == provider_type:
                    provider = self.providers[provider_id]
                    
                    # Check if provider is active
                    if provider.status != AIProviderStatus.ACTIVE:
                        continue
                    
                    # Check requirements
                    if requirements:
                        # Check African language support
                        if requirements.get('african_language') and not config.african_language_support:
                            continue
                        
                        # Check cultural adaptation
                        if requirements.get('cultural_adaptation') and not config.cultural_adaptation:
                            continue
                        
                        # Check cost constraints
                        max_cost = requirements.get('max_cost_per_request')
                        if max_cost and config.cost_per_request > max_cost:
                            continue
                    
                    # Calculate score based on performance and cost
                    performance_score = (
                        provider.metrics.uptime_percentage * 0.4 +
                        (100 - provider.metrics.average_response_time) * 0.3 +
                        (provider.metrics.successful_requests / max(provider.metrics.total_requests, 1)) * 100 * 0.3
                    )
                    
                    cost_score = 100 - (config.cost_per_request * 1000)  # Lower cost = higher score
                    
                    total_score = (performance_score * 0.7 + cost_score * 0.3) * self.load_balancer_weights[provider_id]
                    
                    suitable_providers.append((provider_id, total_score))
            
            if suitable_providers:
                # Sort by score and return the best
                suitable_providers.sort(key=lambda x: x[1], reverse=True)
                return suitable_providers[0][0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error selecting best provider: {e}")
            return None
    
    async def process_with_fallback(self, provider_type: AIProviderType, 
                                   request_data: Dict[str, Any],
                                   requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process request with automatic fallback to alternative providers"""
        try:
            # Get ordered list of suitable providers
            suitable_providers = []
            
            for provider_id, config in self.provider_configs.items():
                if config.provider_type == provider_type:
                    provider = self.providers[provider_id]
                    
                    if provider.status == AIProviderStatus.ACTIVE:
                        # Calculate score
                        performance_score = (
                            provider.metrics.uptime_percentage * 0.4 +
                            (100 - provider.metrics.average_response_time) * 0.3 +
                            (provider.metrics.successful_requests / max(provider.metrics.total_requests, 1)) * 100 * 0.3
                        )
                        
                        cost_score = 100 - (config.cost_per_request * 1000)
                        total_score = (performance_score * 0.7 + cost_score * 0.3) * self.load_balancer_weights[provider_id]
                        
                        suitable_providers.append((provider_id, total_score))
            
            # Sort by score
            suitable_providers.sort(key=lambda x: x[1], reverse=True)
            
            # Try each provider in order
            for provider_id, _ in suitable_providers:
                try:
                    provider = self.providers[provider_id]
                    result = await provider.process_request(request_data)
                    
                    if result.get('success'):
                        # Update cost tracking
                        self.cost_tracker[provider_id] += self.provider_configs[provider_id].cost_per_request
                        return result
                    else:
                        logger.warning(f"Provider {provider_id} failed: {result.get('error')}")
                        continue
                        
                except Exception as e:
                    logger.error(f"Error with provider {provider_id}: {e}")
                    continue
            
            return {
                'success': False,
                'error': 'All suitable providers failed',
                'provider_type': provider_type.value
            }
            
        except Exception as e:
            logger.error(f"Error in process_with_fallback: {e}")
            return {
                'success': False,
                'error': str(e),
                'provider_type': provider_type.value
            }
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics for all providers"""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'total_providers': len(self.providers),
                'active_providers': 0,
                'total_requests': 0,
                'total_cost': sum(self.cost_tracker.values()),
                'providers': {}
            }
            
            for provider_id, provider in self.providers.items():
                provider_metrics = {
                    'status': provider.status.value,
                    'metrics': asdict(provider.metrics),
                    'config': {
                        'name': provider.config.name,
                        'type': provider.config.provider_type.value,
                        'cost_per_request': provider.config.cost_per_request,
                        'african_language_support': provider.config.african_language_support,
                        'cultural_adaptation': provider.config.cultural_adaptation
                    },
                    'total_cost': self.cost_tracker[provider_id]
                }
                
                metrics['providers'][provider_id] = provider_metrics
                
                if provider.status == AIProviderStatus.ACTIVE:
                    metrics['active_providers'] += 1
                
                metrics['total_requests'] += provider.metrics.total_requests
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def shutdown_all_providers(self):
        """Shutdown all providers gracefully"""
        for provider_id, provider in self.providers.items():
            try:
                await provider.shutdown()
                logger.info(f"Shutdown provider: {provider_id}")
            except Exception as e:
                logger.error(f"Error shutting down provider {provider_id}: {e}")

# Global AI provider manager instance
ai_provider_manager = AIProviderManager()

# Export key classes and functions
__all__ = [
    'AIProviderType',
    'AIProviderStatus',
    'AIProviderConfig',
    'AIProviderInterface',
    'GoogleVertexAIProvider',
    'AWSBedrockProvider',
    'StabilityAIProvider',
    'ElevenLabsProvider',
    'AssemblyAIProvider',
    'AIProviderManager',
    'ai_provider_manager'
]



# Enhanced Error Handling Patterns for Grand Rule 5 Compliance

class AIProviderError(Exception):
    """Base exception for AI provider errors"""
    def __init__(self, message: str, provider_type: str = None, error_code: str = None):
        super().__init__(message)
        self.provider_type = provider_type
        self.error_code = error_code
        self.timestamp = datetime.now()

class ConnectionError(AIProviderError):
    """Connection-related errors"""
    pass

class AuthenticationError(AIProviderError):
    """Authentication-related errors"""
    pass

class RateLimitError(AIProviderError):
    """Rate limiting errors"""
    pass

class ConfigurationError(AIProviderError):
    """Configuration-related errors"""
    pass

class ErrorHandler:
    """Centralized error handling for AI providers"""
    
    @staticmethod
    def handle_provider_error(error: Exception, provider_type: str, operation: str) -> Dict[str, Any]:
        """Handle and categorize provider errors"""
        try:
            error_info = {
                'timestamp': datetime.now().isoformat(),
                'provider_type': provider_type,
                'operation': operation,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'severity': 'high'
            }
            
            # Categorize error types
            if isinstance(error, (ConnectionError, aiohttp.ClientConnectorError)):
                error_info['category'] = 'connection'
                error_info['retry_recommended'] = True
                logger.error(f"Connection error in {provider_type} during {operation}: {error}")
                
            elif isinstance(error, (AuthenticationError, aiohttp.ClientResponseError)):
                if hasattr(error, 'status') and error.status in [401, 403]:
                    error_info['category'] = 'authentication'
                    error_info['retry_recommended'] = False
                    error_info['severity'] = 'critical'
                    logger.error(f"Authentication error in {provider_type}: {error}")
                else:
                    error_info['category'] = 'api_error'
                    error_info['retry_recommended'] = True
                    logger.error(f"API error in {provider_type}: {error}")
                    
            elif isinstance(error, (RateLimitError, asyncio.TimeoutError)):
                error_info['category'] = 'rate_limit'
                error_info['retry_recommended'] = True
                error_info['retry_delay'] = 60  # seconds
                logger.warning(f"Rate limit/timeout in {provider_type}: {error}")
                
            elif isinstance(error, (ConfigurationError, ValueError, KeyError)):
                error_info['category'] = 'configuration'
                error_info['retry_recommended'] = False
                error_info['severity'] = 'critical'
                logger.error(f"Configuration error in {provider_type}: {error}")
                
            else:
                error_info['category'] = 'unknown'
                error_info['retry_recommended'] = False
                error_info['severity'] = 'critical'
                logger.error(f"Unknown error in {provider_type} during {operation}: {error}")
            
            return error_info
            
        except Exception as handler_error:
            logger.critical(f"Error handler itself failed: {handler_error}")
            return {
                'timestamp': datetime.now().isoformat(),
                'provider_type': provider_type,
                'operation': operation,
                'error_type': 'handler_failure',
                'error_message': str(handler_error),
                'severity': 'critical',
                'category': 'system',
                'retry_recommended': False
            }
    
    @staticmethod
    def should_retry(error_info: Dict[str, Any], attempt_count: int, max_retries: int = 3) -> bool:
        """Determine if operation should be retried"""
        try:
            if attempt_count >= max_retries:
                logger.warning(f"Max retries ({max_retries}) reached for {error_info.get('provider_type')}")
                return False
            
            if not error_info.get('retry_recommended', False):
                logger.info(f"Retry not recommended for {error_info.get('category')} error")
                return False
            
            if error_info.get('severity') == 'critical':
                logger.error(f"Critical error, no retry: {error_info.get('error_message')}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in retry logic: {e}")
            return False
    
    @staticmethod
    def get_retry_delay(error_info: Dict[str, Any], attempt_count: int) -> int:
        """Calculate retry delay with exponential backoff"""
        try:
            base_delay = error_info.get('retry_delay', 5)
            exponential_delay = base_delay * (2 ** (attempt_count - 1))
            max_delay = 300  # 5 minutes maximum
            
            delay = min(exponential_delay, max_delay)
            logger.info(f"Retry delay calculated: {delay}s for attempt {attempt_count}")
            return delay
            
        except Exception as e:
            logger.error(f"Error calculating retry delay: {e}")
            return 30  # Default 30 seconds

# Enhanced AIProviderManager with comprehensive error handling
class EnhancedAIProviderManager(AIProviderManager):
    """Enhanced AI Provider Manager with comprehensive error handling"""
    
    def __init__(self):
        super().__init__()
        self.error_handler = ErrorHandler()
        self.error_history: List[Dict[str, Any]] = []
        self.max_error_history = 1000
    
    async def initialize_provider_with_retry(self, provider_type: AIProviderType, max_retries: int = 3) -> Optional[AIProviderInterface]:
        """Initialize provider with comprehensive error handling and retry logic"""
        attempt_count = 0
        
        while attempt_count < max_retries:
            try:
                attempt_count += 1
                logger.info(f"Initializing {provider_type.value} (attempt {attempt_count}/{max_retries})")
                
                provider = await self.initialize_provider(provider_type)
                if provider:
                    logger.info(f"Successfully initialized {provider_type.value}")
                    return provider
                else:
                    raise ConfigurationError(f"Provider {provider_type.value} returned None")
                    
            except Exception as e:
                error_info = self.error_handler.handle_provider_error(e, provider_type.value, "initialization")
                self._record_error(error_info)
                
                if self.error_handler.should_retry(error_info, attempt_count, max_retries):
                    delay = self.error_handler.get_retry_delay(error_info, attempt_count)
                    logger.info(f"Retrying {provider_type.value} initialization in {delay}s")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Failed to initialize {provider_type.value} after {attempt_count} attempts")
                    return None
        
        logger.error(f"Exhausted all retry attempts for {provider_type.value}")
        return None
    
    def _record_error(self, error_info: Dict[str, Any]):
        """Record error in history with rotation"""
        try:
            self.error_history.append(error_info)
            
            # Rotate error history if it gets too large
            if len(self.error_history) > self.max_error_history:
                self.error_history = self.error_history[-self.max_error_history:]
                logger.info(f"Rotated error history, keeping last {self.max_error_history} entries")
                
        except Exception as e:
            logger.error(f"Failed to record error: {e}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get comprehensive error summary"""
        try:
            if not self.error_history:
                return {"total_errors": 0, "summary": "No errors recorded"}
            
            # Categorize errors
            error_categories = {}
            provider_errors = {}
            severity_counts = {}
            
            for error in self.error_history:
                # Count by category
                category = error.get('category', 'unknown')
                error_categories[category] = error_categories.get(category, 0) + 1
                
                # Count by provider
                provider = error.get('provider_type', 'unknown')
                provider_errors[provider] = provider_errors.get(provider, 0) + 1
                
                # Count by severity
                severity = error.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            return {
                "total_errors": len(self.error_history),
                "error_categories": error_categories,
                "provider_errors": provider_errors,
                "severity_counts": severity_counts,
                "recent_errors": self.error_history[-10:] if len(self.error_history) > 10 else self.error_history
            }
            
        except Exception as e:
            logger.error(f"Failed to generate error summary: {e}")
            return {"error": "Failed to generate summary", "exception": str(e)}

# Global enhanced manager instance
enhanced_ai_manager = EnhancedAIProviderManager()

# Error handling decorators
def handle_provider_errors(provider_type: str = "unknown", operation: str = "unknown"):
    """Decorator for comprehensive error handling"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_info = ErrorHandler.handle_provider_error(e, provider_type, operation)
                enhanced_ai_manager._record_error(error_info)
                raise
        return wrapper
    return decorator

def graceful_degradation(fallback_value=None, log_error=True):
    """Decorator for graceful degradation on errors"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.warning(f"Graceful degradation in {func.__name__}: {e}")
                return fallback_value
        return wrapper
    return decorator

# Validation functions
def validate_provider_config(config: AIProviderConfig) -> bool:
    """Validate provider configuration with comprehensive checks"""
    try:
        if not config:
            raise ConfigurationError("Provider configuration is None")
        
        if not config.provider_id:
            raise ConfigurationError("Provider ID is required")
        
        if not config.api_key:
            raise ConfigurationError("API key is required")
        
        if config.timeout <= 0:
            raise ConfigurationError("Timeout must be positive")
        
        if config.max_retries < 0:
            raise ConfigurationError("Max retries cannot be negative")
        
        logger.info(f"Provider configuration validated for {config.provider_id}")
        return True
        
    except Exception as e:
        logger.error(f"Provider configuration validation failed: {e}")
        raise ConfigurationError(f"Configuration validation failed: {e}")

def validate_request_data(request_data: Dict[str, Any]) -> bool:
    """Validate request data with comprehensive checks"""
    try:
        if not isinstance(request_data, dict):
            raise ValueError("Request data must be a dictionary")
        
        if not request_data:
            raise ValueError("Request data cannot be empty")
        
        # Check for required fields (can be customized per provider)
        required_fields = ['prompt', 'model']  # Basic requirements
        for field in required_fields:
            if field not in request_data:
                logger.warning(f"Optional field '{field}' not found in request data")
        
        logger.debug("Request data validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Request data validation failed: {e}")
        raise ValueError(f"Request validation failed: {e}")

# Health check functions with error handling
async def comprehensive_health_check() -> Dict[str, Any]:
    """Perform comprehensive health check with error handling"""
    try:
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "provider_status": {},
            "error_summary": enhanced_ai_manager.get_error_summary(),
            "system_metrics": {
                "active_providers": 0,
                "total_providers": 0,
                "error_rate": 0.0
            }
        }
        
        # Check each provider
        for provider_type in AIProviderType:
            try:
                provider = enhanced_ai_manager.providers.get(provider_type)
                if provider:
                    is_healthy = await provider.health_check()
                    health_status["provider_status"][provider_type.value] = {
                        "status": "healthy" if is_healthy else "unhealthy",
                        "last_check": datetime.now().isoformat()
                    }
                    if is_healthy:
                        health_status["system_metrics"]["active_providers"] += 1
                else:
                    health_status["provider_status"][provider_type.value] = {
                        "status": "not_initialized",
                        "last_check": datetime.now().isoformat()
                    }
                
                health_status["system_metrics"]["total_providers"] += 1
                
            except Exception as e:
                logger.error(f"Health check failed for {provider_type.value}: {e}")
                health_status["provider_status"][provider_type.value] = {
                    "status": "error",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        # Calculate overall health
        active_providers = health_status["system_metrics"]["active_providers"]
        total_providers = health_status["system_metrics"]["total_providers"]
        
        if active_providers == 0:
            health_status["overall_status"] = "critical"
        elif active_providers < total_providers / 2:
            health_status["overall_status"] = "degraded"
        
        # Calculate error rate
        error_count = health_status["error_summary"]["total_errors"]
        if error_count > 0:
            health_status["system_metrics"]["error_rate"] = error_count / max(total_providers, 1)
        
        return health_status
        
    except Exception as e:
        logger.critical(f"Comprehensive health check failed: {e}")
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "critical",
            "error": str(e),
            "system_metrics": {"error": "Health check system failure"}
        }

# Export enhanced components
__all__ = [
    'AIProviderError', 'ConnectionError', 'AuthenticationError', 'RateLimitError', 'ConfigurationError',
    'ErrorHandler', 'EnhancedAIProviderManager', 'enhanced_ai_manager',
    'handle_provider_errors', 'graceful_degradation',
    'validate_provider_config', 'validate_request_data', 'comprehensive_health_check'
]

