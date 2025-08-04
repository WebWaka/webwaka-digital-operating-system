import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.ai_services import ai_bp

# WebWaka Digital Operating System - Backend API
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'webwaka-super-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes and origins (required for frontend-backend interaction)
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api/ai')

# Database initialization
db.init_app(app)
with app.app_context():
    db.create_all()

# WebWaka API Health Check
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'WebWaka Digital Operating System',
        'version': '1.0.0',
        'message': 'Africa\'s Premier AI-Powered Digital Transformation Operating System'
    })

# WebWaka API Status
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
