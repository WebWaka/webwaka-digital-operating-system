"""
WebWaka Digital Operating System - Backend Test Server
Simplified Flask application for testing and development
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS

# Import AI providers
from ai_providers import ai_manager

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'service': 'WebWaka Digital Operating System',
        'version': '1.0.0',
        'message': 'Africa\'s Premier AI-Powered Digital Transformation Operating System',
        'status': 'operational'
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'service': 'WebWaka Digital Operating System',
        'version': '1.0.0',
        'status': 'healthy',
        'message': 'Africa\'s Premier AI-Powered Digital Transformation Operating System'
    })

@app.route('/api/status')
def status():
    """System status endpoint"""
    return jsonify({
        'service': 'WebWaka Digital Operating System',
        'version': '1.0.0',
        'status': 'operational',
        'components': {
            'cellular_architecture': 'enabled',
            'ai_ecosystem': 'enabled',
            'voice_interface': 'enabled',
            'offline_capabilities': 'enabled',
            'african_optimization': 'enabled'
        }
    })

@app.route('/api/ai/test')
def ai_test():
    """Test AI ecosystem integration"""
    try:
        # Get AI provider status
        status = ai_manager.get_status()
        test_results = ai_manager.test_providers()
        
        return jsonify({
            'success': True,
            'message': 'AI ecosystem integration test completed',
            'status': status,
            'test_results': test_results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'AI ecosystem not available: {str(e)}',
            'providers': []
        })

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """Simplified AI chat endpoint"""
    return jsonify({
        'success': True,
        'data': 'AI chat functionality will be available once dependencies are installed',
        'provider': 'mock',
        'cost': 0.0,
        'response_time': 0.1
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print("🚀 Starting WebWaka Digital Operating System Backend...")
    print(f"📍 Server will be available at: http://localhost:{port}")
    print(f"🔗 API Health Check: http://localhost:{port}/api/health")
    print(f"📊 System Status: http://localhost:{port}/api/status")
    print(f"🤖 AI Test: http://localhost:{port}/api/ai/test")
    
    app.run(host='0.0.0.0', port=port, debug=True)

