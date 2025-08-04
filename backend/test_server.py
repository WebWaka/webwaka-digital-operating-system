#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Test Backend Server
Simplified version for testing core functionality
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'WebWaka Digital Operating System',
        'version': '1.0.0',
        'message': 'Africa\'s Premier AI-Powered Digital Transformation Operating System'
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        'webwaka': {
            'status': 'operational',
            'cellular_architecture': 'active',
            'sectors': 42,
            'subsectors': 504,
            'cellular_modules': '25,200+',
            'ai_integration': 'ready',
            'partner_ecosystem': 'initialized',
            'african_optimization': 'enabled'
        }
    })

@app.route('/api/ai/test')
def ai_test():
    """Test AI ecosystem integration"""
    try:
        # Try to import AI ecosystem
        from src.ai_ecosystem.ai_orchestrator import AIOrchestrator
        ai_orchestrator = AIOrchestrator()
        
        return jsonify({
            'success': True,
            'message': 'AI ecosystem loaded successfully',
            'providers': ['eden_ai', 'huggingface', 'openrouter']
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
        'model': 'test',
        'cost': 0.0,
        'response_time': 0.1
    })

if __name__ == '__main__':
    print("🚀 Starting WebWaka Digital Operating System Backend...")
    print("📍 Server will be available at: http://localhost:5001")
    print("🔗 API Health Check: http://localhost:5001/api/health")
    print("📊 System Status: http://localhost:5001/api/status")
    print("🤖 AI Test: http://localhost:5001/api/ai/test")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

