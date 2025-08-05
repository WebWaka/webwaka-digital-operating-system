#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Conversational Interface Agent (Agent 24)
African communication styles with social hierarchy recognition, cultural context awareness,
and Ubuntu philosophy integration for natural, culturally appropriate conversations

Author: WebWaka Development Team
Version: 4.0.0
License: MIT
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path
import uuid
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CommunicationStyle(Enum):
    """African communication styles"""
    DIRECT = "direct"
    INDIRECT = "indirect"
    STORYTELLING = "storytelling"
    PROVERB_RICH = "proverb_rich"
    FORMAL_HIERARCHICAL = "formal_hierarchical"
    CONSENSUS_BUILDING = "consensus_building"

class SocialHierarchy(Enum):
    """Social hierarchy levels"""
    ELDER = "elder"
    AUTHORITY = "authority"
    PEER = "peer"
    YOUNGER = "younger"
    CHILD = "child"
    UNKNOWN = "unknown"

class CulturalContext(Enum):
    """Cultural contexts"""
    TRADITIONAL = "traditional"
    MODERN = "modern"
    BUSINESS = "business"
    FAMILY = "family"
    COMMUNITY = "community"
    RELIGIOUS = "religious"
    EDUCATIONAL = "educational"

class ConversationTone(Enum):
    """Conversation tones"""
    RESPECTFUL = "respectful"
    WARM = "warm"
    FORMAL = "formal"
    CASUAL = "casual"
    AUTHORITATIVE = "authoritative"
    NURTURING = "nurturing"

@dataclass
class CulturalProfile:
    """User cultural profile"""
    primary_language: str
    secondary_languages: List[str]
    cultural_region: str
    communication_style: CommunicationStyle
    social_hierarchy: SocialHierarchy
    cultural_context: CulturalContext
    ubuntu_preference: float
    traditional_values: Dict[str, float]

@dataclass
class ConversationContext:
    """Conversation context"""
    conversation_id: str
    user_profile: CulturalProfile
    current_topic: str
    conversation_history: List[Dict[str, Any]]
    cultural_adaptations: List[str]
    ubuntu_score: float
    hierarchy_awareness: float

@dataclass
class ConversationalResponse:
    """Conversational response with cultural intelligence"""
    response_id: str
    original_input: str
    processed_response: str
    communication_style: CommunicationStyle
    cultural_adaptations: List[str]
    hierarchy_adjustments: List[str]
    ubuntu_integration: Dict[str, Any]
    proverbs_used: List[str]
    cultural_appropriateness: float
    ubuntu_score: float
    confidence_score: float
    processing_time: float

class ConversationalInterfaceAgent:
    """
    Conversational Interface Agent for WebWaka Digital Operating System
    
    Provides culturally intelligent conversational interfaces with:
    - African communication styles (indirect, storytelling, proverb-rich)
    - Social hierarchy recognition and appropriate responses
    - Cultural context awareness and adaptation
    - Ubuntu philosophy integration in dialogue flow
    - Multi-language code-switching support
    - Traditional wisdom and proverb integration
    - Consensus-building conversation patterns
    - Cultural taboo avoidance and sensitive handling
    
    Communication Styles Supported:
    - Direct communication (Igbo, Luo business culture)
    - Indirect communication (Yoruba, Akan traditional style)
    - Storytelling traditions (Bantu cultures, griots)
    - Proverb-rich dialogue (West African wisdom traditions)
    - Formal hierarchical (Islamic cultures, traditional kingdoms)
    - Consensus building (Ubuntu-based decision making)
    
    Features:
    - Real-time cultural adaptation based on user profile
    - Dynamic hierarchy recognition and response adjustment
    - Traditional greeting and courtesy integration
    - Cultural taboo detection and avoidance
    - Ubuntu philosophy integration in all interactions
    - Multi-generational communication bridging
    - Traditional wisdom and modern context integration
    """
    
    def __init__(self):
        self.database_path = "/tmp/webwaka_conversational_interface.db"
        self.setup_database()
        self.cultural_patterns = self._initialize_cultural_patterns()
        self.proverb_database = self._initialize_proverb_database()
        self.hierarchy_rules = self._initialize_hierarchy_rules()
        self.ubuntu_principles = [
            "community_first",
            "collective_wisdom",
            "elder_respect",
            "consensus_building",
            "mutual_support",
            "cultural_preservation",
            "harmonious_dialogue",
            "inclusive_communication"
        ]
        
    def setup_database(self):
        """Setup database for conversational interface tracking"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                cultural_profile TEXT,
                session_start TIMESTAMP,
                session_end TIMESTAMP,
                total_exchanges INTEGER DEFAULT 0,
                avg_cultural_score REAL DEFAULT 0.0,
                avg_ubuntu_score REAL DEFAULT 0.0,
                communication_style TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_exchanges (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                user_input TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                communication_style TEXT,
                social_hierarchy TEXT,
                cultural_context TEXT,
                cultural_adaptations TEXT,
                ubuntu_integration TEXT,
                proverbs_used TEXT,
                cultural_appropriateness REAL,
                ubuntu_score REAL,
                confidence_score REAL,
                processing_time REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES conversation_sessions (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cultural_patterns (
                id TEXT PRIMARY KEY,
                culture TEXT NOT NULL,
                communication_style TEXT NOT NULL,
                pattern_description TEXT,
                example_phrases TEXT,
                hierarchy_sensitivity REAL,
                ubuntu_alignment REAL,
                usage_frequency INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proverb_wisdom (
                id TEXT PRIMARY KEY,
                culture TEXT NOT NULL,
                language TEXT NOT NULL,
                proverb_local TEXT NOT NULL,
                proverb_english TEXT NOT NULL,
                context_usage TEXT,
                wisdom_category TEXT,
                ubuntu_relevance REAL,
                cultural_importance REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hierarchy_rules (
                id TEXT PRIMARY KEY,
                culture TEXT NOT NULL,
                hierarchy_level TEXT NOT NULL,
                communication_rules TEXT,
                respect_markers TEXT,
                taboo_topics TEXT,
                appropriate_responses TEXT,
                ubuntu_considerations TEXT
            )
        ''')
        
        # Insert cultural patterns
        cultural_patterns = [
            # Yoruba indirect communication
            ("CP_YO_001", "yoruba", "indirect", "Use of metaphors and proverbs for sensitive topics",
             '["We say the wise bird knows when to sing", "The elder tree provides shade for all"]',
             8.5, 9.0, 150),
            
            # Igbo direct business communication
            ("CP_IG_001", "igbo", "direct", "Straightforward business discussion with respect",
             '["Let us speak plainly about this matter", "The truth serves us all better"]',
             6.0, 8.0, 200),
            
            # Zulu storytelling tradition
            ("CP_ZU_001", "zulu", "storytelling", "Narrative approach to explain concepts",
             '["There was once a village where...", "Our ancestors tell us that..."]',
             9.0, 9.5, 180),
            
            # Akan proverb-rich communication
            ("CP_AK_001", "akan", "proverb_rich", "Heavy use of traditional proverbs and sayings",
             '["When the spider webs unite, they can tie up a lion", "The ruin of a nation begins in the homes"]',
             8.8, 9.2, 160),
            
            # Hausa formal hierarchical
            ("CP_HA_001", "hausa", "formal_hierarchical", "Structured formal communication with Islamic respect",
             '["With your permission, respected elder", "If Allah wills, we shall proceed"]',
             9.5, 8.5, 140),
            
            # Swahili consensus building
            ("CP_SW_001", "swahili", "consensus_building", "Inclusive dialogue seeking agreement",
             '["What do our brothers and sisters think?", "Let us find the path that serves all"]',
             7.5, 9.8, 170),
            
            # Amharic traditional formal
            ("CP_AM_001", "amharic", "formal_hierarchical", "Highland Ethiopian formal communication",
             '["With great respect to the elders", "Following our ancient customs"]',
             9.2, 8.8, 120),
            
            # Luo direct but respectful
            ("CP_LU_001", "luo", "direct", "Clear communication with traditional respect",
             '["Let me speak truthfully, respected ones", "The matter stands thus before us"]',
             7.0, 8.5, 130)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO cultural_patterns 
            (id, culture, communication_style, pattern_description, example_phrases, hierarchy_sensitivity, ubuntu_alignment, usage_frequency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', cultural_patterns)
        
        # Insert proverbs and wisdom
        proverbs = [
            # Yoruba proverbs
            ("PW_YO_001", "yoruba", "yoruba", "Eniyan ni aṣọ mi", "People are my clothing",
             "community_importance", "ubuntu_humanity", 9.5, 9.8),
            ("PW_YO_002", "yoruba", "yoruba", "Bi a ba n gun igi, a o gun epo", "When we climb a tree, we don't climb the palm oil",
             "patience_wisdom", "collective_benefit", 8.8, 9.0),
            
            # Zulu proverbs
            ("PW_ZU_001", "zulu", "zulu", "Umuntu ngumuntu ngabantu", "A person is a person through other people",
             "ubuntu_core", "ubuntu_humanity", 10.0, 10.0),
            ("PW_ZU_002", "zulu", "zulu", "Indlela ibuzwa kwabaphambili", "The path is asked from those who have traveled it",
             "elder_wisdom", "traditional_knowledge", 9.2, 9.5),
            
            # Akan proverbs
            ("PW_AK_001", "akan", "twi", "Se wo were fi na wosankofa a yenkyi", "It is not wrong to go back for that which you have forgotten",
             "learning_humility", "continuous_improvement", 9.0, 9.3),
            ("PW_AK_002", "akan", "twi", "Obi nkyere abofra Nyame", "No one teaches a child about God",
             "innate_wisdom", "spiritual_connection", 8.5, 8.8),
            
            # Swahili proverbs
            ("PW_SW_001", "swahili", "swahili", "Haba ya mvua ni pamoja", "Raindrops are together",
             "unity_strength", "collective_power", 9.3, 9.6),
            ("PW_SW_002", "swahili", "swahili", "Asiyefunzwa na mamaye hufunzwa na ulimwengu", "One who is not taught by their mother will be taught by the world",
             "education_importance", "family_wisdom", 8.7, 9.0),
            
            # Hausa proverbs
            ("PW_HA_001", "hausa", "hausa", "Kowa ya san inda ya ke zuwa", "Everyone knows where they are going",
             "personal_responsibility", "individual_purpose", 8.0, 8.3),
            ("PW_HA_002", "hausa", "hausa", "Gaskiya ta fi karfi", "Truth is stronger",
             "honesty_virtue", "moral_strength", 9.1, 9.4),
            
            # Amharic proverbs
            ("PW_AM_001", "amharic", "amharic", "የሰው ልጅ በመልካም ስራው ይታወቃል", "A person is known by their good deeds",
             "character_importance", "moral_behavior", 8.9, 9.2),
            ("PW_AM_002", "amharic", "amharic", "ከብዙ አንድ ይወጣል", "From many comes one",
             "unity_diversity", "collective_strength", 9.0, 9.3)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO proverb_wisdom 
            (id, culture, language, proverb_local, proverb_english, context_usage, wisdom_category, ubuntu_relevance, cultural_importance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', proverbs)
        
        # Insert hierarchy rules
        hierarchy_rules = [
            ("HR_001", "yoruba", "elder", 
             '{"greeting": "prostration_or_kneeling", "address": "baba/mama", "tone": "highly_respectful"}',
             '["baba", "mama", "oga agba"]',
             '["direct_contradiction", "casual_address"]',
             '["seek_blessing_first", "use_proverbs", "show_deference"]',
             '{"elder_wisdom": 10.0, "community_respect": 9.5}'),
            
            ("HR_002", "zulu", "elder",
             '{"greeting": "respectful_bow", "address": "mkhulu/gogo", "tone": "deeply_respectful"}',
             '["mkhulu", "gogo", "baba", "mama"]',
             '["interrupting", "casual_tone", "direct_disagreement"]',
             '["listen_first", "seek_guidance", "show_ubuntu"]',
             '{"ubuntu_respect": 10.0, "traditional_authority": 9.8}'),
            
            ("HR_003", "hausa", "authority",
             '{"greeting": "formal_salutation", "address": "malam/hajiya", "tone": "formal_respectful"}',
             '["malam", "hajiya", "alhaji", "mai"]',
             '["religious_disrespect", "informal_address"]',
             '["islamic_greeting", "formal_language", "seek_permission"]',
             '{"religious_respect": 9.5, "traditional_authority": 9.0}'),
            
            ("HR_004", "akan", "peer",
             '{"greeting": "friendly_respectful", "address": "brother/sister", "tone": "warm_respectful"}',
             '["brother", "sister", "friend"]',
             '["disrespect_to_elders", "cultural_insensitivity"]',
             '["use_proverbs", "seek_consensus", "show_wisdom"]',
             '{"community_harmony": 8.5, "mutual_respect": 9.0}'),
            
            ("HR_005", "swahili", "younger",
             '{"greeting": "respectful_friendly", "address": "ndugu", "tone": "nurturing_guidance"}',
             '["ndugu", "kaka", "dada"]',
             '["condescending_tone", "dismissive_attitude"]',
             '["provide_guidance", "encourage_learning", "show_ubuntu"]',
             '{"mentorship": 8.8, "community_building": 9.2}')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO hierarchy_rules 
            (id, culture, hierarchy_level, communication_rules, respect_markers, taboo_topics, appropriate_responses, ubuntu_considerations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', hierarchy_rules)
        
        conn.commit()
        conn.close()
        logger.info("Conversational interface database setup completed")

    def _initialize_cultural_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize cultural communication patterns"""
        patterns = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT culture, communication_style, pattern_description, example_phrases, 
                   hierarchy_sensitivity, ubuntu_alignment
            FROM cultural_patterns
        ''')
        
        for row in cursor.fetchall():
            culture = row[0]
            if culture not in patterns:
                patterns[culture] = {}
            
            patterns[culture][row[1]] = {
                "description": row[2],
                "examples": json.loads(row[3]) if row[3] else [],
                "hierarchy_sensitivity": row[4],
                "ubuntu_alignment": row[5]
            }
        
        conn.close()
        return patterns

    def _initialize_proverb_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize proverb and wisdom database"""
        proverbs = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT culture, language, proverb_local, proverb_english, context_usage, 
                   wisdom_category, ubuntu_relevance, cultural_importance
            FROM proverb_wisdom
        ''')
        
        for row in cursor.fetchall():
            culture = row[0]
            if culture not in proverbs:
                proverbs[culture] = []
            
            proverbs[culture].append({
                "language": row[1],
                "local": row[2],
                "english": row[3],
                "context": row[4],
                "category": row[5],
                "ubuntu_relevance": row[6],
                "cultural_importance": row[7]
            })
        
        conn.close()
        return proverbs

    def _initialize_hierarchy_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize social hierarchy rules"""
        rules = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT culture, hierarchy_level, communication_rules, respect_markers, 
                   taboo_topics, appropriate_responses, ubuntu_considerations
            FROM hierarchy_rules
        ''')
        
        for row in cursor.fetchall():
            culture = row[0]
            if culture not in rules:
                rules[culture] = {}
            
            rules[culture][row[1]] = {
                "communication_rules": json.loads(row[2]) if row[2] else {},
                "respect_markers": json.loads(row[3]) if row[3] else [],
                "taboo_topics": json.loads(row[4]) if row[4] else [],
                "appropriate_responses": json.loads(row[5]) if row[5] else [],
                "ubuntu_considerations": json.loads(row[6]) if row[6] else {}
            }
        
        conn.close()
        return rules

    async def process_conversation(self, user_input: str, user_profile: CulturalProfile, 
                                 conversation_context: ConversationContext) -> ConversationalResponse:
        """Process conversation with cultural intelligence and hierarchy awareness"""
        start_time = datetime.now()
        response_id = str(uuid.uuid4())
        
        try:
            # Analyze user input for cultural context
            input_analysis = await self._analyze_user_input(user_input, user_profile)
            
            # Determine appropriate communication style
            communication_style = await self._determine_communication_style(
                user_input, user_profile, conversation_context
            )
            
            # Apply hierarchy-aware processing
            hierarchy_adjustments = await self._apply_hierarchy_awareness(
                user_input, user_profile, communication_style
            )
            
            # Generate culturally appropriate response
            base_response = await self._generate_base_response(
                user_input, user_profile, communication_style
            )
            
            # Apply cultural adaptations
            cultural_adaptations = await self._apply_cultural_adaptations(
                base_response, user_profile, communication_style
            )
            
            # Integrate Ubuntu philosophy
            ubuntu_integration = await self._integrate_ubuntu_philosophy(
                cultural_adaptations, user_profile, conversation_context
            )
            
            # Add proverbs and wisdom if appropriate
            proverbs_used = await self._add_traditional_wisdom(
                ubuntu_integration, user_profile, communication_style
            )
            
            # Finalize response
            final_response = await self._finalize_response(
                ubuntu_integration, proverbs_used, user_profile
            )
            
            # Calculate quality metrics
            cultural_appropriateness = await self._calculate_cultural_appropriateness(
                final_response, user_profile, communication_style
            )
            ubuntu_score = await self._calculate_ubuntu_score(
                final_response, ubuntu_integration, user_profile
            )
            confidence_score = await self._calculate_confidence_score(
                cultural_appropriateness, ubuntu_score, communication_style
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = ConversationalResponse(
                response_id=response_id,
                original_input=user_input,
                processed_response=final_response,
                communication_style=communication_style,
                cultural_adaptations=cultural_adaptations.get("adaptations", []),
                hierarchy_adjustments=hierarchy_adjustments,
                ubuntu_integration=ubuntu_integration,
                proverbs_used=[p["english"] for p in proverbs_used],
                cultural_appropriateness=cultural_appropriateness,
                ubuntu_score=ubuntu_score,
                confidence_score=confidence_score,
                processing_time=processing_time
            )
            
            # Store conversation exchange
            await self._store_conversation_exchange(result, user_profile, conversation_context)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in conversation processing: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ConversationalResponse(
                response_id=response_id,
                original_input=user_input,
                processed_response=f"I apologize, but I encountered an issue. Let me try to help you in a different way.",
                communication_style=CommunicationStyle.DIRECT,
                cultural_adaptations=[],
                hierarchy_adjustments=[],
                ubuntu_integration={"error": str(e)},
                proverbs_used=[],
                cultural_appropriateness=0.0,
                ubuntu_score=0.0,
                confidence_score=0.0,
                processing_time=processing_time
            )

    async def _analyze_user_input(self, user_input: str, user_profile: CulturalProfile) -> Dict[str, Any]:
        """Analyze user input for cultural and contextual clues"""
        analysis = {
            "input_length": len(user_input),
            "formality_level": self._detect_formality_level(user_input),
            "emotional_tone": self._detect_emotional_tone(user_input),
            "cultural_markers": self._detect_cultural_markers(user_input, user_profile),
            "hierarchy_indicators": self._detect_hierarchy_indicators(user_input),
            "topic_category": self._categorize_topic(user_input)
        }
        
        return analysis

    async def _determine_communication_style(self, user_input: str, user_profile: CulturalProfile, 
                                           context: ConversationContext) -> CommunicationStyle:
        """Determine appropriate communication style based on cultural profile and context"""
        
        # Get cultural patterns for user's culture
        culture_patterns = self.cultural_patterns.get(user_profile.primary_language, {})
        
        # Default to user's preferred style
        preferred_style = user_profile.communication_style
        
        # Adjust based on context and input analysis
        if "urgent" in user_input.lower() or "quickly" in user_input.lower():
            return CommunicationStyle.DIRECT
        
        if any(word in user_input.lower() for word in ["story", "tell me", "explain"]):
            return CommunicationStyle.STORYTELLING
        
        if user_profile.social_hierarchy in [SocialHierarchy.ELDER, SocialHierarchy.AUTHORITY]:
            return CommunicationStyle.FORMAL_HIERARCHICAL
        
        if context.current_topic in ["decision", "agreement", "consensus"]:
            return CommunicationStyle.CONSENSUS_BUILDING
        
        return preferred_style

    async def _apply_hierarchy_awareness(self, user_input: str, user_profile: CulturalProfile, 
                                       communication_style: CommunicationStyle) -> List[str]:
        """Apply hierarchy-aware adjustments to communication"""
        adjustments = []
        
        culture = user_profile.primary_language
        hierarchy_level = user_profile.social_hierarchy.value
        
        # Get hierarchy rules for the culture
        culture_rules = self.hierarchy_rules.get(culture, {})
        level_rules = culture_rules.get(hierarchy_level, {})
        
        if level_rules:
            # Add appropriate respect markers
            respect_markers = level_rules.get("respect_markers", [])
            if respect_markers and communication_style == CommunicationStyle.FORMAL_HIERARCHICAL:
                adjustments.append(f"use_respect_marker: {respect_markers[0]}")
            
            # Check for taboo topics
            taboo_topics = level_rules.get("taboo_topics", [])
            for taboo in taboo_topics:
                if taboo in user_input.lower():
                    adjustments.append(f"avoid_taboo: {taboo}")
            
            # Apply appropriate response style
            appropriate_responses = level_rules.get("appropriate_responses", [])
            if appropriate_responses:
                adjustments.extend(appropriate_responses)
        
        return adjustments

    async def _generate_base_response(self, user_input: str, user_profile: CulturalProfile, 
                                    communication_style: CommunicationStyle) -> str:
        """Generate base response based on input and cultural context"""
        
        # Simple response generation (in real implementation, would use more sophisticated NLG)
        if "hello" in user_input.lower() or "hi" in user_input.lower():
            greetings = {
                "yoruba": "Ẹ kú àárọ̀! How may I assist you today?",
                "zulu": "Sawubona! How can I help you?",
                "swahili": "Hujambo! What can I do for you?",
                "hausa": "Sannu! How may I be of service?",
                "amharic": "Selam! How can I assist you?"
            }
            return greetings.get(user_profile.primary_language, "Hello! How can I help you?")
        
        elif "help" in user_input.lower():
            if communication_style == CommunicationStyle.STORYTELLING:
                return "Let me share with you how we can work together, like the story of the village that prospered through unity..."
            elif communication_style == CommunicationStyle.CONSENSUS_BUILDING:
                return "Together, we can find the best path forward. What would serve our community's needs?"
            else:
                return "I am here to assist you. What specific help do you need?"
        
        elif "business" in user_input.lower():
            if communication_style == CommunicationStyle.PROVERB_RICH:
                return "As our elders say, 'A tree cannot make a forest.' Let us discuss how we can grow together."
            else:
                return "I would be honored to help you with your business needs."
        
        else:
            return "Thank you for sharing that with me. How can I best assist you?"

    async def _apply_cultural_adaptations(self, base_response: str, user_profile: CulturalProfile, 
                                        communication_style: CommunicationStyle) -> Dict[str, Any]:
        """Apply cultural adaptations to the base response"""
        adapted_response = base_response
        adaptations = []
        
        culture = user_profile.primary_language
        
        # Add cultural greetings
        if user_profile.cultural_context == CulturalContext.TRADITIONAL:
            traditional_greetings = {
                "yoruba": "May your day be blessed",
                "zulu": "May you live well",
                "swahili": "Peace be with you",
                "hausa": "May Allah bless you",
                "amharic": "May God give you strength"
            }
            
            greeting = traditional_greetings.get(culture)
            if greeting and greeting not in adapted_response:
                adapted_response = f"{greeting}. {adapted_response}"
                adaptations.append("added_traditional_greeting")
        
        # Add respect markers for hierarchical communication
        if communication_style == CommunicationStyle.FORMAL_HIERARCHICAL:
            if user_profile.social_hierarchy == SocialHierarchy.ELDER:
                respect_markers = {
                    "yoruba": "respected elder",
                    "zulu": "honored mkhulu",
                    "hausa": "esteemed malam",
                    "swahili": "respected mzee"
                }
                
                marker = respect_markers.get(culture, "respected one")
                if marker not in adapted_response.lower():
                    adapted_response = f"{marker}, {adapted_response.lower()}"
                    adaptations.append("added_respect_marker")
        
        # Add community focus for Ubuntu cultures
        if culture in ["zulu", "xhosa", "swahili"] and "community" not in adapted_response.lower():
            adapted_response = adapted_response.replace("you", "we together")
            adaptations.append("ubuntu_community_focus")
        
        return {
            "response": adapted_response,
            "adaptations": adaptations
        }

    async def _integrate_ubuntu_philosophy(self, cultural_adaptations: Dict[str, Any], 
                                         user_profile: CulturalProfile, 
                                         context: ConversationContext) -> Dict[str, Any]:
        """Integrate Ubuntu philosophy into the response"""
        response = cultural_adaptations["response"]
        ubuntu_integration = {
            "principles_applied": [],
            "community_focus": False,
            "collective_language": False,
            "elder_respect": False
        }
        
        # Apply Ubuntu principles based on user preference
        if user_profile.ubuntu_preference > 0.7:
            # High Ubuntu preference - apply strong Ubuntu principles
            
            # Community first principle
            if "success" in response.lower():
                response = response.replace("success", "collective success")
                ubuntu_integration["principles_applied"].append("community_first")
                ubuntu_integration["community_focus"] = True
            
            # Collective wisdom
            if "decision" in response.lower() or "choice" in response.lower():
                response = response.replace("your decision", "our collective wisdom")
                ubuntu_integration["principles_applied"].append("collective_wisdom")
            
            # Elder respect
            if user_profile.social_hierarchy == SocialHierarchy.ELDER:
                ubuntu_integration["elder_respect"] = True
                ubuntu_integration["principles_applied"].append("elder_respect")
            
            # Mutual support
            if "help" in response.lower():
                response = response.replace("help you", "support each other")
                ubuntu_integration["principles_applied"].append("mutual_support")
                ubuntu_integration["collective_language"] = True
        
        ubuntu_integration["final_response"] = response
        return ubuntu_integration

    async def _add_traditional_wisdom(self, ubuntu_integration: Dict[str, Any], 
                                    user_profile: CulturalProfile, 
                                    communication_style: CommunicationStyle) -> List[Dict[str, Any]]:
        """Add traditional proverbs and wisdom when appropriate"""
        proverbs_used = []
        
        if communication_style in [CommunicationStyle.PROVERB_RICH, CommunicationStyle.STORYTELLING]:
            culture = user_profile.primary_language
            available_proverbs = self.proverb_database.get(culture, [])
            
            if available_proverbs:
                # Select appropriate proverb based on context
                response = ubuntu_integration["final_response"]
                
                if "community" in response.lower() or "together" in response.lower():
                    unity_proverbs = [p for p in available_proverbs if "unity" in p["category"] or "collective" in p["category"]]
                    if unity_proverbs:
                        selected_proverb = random.choice(unity_proverbs)
                        proverbs_used.append(selected_proverb)
                
                elif "wisdom" in response.lower() or "decision" in response.lower():
                    wisdom_proverbs = [p for p in available_proverbs if "wisdom" in p["category"]]
                    if wisdom_proverbs:
                        selected_proverb = random.choice(wisdom_proverbs)
                        proverbs_used.append(selected_proverb)
                
                elif ubuntu_integration.get("elder_respect", False):
                    elder_proverbs = [p for p in available_proverbs if p["ubuntu_relevance"] > 9.0]
                    if elder_proverbs:
                        selected_proverb = random.choice(elder_proverbs)
                        proverbs_used.append(selected_proverb)
        
        return proverbs_used

    async def _finalize_response(self, ubuntu_integration: Dict[str, Any], 
                               proverbs_used: List[Dict[str, Any]], 
                               user_profile: CulturalProfile) -> str:
        """Finalize the response with proverbs and final touches"""
        final_response = ubuntu_integration["final_response"]
        
        # Add proverbs if any were selected
        if proverbs_used:
            proverb = proverbs_used[0]  # Use the first selected proverb
            proverb_text = f'As we say in our tradition: "{proverb["english"]}"'
            final_response = f"{final_response} {proverb_text}"
        
        # Add closing based on cultural context
        if user_profile.cultural_context == CulturalContext.TRADITIONAL:
            closings = {
                "yoruba": "May your path be blessed.",
                "zulu": "Go well, stay well.",
                "swahili": "Tutaonana (until we meet again).",
                "hausa": "Allah ya ba ku albarka (May Allah bless you).",
                "amharic": "Egziyabher yistilign (May God give you strength)."
            }
            
            closing = closings.get(user_profile.primary_language)
            if closing and len(final_response) < 200:  # Don't add if response is already long
                final_response = f"{final_response} {closing}"
        
        return final_response

    # Helper methods for analysis
    
    def _detect_formality_level(self, text: str) -> str:
        """Detect formality level of input text"""
        formal_indicators = ["please", "kindly", "would you", "could you", "sir", "madam"]
        informal_indicators = ["hey", "hi", "what's up", "gonna", "wanna"]
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in text.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in text.lower())
        
        if formal_count > informal_count:
            return "formal"
        elif informal_count > formal_count:
            return "informal"
        else:
            return "neutral"

    def _detect_emotional_tone(self, text: str) -> str:
        """Detect emotional tone of input text"""
        positive_words = ["happy", "good", "great", "excellent", "wonderful", "thank"]
        negative_words = ["sad", "bad", "terrible", "awful", "angry", "frustrated"]
        urgent_words = ["urgent", "quickly", "immediately", "asap", "emergency"]
        
        if any(word in text.lower() for word in urgent_words):
            return "urgent"
        elif any(word in text.lower() for word in positive_words):
            return "positive"
        elif any(word in text.lower() for word in negative_words):
            return "negative"
        else:
            return "neutral"

    def _detect_cultural_markers(self, text: str, user_profile: CulturalProfile) -> List[str]:
        """Detect cultural markers in the input text"""
        markers = []
        
        # Language-specific cultural markers
        cultural_words = {
            "yoruba": ["baba", "mama", "oga", "omo"],
            "zulu": ["baba", "mama", "mkhulu", "gogo"],
            "swahili": ["mzee", "mama", "baba", "ndugu"],
            "hausa": ["malam", "hajiya", "alhaji"],
            "amharic": ["ato", "weizero", "ababa"]
        }
        
        culture_words = cultural_words.get(user_profile.primary_language, [])
        for word in culture_words:
            if word in text.lower():
                markers.append(f"cultural_address: {word}")
        
        # Religious markers
        religious_words = ["allah", "god", "blessing", "prayer", "inshallah"]
        for word in religious_words:
            if word in text.lower():
                markers.append(f"religious_reference: {word}")
        
        return markers

    def _detect_hierarchy_indicators(self, text: str) -> List[str]:
        """Detect social hierarchy indicators in text"""
        indicators = []
        
        elder_indicators = ["elder", "senior", "experienced", "wise", "respected"]
        authority_indicators = ["boss", "manager", "leader", "chief", "director"]
        peer_indicators = ["colleague", "friend", "partner", "brother", "sister"]
        
        for indicator in elder_indicators:
            if indicator in text.lower():
                indicators.append(f"elder_reference: {indicator}")
        
        for indicator in authority_indicators:
            if indicator in text.lower():
                indicators.append(f"authority_reference: {indicator}")
        
        for indicator in peer_indicators:
            if indicator in text.lower():
                indicators.append(f"peer_reference: {indicator}")
        
        return indicators

    def _categorize_topic(self, text: str) -> str:
        """Categorize the topic of conversation"""
        business_words = ["business", "work", "job", "career", "money", "profit"]
        family_words = ["family", "children", "parents", "home", "marriage"]
        community_words = ["community", "village", "neighborhood", "together", "help"]
        education_words = ["school", "learn", "teach", "education", "study"]
        
        if any(word in text.lower() for word in business_words):
            return "business"
        elif any(word in text.lower() for word in family_words):
            return "family"
        elif any(word in text.lower() for word in community_words):
            return "community"
        elif any(word in text.lower() for word in education_words):
            return "education"
        else:
            return "general"

    async def _calculate_cultural_appropriateness(self, response: str, user_profile: CulturalProfile, 
                                                communication_style: CommunicationStyle) -> float:
        """Calculate cultural appropriateness score"""
        score = 7.0  # Base score
        
        # Check for cultural elements
        culture = user_profile.primary_language
        
        # Bonus for appropriate communication style
        if communication_style == user_profile.communication_style:
            score += 1.0
        
        # Bonus for cultural greetings
        cultural_greetings = ["blessed", "peace", "allah", "god", "well"]
        if any(greeting in response.lower() for greeting in cultural_greetings):
            score += 0.5
        
        # Bonus for respect markers
        respect_words = ["respected", "honored", "elder", "mzee", "baba", "mama"]
        if any(word in response.lower() for word in respect_words):
            score += 0.8
        
        # Bonus for proverbs or traditional wisdom
        if "tradition" in response.lower() or "say" in response.lower():
            score += 0.7
        
        return min(score, 10.0)

    async def _calculate_ubuntu_score(self, response: str, ubuntu_integration: Dict[str, Any], 
                                    user_profile: CulturalProfile) -> float:
        """Calculate Ubuntu philosophy integration score"""
        score = 0.0
        
        # Base score for Ubuntu preference
        score += user_profile.ubuntu_preference * 3.0
        
        # Score for Ubuntu principles applied
        principles_applied = ubuntu_integration.get("principles_applied", [])
        score += len(principles_applied) * 1.5
        
        # Score for community focus
        if ubuntu_integration.get("community_focus", False):
            score += 2.0
        
        # Score for collective language
        if ubuntu_integration.get("collective_language", False):
            score += 1.5
        
        # Score for elder respect
        if ubuntu_integration.get("elder_respect", False):
            score += 1.0
        
        # Check for Ubuntu keywords in response
        ubuntu_words = ["together", "community", "collective", "we", "our", "shared"]
        ubuntu_count = sum(1 for word in ubuntu_words if word in response.lower())
        score += min(ubuntu_count * 0.5, 2.0)
        
        return min(score, 10.0)

    async def _calculate_confidence_score(self, cultural_appropriateness: float, ubuntu_score: float, 
                                        communication_style: CommunicationStyle) -> float:
        """Calculate overall confidence score"""
        scores = [cultural_appropriateness / 10.0, ubuntu_score / 10.0]
        
        # Bonus for complex communication styles
        if communication_style in [CommunicationStyle.STORYTELLING, CommunicationStyle.PROVERB_RICH]:
            scores.append(0.9)
        else:
            scores.append(0.7)
        
        return sum(scores) / len(scores)

    async def _store_conversation_exchange(self, result: ConversationalResponse, 
                                         user_profile: CulturalProfile, 
                                         context: ConversationContext):
        """Store conversation exchange in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversation_exchanges 
                (id, user_input, agent_response, communication_style, social_hierarchy, 
                 cultural_context, cultural_adaptations, ubuntu_integration, proverbs_used,
                 cultural_appropriateness, ubuntu_score, confidence_score, processing_time, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.response_id,
                result.original_input,
                result.processed_response,
                result.communication_style.value,
                user_profile.social_hierarchy.value,
                user_profile.cultural_context.value,
                json.dumps(result.cultural_adaptations),
                json.dumps(result.ubuntu_integration),
                json.dumps(result.proverbs_used),
                result.cultural_appropriateness,
                result.ubuntu_score,
                result.confidence_score,
                result.processing_time,
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing conversation exchange: {str(e)}")

    async def get_conversational_analytics(self) -> Dict[str, Any]:
        """Get comprehensive conversational interface analytics"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Get conversation statistics
        cursor.execute('''
            SELECT communication_style, COUNT(*) as exchange_count,
                   AVG(cultural_appropriateness) as avg_cultural,
                   AVG(ubuntu_score) as avg_ubuntu,
                   AVG(confidence_score) as avg_confidence,
                   AVG(processing_time) as avg_processing_time
            FROM conversation_exchanges 
            GROUP BY communication_style
        ''')
        
        style_stats = {}
        for row in cursor.fetchall():
            style_stats[row[0]] = {
                "exchange_count": row[1],
                "avg_cultural": round(row[2], 2) if row[2] else 0,
                "avg_ubuntu": round(row[3], 2) if row[3] else 0,
                "avg_confidence": round(row[4], 2) if row[4] else 0,
                "avg_processing_time": round(row[5], 4) if row[5] else 0
            }
        
        # Get cultural pattern usage
        cursor.execute('''
            SELECT culture, communication_style, COUNT(*) as usage_count
            FROM cultural_patterns 
            GROUP BY culture, communication_style
        ''')
        
        pattern_usage = {}
        for row in cursor.fetchall():
            culture = row[0]
            if culture not in pattern_usage:
                pattern_usage[culture] = {}
            pattern_usage[culture][row[1]] = row[2]
        
        conn.close()
        
        return {
            "communication_styles": [style.value for style in CommunicationStyle],
            "style_statistics": style_stats,
            "pattern_usage": pattern_usage,
            "ubuntu_principles": self.ubuntu_principles,
            "total_exchanges": sum(stats["exchange_count"] for stats in style_stats.values()),
            "overall_cultural_score": sum(stats["avg_cultural"] for stats in style_stats.values()) / len(style_stats) if style_stats else 0,
            "overall_ubuntu_score": sum(stats["avg_ubuntu"] for stats in style_stats.values()) / len(style_stats) if style_stats else 0,
            "supported_cultures": list(self.cultural_patterns.keys()),
            "proverb_cultures": list(self.proverb_database.keys())
        }

async def main():
    """Main function for testing Conversational Interface Agent"""
    agent = ConversationalInterfaceAgent()
    
    # Create test user profiles
    test_profiles = [
        CulturalProfile(
            primary_language="zulu",
            secondary_languages=["english"],
            cultural_region="southern_africa",
            communication_style=CommunicationStyle.STORYTELLING,
            social_hierarchy=SocialHierarchy.ELDER,
            cultural_context=CulturalContext.TRADITIONAL,
            ubuntu_preference=0.9,
            traditional_values={"ubuntu": 10.0, "elder_respect": 9.5}
        ),
        CulturalProfile(
            primary_language="yoruba",
            secondary_languages=["english"],
            cultural_region="west_africa",
            communication_style=CommunicationStyle.PROVERB_RICH,
            social_hierarchy=SocialHierarchy.PEER,
            cultural_context=CulturalContext.BUSINESS,
            ubuntu_preference=0.7,
            traditional_values={"wisdom": 9.0, "respect": 8.5}
        ),
        CulturalProfile(
            primary_language="swahili",
            secondary_languages=["english"],
            cultural_region="east_africa",
            communication_style=CommunicationStyle.CONSENSUS_BUILDING,
            social_hierarchy=SocialHierarchy.AUTHORITY,
            cultural_context=CulturalContext.COMMUNITY,
            ubuntu_preference=0.8,
            traditional_values={"unity": 9.2, "leadership": 8.8}
        )
    ]
    
    # Test conversations
    test_conversations = [
        ("Hello, I need help with my business", test_profiles[0]),
        ("Can you tell me about community development?", test_profiles[1]),
        ("We need to make a decision together", test_profiles[2]),
        ("What wisdom can you share about success?", test_profiles[0]),
        ("How can we work together for our community?", test_profiles[2])
    ]
    
    print("🗣️ Testing Conversational Interface Agent")
    print("=" * 60)
    
    for i, (user_input, profile) in enumerate(test_conversations, 1):
        print(f"\n💬 Test Conversation {i}:")
        print(f"User ({profile.primary_language.title()}, {profile.social_hierarchy.value}): {user_input}")
        print(f"Communication Style: {profile.communication_style.value}")
        print(f"Ubuntu Preference: {profile.ubuntu_preference}")
        
        # Create conversation context
        context = ConversationContext(
            conversation_id=str(uuid.uuid4()),
            user_profile=profile,
            current_topic="general",
            conversation_history=[],
            cultural_adaptations=[],
            ubuntu_score=0.0,
            hierarchy_awareness=0.0
        )
        
        result = await agent.process_conversation(user_input, profile, context)
        
        print(f"✅ Agent Response: {result.processed_response}")
        print(f"🎭 Communication Style Used: {result.communication_style.value}")
        print(f"🌍 Cultural Appropriateness: {result.cultural_appropriateness:.1f}/10")
        print(f"🤝 Ubuntu Score: {result.ubuntu_score:.1f}/10")
        print(f"📊 Confidence: {result.confidence_score:.2f}")
        print(f"⏱️ Processing Time: {result.processing_time:.4f}s")
        print(f"🏛️ Cultural Adaptations: {len(result.cultural_adaptations)}")
        print(f"👑 Hierarchy Adjustments: {len(result.hierarchy_adjustments)}")
        print(f"💎 Proverbs Used: {len(result.proverbs_used)}")
        if result.proverbs_used:
            print(f"   Proverb: {result.proverbs_used[0]}")
    
    # Get analytics
    analytics = await agent.get_conversational_analytics()
    print(f"\n📈 Conversational Interface Analytics:")
    print(f"Communication Styles: {len(analytics['communication_styles'])}")
    print(f"Total Exchanges: {analytics['total_exchanges']}")
    print(f"Overall Cultural Score: {analytics['overall_cultural_score']:.2f}/10")
    print(f"Overall Ubuntu Score: {analytics['overall_ubuntu_score']:.2f}/10")
    print(f"Supported Cultures: {len(analytics['supported_cultures'])}")
    print(f"Proverb Cultures: {len(analytics['proverb_cultures'])}")
    
    print("\n🎉 Conversational Interface Agent testing completed!")

if __name__ == "__main__":
    asyncio.run(main())

