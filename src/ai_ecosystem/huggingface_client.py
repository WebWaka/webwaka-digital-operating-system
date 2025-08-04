"""
Hugging Face Client - Open-Source AI Models for African Contexts
Specialized in African languages and culturally adapted models
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import logging
from huggingface_hub import InferenceClient, list_models
import time

logger = logging.getLogger(__name__)

@dataclass
class HFResponse:
    """Standardized Hugging Face response format"""
    success: bool
    data: Any
    model: str
    cost: float = 0.0  # Most HF models are free/low-cost
    error: Optional[str] = None
    inference_time: float = 0.0

class HuggingFaceClient:
    """
    Hugging Face Client for open-source AI models
    Specialized in African languages and cultural adaptation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.client = InferenceClient(token=self.api_key)
        
        # African language models mapping
        self.african_language_models = {
            "swahili": "benjamin/autonlp-swahili-sentiment-615517563",
            "yoruba": "Davlan/distilbert-base-multilingual-cased-ner-hrl",
            "hausa": "Davlan/bert-base-multilingual-cased-ner-hrl",
            "amharic": "Davlan/distilbert-base-multilingual-cased-ner-hrl",
            "zulu": "Davlan/distilbert-base-multilingual-cased-ner-hrl",
            "xhosa": "Davlan/distilbert-base-multilingual-cased-ner-hrl",
            "afrikaans": "Davlan/distilbert-base-multilingual-cased-ner-hrl",
            "multilingual_african": "masakhane/afriberta_large"
        }
        
        # Recommended models for different tasks
        self.task_models = {
            "text_generation": "microsoft/DialoGPT-medium",
            "sentiment_analysis": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "translation": "Helsinki-NLP/opus-mt-en-mul",
            "summarization": "facebook/bart-large-cnn",
            "question_answering": "deepset/roberta-base-squad2",
            "text_classification": "microsoft/DialoGPT-medium",
            "speech_recognition": "facebook/wav2vec2-large-960h-lv60-self",
            "image_classification": "google/vit-base-patch16-224",
            "object_detection": "facebook/detr-resnet-50"
        }
        
        if not self.api_key:
            logger.warning("Hugging Face API key not found. Some features may be limited.")
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: str = "microsoft/DialoGPT-medium",
                       max_tokens: int = 1000,
                       temperature: float = 0.7,
                       african_context: bool = True) -> HFResponse:
        """
        Chat completion with African cultural context
        """
        start_time = time.time()
        
        try:
            # Prepare context for African cultural intelligence
            system_prompt = ""
            if african_context:
                system_prompt = """You are an AI assistant designed for African users. 
                Respect Ubuntu philosophy, understand diverse African cultures, 
                and provide culturally appropriate responses. Consider local contexts, 
                traditional values, and community-oriented thinking."""
            
            # Combine messages into a single prompt for simpler models
            conversation = system_prompt + "\n"
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                conversation += f"{role.capitalize()}: {content}\n"
            conversation += "Assistant:"
            
            response = self.client.text_generation(
                conversation,
                model=model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                return_full_text=False
            )
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=response,
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"Hugging Face chat completion error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model=model,
                error=str(e),
                inference_time=time.time() - start_time
            )
    
    def african_language_processing(self, 
                                  text: str, 
                                  language: str, 
                                  task: str = "sentiment") -> HFResponse:
        """
        Process text in African languages
        """
        start_time = time.time()
        
        try:
            # Select appropriate model for the language
            model = self.african_language_models.get(
                language.lower(), 
                self.african_language_models["multilingual_african"]
            )
            
            if task == "sentiment":
                result = self.client.text_classification(text, model=model)
            elif task == "ner":  # Named Entity Recognition
                result = self.client.token_classification(text, model=model)
            else:
                result = self.client.text_generation(text, model=model, max_new_tokens=100)
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=result,
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"African language processing error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model=model if 'model' in locals() else "unknown",
                error=str(e),
                inference_time=time.time() - start_time
            )
    
    def translate_african_languages(self, 
                                  text: str, 
                                  source_lang: str, 
                                  target_lang: str) -> HFResponse:
        """
        Translation between African languages and major languages
        """
        start_time = time.time()
        
        try:
            # Use multilingual translation model
            model = "Helsinki-NLP/opus-mt-mul-en"
            
            # For African languages, we might need to use English as intermediate
            if source_lang in self.african_language_models:
                # First translate to English, then to target
                intermediate = self.client.translation(text, model=model)
                if target_lang != "en":
                    target_model = f"Helsinki-NLP/opus-mt-en-{target_lang}"
                    result = self.client.translation(intermediate[0]["translation_text"], model=target_model)
                else:
                    result = intermediate
            else:
                # Direct translation
                translation_model = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
                result = self.client.translation(text, model=translation_model)
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=result[0]["translation_text"] if result else text,
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"African language translation error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model="translation",
                error=str(e),
                inference_time=time.time() - start_time
            )
    
    def speech_to_text_african(self, 
                             audio_data: bytes, 
                             language: str = "en") -> HFResponse:
        """
        Speech recognition optimized for African accents and languages
        """
        start_time = time.time()
        
        try:
            # Use Wav2Vec2 model optimized for diverse accents
            model = "facebook/wav2vec2-large-960h-lv60-self"
            
            result = self.client.automatic_speech_recognition(audio_data, model=model)
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=result["text"],
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"African speech recognition error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model="speech_recognition",
                error=str(e),
                inference_time=time.time() - start_time
            )
    
    def business_document_analysis(self, 
                                 text: str, 
                                 analysis_type: str = "summarization") -> HFResponse:
        """
        Analyze business documents with African business context
        """
        start_time = time.time()
        
        try:
            model = self.task_models.get(analysis_type, "facebook/bart-large-cnn")
            
            if analysis_type == "summarization":
                result = self.client.summarization(text, model=model)
                data = result[0]["summary_text"]
            elif analysis_type == "sentiment":
                result = self.client.text_classification(text, model=model)
                data = result[0]
            elif analysis_type == "question_answering":
                # For Q&A, we need a question - use a default business question
                question = "What are the key business insights from this document?"
                result = self.client.question_answering(question=question, context=text, model=model)
                data = result["answer"]
            else:
                result = self.client.text_generation(text, model=model, max_new_tokens=200)
                data = result
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=data,
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"Business document analysis error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model=model if 'model' in locals() else "unknown",
                error=str(e),
                inference_time=time.time() - start_time
            )
    
    def image_analysis_african_context(self, 
                                     image_data: bytes, 
                                     task: str = "classification") -> HFResponse:
        """
        Image analysis with African context understanding
        """
        start_time = time.time()
        
        try:
            if task == "classification":
                model = "google/vit-base-patch16-224"
                result = self.client.image_classification(image_data, model=model)
            elif task == "object_detection":
                model = "facebook/detr-resnet-50"
                result = self.client.object_detection(image_data, model=model)
            else:
                model = "google/vit-base-patch16-224"
                result = self.client.image_classification(image_data, model=model)
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=result,
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"African context image analysis error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model="image_analysis",
                error=str(e),
                inference_time=time.time() - start_time
            )
    
    def get_available_african_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available African language and context models
        """
        try:
            # Search for African-related models
            african_models = []
            
            # Add our curated African language models
            for lang, model_id in self.african_language_models.items():
                african_models.append({
                    "language": lang,
                    "model_id": model_id,
                    "type": "language_processing",
                    "description": f"Model optimized for {lang} language processing"
                })
            
            # Search for additional African models on the hub
            try:
                models = list_models(
                    search="african OR swahili OR yoruba OR hausa OR amharic",
                    limit=20
                )
                
                for model in models:
                    african_models.append({
                        "model_id": model.modelId,
                        "type": "community",
                        "description": f"Community model: {model.modelId}",
                        "downloads": getattr(model, 'downloads', 0)
                    })
            except Exception as e:
                logger.warning(f"Could not fetch community models: {str(e)}")
            
            return african_models
            
        except Exception as e:
            logger.error(f"Error getting African models: {str(e)}")
            return []
    
    def cultural_intelligence_check(self, 
                                  text: str, 
                                  cultural_context: str = "general_african") -> HFResponse:
        """
        Check text for cultural appropriateness and intelligence
        """
        start_time = time.time()
        
        try:
            # Use sentiment analysis as a proxy for cultural appropriateness
            model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
            
            # Add cultural context to the analysis
            cultural_prompt = f"""
            Analyze this text for cultural appropriateness in {cultural_context} context:
            "{text}"
            
            Consider: Ubuntu philosophy, community values, respect for elders, 
            traditional practices, and inclusive language.
            """
            
            result = self.client.text_classification(cultural_prompt, model=model)
            
            # Interpret results for cultural intelligence
            cultural_score = {
                "appropriateness": "high" if result[0]["label"] == "POSITIVE" else "medium",
                "confidence": result[0]["score"],
                "recommendations": []
            }
            
            if result[0]["label"] == "NEGATIVE":
                cultural_score["recommendations"].append(
                    "Consider more culturally sensitive language"
                )
            
            inference_time = time.time() - start_time
            
            return HFResponse(
                success=True,
                data=cultural_score,
                model=model,
                inference_time=inference_time
            )
            
        except Exception as e:
            logger.error(f"Cultural intelligence check error: {str(e)}")
            return HFResponse(
                success=False,
                data=None,
                model="cultural_intelligence",
                error=str(e),
                inference_time=time.time() - start_time
            )

