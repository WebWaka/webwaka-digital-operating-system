"""
Test suite for WebWaka AI Providers
Comprehensive testing for all AI provider integrations
"""

import unittest
import os
from unittest.mock import patch, Mock
import sys
import json

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_providers import (
    AIProviderManager,
    BaseAIProvider,
    EdenAIProvider,
    HuggingFaceProvider,
    OpenRouterProvider
)

class TestAIProviderManager(unittest.TestCase):
    """Test AI Provider Manager functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.manager = AIProviderManager()
    
    def test_manager_initialization(self):
        """Test manager initializes correctly"""
        self.assertIsInstance(self.manager, AIProviderManager)
        self.assertIsInstance(self.manager.providers, dict)
    
    def test_get_status_no_providers(self):
        """Test status when no providers are configured"""
        status = self.manager.get_status()
        
        self.assertIn('providers', status)
        self.assertIn('total_providers', status)
        self.assertIn('available_providers', status)
        self.assertEqual(status['total_providers'], 0)
        self.assertEqual(status['available_providers'], 0)
    
    @patch.dict(os.environ, {'EDEN_AI_API_KEY': 'test_key'})
    def test_get_status_with_providers(self):
        """Test status with providers configured"""
        manager = AIProviderManager()
        status = manager.get_status()
        
        self.assertGreater(status['total_providers'], 0)
        self.assertIn('eden', status['providers'])
    
    def test_test_providers_empty(self):
        """Test provider testing with no providers"""
        results = self.manager.test_providers()
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 0)

class TestBaseAIProvider(unittest.TestCase):
    """Test Base AI Provider functionality"""
    
    def setUp(self):
        """Set up test provider"""
        self.provider = BaseAIProvider(
            name="Test Provider",
            api_key="test_key",
            base_url="https://api.test.com"
        )
    
    def test_provider_initialization(self):
        """Test provider initializes correctly"""
        self.assertEqual(self.provider.name, "Test Provider")
        self.assertEqual(self.provider.api_key, "test_key")
        self.assertEqual(self.provider.base_url, "https://api.test.com")
        self.assertTrue(self.provider.available)
    
    def test_provider_no_api_key(self):
        """Test provider with no API key"""
        provider = BaseAIProvider("Test", "", "https://api.test.com")
        self.assertFalse(provider.available)
    
    def test_get_status(self):
        """Test provider status"""
        status = self.provider.get_status()
        
        self.assertIn('name', status)
        self.assertIn('available', status)
        self.assertIn('api_key_configured', status)
        self.assertIn('base_url', status)
        
        self.assertEqual(status['name'], "Test Provider")
        self.assertTrue(status['available'])
        self.assertTrue(status['api_key_configured'])
    
    def test_test_connection_not_implemented(self):
        """Test that base provider raises NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.provider.test_connection()

class TestEdenAIProvider(unittest.TestCase):
    """Test Eden AI Provider functionality"""
    
    def setUp(self):
        """Set up Eden AI provider"""
        with patch.dict(os.environ, {'EDEN_AI_API_KEY': 'test_eden_key'}):
            self.provider = EdenAIProvider()
    
    def test_eden_initialization(self):
        """Test Eden AI provider initialization"""
        self.assertEqual(self.provider.name, "Eden AI")
        self.assertEqual(self.provider.base_url, "https://api.edenai.run/v2")
        self.assertTrue(self.provider.available)
    
    def test_eden_no_api_key(self):
        """Test Eden AI provider without API key"""
        with patch.dict(os.environ, {}, clear=True):
            provider = EdenAIProvider()
            self.assertFalse(provider.available)
    
    def test_eden_test_connection_no_key(self):
        """Test Eden AI connection without API key"""
        with patch.dict(os.environ, {}, clear=True):
            provider = EdenAIProvider()
            result = provider.test_connection()
            self.assertIn('error', result)
    
    @patch('requests.post')
    def test_eden_test_connection_success(self, mock_post):
        """Test successful Eden AI connection"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_post.return_value = mock_response
        
        result = self.provider.test_connection()
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('Eden AI connection successful', result['message'])
        self.assertEqual(result['response_time'], 0.5)
    
    @patch('requests.post')
    def test_eden_test_connection_error(self, mock_post):
        """Test Eden AI connection error"""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response
        
        result = self.provider.test_connection()
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('Eden AI error: 401', result['message'])

class TestHuggingFaceProvider(unittest.TestCase):
    """Test Hugging Face Provider functionality"""
    
    def setUp(self):
        """Set up Hugging Face provider"""
        with patch.dict(os.environ, {'HUGGINGFACE_API_KEY': 'test_hf_key'}):
            self.provider = HuggingFaceProvider()
    
    def test_huggingface_initialization(self):
        """Test Hugging Face provider initialization"""
        self.assertEqual(self.provider.name, "Hugging Face")
        self.assertEqual(self.provider.base_url, "https://api-inference.huggingface.co/models")
        self.assertTrue(self.provider.available)
    
    @patch('requests.post')
    def test_huggingface_test_connection_success(self, mock_post):
        """Test successful Hugging Face connection"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 1.2
        mock_post.return_value = mock_response
        
        result = self.provider.test_connection()
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('Hugging Face connection successful', result['message'])
        self.assertEqual(result['response_time'], 1.2)

class TestOpenRouterProvider(unittest.TestCase):
    """Test OpenRouter Provider functionality"""
    
    def setUp(self):
        """Set up OpenRouter provider"""
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_or_key'}):
            self.provider = OpenRouterProvider()
    
    def test_openrouter_initialization(self):
        """Test OpenRouter provider initialization"""
        self.assertEqual(self.provider.name, "OpenRouter")
        self.assertEqual(self.provider.base_url, "https://openrouter.ai/api/v1")
        self.assertTrue(self.provider.available)
    
    @patch('requests.post')
    def test_openrouter_test_connection_success(self, mock_post):
        """Test successful OpenRouter connection"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.8
        mock_post.return_value = mock_response
        
        result = self.provider.test_connection()
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('OpenRouter connection successful', result['message'])
        self.assertEqual(result['response_time'], 0.8)

class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios"""
    
    @patch.dict(os.environ, {
        'EDEN_AI_API_KEY': 'test_eden',
        'HUGGINGFACE_API_KEY': 'test_hf',
        'OPENROUTER_API_KEY': 'test_or'
    })
    def test_full_provider_setup(self):
        """Test full provider setup with all API keys"""
        manager = AIProviderManager()
        status = manager.get_status()
        
        self.assertEqual(status['total_providers'], 3)
        self.assertIn('eden', status['providers'])
        self.assertIn('huggingface', status['providers'])
        self.assertIn('openrouter', status['providers'])
    
    def test_graceful_degradation(self):
        """Test system works without any API keys"""
        manager = AIProviderManager()
        status = manager.get_status()
        results = manager.test_providers()
        
        # Should not crash, just return empty results
        self.assertEqual(status['total_providers'], 0)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    # Create test directory if it doesn't exist
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2)

