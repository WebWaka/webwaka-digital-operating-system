"""
AI Orchestrator - Unified AI Service Management
Coordinates between Eden AI, Hugging Face, and OpenRouter for optimal performance and cost
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import time
import json

from .eden_ai_client import EdenAIClient, AIResponse
from .huggingface_client import HuggingFaceClient, HFResponse
from .openrouter_client import OpenRouterClient, OpenRouterResponse

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    EDEN_AI = "eden_ai"
    HUGGINGFACE = "huggingface"
    OPENROUTER = "openrouter"

class TaskType(Enum):
    CHAT = "chat"
    TRANSLATION = "translation"
    SPEECH_TO_TEXT = "speech_to_text"
    TEXT_TO_SPEECH = "text_to_speech"
    IMAGE_ANALYSIS = "image_analysis"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    DOCUMENT_ANALYSIS = "document_analysis"
    CODE_GENERATION = "code_generation"
    BUSINESS_CONSULTATION = "business_consultation"

@dataclass
class UnifiedResponse:
    """Unified response format across all AI providers"""
    success: bool
    data: Any
    provider: str
    model: str
    cost: float
    response_time: float
    tokens_used: int = 0
    error: Optional[str] = None
    fallback_used: bool = False
    cultural_score: Optional[float] = None

@dataclass
class ProviderConfig:
    """Configuration for each AI provider"""
    enabled: bool = True
    priority: int = 1  # 1 = highest priority
    cost_weight: float = 0.3  # Weight for cost optimization
    performance_weight: float = 0.4  # Weight for performance
    quality_weight: float = 0.3  # Weight for quality
    max_retries: int = 3
    timeout: float = 30.0

class AIOrchestrator:
    """
    AI Orchestrator for WebWaka Digital Operating System
    Manages multiple AI providers with intelligent routing and fallback
    """
    
    def __init__(self):
        # Initialize AI clients
        self.eden_ai = EdenAIClient()
        self.huggingface = HuggingFaceClient()
        self.openrouter = OpenRouterClient()
        
        # Provider configurations
        self.provider_configs = {
            AIProvider.EDEN_AI: ProviderConfig(enabled=True, priority=1),
            AIProvider.HUGGINGFACE: ProviderConfig(enabled=True, priority=2),
            AIProvider.OPENROUTER: ProviderConfig(enabled=True, priority=3)
        }
        
        # Task routing preferences
        self.task_routing = {
            TaskType.CHAT: [AIProvider.OPENROUTER, AIProvider.EDEN_AI, AIProvider.HUGGINGFACE],
            TaskType.TRANSLATION: [AIProvider.EDEN_AI, AIProvider.HUGGINGFACE, AIProvider.OPENROUTER],
            TaskType.SPEECH_TO_TEXT: [AIProvider.EDEN_AI, AIProvider.HUGGINGFACE],
            TaskType.TEXT_TO_SPEECH: [AIProvider.EDEN_AI],
            TaskType.IMAGE_ANALYSIS: [AIProvider.EDEN_AI, AIProvider.HUGGINGFACE],
            TaskType.SENTIMENT_ANALYSIS: [AIProvider.EDEN_AI, AIProvider.HUGGINGFACE],
            TaskType.DOCUMENT_ANALYSIS: [AIProvider.HUGGINGFACE, AIProvider.EDEN_AI],
            TaskType.CODE_GENERATION: [AIProvider.OPENROUTER, AIProvider.HUGGINGFACE],
            TaskType.BUSINESS_CONSULTATION: [AIProvider.OPENROUTER, AIProvider.EDEN_AI]
        }
        
        # Cost tracking
        self.cost_tracker = {
            "total_cost": 0.0,
            "provider_costs": {provider.value: 0.0 for provider in AIProvider},
            "daily_limit": float(os.getenv('DAILY_AI_COST_LIMIT', '10.0')),
            "monthly_limit": float(os.getenv('MONTHLY_AI_COST_LIMIT', '100.0'))
        }
        
        # Performance tracking
        self.performance_tracker = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "provider_performance": {provider.value: {"requests": 0, "successes": 0, "avg_time": 0.0} 
                                   for provider in AIProvider}
        }
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: Optional[str] = None,
                       max_tokens: int = 1000,
                       temperature: float = 0.7,
                       african_context: bool = True,
                       cost_optimize: bool = True) -> UnifiedResponse:
        """
        Unified chat completion with intelligent provider selection
        """
        start_time = time.time()
        
        try:
            # Select optimal provider
            providers = self._select_providers(TaskType.CHAT, cost_optimize)
            
            for provider in providers:
                try:
                    if provider == AIProvider.OPENROUTER:
                        response = self.openrouter.chat_completion(
                            messages=messages,
                            model=model,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            use_free_model=cost_optimize,
                            african_context=african_context
                        )
                        
                        if response.success:
                            return self._create_unified_response(
                                response, provider, start_time, fallback_used=provider != providers[0]
                            )
                    
                    elif provider == AIProvider.EDEN_AI:
                        response = self.eden_ai.chat_completion(
                            messages=messages,
                            model=model or "openai/gpt-3.5-turbo",
                            max_tokens=max_tokens,
                            temperature=temperature,
                            optimize_cost=cost_optimize
                        )
                        
                        if response.success:
                            return self._create_unified_response(
                                response, provider, start_time, fallback_used=provider != providers[0]
                            )
                    
                    elif provider == AIProvider.HUGGINGFACE:
                        response = self.huggingface.chat_completion(
                            messages=messages,
                            model=model or "microsoft/DialoGPT-medium",
                            max_tokens=max_tokens,
                            temperature=temperature,
                            african_context=african_context
                        )
                        
                        if response.success:
                            return self._create_unified_response(
                                response, provider, start_time, fallback_used=provider != providers[0]
                            )
                
                except Exception as e:
                    logger.warning(f"Provider {provider.value} failed: {str(e)}")
                    continue
            
            # All providers failed
            return UnifiedResponse(
                success=False,
                data=None,
                provider="none",
                model=model or "unknown",
                cost=0.0,
                response_time=time.time() - start_time,
                error="All AI providers failed"
            )
            
        except Exception as e:
            logger.error(f"AI Orchestrator chat completion error: {str(e)}")
            return UnifiedResponse(
                success=False,
                data=None,
                provider="orchestrator",
                model=model or "unknown",
                cost=0.0,
                response_time=time.time() - start_time,
                error=str(e)
            )
    
    def african_voice_processing(self, 
                               audio_data: bytes, 
                               language: str = "en",
                               task: str = "speech_to_text") -> UnifiedResponse:
        """
        Process voice input with African language optimization
        """
        start_time = time.time()
        
        try:
            if task == "speech_to_text":
                # Try Eden AI first for speech recognition
                try:
                    # For Eden AI, we need audio URL, so this is a simplified version
                    # In production, you'd upload the audio and get a URL
                    response = self.huggingface.speech_to_text_african(audio_data, language)
                    
                    if response.success:
                        return self._create_unified_response(
                            response, AIProvider.HUGGINGFACE, start_time
                        )
                except Exception as e:
                    logger.warning(f"Speech recognition failed: {str(e)}")
            
            return UnifiedResponse(
                success=False,
                data=None,
                provider="none",
                model="speech_processing",
                cost=0.0,
                response_time=time.time() - start_time,
                error="Voice processing failed"
            )
            
        except Exception as e:
            logger.error(f"African voice processing error: {str(e)}")
            return UnifiedResponse(
                success=False,
                data=None,
                provider="orchestrator",
                model="speech_processing",
                cost=0.0,
                response_time=time.time() - start_time,
                error=str(e)
            )
    
    def business_workflow_automation(self, 
                                   workflow_description: str, 
                                   sector: str,
                                   country: str = "general") -> UnifiedResponse:
        """
        Automate business workflows with AI assistance
        """
        start_time = time.time()
        
        try:
            # Use OpenRouter for business consultation
            response = self.openrouter.african_business_consultation(
                query=f"Create an automated workflow for: {workflow_description}",
                business_sector=sector,
                country=country
            )
            
            if response.success:
                return self._create_unified_response(
                    response, AIProvider.OPENROUTER, start_time
                )
            
            # Fallback to Eden AI
            messages = [
                {
                    "role": "system",
                    "content": f"You are a business automation expert for the {sector} sector in {country}. Create detailed workflow automation recommendations."
                },
                {
                    "role": "user",
                    "content": workflow_description
                }
            ]
            
            response = self.eden_ai.chat_completion(messages)
            
            if response.success:
                return self._create_unified_response(
                    response, AIProvider.EDEN_AI, start_time, fallback_used=True
                )
            
            return UnifiedResponse(
                success=False,
                data=None,
                provider="none",
                model="workflow_automation",
                cost=0.0,
                response_time=time.time() - start_time,
                error="Workflow automation failed"
            )
            
        except Exception as e:
            logger.error(f"Business workflow automation error: {str(e)}")
            return UnifiedResponse(
                success=False,
                data=None,
                provider="orchestrator",
                model="workflow_automation",
                cost=0.0,
                response_time=time.time() - start_time,
                error=str(e)
            )
    
    def cultural_intelligence_analysis(self, 
                                     content: str, 
                                     cultural_context: str = "general_african") -> UnifiedResponse:
        """
        Analyze content for cultural appropriateness and intelligence
        """
        start_time = time.time()
        
        try:
            # Use Hugging Face for cultural intelligence
            response = self.huggingface.cultural_intelligence_check(content, cultural_context)
            
            if response.success:
                unified_response = self._create_unified_response(
                    response, AIProvider.HUGGINGFACE, start_time
                )
                unified_response.cultural_score = response.data.get("confidence", 0.0)
                return unified_response
            
            # Fallback to sentiment analysis via Eden AI
            response = self.eden_ai.sentiment_analysis(content)
            
            if response.success:
                # Convert sentiment to cultural score
                cultural_score = 0.8 if response.data.get("sentiment") == "POSITIVE" else 0.4
                unified_response = self._create_unified_response(
                    response, AIProvider.EDEN_AI, start_time, fallback_used=True
                )
                unified_response.cultural_score = cultural_score
                return unified_response
            
            return UnifiedResponse(
                success=False,
                data=None,
                provider="none",
                model="cultural_intelligence",
                cost=0.0,
                response_time=time.time() - start_time,
                error="Cultural intelligence analysis failed"
            )
            
        except Exception as e:
            logger.error(f"Cultural intelligence analysis error: {str(e)}")
            return UnifiedResponse(
                success=False,
                data=None,
                provider="orchestrator",
                model="cultural_intelligence",
                cost=0.0,
                response_time=time.time() - start_time,
                error=str(e)
            )
    
    def _select_providers(self, task_type: TaskType, cost_optimize: bool = True) -> List[AIProvider]:
        """
        Select optimal providers for a given task
        """
        # Get preferred providers for this task
        preferred_providers = self.task_routing.get(task_type, list(AIProvider))
        
        # Filter enabled providers
        available_providers = [p for p in preferred_providers 
                             if self.provider_configs[p].enabled]
        
        if cost_optimize:
            # Prioritize free/low-cost providers
            cost_priority = [AIProvider.HUGGINGFACE, AIProvider.OPENROUTER, AIProvider.EDEN_AI]
            available_providers = sorted(available_providers, 
                                       key=lambda p: cost_priority.index(p) if p in cost_priority else 999)
        
        return available_providers
    
    def _create_unified_response(self, 
                               response: Union[AIResponse, HFResponse, OpenRouterResponse], 
                               provider: AIProvider, 
                               start_time: float,
                               fallback_used: bool = False) -> UnifiedResponse:
        """
        Create unified response from provider-specific response
        """
        response_time = time.time() - start_time
        
        # Extract common fields
        if isinstance(response, OpenRouterResponse):
            cost = response.cost
            tokens_used = response.tokens_used
        elif isinstance(response, AIResponse):
            cost = response.cost
            tokens_used = 0  # Eden AI doesn't always provide token count
        else:  # HFResponse
            cost = response.cost
            tokens_used = 0  # Hugging Face is mostly free
        
        # Update cost tracking
        self._update_cost_tracking(provider, cost)
        
        # Update performance tracking
        self._update_performance_tracking(provider, response.success, response_time)
        
        return UnifiedResponse(
            success=response.success,
            data=response.data,
            provider=provider.value,
            model=response.model,
            cost=cost,
            response_time=response_time,
            tokens_used=tokens_used,
            error=response.error,
            fallback_used=fallback_used
        )
    
    def _update_cost_tracking(self, provider: AIProvider, cost: float):
        """Update cost tracking statistics"""
        self.cost_tracker["total_cost"] += cost
        self.cost_tracker["provider_costs"][provider.value] += cost
    
    def _update_performance_tracking(self, provider: AIProvider, success: bool, response_time: float):
        """Update performance tracking statistics"""
        self.performance_tracker["total_requests"] += 1
        
        if success:
            self.performance_tracker["successful_requests"] += 1
        else:
            self.performance_tracker["failed_requests"] += 1
        
        # Update provider-specific stats
        provider_stats = self.performance_tracker["provider_performance"][provider.value]
        provider_stats["requests"] += 1
        if success:
            provider_stats["successes"] += 1
        
        # Update average response time
        current_avg = provider_stats["avg_time"]
        request_count = provider_stats["requests"]
        provider_stats["avg_time"] = ((current_avg * (request_count - 1)) + response_time) / request_count
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status and statistics
        """
        return {
            "cost_tracking": self.cost_tracker,
            "performance_tracking": self.performance_tracker,
            "provider_configs": {p.value: {
                "enabled": config.enabled,
                "priority": config.priority
            } for p, config in self.provider_configs.items()},
            "health_check": self._health_check()
        }
    
    def _health_check(self) -> Dict[str, str]:
        """
        Perform health check on all providers
        """
        health_status = {}
        
        # Test each provider with a simple request
        test_messages = [{"role": "user", "content": "Hello"}]
        
        try:
            # Test OpenRouter
            response = self.openrouter.chat_completion(test_messages, max_tokens=10, use_free_model=True)
            health_status["openrouter"] = "healthy" if response.success else "unhealthy"
        except:
            health_status["openrouter"] = "error"
        
        try:
            # Test Eden AI
            response = self.eden_ai.chat_completion(test_messages, max_tokens=10)
            health_status["eden_ai"] = "healthy" if response.success else "unhealthy"
        except:
            health_status["eden_ai"] = "error"
        
        try:
            # Test Hugging Face
            response = self.huggingface.chat_completion(test_messages, max_tokens=10)
            health_status["huggingface"] = "healthy" if response.success else "unhealthy"
        except:
            health_status["huggingface"] = "error"
        
        return health_status
    
    def optimize_costs(self) -> Dict[str, Any]:
        """
        Analyze and optimize AI costs
        """
        recommendations = []
        
        # Check if approaching limits
        daily_usage = self.cost_tracker["total_cost"]  # Simplified - should be daily only
        if daily_usage > self.cost_tracker["daily_limit"] * 0.8:
            recommendations.append("Approaching daily cost limit - consider using more free models")
        
        # Analyze provider efficiency
        for provider, stats in self.performance_tracker["provider_performance"].items():
            if stats["requests"] > 0:
                success_rate = stats["successes"] / stats["requests"]
                if success_rate < 0.8:
                    recommendations.append(f"Provider {provider} has low success rate: {success_rate:.2%}")
        
        return {
            "current_costs": self.cost_tracker,
            "recommendations": recommendations,
            "optimization_suggestions": [
                "Use Hugging Face for simple tasks (free)",
                "Use OpenRouter free models for basic chat",
                "Reserve Eden AI for complex multi-modal tasks",
                "Enable cost optimization in all requests"
            ]
        }

