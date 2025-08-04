"""
AI Services API Routes
Provides REST API endpoints for WebWaka AI ecosystem integration
"""

import os
import sys
import json
from flask import Blueprint, request, jsonify
from typing import Dict, Any

# Add the project root to the path to import AI ecosystem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from src.ai_ecosystem.ai_orchestrator import AIOrchestrator
    from src.ai_ecosystem.eden_ai_client import EdenAIClient
    from src.ai_ecosystem.huggingface_client import HuggingFaceClient
    from src.ai_ecosystem.openrouter_client import OpenRouterClient
except ImportError as e:
    print(f"Warning: AI ecosystem import failed: {e}")
    # Create mock classes for development
    class AIOrchestrator:
        def chat_completion(self, *args, **kwargs):
            return type('MockResponse', (), {
                'success': False, 
                'data': 'AI services not configured', 
                'error': 'Import failed',
                'provider': 'mock',
                'model': 'mock',
                'cost': 0.0,
                'response_time': 0.0
            })()
        
        def get_system_status(self):
            return {"status": "AI services not configured"}

ai_bp = Blueprint('ai_services', __name__)

# Initialize AI orchestrator
try:
    ai_orchestrator = AIOrchestrator()
except Exception as e:
    print(f"Warning: AI orchestrator initialization failed: {e}")
    ai_orchestrator = AIOrchestrator()  # Use mock version

@ai_bp.route('/chat', methods=['POST'])
def chat_completion():
    """
    Chat completion endpoint with AI provider orchestration
    """
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({
                'success': False,
                'error': 'Messages are required'
            }), 400
        
        messages = data['messages']
        model = data.get('model')
        max_tokens = data.get('max_tokens', 1000)
        temperature = data.get('temperature', 0.7)
        african_context = data.get('african_context', True)
        cost_optimize = data.get('cost_optimize', True)
        
        # Process chat completion through AI orchestrator
        response = ai_orchestrator.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            african_context=african_context,
            cost_optimize=cost_optimize
        )
        
        return jsonify({
            'success': response.success,
            'data': response.data,
            'provider': response.provider,
            'model': response.model,
            'cost': response.cost,
            'response_time': response.response_time,
            'tokens_used': response.tokens_used,
            'fallback_used': response.fallback_used,
            'error': response.error
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Chat completion failed: {str(e)}'
        }), 500

@ai_bp.route('/voice/process', methods=['POST'])
def voice_processing():
    """
    Voice processing endpoint for African languages
    """
    try:
        # Handle file upload or audio data
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Audio file is required'
            }), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        task = request.form.get('task', 'speech_to_text')
        
        # Read audio data
        audio_data = audio_file.read()
        
        # Process through AI orchestrator
        response = ai_orchestrator.african_voice_processing(
            audio_data=audio_data,
            language=language,
            task=task
        )
        
        return jsonify({
            'success': response.success,
            'data': response.data,
            'provider': response.provider,
            'model': response.model,
            'cost': response.cost,
            'response_time': response.response_time,
            'error': response.error
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Voice processing failed: {str(e)}'
        }), 500

@ai_bp.route('/business/workflow', methods=['POST'])
def business_workflow_automation():
    """
    Business workflow automation endpoint
    """
    try:
        data = request.get_json()
        
        if not data or 'workflow_description' not in data:
            return jsonify({
                'success': False,
                'error': 'Workflow description is required'
            }), 400
        
        workflow_description = data['workflow_description']
        sector = data.get('sector', 'general')
        country = data.get('country', 'general')
        
        # Process through AI orchestrator
        response = ai_orchestrator.business_workflow_automation(
            workflow_description=workflow_description,
            sector=sector,
            country=country
        )
        
        return jsonify({
            'success': response.success,
            'data': response.data,
            'provider': response.provider,
            'model': response.model,
            'cost': response.cost,
            'response_time': response.response_time,
            'error': response.error
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Workflow automation failed: {str(e)}'
        }), 500

@ai_bp.route('/cultural/analysis', methods=['POST'])
def cultural_intelligence_analysis():
    """
    Cultural intelligence analysis endpoint
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'Content is required'
            }), 400
        
        content = data['content']
        cultural_context = data.get('cultural_context', 'general_african')
        
        # Process through AI orchestrator
        response = ai_orchestrator.cultural_intelligence_analysis(
            content=content,
            cultural_context=cultural_context
        )
        
        return jsonify({
            'success': response.success,
            'data': response.data,
            'provider': response.provider,
            'model': response.model,
            'cost': response.cost,
            'response_time': response.response_time,
            'cultural_score': response.cultural_score,
            'error': response.error
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Cultural analysis failed: {str(e)}'
        }), 500

@ai_bp.route('/system/status', methods=['GET'])
def ai_system_status():
    """
    AI system status and health check endpoint
    """
    try:
        status = ai_orchestrator.get_system_status()
        
        return jsonify({
            'success': True,
            'data': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Status check failed: {str(e)}'
        }), 500

@ai_bp.route('/cost/optimize', methods=['GET'])
def cost_optimization():
    """
    Cost optimization analysis and recommendations
    """
    try:
        optimization = ai_orchestrator.optimize_costs()
        
        return jsonify({
            'success': True,
            'data': optimization
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Cost optimization failed: {str(e)}'
        }), 500

@ai_bp.route('/providers/test', methods=['GET'])
def test_providers():
    """
    Test all AI providers to ensure they're working
    """
    try:
        results = {}
        
        # Test OpenRouter
        try:
            from src.ai_ecosystem.openrouter_client import OpenRouterClient
            openrouter = OpenRouterClient()
            test_result = openrouter.test_free_models()
            results['openrouter'] = test_result
        except Exception as e:
            results['openrouter'] = {'error': str(e)}
        
        # Test Eden AI
        try:
            from src.ai_ecosystem.eden_ai_client import EdenAIClient
            eden_ai = EdenAIClient()
            test_messages = [{"role": "user", "content": "Hello"}]
            response = eden_ai.chat_completion(test_messages, max_tokens=10)
            results['eden_ai'] = {
                'status': 'working' if response.success else 'failed',
                'response': response.data if response.success else response.error
            }
        except Exception as e:
            results['eden_ai'] = {'error': str(e)}
        
        # Test Hugging Face
        try:
            from src.ai_ecosystem.huggingface_client import HuggingFaceClient
            huggingface = HuggingFaceClient()
            test_messages = [{"role": "user", "content": "Hello"}]
            response = huggingface.chat_completion(test_messages, max_tokens=10)
            results['huggingface'] = {
                'status': 'working' if response.success else 'failed',
                'response': response.data if response.success else response.error
            }
        except Exception as e:
            results['huggingface'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Provider testing failed: {str(e)}'
        }), 500

@ai_bp.route('/models/available', methods=['GET'])
def available_models():
    """
    Get available models from all providers
    """
    try:
        models = {}
        
        # Get OpenRouter models
        try:
            from src.ai_ecosystem.openrouter_client import OpenRouterClient
            openrouter = OpenRouterClient()
            models['openrouter'] = openrouter.get_available_models()
        except Exception as e:
            models['openrouter'] = {'error': str(e)}
        
        # Get Hugging Face African models
        try:
            from src.ai_ecosystem.huggingface_client import HuggingFaceClient
            huggingface = HuggingFaceClient()
            models['huggingface'] = huggingface.get_available_african_models()
        except Exception as e:
            models['huggingface'] = {'error': str(e)}
        
        # Eden AI models (static list)
        models['eden_ai'] = {
            'chat': ['openai/gpt-3.5-turbo', 'anthropic/claude-3-haiku', 'google/gemini-pro'],
            'vision': ['google/vision', 'amazon/rekognition', 'microsoft/computer-vision'],
            'speech': ['amazon/polly', 'google/text-to-speech', 'microsoft/speech'],
            'translation': ['google/translate', 'amazon/translate', 'microsoft/translator']
        }
        
        return jsonify({
            'success': True,
            'data': models
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Model listing failed: {str(e)}'
        }), 500

# Voice command processing for "sell packet of sugar" example
@ai_bp.route('/voice/command', methods=['POST'])
def voice_command_processing():
    """
    Process voice commands for business operations
    Example: "I want to sell a packet of sugar"
    """
    try:
        data = request.get_json()
        
        if not data or 'command' not in data:
            return jsonify({
                'success': False,
                'error': 'Voice command is required'
            }), 400
        
        command = data['command']
        language = data.get('language', 'en')
        business_context = data.get('business_context', 'retail')
        
        # Process command through AI orchestrator
        messages = [
            {
                "role": "system",
                "content": f"""You are a voice command processor for a {business_context} business management system.
                Parse voice commands and convert them to structured actions.
                
                For sales commands like "I want to sell a packet of sugar":
                1. Identify the action (sell)
                2. Extract the product (packet of sugar)
                3. Search inventory for the product
                4. Return structured response for system processing
                
                Respond in JSON format with: action, product, quantity, next_steps"""
            },
            {
                "role": "user",
                "content": f"Process this voice command: {command}"
            }
        ]
        
        response = ai_orchestrator.chat_completion(
            messages=messages,
            max_tokens=500,
            temperature=0.3,  # Lower temperature for more consistent parsing
            african_context=True,
            cost_optimize=True
        )
        
        if response.success:
            try:
                # Try to parse JSON response
                parsed_command = json.loads(response.data)
            except:
                # If not JSON, create structured response
                parsed_command = {
                    "action": "unknown",
                    "raw_response": response.data,
                    "needs_clarification": True
                }
        else:
            parsed_command = {
                "action": "error",
                "error": response.error
            }
        
        return jsonify({
            'success': response.success,
            'data': parsed_command,
            'provider': response.provider,
            'model': response.model,
            'cost': response.cost,
            'response_time': response.response_time,
            'original_command': command,
            'language': language,
            'error': response.error
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Voice command processing failed: {str(e)}'
        }), 500

