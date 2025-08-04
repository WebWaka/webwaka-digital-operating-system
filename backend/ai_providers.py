"""
WebWaka AI Providers Integration
Direct implementation for backend API integration
"""

import os
import requests
import json
from typing import Dict, Any, List, Optional

class AIProviderManager:
    """Manages all AI provider integrations for WebWaka"""
    
    def __init__(self):
        self.providers = {}
        self.initialize_providers()
    
    def initialize_providers(self):
        """Initialize all AI providers"""
        # Eden AI
        if os.getenv('EDEN_AI_API_KEY'):
            self.providers['eden'] = EdenAIProvider()
        
        # Hugging Face
        if os.getenv('HUGGINGFACE_API_KEY'):
            self.providers['huggingface'] = HuggingFaceProvider()
        
        # OpenRouter
        if os.getenv('OPENROUTER_API_KEY'):
            self.providers['openrouter'] = OpenRouterProvider()
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all AI providers"""
        status = {
            'providers': {},
            'total_providers': len(self.providers),
            'available_providers': 0
        }
        
        for name, provider in self.providers.items():
            provider_status = provider.get_status()
            status['providers'][name] = provider_status
            if provider_status['available']:
                status['available_providers'] += 1
        
        return status
    
    def test_providers(self) -> Dict[str, Any]:
        """Test all AI providers"""
        results = {}
        
        for name, provider in self.providers.items():
            try:
                result = provider.test_connection()
                results[name] = {
                    'success': True,
                    'response': result,
                    'error': None
                }
            except Exception as e:
                results[name] = {
                    'success': False,
                    'response': None,
                    'error': str(e)
                }
        
        return results

class BaseAIProvider:
    """Base class for AI providers"""
    
    def __init__(self, name: str, api_key: str, base_url: str):
        self.name = name
        self.api_key = api_key
        self.base_url = base_url
        self.available = bool(api_key)
    
    def get_status(self) -> Dict[str, Any]:
        """Get provider status"""
        return {
            'name': self.name,
            'available': self.available,
            'api_key_configured': bool(self.api_key),
            'base_url': self.base_url
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test provider connection - override in subclasses"""
        raise NotImplementedError("Subclasses must implement test_connection")

class EdenAIProvider(BaseAIProvider):
    """Eden AI provider implementation"""
    
    def __init__(self):
        super().__init__(
            name="Eden AI",
            api_key=os.getenv('EDEN_AI_API_KEY', ''),
            base_url="https://api.edenai.run/v2"
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Eden AI connection"""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        # Test with a simple text generation request
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'providers': 'openai',
            'text': 'Hello, this is a test for WebWaka Digital Operating System',
            'max_tokens': 10,
            'temperature': 0.1
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/text/generation',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'Eden AI connection successful',
                    'response_time': response.elapsed.total_seconds()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Eden AI error: {response.status_code}',
                    'details': response.text
                }
        
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }

class HuggingFaceProvider(BaseAIProvider):
    """Hugging Face provider implementation"""
    
    def __init__(self):
        super().__init__(
            name="Hugging Face",
            api_key=os.getenv('HUGGINGFACE_API_KEY', ''),
            base_url="https://api-inference.huggingface.co/models"
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Hugging Face connection"""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        # Test with a simple text generation model
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'inputs': 'WebWaka Digital Operating System for Africa',
            'parameters': {
                'max_length': 20,
                'temperature': 0.1
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/gpt2',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'Hugging Face connection successful',
                    'response_time': response.elapsed.total_seconds()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Hugging Face error: {response.status_code}',
                    'details': response.text
                }
        
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }

class OpenRouterProvider(BaseAIProvider):
    """OpenRouter provider implementation"""
    
    def __init__(self):
        super().__init__(
            name="OpenRouter",
            api_key=os.getenv('OPENROUTER_API_KEY', ''),
            base_url="https://openrouter.ai/api/v1"
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test OpenRouter connection"""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        # Test with a simple chat completion
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://webwaka.com',
            'X-Title': 'WebWaka Digital Operating System'
        }
        
        payload = {
            'model': 'meta-llama/llama-3.1-8b-instruct:free',
            'messages': [
                {
                    'role': 'user',
                    'content': 'Hello from WebWaka Digital Operating System'
                }
            ],
            'max_tokens': 10,
            'temperature': 0.1
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'OpenRouter connection successful',
                    'response_time': response.elapsed.total_seconds()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'OpenRouter error: {response.status_code}',
                    'details': response.text
                }
        
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }

# Global AI provider manager instance
ai_manager = AIProviderManager()

