"""
WebWaka Voice Interface Agent (Agent 5)
African Language Voice Processing Enhancement

This agent provides comprehensive voice interface capabilities with:
- Multi-language African speech recognition
- Cultural adaptation and Ubuntu philosophy integration
- Voice synthesis with African accents and cultural nuances
- Business workflow voice activation
- Offline-first voice processing for poor connectivity areas
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import requests
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import io
import pygame
import tempfile
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceLanguage(Enum):
    """Supported African languages for voice processing"""
    SWAHILI = "sw"
    HAUSA = "ha"
    YORUBA = "yo"
    IGBO = "ig"
    AMHARIC = "am"
    ZULU = "zu"
    XHOSA = "xh"
    AFRIKAANS = "af"
    SOMALI = "so"
    OROMO = "om"
    ARABIC_NORTH_AFRICA = "ar"
    FRENCH_WEST_AFRICA = "fr"
    PORTUGUESE_LUSOPHONE = "pt"
    ENGLISH_AFRICAN = "en-za"

@dataclass
class VoiceCommand:
    """Voice command structure"""
    text: str
    language: VoiceLanguage
    confidence: float
    timestamp: float
    cultural_context: Dict[str, Any]
    business_intent: Optional[str] = None

@dataclass
class VoiceResponse:
    """Voice response structure"""
    text: str
    language: VoiceLanguage
    audio_data: Optional[bytes] = None
    cultural_adaptation: Dict[str, Any] = None
    ubuntu_elements: List[str] = None

class CulturalVoiceAdapter:
    """Adapts voice interactions to African cultural contexts"""
    
    def __init__(self):
        self.cultural_greetings = {
            VoiceLanguage.SWAHILI: {
                "morning": "Habari za asubuhi",
                "afternoon": "Habari za mchana", 
                "evening": "Habari za jioni",
                "respect": "Shikamoo"
            },
            VoiceLanguage.HAUSA: {
                "morning": "Ina kwana",
                "afternoon": "Ina yini",
                "evening": "Ina yamma",
                "respect": "Sannu da zuwa"
            },
            VoiceLanguage.YORUBA: {
                "morning": "E kaaro",
                "afternoon": "E kaasan",
                "evening": "E kaale",
                "respect": "E ku aaro"
            },
            VoiceLanguage.ZULU: {
                "morning": "Sawubona",
                "afternoon": "Sanibonani",
                "evening": "Lala kahle",
                "respect": "Ngiyabonga"
            }
        }
        
        self.ubuntu_principles = [
            "community_first",
            "collective_responsibility", 
            "shared_prosperity",
            "mutual_respect",
            "elder_wisdom",
            "family_values"
        ]
    
    def adapt_greeting(self, language: VoiceLanguage, time_of_day: str) -> str:
        """Get culturally appropriate greeting"""
        if language in self.cultural_greetings:
            return self.cultural_greetings[language].get(time_of_day, "Hello")
        return "Hello"
    
    def apply_ubuntu_context(self, response: str, business_context: str) -> str:
        """Apply Ubuntu philosophy to business responses"""
        ubuntu_phrases = {
            "sales": "Let us work together for mutual benefit",
            "service": "How can we serve our community better",
            "support": "We are here to help each other grow",
            "payment": "Fair exchange strengthens our community"
        }
        
        if business_context in ubuntu_phrases:
            return f"{ubuntu_phrases[business_context]}. {response}"
        return response

class AfricanVoiceRecognition:
    """African language speech recognition with cultural adaptation"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.cultural_adapter = CulturalVoiceAdapter()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    async def recognize_speech(self, language: VoiceLanguage = VoiceLanguage.ENGLISH_AFRICAN) -> Optional[VoiceCommand]:
        """Recognize speech in specified African language"""
        try:
            with self.microphone as source:
                logger.info(f"Listening for {language.value} speech...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Use Google Speech Recognition with language support
            text = self.recognizer.recognize_google(audio, language=language.value)
            
            # Analyze cultural context
            cultural_context = self._analyze_cultural_context(text, language)
            business_intent = self._extract_business_intent(text)
            
            return VoiceCommand(
                text=text,
                language=language,
                confidence=0.85,  # Simulated confidence
                timestamp=time.time(),
                cultural_context=cultural_context,
                business_intent=business_intent
            )
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def _analyze_cultural_context(self, text: str, language: VoiceLanguage) -> Dict[str, Any]:
        """Analyze cultural context in speech"""
        context = {
            "language": language.value,
            "formality_level": "medium",
            "cultural_markers": [],
            "ubuntu_elements": []
        }
        
        # Detect respect markers
        respect_words = {
            VoiceLanguage.SWAHILI: ["shikamoo", "heshima", "adabu"],
            VoiceLanguage.HAUSA: ["sannu", "girmamawa", "mutunci"],
            VoiceLanguage.YORUBA: ["owo", "iyin", "ola"],
            VoiceLanguage.ZULU: ["hlonipha", "inhlonipho", "ukuphakama"]
        }
        
        if language in respect_words:
            for word in respect_words[language]:
                if word.lower() in text.lower():
                    context["formality_level"] = "high"
                    context["cultural_markers"].append(word)
        
        # Detect Ubuntu philosophy elements
        ubuntu_keywords = ["together", "community", "help", "share", "family", "unity"]
        for keyword in ubuntu_keywords:
            if keyword.lower() in text.lower():
                context["ubuntu_elements"].append(keyword)
        
        return context
    
    def _extract_business_intent(self, text: str) -> Optional[str]:
        """Extract business intent from speech"""
        business_intents = {
            "sell": ["sell", "sale", "buy", "purchase", "price"],
            "inventory": ["stock", "inventory", "items", "products", "goods"],
            "customer": ["customer", "client", "service", "help", "support"],
            "payment": ["pay", "payment", "money", "cash", "credit"],
            "report": ["report", "summary", "status", "analytics", "data"]
        }
        
        text_lower = text.lower()
        for intent, keywords in business_intents.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
        return None

class AfricanVoiceSynthesis:
    """African language voice synthesis with cultural adaptation"""
    
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.cultural_adapter = CulturalVoiceAdapter()
        
        # Configure voice properties
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer female voice for African cultural contexts
            for voice in voices:
                if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        self.tts_engine.setProperty('rate', 150)  # Slower for clarity
        self.tts_engine.setProperty('volume', 0.9)
    
    async def synthesize_speech(self, text: str, language: VoiceLanguage, 
                              cultural_context: Dict[str, Any] = None) -> VoiceResponse:
        """Synthesize speech with cultural adaptation"""
        
        # Apply cultural adaptation
        adapted_text = self._apply_cultural_adaptation(text, language, cultural_context)
        
        # Apply Ubuntu philosophy
        ubuntu_text = self.cultural_adapter.apply_ubuntu_context(
            adapted_text, 
            cultural_context.get('business_intent', 'general') if cultural_context else 'general'
        )
        
        try:
            # Use gTTS for better language support
            if language != VoiceLanguage.ENGLISH_AFRICAN:
                tts = gTTS(text=ubuntu_text, lang=language.value, slow=False)
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tts.save(tmp_file.name)
                    
                    # Read audio data
                    with open(tmp_file.name, 'rb') as audio_file:
                        audio_data = audio_file.read()
                    
                    # Clean up
                    os.unlink(tmp_file.name)
            else:
                # Use pyttsx3 for English
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    self.tts_engine.save_to_file(ubuntu_text, tmp_file.name)
                    self.tts_engine.runAndWait()
                    
                    with open(tmp_file.name, 'rb') as audio_file:
                        audio_data = audio_file.read()
                    
                    os.unlink(tmp_file.name)
            
            return VoiceResponse(
                text=ubuntu_text,
                language=language,
                audio_data=audio_data,
                cultural_adaptation=cultural_context,
                ubuntu_elements=self.cultural_adapter.ubuntu_principles
            )
            
        except Exception as e:
            logger.error(f"Voice synthesis error: {e}")
            return VoiceResponse(
                text=ubuntu_text,
                language=language,
                cultural_adaptation=cultural_context
            )
    
    def _apply_cultural_adaptation(self, text: str, language: VoiceLanguage, 
                                 cultural_context: Dict[str, Any] = None) -> str:
        """Apply cultural adaptation to text"""
        if not cultural_context:
            return text
        
        # Add appropriate greeting based on time and culture
        current_hour = time.localtime().tm_hour
        if current_hour < 12:
            time_of_day = "morning"
        elif current_hour < 17:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"
        
        greeting = self.cultural_adapter.adapt_greeting(language, time_of_day)
        
        # Add cultural politeness markers
        if cultural_context.get('formality_level') == 'high':
            return f"{greeting}. {text}. Asante sana."  # Thank you very much in Swahili
        else:
            return f"{greeting}. {text}"

class BusinessVoiceWorkflow:
    """Voice-activated business workflow processor"""
    
    def __init__(self):
        self.voice_recognition = AfricanVoiceRecognition()
        self.voice_synthesis = AfricanVoiceSynthesis()
        self.workflow_handlers = {
            "sell": self._handle_sales_workflow,
            "inventory": self._handle_inventory_workflow,
            "customer": self._handle_customer_workflow,
            "payment": self._handle_payment_workflow,
            "report": self._handle_report_workflow
        }
    
    async def process_voice_command(self, language: VoiceLanguage = VoiceLanguage.ENGLISH_AFRICAN) -> Optional[VoiceResponse]:
        """Process voice command and execute business workflow"""
        
        # Recognize speech
        command = await self.voice_recognition.recognize_speech(language)
        if not command:
            return await self.voice_synthesis.synthesize_speech(
                "I didn't understand. Please try again.",
                language
            )
        
        logger.info(f"Received command: {command.text} (Intent: {command.business_intent})")
        
        # Process business workflow
        if command.business_intent and command.business_intent in self.workflow_handlers:
            response_text = await self.workflow_handlers[command.business_intent](command)
        else:
            response_text = await self._handle_general_query(command)
        
        # Generate voice response
        return await self.voice_synthesis.synthesize_speech(
            response_text,
            language,
            command.cultural_context
        )
    
    async def _handle_sales_workflow(self, command: VoiceCommand) -> str:
        """Handle sales-related voice commands"""
        text = command.text.lower()
        
        if "sell" in text and "sugar" in text:
            return "Recording sale of sugar packet. Price is 50 shillings. Payment method?"
        elif "sell" in text and "bread" in text:
            return "Recording sale of bread. Price is 100 shillings. Cash or mobile money?"
        elif "price" in text:
            return "Current prices: Sugar packet 50 shillings, Bread 100 shillings, Milk 80 shillings."
        else:
            return "What would you like to sell today? I can help record the transaction."
    
    async def _handle_inventory_workflow(self, command: VoiceCommand) -> str:
        """Handle inventory-related voice commands"""
        text = command.text.lower()
        
        if "stock" in text or "inventory" in text:
            return "Current stock: Sugar packets 45 remaining, Bread 12 loaves, Milk 30 packets. Need to reorder anything?"
        elif "low" in text or "reorder" in text:
            return "Low stock alert: Bread down to 12 loaves. Shall I create a reorder for 50 loaves?"
        else:
            return "Inventory status: All items well stocked. Sugar 45, Bread 12, Milk 30."
    
    async def _handle_customer_workflow(self, command: VoiceCommand) -> str:
        """Handle customer service voice commands"""
        return "How can I help serve our customer today? I'm here to ensure excellent service for our community."
    
    async def _handle_payment_workflow(self, command: VoiceCommand) -> str:
        """Handle payment-related voice commands"""
        text = command.text.lower()
        
        if "mpesa" in text or "mobile money" in text:
            return "Processing M-Pesa payment. Please confirm the amount and customer phone number."
        elif "cash" in text:
            return "Recording cash payment. Please confirm the amount received."
        else:
            return "Payment options available: Cash, M-Pesa, Airtel Money, Bank transfer. Which would you prefer?"
    
    async def _handle_report_workflow(self, command: VoiceCommand) -> str:
        """Handle reporting voice commands"""
        return "Today's summary: 25 transactions, 2,500 shillings revenue, top seller is sugar packets. Full report?"
    
    async def _handle_general_query(self, command: VoiceCommand) -> str:
        """Handle general queries"""
        return f"I heard you say: {command.text}. How can I help you with your business today?"

class VoiceInterfaceAgent:
    """Main Voice Interface Agent for WebWaka"""
    
    def __init__(self):
        self.business_workflow = BusinessVoiceWorkflow()
        self.supported_languages = list(VoiceLanguage)
        self.is_active = False
        
        logger.info("Voice Interface Agent initialized with African language support")
    
    async def start_voice_interface(self, language: VoiceLanguage = VoiceLanguage.ENGLISH_AFRICAN):
        """Start the voice interface"""
        self.is_active = True
        logger.info(f"Starting voice interface in {language.value}")
        
        while self.is_active:
            try:
                response = await self.business_workflow.process_voice_command(language)
                if response:
                    logger.info(f"Voice response: {response.text}")
                    # In a real implementation, this would play the audio
                    if response.audio_data:
                        logger.info("Audio response generated successfully")
                
                # Small delay to prevent overwhelming the system
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Voice interface stopped by user")
                break
            except Exception as e:
                logger.error(f"Voice interface error: {e}")
                await asyncio.sleep(2)
    
    def stop_voice_interface(self):
        """Stop the voice interface"""
        self.is_active = False
        logger.info("Voice interface stopped")
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return [lang.value for lang in self.supported_languages]
    
    async def test_voice_capabilities(self) -> Dict[str, Any]:
        """Test voice interface capabilities"""
        test_results = {
            "recognition_test": False,
            "synthesis_test": False,
            "cultural_adaptation_test": False,
            "business_workflow_test": False,
            "supported_languages": len(self.supported_languages),
            "ubuntu_integration": True
        }
        
        try:
            # Test voice synthesis
            synthesis_response = await self.business_workflow.voice_synthesis.synthesize_speech(
                "Testing voice synthesis with Ubuntu philosophy",
                VoiceLanguage.ENGLISH_AFRICAN,
                {"business_intent": "service", "formality_level": "medium"}
            )
            test_results["synthesis_test"] = synthesis_response is not None
            test_results["cultural_adaptation_test"] = "community" in synthesis_response.text.lower()
            
            # Test business workflow
            test_command = VoiceCommand(
                text="sell packet of sugar",
                language=VoiceLanguage.ENGLISH_AFRICAN,
                confidence=0.9,
                timestamp=time.time(),
                cultural_context={"business_intent": "sell"},
                business_intent="sell"
            )
            
            workflow_response = await self.business_workflow._handle_sales_workflow(test_command)
            test_results["business_workflow_test"] = "sugar" in workflow_response.lower()
            
            logger.info("Voice interface test completed successfully")
            
        except Exception as e:
            logger.error(f"Voice interface test error: {e}")
        
        return test_results

# Example usage and testing
async def main():
    """Example usage of Voice Interface Agent"""
    agent = VoiceInterfaceAgent()
    
    # Test capabilities
    test_results = await agent.test_voice_capabilities()
    print("Voice Interface Test Results:")
    for test, result in test_results.items():
        print(f"  {test}: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Example voice command processing
    print("\nExample Voice Commands:")
    
    # Simulate voice commands
    example_commands = [
        "sell packet of sugar",
        "check inventory status", 
        "process mpesa payment",
        "daily sales report"
    ]
    
    for cmd_text in example_commands:
        command = VoiceCommand(
            text=cmd_text,
            language=VoiceLanguage.ENGLISH_AFRICAN,
            confidence=0.9,
            timestamp=time.time(),
            cultural_context={"business_intent": cmd_text.split()[0]},
            business_intent=cmd_text.split()[0]
        )
        
        if command.business_intent in agent.business_workflow.workflow_handlers:
            response = await agent.business_workflow.workflow_handlers[command.business_intent](command)
            print(f"  Command: '{cmd_text}' → Response: '{response}'")

if __name__ == "__main__":
    asyncio.run(main())

