"""
WebWaka Documentation Systems Agent (Agent 8)
Comprehensive Technical Documentation

This agent provides comprehensive documentation capabilities with:
- Automated API documentation generation
- User guide creation with African context
- Developer documentation and code examples
- Multi-language documentation support
- Interactive documentation with voice integration
- Cultural adaptation for African business contexts
"""

import os
import json
import logging
import asyncio
import inspect
import ast
import re
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import markdown
import jinja2
from pathlib import Path
import yaml
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DocumentationSection:
    """Documentation section structure"""
    title: str
    content: str
    language: str = "en"
    category: str = "general"
    tags: List[str] = None
    last_updated: datetime = None
    author: str = "WebWaka Documentation System"
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class APIEndpoint:
    """API endpoint documentation structure"""
    path: str
    method: str
    description: str
    parameters: List[Dict[str, Any]]
    responses: Dict[str, Dict[str, Any]]
    examples: List[Dict[str, Any]]
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class UserGuideSection:
    """User guide section with African context"""
    title: str
    content: str
    difficulty_level: str  # beginner, intermediate, advanced
    business_context: str  # retail, agriculture, services, etc.
    language: str = "en"
    voice_instructions: Optional[str] = None
    cultural_notes: List[str] = None
    
    def __post_init__(self):
        if self.cultural_notes is None:
            self.cultural_notes = []

class AfricanContextualizer:
    """Add African business and cultural context to documentation"""
    
    def __init__(self):
        self.business_contexts = {
            "retail": {
                "common_scenarios": [
                    "selling sugar packets",
                    "managing inventory for small shop",
                    "processing mobile money payments",
                    "handling customer credit"
                ],
                "cultural_considerations": [
                    "Ubuntu philosophy in customer service",
                    "Community-centered business approach",
                    "Respect for elders in business decisions",
                    "Family involvement in business operations"
                ]
            },
            "agriculture": {
                "common_scenarios": [
                    "tracking crop yields",
                    "managing seasonal workers",
                    "coordinating with cooperatives",
                    "weather-dependent planning"
                ],
                "cultural_considerations": [
                    "Traditional farming knowledge integration",
                    "Community land management",
                    "Seasonal ceremony considerations",
                    "Elder wisdom in agricultural decisions"
                ]
            },
            "services": {
                "common_scenarios": [
                    "appointment scheduling",
                    "service quality tracking",
                    "customer feedback management",
                    "skill development tracking"
                ],
                "cultural_considerations": [
                    "Personal relationship importance",
                    "Word-of-mouth reputation",
                    "Community service expectations",
                    "Traditional service delivery methods"
                ]
            }
        }
        
        self.language_adaptations = {
            "swahili": {
                "greetings": ["Habari", "Mambo", "Salama"],
                "business_terms": {
                    "customer": "mteja",
                    "sale": "mauzo",
                    "inventory": "hesabu ya bidhaa",
                    "payment": "malipo"
                }
            },
            "hausa": {
                "greetings": ["Sannu", "Ina kwana", "Barka"],
                "business_terms": {
                    "customer": "abokin ciniki",
                    "sale": "sayarwa",
                    "inventory": "kayayyaki",
                    "payment": "biya"
                }
            },
            "yoruba": {
                "greetings": ["Bawo", "E kaaro", "Pele"],
                "business_terms": {
                    "customer": "onibara",
                    "sale": "tita",
                    "inventory": "oja",
                    "payment": "isanwo"
                }
            }
        }
    
    def add_african_context(self, content: str, business_type: str, language: str = "en") -> str:
        """Add African business and cultural context to documentation"""
        
        # Add business context examples
        if business_type in self.business_contexts:
            context = self.business_contexts[business_type]
            
            context_section = "\n\n## African Business Context\n\n"
            context_section += f"**Common {business_type.title()} Scenarios:**\n"
            for scenario in context["common_scenarios"]:
                context_section += f"- {scenario.title()}\n"
            
            context_section += f"\n**Cultural Considerations:**\n"
            for consideration in context["cultural_considerations"]:
                context_section += f"- {consideration}\n"
            
            content += context_section
        
        # Add language-specific adaptations
        if language != "en" and language in self.language_adaptations:
            lang_data = self.language_adaptations[language]
            
            lang_section = f"\n\n## {language.title()} Language Integration\n\n"
            lang_section += "**Common Greetings:**\n"
            for greeting in lang_data["greetings"]:
                lang_section += f"- {greeting}\n"
            
            lang_section += "\n**Business Terms:**\n"
            for english, local in lang_data["business_terms"].items():
                lang_section += f"- {english.title()}: {local}\n"
            
            content += lang_section
        
        return content
    
    def generate_voice_instructions(self, content: str, language: str = "en") -> str:
        """Generate voice command instructions for African languages"""
        
        voice_commands = {
            "en": [
                "Say 'WebWaka help' to get assistance",
                "Say 'sell sugar packet' to record a sale",
                "Say 'check inventory' to view stock levels",
                "Say 'daily report' to get business summary"
            ],
            "swahili": [
                "Sema 'WebWaka msaada' kupata usaidizi",
                "Sema 'uza paketi ya sukari' kurekodi mauzo",
                "Sema 'angalia hesabu' kuona viwango vya hifadhi",
                "Sema 'ripoti ya kila siku' kupata muhtasari wa biashara"
            ]
        }
        
        if language in voice_commands:
            voice_section = "\n\n## Voice Commands\n\n"
            for command in voice_commands[language]:
                voice_section += f"- {command}\n"
            return voice_section
        
        return ""

class APIDocumentationGenerator:
    """Generate comprehensive API documentation"""
    
    def __init__(self):
        self.endpoints = []
        self.contextualizer = AfricanContextualizer()
    
    def analyze_flask_app(self, app_path: str) -> List[APIEndpoint]:
        """Analyze Flask application to extract API endpoints"""
        endpoints = []
        
        try:
            # Read the Flask application file
            with open(app_path, 'r') as file:
                content = file.read()
            
            # Parse the AST to find route decorators
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check for route decorators
                    for decorator in node.decorator_list:
                        if self._is_route_decorator(decorator):
                            endpoint = self._extract_endpoint_info(node, decorator)
                            if endpoint:
                                endpoints.append(endpoint)
            
        except Exception as e:
            logger.error(f"Error analyzing Flask app: {e}")
        
        return endpoints
    
    def _is_route_decorator(self, decorator) -> bool:
        """Check if decorator is a Flask route decorator"""
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr == 'route'
            elif isinstance(decorator.func, ast.Name):
                return decorator.func.id in ['route', 'get', 'post', 'put', 'delete']
        return False
    
    def _extract_endpoint_info(self, func_node, decorator) -> Optional[APIEndpoint]:
        """Extract endpoint information from function and decorator"""
        try:
            # Extract path from decorator
            path = "/"
            method = "GET"
            
            if isinstance(decorator, ast.Call) and decorator.args:
                if isinstance(decorator.args[0], ast.Str):
                    path = decorator.args[0].s
                elif isinstance(decorator.args[0], ast.Constant):
                    path = decorator.args[0].value
            
            # Extract method from decorator keywords
            for keyword in decorator.keywords if hasattr(decorator, 'keywords') else []:
                if keyword.arg == 'methods':
                    if isinstance(keyword.value, ast.List):
                        methods = [elt.s if isinstance(elt, ast.Str) else elt.value 
                                 for elt in keyword.value.elts]
                        method = methods[0] if methods else "GET"
            
            # Extract description from docstring
            description = "No description available"
            if func_node.body and isinstance(func_node.body[0], ast.Expr):
                if isinstance(func_node.body[0].value, ast.Str):
                    description = func_node.body[0].value.s
                elif isinstance(func_node.body[0].value, ast.Constant):
                    description = func_node.body[0].value.value
            
            # Extract parameters from function arguments
            parameters = []
            for arg in func_node.args.args:
                if arg.arg not in ['self', 'cls']:
                    parameters.append({
                        "name": arg.arg,
                        "type": "string",
                        "required": True,
                        "description": f"Parameter {arg.arg}"
                    })
            
            return APIEndpoint(
                path=path,
                method=method,
                description=description,
                parameters=parameters,
                responses={
                    "200": {"description": "Success", "content": {"application/json": {}}},
                    "400": {"description": "Bad Request"},
                    "500": {"description": "Internal Server Error"}
                },
                examples=[{
                    "name": "Example request",
                    "request": {"method": method, "path": path},
                    "response": {"status": 200, "body": {"message": "Success"}}
                }],
                tags=[self._categorize_endpoint(path)]
            )
            
        except Exception as e:
            logger.error(f"Error extracting endpoint info: {e}")
            return None
    
    def _categorize_endpoint(self, path: str) -> str:
        """Categorize endpoint based on path"""
        if "/api/ai" in path:
            return "AI Services"
        elif "/api/voice" in path:
            return "Voice Interface"
        elif "/api/business" in path:
            return "Business Operations"
        elif "/api/auth" in path:
            return "Authentication"
        else:
            return "General"
    
    def generate_openapi_spec(self, endpoints: List[APIEndpoint]) -> Dict[str, Any]:
        """Generate OpenAPI 3.0 specification"""
        
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "WebWaka Digital Operating System API",
                "description": "Comprehensive API for African business management with AI integration",
                "version": "1.0.0",
                "contact": {
                    "name": "WebWaka Support",
                    "email": "support@webwaka.com"
                }
            },
            "servers": [
                {
                    "url": "https://api.webwaka.com",
                    "description": "Production server"
                },
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            },
            "tags": []
        }
        
        # Add endpoints to spec
        tags_set = set()
        for endpoint in endpoints:
            path_spec = {
                endpoint.method.lower(): {
                    "summary": endpoint.description,
                    "description": endpoint.description,
                    "tags": endpoint.tags,
                    "parameters": [
                        {
                            "name": param["name"],
                            "in": "query" if endpoint.method == "GET" else "body",
                            "required": param["required"],
                            "description": param["description"],
                            "schema": {"type": param["type"]}
                        }
                        for param in endpoint.parameters
                    ],
                    "responses": endpoint.responses
                }
            }
            
            spec["paths"][endpoint.path] = path_spec
            tags_set.update(endpoint.tags)
        
        # Add tags
        spec["tags"] = [{"name": tag, "description": f"{tag} endpoints"} for tag in tags_set]
        
        return spec
    
    def generate_markdown_docs(self, endpoints: List[APIEndpoint]) -> str:
        """Generate Markdown API documentation"""
        
        doc = "# WebWaka API Documentation\n\n"
        doc += "Welcome to the WebWaka Digital Operating System API documentation. "
        doc += "This API is designed specifically for African businesses with cultural intelligence and voice-first interfaces.\n\n"
        
        # Add African context
        doc = self.contextualizer.add_african_context(doc, "services", "en")
        
        # Group endpoints by tags
        endpoints_by_tag = {}
        for endpoint in endpoints:
            for tag in endpoint.tags:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append(endpoint)
        
        # Generate documentation for each tag
        for tag, tag_endpoints in endpoints_by_tag.items():
            doc += f"\n## {tag}\n\n"
            
            for endpoint in tag_endpoints:
                doc += f"### {endpoint.method} {endpoint.path}\n\n"
                doc += f"{endpoint.description}\n\n"
                
                if endpoint.parameters:
                    doc += "**Parameters:**\n\n"
                    for param in endpoint.parameters:
                        doc += f"- `{param['name']}` ({param['type']}) - {param['description']}\n"
                    doc += "\n"
                
                doc += "**Responses:**\n\n"
                for status, response in endpoint.responses.items():
                    doc += f"- `{status}`: {response['description']}\n"
                doc += "\n"
                
                if endpoint.examples:
                    doc += "**Example:**\n\n"
                    example = endpoint.examples[0]
                    doc += f"```bash\ncurl -X {endpoint.method} {endpoint.path}\n```\n\n"
        
        return doc

class UserGuideGenerator:
    """Generate user guides with African business context"""
    
    def __init__(self):
        self.contextualizer = AfricanContextualizer()
        self.guide_templates = {
            "getting_started": self._get_getting_started_template(),
            "voice_commands": self._get_voice_commands_template(),
            "business_operations": self._get_business_operations_template(),
            "mobile_usage": self._get_mobile_usage_template()
        }
    
    def generate_user_guide(self, business_type: str, language: str = "en") -> List[UserGuideSection]:
        """Generate comprehensive user guide for specific business type"""
        
        sections = []
        
        # Getting Started section
        getting_started = UserGuideSection(
            title="Getting Started with WebWaka",
            content=self._generate_getting_started_content(business_type, language),
            difficulty_level="beginner",
            business_context=business_type,
            language=language,
            voice_instructions=self.contextualizer.generate_voice_instructions("", language),
            cultural_notes=[
                "WebWaka respects Ubuntu philosophy - we are here to help each other succeed",
                "The system adapts to your local business customs and practices",
                "Voice commands work in your local language for natural interaction"
            ]
        )
        sections.append(getting_started)
        
        # Voice Commands section
        voice_commands = UserGuideSection(
            title="Using Voice Commands",
            content=self._generate_voice_commands_content(business_type, language),
            difficulty_level="beginner",
            business_context=business_type,
            language=language,
            voice_instructions=self.contextualizer.generate_voice_instructions("voice", language)
        )
        sections.append(voice_commands)
        
        # Business Operations section
        business_ops = UserGuideSection(
            title="Managing Your Business Operations",
            content=self._generate_business_operations_content(business_type, language),
            difficulty_level="intermediate",
            business_context=business_type,
            language=language
        )
        sections.append(business_ops)
        
        # Mobile Usage section
        mobile_usage = UserGuideSection(
            title="Using WebWaka on Mobile Devices",
            content=self._generate_mobile_usage_content(business_type, language),
            difficulty_level="beginner",
            business_context=business_type,
            language=language
        )
        sections.append(mobile_usage)
        
        return sections
    
    def _generate_getting_started_content(self, business_type: str, language: str) -> str:
        """Generate getting started content"""
        content = f"""
# Welcome to WebWaka - Your Digital Business Assistant

WebWaka is designed specifically for {business_type} businesses in Africa, combining modern technology with traditional business wisdom.

## What Makes WebWaka Special

- **Voice-First Interface**: Speak naturally in your local language
- **Ubuntu Philosophy**: Built on principles of community and mutual support
- **Offline-First**: Works even when internet connection is poor
- **Cultural Intelligence**: Understands African business practices
- **Mobile-Optimized**: Perfect for smartphone-based business management

## Quick Setup

1. **Create Your Account**: Use your mobile number or email
2. **Choose Your Language**: Select from 50+ African languages
3. **Set Up Your Business**: Tell us about your {business_type} business
4. **Start with Voice**: Say "WebWaka, help me get started"

## First Steps

### For {business_type.title()} Businesses:

1. **Add Your Products/Services**: Start with your most common items
2. **Set Up Payment Methods**: Include mobile money, cash, and credit options
3. **Configure Voice Commands**: Practice basic commands in your language
4. **Test Offline Mode**: Ensure everything works without internet

## Getting Help

- **Voice Help**: Say "WebWaka help" anytime
- **Community Support**: Connect with other {business_type} business owners
- **Elder Wisdom**: Access traditional business knowledge integrated with modern tools
"""
        
        return self.contextualizer.add_african_context(content, business_type, language)
    
    def _generate_voice_commands_content(self, business_type: str, language: str) -> str:
        """Generate voice commands content"""
        content = f"""
# Voice Commands for {business_type.title()} Business

WebWaka's voice interface is designed to feel natural and respect African communication styles.

## Basic Commands

### Sales and Transactions
- "Sell [item name]" - Record a sale
- "Price of [item]" - Check item price
- "Customer paid [amount]" - Record payment
- "Credit for [customer name]" - Set up customer credit

### Inventory Management
- "Check stock" - View current inventory
- "Add [quantity] [item]" - Add items to inventory
- "Low stock alert" - Check items running low
- "Reorder [item]" - Create reorder request

### Customer Service
- "New customer [name]" - Add new customer
- "Customer history [name]" - View customer purchase history
- "Send receipt" - Send receipt via SMS or WhatsApp
- "Customer feedback" - Record customer feedback

### Reports and Analytics
- "Daily sales" - Get today's sales summary
- "Weekly report" - Get weekly business summary
- "Best selling items" - View top products
- "Profit analysis" - View profit margins

## Cultural Voice Patterns

WebWaka understands African communication styles:

- **Respectful Greetings**: Start with traditional greetings
- **Community Context**: "Our community needs..." for group orders
- **Elder Consultation**: "Ask the elders" for traditional business wisdom
- **Ubuntu Principles**: "Help our neighbor" for community support

## Language-Specific Commands

Commands work naturally in your local language while maintaining business context.
"""
        
        return self.contextualizer.add_african_context(content, business_type, language)
    
    def _generate_business_operations_content(self, business_type: str, language: str) -> str:
        """Generate business operations content"""
        content = f"""
# Managing Your {business_type.title()} Business with WebWaka

## Daily Operations

### Morning Routine
1. **Check overnight sync**: Review any offline transactions
2. **Inventory check**: Verify stock levels for the day
3. **Weather check**: Plan for weather-dependent operations
4. **Community updates**: Check for local events affecting business

### During Business Hours
1. **Voice-activated sales**: Use voice commands for quick transactions
2. **Customer service**: Maintain Ubuntu principles in all interactions
3. **Inventory monitoring**: Track stock levels throughout the day
4. **Payment processing**: Handle multiple payment methods efficiently

### Evening Routine
1. **Daily reconciliation**: Review all transactions
2. **Inventory update**: Record any stock changes
3. **Customer follow-up**: Send thank you messages
4. **Next day preparation**: Plan for tomorrow's operations

## Advanced Features

### Community Integration
- **Cooperative management**: Coordinate with local cooperatives
- **Group purchasing**: Organize community buying groups
- **Skill sharing**: Connect with other business owners
- **Traditional knowledge**: Access elder wisdom for business decisions

### Financial Management
- **Mobile money integration**: Seamless M-Pesa, Airtel Money support
- **Credit management**: Track customer credit and payments
- **Profit tracking**: Monitor margins and profitability
- **Tax preparation**: Prepare for local tax requirements

### Growth Strategies
- **Market expansion**: Identify new opportunities
- **Product diversification**: Add complementary products/services
- **Customer retention**: Build long-term relationships
- **Community leadership**: Become a business leader in your area
"""
        
        return self.contextualizer.add_african_context(content, business_type, language)
    
    def _generate_mobile_usage_content(self, business_type: str, language: str) -> str:
        """Generate mobile usage content"""
        content = """
# Using WebWaka on Your Mobile Device

WebWaka is optimized for African mobile usage patterns and infrastructure.

## Mobile Optimization Features

### Network Adaptation
- **2G/3G Optimization**: Works efficiently on slower networks
- **Data Compression**: Minimizes data usage to save costs
- **Offline Mode**: Full functionality without internet connection
- **Smart Sync**: Syncs when connection is available

### Touch Interface
- **Large Buttons**: Easy to use with different hand sizes
- **Gesture Navigation**: Swipe-based navigation for efficiency
- **Voice Integration**: Reduce typing with voice commands
- **High Contrast**: Visible in bright African sunlight

## Battery and Data Management

### Battery Optimization
- **Power Saving Mode**: Extends battery life during power outages
- **Background Sync**: Efficient background operations
- **Dark Mode**: Reduces battery consumption
- **Quick Actions**: Fast access to common functions

### Data Usage Control
- **Data Monitoring**: Track your data usage
- **Compression Settings**: Adjust for your data plan
- **Offline Priority**: Prefer offline operations
- **Smart Loading**: Load only essential content

## Mobile-Specific Features

### Quick Actions
- **Shake to Record Sale**: Quick gesture for sales
- **Double Tap for Help**: Instant voice assistance
- **Swipe for Navigation**: Efficient menu navigation
- **Long Press for Options**: Context-sensitive actions

### Integration with Phone Features
- **SMS Integration**: Send receipts via SMS
- **Contact Sync**: Import customer contacts
- **Camera Integration**: Scan barcodes and QR codes
- **Call Integration**: Call customers directly from app
"""
        
        return self.contextualizer.add_african_context(content, "mobile", language)
    
    def _get_getting_started_template(self) -> str:
        return "getting_started_template"
    
    def _get_voice_commands_template(self) -> str:
        return "voice_commands_template"
    
    def _get_business_operations_template(self) -> str:
        return "business_operations_template"
    
    def _get_mobile_usage_template(self) -> str:
        return "mobile_usage_template"

class DeveloperDocumentationGenerator:
    """Generate developer documentation and code examples"""
    
    def __init__(self):
        self.contextualizer = AfricanContextualizer()
    
    def generate_developer_guide(self) -> str:
        """Generate comprehensive developer guide"""
        
        guide = """
# WebWaka Developer Documentation

## Architecture Overview

WebWaka follows a cellular-tissue-organ architecture inspired by biological systems, designed for African business contexts.

### Core Components

1. **Cellular Level**: Individual business functions (sales, inventory, customers)
2. **Tissue Level**: Related business processes (retail operations, financial management)
3. **Organ Level**: Complete business systems (POS, CRM, ERP)
4. **Organism Level**: Entire business ecosystem

### Technology Stack

- **Backend**: Python Flask with AI integration
- **Frontend**: React with Progressive Web App capabilities
- **AI Services**: Eden AI, Hugging Face, OpenRouter integration
- **Database**: SQLite for local, PostgreSQL for cloud
- **Voice**: Speech recognition and synthesis with African language support
- **Mobile**: PWA with offline-first architecture

## Getting Started for Developers

### Prerequisites

```bash
# Python 3.8+
python --version

# Node.js 16+
node --version

# Git
git --version
```

### Installation

```bash
# Clone repository
git clone https://github.com/WebWaka/webwaka-digital-operating-system.git
cd webwaka-digital-operating-system

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Development Setup

```bash
# Start backend server
python backend/main.py

# Start frontend development server
npm start

# Run tests
python -m pytest tests/
npm test
```

## API Development

### Creating New Endpoints

```python
from flask import Flask, request, jsonify
from backend.ai_ecosystem_integration import AIOrchestrator

app = Flask(__name__)
ai_orchestrator = AIOrchestrator()

@app.route('/api/business/voice-command', methods=['POST'])
def process_voice_command():
    \"\"\"Process voice command with African language support\"\"\"
    data = request.get_json()
    
    # Extract voice data
    voice_text = data.get('text')
    language = data.get('language', 'en')
    business_context = data.get('business_context', 'retail')
    
    # Process with AI
    result = ai_orchestrator.process_voice_command(
        text=voice_text,
        language=language,
        context=business_context
    )
    
    return jsonify({
        'success': True,
        'result': result,
        'cultural_adaptation': result.get('ubuntu_elements', [])
    })
```

### Adding African Language Support

```python
class AfricanLanguageProcessor:
    def __init__(self):
        self.supported_languages = {
            'sw': 'Swahili',
            'ha': 'Hausa', 
            'yo': 'Yoruba',
            'ig': 'Igbo',
            'am': 'Amharic'
        }
    
    def process_text(self, text: str, language: str) -> dict:
        \"\"\"Process text with cultural context\"\"\"
        
        # Apply Ubuntu philosophy
        ubuntu_elements = self.extract_ubuntu_elements(text)
        
        # Add cultural greetings
        cultural_greeting = self.get_cultural_greeting(language)
        
        return {
            'processed_text': text,
            'ubuntu_elements': ubuntu_elements,
            'cultural_greeting': cultural_greeting,
            'language': language
        }
```

## Frontend Development

### Creating Mobile-Optimized Components

```jsx
import React from 'react';
import { TouchOptimizedButton } from './MobileOptimizationAgent';

const AfricanBusinessComponent = ({ businessType }) => {
  const handleVoiceCommand = () => {
    // Trigger voice recognition
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        // Process voice input
      });
  };

  return (
    <div className="african-business-interface">
      <TouchOptimizedButton 
        variant="primary"
        size="large"
        onClick={handleVoiceCommand}
      >
        🎤 Speak in Your Language
      </TouchOptimizedButton>
      
      {/* Ubuntu philosophy integration */}
      <div className="ubuntu-message">
        "Ubuntu: I am because we are"
      </div>
    </div>
  );
};
```

### Voice Integration

```javascript
class VoiceInterface {
  constructor(language = 'en') {
    this.language = language;
    this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    this.synthesis = window.speechSynthesis;
    
    this.setupRecognition();
  }
  
  setupRecognition() {
    this.recognition.lang = this.language;
    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    
    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      this.processVoiceCommand(transcript);
    };
  }
  
  async processVoiceCommand(text) {
    // Send to backend for processing
    const response = await fetch('/api/business/voice-command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        language: this.language,
        business_context: 'retail'
      })
    });
    
    const result = await response.json();
    this.speakResponse(result.result.response_text);
  }
  
  speakResponse(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = this.language;
    this.synthesis.speak(utterance);
  }
}
```

## Testing Guidelines

### Unit Testing

```python
import pytest
from backend.voice_interface_agent import VoiceInterfaceAgent

class TestVoiceInterface:
    def setup_method(self):
        self.voice_agent = VoiceInterfaceAgent()
    
    @pytest.mark.asyncio
    async def test_swahili_voice_command(self):
        # Test Swahili voice command processing
        result = await self.voice_agent.process_voice_command(
            text="uza paketi ya sukari",
            language="sw"
        )
        
        assert result is not None
        assert "sukari" in result.text.lower()
        assert result.language.value == "sw"
    
    def test_ubuntu_philosophy_integration(self):
        # Test Ubuntu philosophy integration
        cultural_adapter = self.voice_agent.business_workflow.voice_synthesis.cultural_adapter
        
        ubuntu_text = cultural_adapter.apply_ubuntu_context(
            "Thank you for your purchase",
            "sales"
        )
        
        assert "community" in ubuntu_text.lower() or "together" in ubuntu_text.lower()
```

### Integration Testing

```python
class TestAfricanBusinessIntegration:
    @pytest.mark.asyncio
    async def test_complete_sales_workflow(self):
        # Test complete sales workflow with African context
        voice_agent = VoiceInterfaceAgent()
        
        # Simulate voice command in Swahili
        command = VoiceCommand(
            text="uza paketi ya sukari kwa shilingi hamsini",
            language=VoiceLanguage.SWAHILI,
            confidence=0.9,
            timestamp=time.time(),
            cultural_context={"business_intent": "sell"},
            business_intent="sell"
        )
        
        response = await voice_agent.business_workflow._handle_sales_workflow(command)
        
        assert "sukari" in response.lower()
        assert "shilingi" in response.lower()
```

## Deployment

### Production Deployment

```bash
# Build frontend
npm run build

# Deploy to production
python deploy.py --environment production

# Monitor deployment
python monitor.py --check-health
```

### African Infrastructure Considerations

- **Network Optimization**: Implement aggressive caching and compression
- **Power Management**: Handle power outages gracefully
- **Mobile-First**: Ensure excellent mobile experience
- **Offline Capability**: Full offline functionality
- **Cultural Sensitivity**: Respect local customs and languages

## Contributing

### Code Style

- Follow PEP 8 for Python
- Use ESLint for JavaScript/React
- Include cultural context in all user-facing features
- Add voice command support for new features
- Test with African languages and business scenarios

### Pull Request Process

1. Create feature branch with descriptive name
2. Include tests for new functionality
3. Update documentation
4. Test with African business scenarios
5. Submit pull request with detailed description

## Support

- **Developer Community**: Join our Slack channel
- **Documentation**: https://docs.webwaka.com
- **Issues**: GitHub Issues
- **Cultural Consultation**: Connect with African business advisors
"""
        
        return guide

class DocumentationSystemsAgent:
    """Main Documentation Systems Agent for WebWaka"""
    
    def __init__(self, project_root: str = "/home/ubuntu/webwaka-digital-operating-system"):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.api_generator = APIDocumentationGenerator()
        self.user_guide_generator = UserGuideGenerator()
        self.dev_guide_generator = DeveloperDocumentationGenerator()
        self.contextualizer = AfricanContextualizer()
        
        # Create docs directory if it doesn't exist
        self.docs_dir.mkdir(exist_ok=True)
        
        logger.info("Documentation Systems Agent initialized")
    
    async def generate_complete_documentation(self) -> Dict[str, str]:
        """Generate complete documentation suite"""
        
        documentation_files = {}
        
        try:
            # Generate API documentation
            api_docs = await self.generate_api_documentation()
            documentation_files.update(api_docs)
            
            # Generate user guides for different business types
            user_guides = await self.generate_user_guides()
            documentation_files.update(user_guides)
            
            # Generate developer documentation
            dev_docs = await self.generate_developer_documentation()
            documentation_files.update(dev_docs)
            
            # Generate README and overview
            overview_docs = await self.generate_overview_documentation()
            documentation_files.update(overview_docs)
            
            logger.info(f"Generated {len(documentation_files)} documentation files")
            
        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
        
        return documentation_files
    
    async def generate_api_documentation(self) -> Dict[str, str]:
        """Generate API documentation"""
        docs = {}
        
        # Analyze Flask applications
        backend_files = [
            self.project_root / "backend" / "main.py",
            self.project_root / "backend" / "robust_server.py"
        ]
        
        all_endpoints = []
        for backend_file in backend_files:
            if backend_file.exists():
                endpoints = self.api_generator.analyze_flask_app(str(backend_file))
                all_endpoints.extend(endpoints)
        
        # Generate OpenAPI specification
        openapi_spec = self.api_generator.generate_openapi_spec(all_endpoints)
        docs["api/openapi.json"] = json.dumps(openapi_spec, indent=2)
        
        # Generate Markdown documentation
        markdown_docs = self.api_generator.generate_markdown_docs(all_endpoints)
        docs["api/README.md"] = markdown_docs
        
        return docs
    
    async def generate_user_guides(self) -> Dict[str, str]:
        """Generate user guides for different business types"""
        docs = {}
        
        business_types = ["retail", "agriculture", "services", "manufacturing"]
        languages = ["en", "sw", "ha", "yo"]
        
        for business_type in business_types:
            for language in languages:
                sections = self.user_guide_generator.generate_user_guide(business_type, language)
                
                # Combine sections into complete guide
                guide_content = f"# WebWaka User Guide - {business_type.title()} Business\n\n"
                guide_content += f"*Language: {language.upper()}*\n\n"
                
                for section in sections:
                    guide_content += f"## {section.title}\n\n"
                    guide_content += f"**Difficulty:** {section.difficulty_level.title()}\n\n"
                    guide_content += section.content + "\n\n"
                    
                    if section.voice_instructions:
                        guide_content += section.voice_instructions + "\n\n"
                    
                    if section.cultural_notes:
                        guide_content += "### Cultural Notes\n\n"
                        for note in section.cultural_notes:
                            guide_content += f"- {note}\n"
                        guide_content += "\n"
                
                docs[f"user-guides/{business_type}-{language}.md"] = guide_content
        
        return docs
    
    async def generate_developer_documentation(self) -> Dict[str, str]:
        """Generate developer documentation"""
        docs = {}
        
        # Generate main developer guide
        dev_guide = self.dev_guide_generator.generate_developer_guide()
        docs["developers/README.md"] = dev_guide
        
        # Generate component documentation
        component_docs = await self.generate_component_documentation()
        docs.update(component_docs)
        
        return docs
    
    async def generate_component_documentation(self) -> Dict[str, str]:
        """Generate documentation for individual components"""
        docs = {}
        
        # Document each agent
        agents = [
            ("Voice Interface Agent", "backend/voice_interface_agent.py"),
            ("Mobile Optimization Agent", "frontend/src/components/MobileOptimizationAgent.jsx"),
            ("Performance Monitoring Agent", "backend/performance_monitoring_agent.py"),
            ("AI Ecosystem Integration", "backend/ai_ecosystem_integration.py")
        ]
        
        for agent_name, agent_path in agents:
            full_path = self.project_root / agent_path
            if full_path.exists():
                component_doc = await self.generate_single_component_doc(agent_name, str(full_path))
                docs[f"developers/components/{agent_name.lower().replace(' ', '-')}.md"] = component_doc
        
        return docs
    
    async def generate_single_component_doc(self, component_name: str, file_path: str) -> str:
        """Generate documentation for a single component"""
        
        doc = f"# {component_name}\n\n"
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Extract docstring
            if '"""' in content:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    docstring = content[start:end].strip()
                    doc += f"{docstring}\n\n"
            
            # Extract classes and functions
            tree = ast.parse(content)
            
            doc += "## Classes\n\n"
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    doc += f"### {node.name}\n\n"
                    if ast.get_docstring(node):
                        doc += f"{ast.get_docstring(node)}\n\n"
            
            doc += "## Functions\n\n"
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    doc += f"### {node.name}\n\n"
                    if ast.get_docstring(node):
                        doc += f"{ast.get_docstring(node)}\n\n"
        
        except Exception as e:
            doc += f"Error generating documentation: {e}\n"
        
        return doc
    
    async def generate_overview_documentation(self) -> Dict[str, str]:
        """Generate overview and README documentation"""
        docs = {}
        
        # Main README
        readme = """
# WebWaka Digital Operating System

The comprehensive digital business management system designed specifically for African businesses.

## Features

- **Voice-First Interface**: Natural language commands in 50+ African languages
- **Ubuntu Philosophy Integration**: Community-centered business approach
- **Offline-First Architecture**: Works without internet connection
- **Mobile-Optimized**: Perfect for smartphone-based business management
- **AI-Powered**: Intelligent automation and decision support
- **Cultural Intelligence**: Understands African business practices

## Quick Start

1. **Installation**: Follow the [Developer Guide](docs/developers/README.md)
2. **User Guide**: See [User Guides](docs/user-guides/) for your business type
3. **API Documentation**: Check [API Docs](docs/api/README.md) for integration

## Business Types Supported

- **Retail**: Small shops, markets, convenience stores
- **Agriculture**: Farming, cooperatives, agricultural services
- **Services**: Professional services, consulting, repairs
- **Manufacturing**: Small-scale manufacturing, crafts, production

## Languages Supported

- English (African variants)
- Swahili (Kenya, Tanzania, Uganda)
- Hausa (Nigeria, Niger, Ghana)
- Yoruba (Nigeria, Benin, Togo)
- Igbo (Nigeria)
- Amharic (Ethiopia)
- Zulu (South Africa)
- Xhosa (South Africa)
- And 40+ more African languages

## Architecture

WebWaka follows a biological cellular-tissue-organ architecture:

- **Cellular Level**: Individual business functions
- **Tissue Level**: Related business processes  
- **Organ Level**: Complete business systems
- **Organism Level**: Entire business ecosystem

## Contributing

We welcome contributions from developers across Africa. See our [Developer Guide](docs/developers/README.md) for details.

## Support

- **Community**: Join our developer community
- **Documentation**: Comprehensive guides and API docs
- **Cultural Consultation**: African business advisors available
- **Voice Support**: Multi-language voice assistance

## License

MIT License - Built for African businesses, by African developers.
"""
        
        docs["README.md"] = readme
        
        # Architecture overview
        architecture_doc = """
# WebWaka Architecture Overview

## Biological Inspiration

WebWaka's architecture is inspired by biological systems, creating a natural and scalable structure.

### Cellular Level
Individual business functions that can operate independently:
- Sales transactions
- Inventory items
- Customer records
- Payment processing

### Tissue Level
Groups of related cells working together:
- Retail operations (sales + inventory + customers)
- Financial management (payments + accounting + reporting)
- Customer service (support + feedback + communication)

### Organ Level
Complete business systems:
- Point of Sale (POS) system
- Customer Relationship Management (CRM)
- Enterprise Resource Planning (ERP)
- Supply Chain Management (SCM)

### Organism Level
The complete business ecosystem:
- Multi-location management
- Partner integration
- Community cooperation
- Regional expansion

## Technical Architecture

### Backend Services
- **Python Flask**: RESTful API services
- **AI Integration**: Eden AI, Hugging Face, OpenRouter
- **Database**: SQLite (local), PostgreSQL (cloud)
- **Voice Processing**: Speech recognition and synthesis
- **Security**: JWT authentication, encryption

### Frontend Applications
- **React PWA**: Progressive Web Application
- **Mobile-First**: Touch-optimized interface
- **Offline-First**: Service worker implementation
- **Voice Interface**: Speech recognition integration
- **Cultural Adaptation**: African UI patterns

### AI Ecosystem
- **Eden AI**: Primary AI aggregation service
- **Hugging Face**: Open-source models for African languages
- **OpenRouter**: LLM diversity and backup services
- **Cultural Intelligence**: Ubuntu philosophy integration
- **Voice Processing**: Multi-language speech capabilities

### Infrastructure
- **Hostinger Horizons**: Primary hosting platform
- **GitHub**: Version control and CI/CD
- **Netlify**: Frontend deployment
- **African CDN**: Content delivery optimization
- **Mobile Networks**: 2G/3G/4G optimization
"""
        
        docs["docs/architecture.md"] = architecture_doc
        
        return docs
    
    async def save_documentation(self, documentation_files: Dict[str, str]) -> List[str]:
        """Save all documentation files to disk"""
        
        saved_files = []
        
        for relative_path, content in documentation_files.items():
            file_path = self.docs_dir / relative_path
            
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            saved_files.append(str(file_path))
            logger.info(f"Saved documentation: {relative_path}")
        
        return saved_files
    
    async def test_documentation_generation(self) -> Dict[str, Any]:
        """Test documentation generation capabilities"""
        
        test_results = {
            "api_documentation": False,
            "user_guides": False,
            "developer_documentation": False,
            "component_documentation": False,
            "file_generation": False
        }
        
        try:
            # Test API documentation
            api_docs = await self.generate_api_documentation()
            test_results["api_documentation"] = len(api_docs) > 0
            
            # Test user guides
            user_guides = await self.generate_user_guides()
            test_results["user_guides"] = len(user_guides) > 0
            
            # Test developer documentation
            dev_docs = await self.generate_developer_documentation()
            test_results["developer_documentation"] = len(dev_docs) > 0
            
            # Test component documentation
            component_docs = await self.generate_component_documentation()
            test_results["component_documentation"] = len(component_docs) > 0
            
            # Test file generation
            all_docs = {**api_docs, **user_guides, **dev_docs, **component_docs}
            saved_files = await self.save_documentation(all_docs)
            test_results["file_generation"] = len(saved_files) > 0
            
            logger.info("Documentation generation test completed successfully")
            
        except Exception as e:
            logger.error(f"Documentation generation test error: {e}")
        
        return test_results

# Example usage and testing
async def main():
    """Example usage of Documentation Systems Agent"""
    agent = DocumentationSystemsAgent()
    
    # Test capabilities
    test_results = await agent.test_documentation_generation()
    print("Documentation Systems Test Results:")
    for test, result in test_results.items():
        print(f"  {test}: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Generate complete documentation
    print("\nGenerating complete documentation suite...")
    documentation_files = await agent.generate_complete_documentation()
    
    print(f"Generated {len(documentation_files)} documentation files:")
    for file_path in documentation_files.keys():
        print(f"  - {file_path}")

if __name__ == "__main__":
    asyncio.run(main())

