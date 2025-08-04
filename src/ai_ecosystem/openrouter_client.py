"""
OpenRouter Client - LLM Diversity and Backup Provider
Access to 300+ LLMs through unified API with cost optimization
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
import time

logger = logging.getLogger(__name__)

@dataclass
class OpenRouterResponse:
    """Standardized OpenRouter response format"""
    success: bool
    data: Any
    model: str
    cost: float
    tokens_used: int
    provider: str
    error: Optional[str] = None
    response_time: float = 0.0

class OpenRouterClient:
    """
    OpenRouter Client for LLM diversity and backup capabilities
    Provides access to 300+ LLMs with cost optimization
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://webwaka.com",
            "X-Title": "WebWaka Digital Operating System"
        }
        
        # Free models available on OpenRouter
        self.free_models = [
            "huggingface/meta-llama/Llama-3.2-1B-Instruct",
            "huggingface/Qwen/Qwen2.5-Coder-32B-Instruct",
            "google/gemma-2-9b-it:free",
            "microsoft/phi-3-mini-128k-instruct:free",
            "meta-llama/llama-3.1-8b-instruct:free"
        ]
        
        # Cost-effective models for different use cases
        self.cost_effective_models = {
            "general_chat": "anthropic/claude-3-haiku",
            "coding": "huggingface/Qwen/Qwen2.5-Coder-32B-Instruct",
            "analysis": "google/gemini-flash-1.5",
            "creative": "meta-llama/llama-3.1-8b-instruct",
            "african_context": "anthropic/claude-3-haiku"  # Good for cultural understanding
        }
        
        if not self.api_key:
            logger.warning("OpenRouter API key not found. Set OPENROUTER_API_KEY environment variable.")
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: Optional[str] = None,
                       max_tokens: int = 1000,
                       temperature: float = 0.7,
                       use_free_model: bool = True,
                       african_context: bool = True) -> OpenRouterResponse:
        """
        Chat completion with model selection and cost optimization
        """
        start_time = time.time()
        
        try:
            # Select model based on preferences
            if model is None:
                if use_free_model:
                    model = self.free_models[0]  # Default to first free model
                else:
                    model = self.cost_effective_models["general_chat"]
            
            # Add African cultural context if requested
            if african_context and messages:
                system_message = {
                    "role": "system",
                    "content": """You are an AI assistant designed for African users and contexts. 
                    Understand and respect Ubuntu philosophy, diverse African cultures, traditional values, 
                    and community-oriented thinking. Provide culturally appropriate responses that consider 
                    local contexts, languages, and business practices across Africa."""
                }
                
                # Insert system message if not already present
                if messages[0].get("role") != "system":
                    messages = [system_message] + messages
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract usage and cost information
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                
                # Estimate cost (OpenRouter provides this in headers sometimes)
                cost = 0.0
                if "x-ratelimit-remaining-credits" in response.headers:
                    # Calculate approximate cost based on token usage
                    # This is an approximation - actual costs vary by model
                    cost = total_tokens * 0.000001  # Very rough estimate
                
                return OpenRouterResponse(
                    success=True,
                    data=result["choices"][0]["message"]["content"],
                    model=model,
                    cost=cost,
                    tokens_used=total_tokens,
                    provider="openrouter",
                    response_time=response_time
                )
            else:
                return OpenRouterResponse(
                    success=False,
                    data=None,
                    model=model,
                    cost=0.0,
                    tokens_used=0,
                    provider="openrouter",
                    error=f"API Error: {response.status_code} - {response.text}",
                    response_time=response_time
                )
                
        except Exception as e:
            logger.error(f"OpenRouter chat completion error: {str(e)}")
            return OpenRouterResponse(
                success=False,
                data=None,
                model=model or "unknown",
                cost=0.0,
                tokens_used=0,
                provider="openrouter",
                error=str(e),
                response_time=time.time() - start_time
            )
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models with pricing information
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers
            )
            
            if response.status_code == 200:
                models = response.json()["data"]
                
                # Filter and organize models
                organized_models = {
                    "free": [],
                    "cost_effective": [],
                    "premium": []
                }
                
                for model in models:
                    model_info = {
                        "id": model["id"],
                        "name": model.get("name", model["id"]),
                        "description": model.get("description", ""),
                        "context_length": model.get("context_length", 0),
                        "pricing": model.get("pricing", {}),
                        "top_provider": model.get("top_provider", {})
                    }
                    
                    # Categorize by cost
                    pricing = model.get("pricing", {})
                    prompt_cost = float(pricing.get("prompt", "0"))
                    
                    if prompt_cost == 0:
                        organized_models["free"].append(model_info)
                    elif prompt_cost < 0.000001:  # Very low cost
                        organized_models["cost_effective"].append(model_info)
                    else:
                        organized_models["premium"].append(model_info)
                
                return organized_models
            else:
                logger.error(f"Failed to get models: {response.status_code}")
                return {"error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return {"error": str(e)}
    
    def african_business_consultation(self, 
                                    query: str, 
                                    business_sector: str,
                                    country: str = "general") -> OpenRouterResponse:
        """
        Specialized consultation for African business contexts
        """
        start_time = time.time()
        
        try:
            # Use a model good for analysis and cultural understanding
            model = self.cost_effective_models["african_context"]
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a business consultant specializing in African markets and the {business_sector} sector. 
                    You understand local business practices, regulatory environments, cultural considerations, 
                    and economic conditions across Africa, with specific knowledge of {country} if applicable.
                    
                    Provide practical, culturally appropriate business advice that considers:
                    - Local market conditions and opportunities
                    - Cultural business practices and Ubuntu philosophy
                    - Regulatory and compliance requirements
                    - Infrastructure challenges and solutions
                    - Community-centered business approaches
                    - Traditional and modern business integration"""
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            return self.chat_completion(
                messages=messages,
                model=model,
                max_tokens=1500,
                temperature=0.7,
                use_free_model=False,
                african_context=False  # Already included in system message
            )
            
        except Exception as e:
            logger.error(f"African business consultation error: {str(e)}")
            return OpenRouterResponse(
                success=False,
                data=None,
                model="consultation",
                cost=0.0,
                tokens_used=0,
                provider="openrouter",
                error=str(e),
                response_time=time.time() - start_time
            )
    
    def code_generation_african_context(self, 
                                      requirements: str, 
                                      programming_language: str = "python",
                                      framework: str = "flask") -> OpenRouterResponse:
        """
        Generate code with African business context considerations
        """
        start_time = time.time()
        
        try:
            model = self.cost_effective_models["coding"]
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are an expert software developer specializing in applications for African markets. 
                    Generate {programming_language} code using {framework} that considers:
                    
                    - Offline-first capabilities for poor internet connectivity
                    - Mobile-first design for smartphone-dominant markets
                    - Multi-language support for African languages
                    - Low-bandwidth optimization
                    - Cultural appropriateness in UI/UX
                    - Local payment system integration
                    - SMS and USSD fallback options
                    - Community-centered features
                    
                    Write clean, well-documented, production-ready code."""
                },
                {
                    "role": "user",
                    "content": f"Generate code for: {requirements}"
                }
            ]
            
            return self.chat_completion(
                messages=messages,
                model=model,
                max_tokens=2000,
                temperature=0.3,  # Lower temperature for more consistent code
                use_free_model=True,  # Coding models often available for free
                african_context=False  # Already included in system message
            )
            
        except Exception as e:
            logger.error(f"Code generation error: {str(e)}")
            return OpenRouterResponse(
                success=False,
                data=None,
                model="coding",
                cost=0.0,
                tokens_used=0,
                provider="openrouter",
                error=str(e),
                response_time=time.time() - start_time
            )
    
    def multi_language_translation(self, 
                                 text: str, 
                                 source_language: str, 
                                 target_language: str,
                                 cultural_adaptation: bool = True) -> OpenRouterResponse:
        """
        Translation with cultural adaptation for African languages
        """
        start_time = time.time()
        
        try:
            model = self.cost_effective_models["general_chat"]
            
            cultural_note = ""
            if cultural_adaptation:
                cultural_note = """
                Ensure the translation is culturally appropriate and considers:
                - Local idioms and expressions
                - Cultural context and sensitivity
                - Business and social etiquette
                - Traditional and modern language usage
                """
            
            messages = [
                {
                    "role": "system",
                    "content": f"""You are an expert translator specializing in African languages and cultural contexts. 
                    Translate accurately while preserving meaning and cultural appropriateness.
                    {cultural_note}"""
                },
                {
                    "role": "user",
                    "content": f"Translate this text from {source_language} to {target_language}:\n\n{text}"
                }
            ]
            
            return self.chat_completion(
                messages=messages,
                model=model,
                max_tokens=1000,
                temperature=0.3,
                use_free_model=True,
                african_context=False  # Already included in system message
            )
            
        except Exception as e:
            logger.error(f"Multi-language translation error: {str(e)}")
            return OpenRouterResponse(
                success=False,
                data=None,
                model="translation",
                cost=0.0,
                tokens_used=0,
                provider="openrouter",
                error=str(e),
                response_time=time.time() - start_time
            )
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics and remaining credits
        """
        try:
            response = requests.get(
                f"{self.base_url}/auth/key",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"OpenRouter usage stats error: {str(e)}")
            return {"error": str(e)}
    
    def test_free_models(self) -> Dict[str, Any]:
        """
        Test all free models to ensure they're working
        """
        results = {}
        test_message = [{"role": "user", "content": "Hello, please respond with 'Working' if you can understand this message."}]
        
        for model in self.free_models:
            try:
                response = self.chat_completion(
                    messages=test_message,
                    model=model,
                    max_tokens=50,
                    use_free_model=True,
                    african_context=False
                )
                
                results[model] = {
                    "status": "working" if response.success else "failed",
                    "response": response.data if response.success else response.error,
                    "cost": response.cost,
                    "response_time": response.response_time
                }
                
            except Exception as e:
                results[model] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results

