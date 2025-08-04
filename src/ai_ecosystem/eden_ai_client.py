"""
Eden AI Client - Primary AI Aggregation Layer
Provides unified access to comprehensive AI services with cost optimization
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """Standardized AI response format"""
    success: bool
    data: Any
    provider: str
    cost: float
    model: str
    error: Optional[str] = None

class EdenAIClient:
    """
    Eden AI Client for comprehensive AI services
    Supports: LLM, Computer Vision, NLP, Speech, Translation, and more
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('EDEN_AI_API_KEY')
        self.base_url = "https://api.edenai.run/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if not self.api_key:
            logger.warning("Eden AI API key not found. Set EDEN_AI_API_KEY environment variable.")
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: str = "openai/gpt-3.5-turbo",
                       max_tokens: int = 1000,
                       temperature: float = 0.7,
                       optimize_cost: bool = True) -> AIResponse:
        """
        Chat completion with automatic cost optimization
        """
        try:
            payload = {
                "providers": model,
                "text": messages[-1]["content"] if messages else "",
                "chatbot_global_action": "You are a helpful AI assistant for WebWaka Digital Operating System.",
                "previous_history": messages[:-1] if len(messages) > 1 else [],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "fallback_providers": "openai/gpt-3.5-turbo,anthropic/claude-3-haiku" if optimize_cost else ""
            }
            
            response = requests.post(
                f"{self.base_url}/text/chat",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                provider_result = list(result.keys())[0]
                
                return AIResponse(
                    success=True,
                    data=result[provider_result]["generated_text"],
                    provider=provider_result,
                    cost=result[provider_result].get("cost", 0.0),
                    model=model
                )
            else:
                return AIResponse(
                    success=False,
                    data=None,
                    provider="eden_ai",
                    cost=0.0,
                    model=model,
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Eden AI chat completion error: {str(e)}")
            return AIResponse(
                success=False,
                data=None,
                provider="eden_ai",
                cost=0.0,
                model=model,
                error=str(e)
            )
    
    def text_to_speech(self, 
                      text: str, 
                      language: str = "en",
                      voice: str = "FEMALE",
                      optimize_cost: bool = True) -> AIResponse:
        """
        Text-to-speech with African language support
        """
        try:
            payload = {
                "providers": "amazon,google,microsoft",
                "language": language,
                "text": text,
                "option": voice,
                "fallback_providers": "amazon" if optimize_cost else ""
            }
            
            response = requests.post(
                f"{self.base_url}/audio/text_to_speech",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                provider_result = list(result.keys())[0]
                
                return AIResponse(
                    success=True,
                    data=result[provider_result]["audio_resource_url"],
                    provider=provider_result,
                    cost=result[provider_result].get("cost", 0.0),
                    model="tts"
                )
            else:
                return AIResponse(
                    success=False,
                    data=None,
                    provider="eden_ai",
                    cost=0.0,
                    model="tts",
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Eden AI TTS error: {str(e)}")
            return AIResponse(
                success=False,
                data=None,
                provider="eden_ai",
                cost=0.0,
                model="tts",
                error=str(e)
            )
    
    def speech_to_text(self, 
                      audio_url: str, 
                      language: str = "en",
                      optimize_cost: bool = True) -> AIResponse:
        """
        Speech-to-text with African language support
        """
        try:
            payload = {
                "providers": "amazon,google,microsoft",
                "language": language,
                "file_url": audio_url,
                "fallback_providers": "amazon" if optimize_cost else ""
            }
            
            response = requests.post(
                f"{self.base_url}/audio/speech_to_text_async",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                provider_result = list(result.keys())[0]
                
                return AIResponse(
                    success=True,
                    data=result[provider_result]["text"],
                    provider=provider_result,
                    cost=result[provider_result].get("cost", 0.0),
                    model="stt"
                )
            else:
                return AIResponse(
                    success=False,
                    data=None,
                    provider="eden_ai",
                    cost=0.0,
                    model="stt",
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Eden AI STT error: {str(e)}")
            return AIResponse(
                success=False,
                data=None,
                provider="eden_ai",
                cost=0.0,
                model="stt",
                error=str(e)
            )
    
    def translate_text(self, 
                      text: str, 
                      source_language: str, 
                      target_language: str,
                      optimize_cost: bool = True) -> AIResponse:
        """
        Translation with African language support
        """
        try:
            payload = {
                "providers": "google,amazon,microsoft",
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
                "fallback_providers": "google" if optimize_cost else ""
            }
            
            response = requests.post(
                f"{self.base_url}/translation/automatic_translation",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                provider_result = list(result.keys())[0]
                
                return AIResponse(
                    success=True,
                    data=result[provider_result]["text"],
                    provider=provider_result,
                    cost=result[provider_result].get("cost", 0.0),
                    model="translation"
                )
            else:
                return AIResponse(
                    success=False,
                    data=None,
                    provider="eden_ai",
                    cost=0.0,
                    model="translation",
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Eden AI translation error: {str(e)}")
            return AIResponse(
                success=False,
                data=None,
                provider="eden_ai",
                cost=0.0,
                model="translation",
                error=str(e)
            )
    
    def analyze_image(self, 
                     image_url: str, 
                     analysis_type: str = "object_detection",
                     optimize_cost: bool = True) -> AIResponse:
        """
        Computer vision analysis for business applications
        """
        try:
            endpoint_map = {
                "object_detection": "vision/object_detection",
                "face_detection": "vision/face_detection",
                "text_detection": "vision/ocr",
                "logo_detection": "vision/logo_detection"
            }
            
            endpoint = endpoint_map.get(analysis_type, "vision/object_detection")
            
            payload = {
                "providers": "google,amazon,microsoft",
                "file_url": image_url,
                "fallback_providers": "google" if optimize_cost else ""
            }
            
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                provider_result = list(result.keys())[0]
                
                return AIResponse(
                    success=True,
                    data=result[provider_result]["items"],
                    provider=provider_result,
                    cost=result[provider_result].get("cost", 0.0),
                    model=analysis_type
                )
            else:
                return AIResponse(
                    success=False,
                    data=None,
                    provider="eden_ai",
                    cost=0.0,
                    model=analysis_type,
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Eden AI image analysis error: {str(e)}")
            return AIResponse(
                success=False,
                data=None,
                provider="eden_ai",
                cost=0.0,
                model=analysis_type,
                error=str(e)
            )
    
    def sentiment_analysis(self, 
                          text: str, 
                          language: str = "en",
                          optimize_cost: bool = True) -> AIResponse:
        """
        Sentiment analysis for customer feedback and social monitoring
        """
        try:
            payload = {
                "providers": "amazon,google,microsoft",
                "text": text,
                "language": language,
                "fallback_providers": "amazon" if optimize_cost else ""
            }
            
            response = requests.post(
                f"{self.base_url}/text/sentiment_analysis",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                provider_result = list(result.keys())[0]
                
                return AIResponse(
                    success=True,
                    data={
                        "sentiment": result[provider_result]["general_sentiment"],
                        "confidence": result[provider_result]["general_sentiment_rate"]
                    },
                    provider=provider_result,
                    cost=result[provider_result].get("cost", 0.0),
                    model="sentiment"
                )
            else:
                return AIResponse(
                    success=False,
                    data=None,
                    provider="eden_ai",
                    cost=0.0,
                    model="sentiment",
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Eden AI sentiment analysis error: {str(e)}")
            return AIResponse(
                success=False,
                data=None,
                provider="eden_ai",
                cost=0.0,
                model="sentiment",
                error=str(e)
            )
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics and cost tracking
        """
        try:
            response = requests.get(
                f"{self.base_url}/info/usage",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Eden AI usage stats error: {str(e)}")
            return {"error": str(e)}

