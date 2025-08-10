#!/usr/bin/env python3
"""
WebWaka Digital Operating System - Ubuntu Philosophy Agent (Agent 25)
Community-centered approach integration with Ubuntu principles, collective responsibility,
traditional governance, elder wisdom, and consensus-building mechanisms

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
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UbuntuPrinciple(Enum):
    """Core Ubuntu principles"""
    HUMANITY = "humanity"  # Umuntu ngumuntu ngabantu
    COLLECTIVE_RESPONSIBILITY = "collective_responsibility"
    ELDER_WISDOM = "elder_wisdom"
    COMMUNITY_BENEFIT = "community_benefit"
    CONSENSUS_BUILDING = "consensus_building"
    CULTURAL_PRESERVATION = "cultural_preservation"
    MUTUAL_SUPPORT = "mutual_support"
    HARMONIOUS_COEXISTENCE = "harmonious_coexistence"

class GovernanceStyle(Enum):
    """Traditional governance styles"""
    INDABA = "indaba"  # Zulu council
    DARE = "dare"  # Shona council
    PALAVER = "palaver"  # West African council
    GUURTI = "guurti"  # Somali elder council
    LUKIIKO = "lukiiko"  # Buganda parliament
    KGOTLA = "kgotla"  # Botswana traditional court

class DecisionType(Enum):
    """Types of decisions requiring Ubuntu approach"""
    BUSINESS_STRATEGY = "business_strategy"
    RESOURCE_ALLOCATION = "resource_allocation"
    CONFLICT_RESOLUTION = "conflict_resolution"
    COMMUNITY_DEVELOPMENT = "community_development"
    PARTNERSHIP_FORMATION = "partnership_formation"
    CULTURAL_PRESERVATION = "cultural_preservation"

@dataclass
class UbuntuAssessment:
    """Ubuntu principle assessment"""
    principle: UbuntuPrinciple
    score: float
    evidence: List[str]
    recommendations: List[str]
    cultural_context: str

@dataclass
class CommunityStakeholder:
    """Community stakeholder representation"""
    stakeholder_id: str
    name: str
    role: str
    influence_level: float
    ubuntu_alignment: float
    traditional_authority: bool
    elder_status: bool
    community_contribution: float

@dataclass
class ConsensusProcess:
    """Ubuntu-based consensus building process"""
    process_id: str
    decision_type: DecisionType
    stakeholders: List[CommunityStakeholder]
    governance_style: GovernanceStyle
    ubuntu_principles_applied: List[UbuntuPrinciple]
    consensus_level: float
    elder_guidance: Dict[str, Any]
    community_benefit_score: float

@dataclass
class UbuntuDecision:
    """Ubuntu-informed decision"""
    decision_id: str
    original_proposal: str
    ubuntu_enhanced_proposal: str
    consensus_process: ConsensusProcess
    ubuntu_assessments: List[UbuntuAssessment]
    community_impact: Dict[str, float]
    elder_wisdom_applied: List[str]
    cultural_preservation_score: float
    collective_benefit_score: float
    implementation_guidance: List[str]

class UbuntuPhilosophyAgent:
    """
    Ubuntu Philosophy Agent for WebWaka Digital Operating System
    
    Implements authentic Ubuntu philosophy across all business processes with:
    - Community-centered approach in all decision-making
    - Collective responsibility and mutual support systems
    - Traditional governance integration (Indaba, Dare, Palaver, etc.)
    - Elder wisdom and traditional knowledge systems
    - Consensus-building mechanisms for conflict resolution
    - Cultural preservation and transmission frameworks
    - Harmonious coexistence and community benefit optimization
    
    Core Ubuntu Principles:
    - Umuntu ngumuntu ngabantu (A person is a person through other people)
    - Collective responsibility over individual gain
    - Elder respect and traditional wisdom integration
    - Community benefit optimization in all decisions
    - Consensus-building and harmonious decision-making
    - Cultural preservation and authentic transmission
    - Mutual support and shared prosperity
    - Harmonious coexistence across differences
    
    Features:
    - Ubuntu principle assessment and scoring
    - Traditional governance simulation and integration
    - Elder wisdom database and consultation systems
    - Community stakeholder analysis and engagement
    - Consensus-building algorithms and processes
    - Cultural authenticity validation and preservation
    - Collective benefit optimization across all operations
    - Conflict resolution through Ubuntu principles
    """
    
    def __init__(self):
        self.database_path = "/tmp/webwaka_ubuntu_philosophy.db"
        self.setup_database()
        self.ubuntu_principles = self._initialize_ubuntu_principles()
        self.governance_styles = self._initialize_governance_styles()
        self.elder_wisdom = self._initialize_elder_wisdom()
        self.cultural_contexts = [
            "southern_african_bantu",
            "east_african_bantu",
            "west_african_ubuntu_adaptation",
            "central_african_community",
            "pan_african_ubuntu",
            "modern_ubuntu_application"
        ]
        
    def setup_database(self):
        """Setup database for Ubuntu philosophy tracking"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ubuntu_assessments (
                id TEXT PRIMARY KEY,
                entity_id TEXT,
                entity_type TEXT,
                assessment_date TIMESTAMP,
                overall_ubuntu_score REAL,
                humanity_score REAL,
                collective_responsibility_score REAL,
                elder_wisdom_score REAL,
                community_benefit_score REAL,
                consensus_building_score REAL,
                cultural_preservation_score REAL,
                mutual_support_score REAL,
                harmonious_coexistence_score REAL,
                recommendations TEXT,
                cultural_context TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consensus_processes (
                id TEXT PRIMARY KEY,
                decision_type TEXT,
                governance_style TEXT,
                stakeholder_count INTEGER,
                consensus_level REAL,
                ubuntu_principles_applied TEXT,
                elder_guidance TEXT,
                community_benefit_score REAL,
                process_duration REAL,
                cultural_authenticity REAL,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ubuntu_decisions (
                id TEXT PRIMARY KEY,
                original_proposal TEXT,
                ubuntu_enhanced_proposal TEXT,
                decision_type TEXT,
                consensus_process_id TEXT,
                community_impact TEXT,
                elder_wisdom_applied TEXT,
                cultural_preservation_score REAL,
                collective_benefit_score REAL,
                implementation_status TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (consensus_process_id) REFERENCES consensus_processes (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elder_wisdom_database (
                id TEXT PRIMARY KEY,
                wisdom_category TEXT,
                cultural_origin TEXT,
                wisdom_text_local TEXT,
                wisdom_text_english TEXT,
                ubuntu_principle TEXT,
                application_context TEXT,
                wisdom_authority REAL,
                cultural_authenticity REAL,
                modern_relevance REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_stakeholders (
                id TEXT PRIMARY KEY,
                name TEXT,
                role TEXT,
                community TEXT,
                influence_level REAL,
                ubuntu_alignment REAL,
                traditional_authority BOOLEAN,
                elder_status BOOLEAN,
                community_contribution REAL,
                engagement_history TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ubuntu_principles_framework (
                id TEXT PRIMARY KEY,
                principle_name TEXT,
                ubuntu_concept TEXT,
                description TEXT,
                implementation_details TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS governance_styles_config (
                id TEXT PRIMARY KEY,
                style_name TEXT,
                cultural_origin TEXT,
                structure_details TEXT,
                process_details TEXT,
                ubuntu_alignment REAL,
                cultural_authenticity REAL
            )
        ''')
        
        # Insert Ubuntu principles framework
        ubuntu_principles = [
            ("UP_001", "humanity", "umuntu_ngumuntu_ngabantu", 
             "A person is a person through other people - fundamental interconnectedness",
             '{"recognition": "individual_through_community", "application": "all_decisions", "weight": 10.0}'),
            
            ("UP_002", "collective_responsibility", "shared_accountability",
             "Collective responsibility for community welfare and success",
             '{"recognition": "shared_outcomes", "application": "resource_allocation", "weight": 9.5}'),
            
            ("UP_003", "elder_wisdom", "traditional_knowledge",
             "Respect for elder wisdom and traditional knowledge systems",
             '{"recognition": "elder_guidance", "application": "decision_making", "weight": 9.8}'),
            
            ("UP_004", "community_benefit", "collective_good",
             "Community benefit prioritized over individual gain",
             '{"recognition": "community_first", "application": "business_strategy", "weight": 9.7}'),
            
            ("UP_005", "consensus_building", "harmonious_agreement",
             "Consensus-building and harmonious decision-making processes",
             '{"recognition": "inclusive_decisions", "application": "conflict_resolution", "weight": 9.2}'),
            
            ("UP_006", "cultural_preservation", "tradition_continuity",
             "Cultural preservation and authentic transmission to future generations",
             '{"recognition": "cultural_continuity", "application": "knowledge_transfer", "weight": 9.0}'),
            
            ("UP_007", "mutual_support", "reciprocal_assistance",
             "Mutual support and reciprocal assistance within community",
             '{"recognition": "mutual_aid", "application": "partnership_formation", "weight": 8.8}'),
            
            ("UP_008", "harmonious_coexistence", "peaceful_unity",
             "Harmonious coexistence across differences and diversity",
             '{"recognition": "unity_in_diversity", "application": "community_development", "weight": 8.5}')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO ubuntu_principles_framework 
            (id, principle_name, ubuntu_concept, description, implementation_details)
            VALUES (?, ?, ?, ?, ?)
        ''', ubuntu_principles)
        
        # Insert elder wisdom
        elder_wisdom = [
            ("EW_ZU_001", "decision_making", "zulu", 
             "Indlela ibuzwa kwabaphambili", "The path is asked from those who have traveled it",
             "elder_wisdom", "business_decisions", 9.8, 10.0, 9.5),
            
            ("EW_ZU_002", "community_unity", "zulu",
             "Umuntu ngumuntu ngabantu", "A person is a person through other people",
             "humanity", "all_contexts", 10.0, 10.0, 10.0),
            
            ("EW_SH_001", "collective_work", "shona",
             "Chara chimwe hachitswanyi inda", "One finger cannot kill a louse",
             "collective_responsibility", "teamwork", 9.5, 9.8, 9.2),
            
            ("EW_YO_001", "patience_wisdom", "yoruba",
             "Bi a ba n gun igi, a o gun epo", "When we climb a tree, we don't climb the palm oil",
             "consensus_building", "patience_in_decisions", 9.0, 9.5, 8.8),
            
            ("EW_SW_001", "unity_strength", "swahili",
             "Haba ya mvua ni pamoja", "Raindrops are together",
             "mutual_support", "collective_action", 9.3, 9.6, 9.1),
            
            ("EW_AK_001", "learning_humility", "akan",
             "Se wo were fi na wosankofa a yenkyi", "It is not wrong to go back for that which you have forgotten",
             "cultural_preservation", "continuous_learning", 9.0, 9.3, 8.9),
            
            ("EW_HA_001", "truth_strength", "hausa",
             "Gaskiya ta fi karfi", "Truth is stronger",
             "harmonious_coexistence", "honest_communication", 9.1, 9.4, 8.7),
            
            ("EW_AM_001", "good_deeds", "amharic",
             "የሰው ልጅ በመልካም ስራው ይታወቃል", "A person is known by their good deeds",
             "community_benefit", "character_building", 8.9, 9.2, 8.6)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO elder_wisdom_database 
            (id, wisdom_category, cultural_origin, wisdom_text_local, wisdom_text_english,
             ubuntu_principle, application_context, wisdom_authority, cultural_authenticity, modern_relevance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', elder_wisdom)
        
        # Insert governance styles
        governance_styles = [
            ("GS_001", "indaba", "zulu_traditional", 
             '{"structure": "circular_seating", "leadership": "elder_facilitation", "decision": "consensus_based"}',
             '{"participation": "all_voices_heard", "respect": "elder_deference", "outcome": "community_agreement"}',
             9.8, 9.5),
            
            ("GS_002", "dare", "shona_traditional",
             '{"structure": "under_tree", "leadership": "chief_elder", "decision": "collective_wisdom"}',
             '{"participation": "age_hierarchy", "respect": "traditional_protocol", "outcome": "unanimous_agreement"}',
             9.6, 9.3),
            
            ("GS_003", "palaver", "west_african",
             '{"structure": "community_gathering", "leadership": "rotating_speakers", "decision": "extended_discussion"}',
             '{"participation": "inclusive_dialogue", "respect": "equal_voice", "outcome": "negotiated_consensus"}',
             9.2, 8.8),
            
            ("GS_004", "guurti", "somali_elder",
             '{"structure": "elder_council", "leadership": "senior_elder", "decision": "wisdom_based"}',
             '{"participation": "elder_exclusive", "respect": "age_authority", "outcome": "binding_decision"}',
             9.4, 9.1),
            
            ("GS_005", "lukiiko", "buganda_parliament",
             '{"structure": "formal_assembly", "leadership": "kabaka_representative", "decision": "structured_debate"}',
             '{"participation": "representative_voices", "respect": "royal_protocol", "outcome": "formal_resolution"}',
             8.9, 8.6),
            
            ("GS_006", "kgotla", "botswana_traditional",
             '{"structure": "open_court", "leadership": "chief_kgosi", "decision": "public_consensus"}',
             '{"participation": "community_wide", "respect": "traditional_hierarchy", "outcome": "public_agreement"}',
             9.1, 8.9)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO governance_styles_config 
            (id, style_name, cultural_origin, structure_details, process_details, ubuntu_alignment, cultural_authenticity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', governance_styles)
        
        conn.commit()
        conn.close()
        logger.info("Ubuntu philosophy database setup completed")

    def _initialize_ubuntu_principles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize Ubuntu principles framework"""
        principles = {}
        
        for principle in UbuntuPrinciple:
            principles[principle.value] = {
                "weight": self._get_principle_weight(principle),
                "assessment_criteria": self._get_assessment_criteria(principle),
                "implementation_guidelines": self._get_implementation_guidelines(principle)
            }
        
        return principles

    def _get_principle_weight(self, principle: UbuntuPrinciple) -> float:
        """Get weight for Ubuntu principle"""
        weights = {
            UbuntuPrinciple.HUMANITY: 10.0,
            UbuntuPrinciple.COLLECTIVE_RESPONSIBILITY: 9.5,
            UbuntuPrinciple.ELDER_WISDOM: 9.8,
            UbuntuPrinciple.COMMUNITY_BENEFIT: 9.7,
            UbuntuPrinciple.CONSENSUS_BUILDING: 9.2,
            UbuntuPrinciple.CULTURAL_PRESERVATION: 9.0,
            UbuntuPrinciple.MUTUAL_SUPPORT: 8.8,
            UbuntuPrinciple.HARMONIOUS_COEXISTENCE: 8.5
        }
        return weights.get(principle, 8.0)

    def _get_assessment_criteria(self, principle: UbuntuPrinciple) -> List[str]:
        """Get assessment criteria for Ubuntu principle"""
        criteria = {
            UbuntuPrinciple.HUMANITY: [
                "recognition_of_interconnectedness",
                "individual_through_community_perspective",
                "human_dignity_respect",
                "empathy_and_compassion"
            ],
            UbuntuPrinciple.COLLECTIVE_RESPONSIBILITY: [
                "shared_accountability",
                "community_welfare_priority",
                "collective_problem_solving",
                "resource_sharing"
            ],
            UbuntuPrinciple.ELDER_WISDOM: [
                "elder_consultation",
                "traditional_knowledge_integration",
                "respect_for_experience",
                "wisdom_transmission"
            ],
            UbuntuPrinciple.COMMUNITY_BENEFIT: [
                "community_over_individual_gain",
                "collective_prosperity",
                "shared_value_creation",
                "community_development_focus"
            ],
            UbuntuPrinciple.CONSENSUS_BUILDING: [
                "inclusive_decision_making",
                "conflict_resolution_through_dialogue",
                "harmonious_agreement_seeking",
                "patient_consensus_building"
            ],
            UbuntuPrinciple.CULTURAL_PRESERVATION: [
                "traditional_practice_maintenance",
                "cultural_knowledge_transmission",
                "authentic_cultural_expression",
                "intergenerational_continuity"
            ],
            UbuntuPrinciple.MUTUAL_SUPPORT: [
                "reciprocal_assistance",
                "community_solidarity",
                "shared_burden_bearing",
                "collective_care"
            ],
            UbuntuPrinciple.HARMONIOUS_COEXISTENCE: [
                "peaceful_conflict_resolution",
                "unity_in_diversity",
                "tolerance_and_acceptance",
                "community_harmony"
            ]
        }
        return criteria.get(principle, [])

    def _get_implementation_guidelines(self, principle: UbuntuPrinciple) -> List[str]:
        """Get implementation guidelines for Ubuntu principle"""
        guidelines = {
            UbuntuPrinciple.HUMANITY: [
                "Always consider impact on community members",
                "Prioritize human dignity in all decisions",
                "Foster empathy and understanding",
                "Recognize individual worth through community connection"
            ],
            UbuntuPrinciple.COLLECTIVE_RESPONSIBILITY: [
                "Share accountability for outcomes",
                "Distribute resources equitably",
                "Engage community in problem-solving",
                "Take collective ownership of challenges"
            ],
            UbuntuPrinciple.ELDER_WISDOM: [
                "Consult elders before major decisions",
                "Integrate traditional knowledge",
                "Show respect for experience and age",
                "Create channels for wisdom transmission"
            ],
            UbuntuPrinciple.COMMUNITY_BENEFIT: [
                "Evaluate decisions for community impact",
                "Prioritize collective over individual gain",
                "Invest in community development",
                "Create shared value for all"
            ],
            UbuntuPrinciple.CONSENSUS_BUILDING: [
                "Include all stakeholders in decisions",
                "Use dialogue for conflict resolution",
                "Seek win-win solutions",
                "Build patient consensus processes"
            ],
            UbuntuPrinciple.CULTURAL_PRESERVATION: [
                "Maintain traditional practices",
                "Document and transmit cultural knowledge",
                "Support authentic cultural expression",
                "Bridge traditional and modern contexts"
            ],
            UbuntuPrinciple.MUTUAL_SUPPORT: [
                "Provide reciprocal assistance",
                "Build community solidarity",
                "Share burdens collectively",
                "Create support networks"
            ],
            UbuntuPrinciple.HARMONIOUS_COEXISTENCE: [
                "Resolve conflicts peacefully",
                "Celebrate diversity within unity",
                "Practice tolerance and acceptance",
                "Maintain community harmony"
            ]
        }
        return guidelines.get(principle, [])

    def _initialize_governance_styles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize traditional governance styles"""
        return {
            GovernanceStyle.INDABA.value: {
                "cultural_origin": "zulu_traditional",
                "structure": "circular_seating_elder_facilitation",
                "decision_process": "consensus_based_all_voices",
                "ubuntu_alignment": 9.8,
                "modern_applicability": 9.5
            },
            GovernanceStyle.DARE.value: {
                "cultural_origin": "shona_traditional",
                "structure": "under_tree_chief_elder",
                "decision_process": "collective_wisdom_unanimous",
                "ubuntu_alignment": 9.6,
                "modern_applicability": 9.3
            },
            GovernanceStyle.PALAVER.value: {
                "cultural_origin": "west_african",
                "structure": "community_gathering_rotating",
                "decision_process": "extended_discussion_negotiated",
                "ubuntu_alignment": 9.2,
                "modern_applicability": 8.8
            },
            GovernanceStyle.GUURTI.value: {
                "cultural_origin": "somali_elder",
                "structure": "elder_council_senior",
                "decision_process": "wisdom_based_binding",
                "ubuntu_alignment": 9.4,
                "modern_applicability": 9.1
            },
            GovernanceStyle.LUKIIKO.value: {
                "cultural_origin": "buganda_parliament",
                "structure": "formal_assembly_representative",
                "decision_process": "structured_debate_formal",
                "ubuntu_alignment": 8.9,
                "modern_applicability": 8.6
            },
            GovernanceStyle.KGOTLA.value: {
                "cultural_origin": "botswana_traditional",
                "structure": "open_court_chief",
                "decision_process": "public_consensus_community",
                "ubuntu_alignment": 9.1,
                "modern_applicability": 8.9
            }
        }

    def _initialize_elder_wisdom(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize elder wisdom database"""
        wisdom = {}
        
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT wisdom_category, cultural_origin, wisdom_text_local, wisdom_text_english,
                   ubuntu_principle, application_context, wisdom_authority, cultural_authenticity, modern_relevance
            FROM elder_wisdom_database
        ''')
        
        for row in cursor.fetchall():
            category = row[0]
            if category not in wisdom:
                wisdom[category] = []
            
            wisdom[category].append({
                "cultural_origin": row[1],
                "local_text": row[2],
                "english_text": row[3],
                "ubuntu_principle": row[4],
                "application_context": row[5],
                "wisdom_authority": row[6],
                "cultural_authenticity": row[7],
                "modern_relevance": row[8]
            })
        
        conn.close()
        return wisdom

    async def assess_ubuntu_alignment(self, entity_data: Dict[str, Any], 
                                    entity_type: str = "business_process") -> List[UbuntuAssessment]:
        """Assess Ubuntu alignment of an entity (business process, decision, etc.)"""
        assessments = []
        
        for principle in UbuntuPrinciple:
            assessment = await self._assess_single_principle(entity_data, principle, entity_type)
            assessments.append(assessment)
        
        # Store assessment in database
        await self._store_ubuntu_assessment(assessments, entity_data.get("id", "unknown"), entity_type)
        
        return assessments

    async def _assess_single_principle(self, entity_data: Dict[str, Any], 
                                     principle: UbuntuPrinciple, entity_type: str) -> UbuntuAssessment:
        """Assess a single Ubuntu principle"""
        principle_config = self.ubuntu_principles[principle.value]
        criteria = principle_config["assessment_criteria"]
        
        score = 0.0
        evidence = []
        recommendations = []
        
        # Assess based on principle-specific criteria
        if principle == UbuntuPrinciple.HUMANITY:
            score, evidence = await self._assess_humanity(entity_data)
        elif principle == UbuntuPrinciple.COLLECTIVE_RESPONSIBILITY:
            score, evidence = await self._assess_collective_responsibility(entity_data)
        elif principle == UbuntuPrinciple.ELDER_WISDOM:
            score, evidence = await self._assess_elder_wisdom(entity_data)
        elif principle == UbuntuPrinciple.COMMUNITY_BENEFIT:
            score, evidence = await self._assess_community_benefit(entity_data)
        elif principle == UbuntuPrinciple.CONSENSUS_BUILDING:
            score, evidence = await self._assess_consensus_building(entity_data)
        elif principle == UbuntuPrinciple.CULTURAL_PRESERVATION:
            score, evidence = await self._assess_cultural_preservation(entity_data)
        elif principle == UbuntuPrinciple.MUTUAL_SUPPORT:
            score, evidence = await self._assess_mutual_support(entity_data)
        elif principle == UbuntuPrinciple.HARMONIOUS_COEXISTENCE:
            score, evidence = await self._assess_harmonious_coexistence(entity_data)
        
        # Generate recommendations based on score
        if score < 7.0:
            recommendations = principle_config["implementation_guidelines"]
        elif score < 8.5:
            recommendations = principle_config["implementation_guidelines"][:2]
        
        return UbuntuAssessment(
            principle=principle,
            score=score,
            evidence=evidence,
            recommendations=recommendations,
            cultural_context=entity_data.get("cultural_context", "general")
        )

    async def _assess_humanity(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess humanity principle (Umuntu ngumuntu ngabantu)"""
        score = 5.0  # Base score
        evidence = []
        
        # Check for human-centered language
        text_content = str(entity_data.get("description", "")) + str(entity_data.get("content", ""))
        
        if "people" in text_content.lower() or "community" in text_content.lower():
            score += 1.5
            evidence.append("References to people and community")
        
        if "together" in text_content.lower() or "collective" in text_content.lower():
            score += 1.0
            evidence.append("Collective language usage")
        
        if "dignity" in text_content.lower() or "respect" in text_content.lower():
            score += 1.0
            evidence.append("Human dignity and respect references")
        
        # Check for stakeholder consideration
        if entity_data.get("stakeholders_considered", False):
            score += 1.5
            evidence.append("Stakeholder consideration included")
        
        return min(score, 10.0), evidence

    async def _assess_collective_responsibility(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess collective responsibility principle"""
        score = 5.0
        evidence = []
        
        # Check for shared accountability
        if entity_data.get("shared_accountability", False):
            score += 2.0
            evidence.append("Shared accountability framework")
        
        # Check for resource sharing
        if entity_data.get("resource_sharing", False):
            score += 1.5
            evidence.append("Resource sharing mechanisms")
        
        # Check for collective problem solving
        if entity_data.get("collective_problem_solving", False):
            score += 1.5
            evidence.append("Collective problem-solving approach")
        
        return min(score, 10.0), evidence

    async def _assess_elder_wisdom(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess elder wisdom principle"""
        score = 5.0
        evidence = []
        
        # Check for elder consultation
        if entity_data.get("elder_consultation", False):
            score += 2.5
            evidence.append("Elder consultation included")
        
        # Check for traditional knowledge integration
        if entity_data.get("traditional_knowledge", False):
            score += 2.0
            evidence.append("Traditional knowledge integration")
        
        # Check for wisdom transmission
        if entity_data.get("wisdom_transmission", False):
            score += 1.5
            evidence.append("Wisdom transmission mechanisms")
        
        return min(score, 10.0), evidence

    async def _assess_community_benefit(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess community benefit principle"""
        score = 5.0
        evidence = []
        
        # Check for community impact consideration
        community_impact = entity_data.get("community_impact", 0.0)
        if community_impact > 0.7:
            score += 2.5
            evidence.append(f"High community impact score: {community_impact}")
        elif community_impact > 0.5:
            score += 1.5
            evidence.append(f"Moderate community impact score: {community_impact}")
        
        # Check for shared value creation
        if entity_data.get("shared_value_creation", False):
            score += 2.0
            evidence.append("Shared value creation approach")
        
        return min(score, 10.0), evidence

    async def _assess_consensus_building(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess consensus building principle"""
        score = 5.0
        evidence = []
        
        # Check for inclusive decision making
        if entity_data.get("inclusive_decision_making", False):
            score += 2.0
            evidence.append("Inclusive decision-making process")
        
        # Check for conflict resolution mechanisms
        if entity_data.get("conflict_resolution", False):
            score += 1.5
            evidence.append("Conflict resolution mechanisms")
        
        # Check for consensus seeking
        if entity_data.get("consensus_seeking", False):
            score += 1.5
            evidence.append("Consensus-seeking approach")
        
        return min(score, 10.0), evidence

    async def _assess_cultural_preservation(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess cultural preservation principle"""
        score = 5.0
        evidence = []
        
        # Check for traditional practice maintenance
        if entity_data.get("traditional_practices", False):
            score += 2.0
            evidence.append("Traditional practice maintenance")
        
        # Check for cultural knowledge transmission
        if entity_data.get("cultural_transmission", False):
            score += 2.0
            evidence.append("Cultural knowledge transmission")
        
        # Check for authentic cultural expression
        if entity_data.get("authentic_expression", False):
            score += 1.0
            evidence.append("Authentic cultural expression")
        
        return min(score, 10.0), evidence

    async def _assess_mutual_support(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess mutual support principle"""
        score = 5.0
        evidence = []
        
        # Check for reciprocal assistance
        if entity_data.get("reciprocal_assistance", False):
            score += 2.0
            evidence.append("Reciprocal assistance mechanisms")
        
        # Check for community solidarity
        if entity_data.get("community_solidarity", False):
            score += 1.5
            evidence.append("Community solidarity building")
        
        # Check for shared burden bearing
        if entity_data.get("shared_burdens", False):
            score += 1.5
            evidence.append("Shared burden bearing")
        
        return min(score, 10.0), evidence

    async def _assess_harmonious_coexistence(self, entity_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Assess harmonious coexistence principle"""
        score = 5.0
        evidence = []
        
        # Check for peaceful conflict resolution
        if entity_data.get("peaceful_resolution", False):
            score += 2.0
            evidence.append("Peaceful conflict resolution")
        
        # Check for unity in diversity
        if entity_data.get("unity_in_diversity", False):
            score += 1.5
            evidence.append("Unity in diversity approach")
        
        # Check for tolerance and acceptance
        if entity_data.get("tolerance", False):
            score += 1.5
            evidence.append("Tolerance and acceptance")
        
        return min(score, 10.0), evidence

    async def facilitate_ubuntu_decision(self, proposal: str, stakeholders: List[CommunityStakeholder],
                                       decision_type: DecisionType, 
                                       governance_style: GovernanceStyle = GovernanceStyle.INDABA) -> UbuntuDecision:
        """Facilitate Ubuntu-based decision making process"""
        decision_id = str(uuid.uuid4())
        
        # Create consensus process
        consensus_process = await self._create_consensus_process(
            stakeholders, decision_type, governance_style
        )
        
        # Apply Ubuntu principles to enhance proposal
        ubuntu_enhanced_proposal = await self._enhance_proposal_with_ubuntu(
            proposal, consensus_process
        )
        
        # Conduct Ubuntu assessments
        proposal_data = {
            "id": decision_id,
            "description": ubuntu_enhanced_proposal,
            "stakeholders_considered": True,
            "community_impact": consensus_process.community_benefit_score,
            "elder_consultation": any(s.elder_status for s in stakeholders),
            "inclusive_decision_making": True,
            "consensus_seeking": True
        }
        
        ubuntu_assessments = await self.assess_ubuntu_alignment(proposal_data, "decision")
        
        # Calculate community impact
        community_impact = await self._calculate_community_impact(
            ubuntu_enhanced_proposal, stakeholders, ubuntu_assessments
        )
        
        # Apply elder wisdom
        elder_wisdom_applied = await self._apply_elder_wisdom(
            ubuntu_enhanced_proposal, decision_type, stakeholders
        )
        
        # Calculate scores
        cultural_preservation_score = await self._calculate_cultural_preservation_score(ubuntu_assessments)
        collective_benefit_score = await self._calculate_collective_benefit_score(ubuntu_assessments)
        
        # Generate implementation guidance
        implementation_guidance = await self._generate_implementation_guidance(
            ubuntu_assessments, consensus_process
        )
        
        decision = UbuntuDecision(
            decision_id=decision_id,
            original_proposal=proposal,
            ubuntu_enhanced_proposal=ubuntu_enhanced_proposal,
            consensus_process=consensus_process,
            ubuntu_assessments=ubuntu_assessments,
            community_impact=community_impact,
            elder_wisdom_applied=elder_wisdom_applied,
            cultural_preservation_score=cultural_preservation_score,
            collective_benefit_score=collective_benefit_score,
            implementation_guidance=implementation_guidance
        )
        
        # Store decision
        await self._store_ubuntu_decision(decision)
        
        return decision

    async def _create_consensus_process(self, stakeholders: List[CommunityStakeholder],
                                      decision_type: DecisionType, 
                                      governance_style: GovernanceStyle) -> ConsensusProcess:
        """Create Ubuntu-based consensus process"""
        process_id = str(uuid.uuid4())
        
        # Determine Ubuntu principles to apply
        ubuntu_principles_applied = [
            UbuntuPrinciple.CONSENSUS_BUILDING,
            UbuntuPrinciple.ELDER_WISDOM,
            UbuntuPrinciple.COMMUNITY_BENEFIT
        ]
        
        if any(s.elder_status for s in stakeholders):
            ubuntu_principles_applied.append(UbuntuPrinciple.ELDER_WISDOM)
        
        # Calculate consensus level based on stakeholder alignment
        consensus_level = sum(s.ubuntu_alignment for s in stakeholders) / len(stakeholders)
        
        # Generate elder guidance
        elder_guidance = await self._generate_elder_guidance(stakeholders, decision_type)
        
        # Calculate community benefit score
        community_benefit_score = await self._calculate_community_benefit_score_for_process(
            stakeholders, decision_type
        )
        
        return ConsensusProcess(
            process_id=process_id,
            decision_type=decision_type,
            stakeholders=stakeholders,
            governance_style=governance_style,
            ubuntu_principles_applied=ubuntu_principles_applied,
            consensus_level=consensus_level,
            elder_guidance=elder_guidance,
            community_benefit_score=community_benefit_score
        )

    async def _enhance_proposal_with_ubuntu(self, proposal: str, 
                                          consensus_process: ConsensusProcess) -> str:
        """Enhance proposal with Ubuntu principles"""
        enhanced_proposal = proposal
        
        # Add community benefit focus
        if "benefit" not in enhanced_proposal.lower():
            enhanced_proposal += " This initiative will prioritize community benefit and collective prosperity."
        
        # Add consensus building
        if "consensus" not in enhanced_proposal.lower():
            enhanced_proposal += " We will seek consensus through inclusive dialogue and traditional wisdom."
        
        # Add elder wisdom integration
        if any(s.elder_status for s in consensus_process.stakeholders):
            enhanced_proposal += " Elder guidance and traditional knowledge will inform our approach."
        
        # Add Ubuntu humanity principle
        enhanced_proposal += " Recognizing that we are interconnected and that our individual success depends on our collective wellbeing."
        
        return enhanced_proposal

    async def _calculate_community_impact(self, proposal: str, stakeholders: List[CommunityStakeholder],
                                        ubuntu_assessments: List[UbuntuAssessment]) -> Dict[str, float]:
        """Calculate community impact metrics"""
        impact = {
            "economic_impact": 0.0,
            "social_impact": 0.0,
            "cultural_impact": 0.0,
            "environmental_impact": 0.0,
            "overall_impact": 0.0
        }
        
        # Calculate based on Ubuntu assessments
        community_benefit_score = next(
            (a.score for a in ubuntu_assessments if a.principle == UbuntuPrinciple.COMMUNITY_BENEFIT),
            5.0
        ) / 10.0
        
        cultural_preservation_score = next(
            (a.score for a in ubuntu_assessments if a.principle == UbuntuPrinciple.CULTURAL_PRESERVATION),
            5.0
        ) / 10.0
        
        # Estimate impacts
        impact["economic_impact"] = community_benefit_score * 0.8
        impact["social_impact"] = community_benefit_score * 0.9
        impact["cultural_impact"] = cultural_preservation_score * 0.9
        impact["environmental_impact"] = community_benefit_score * 0.6  # Assume positive correlation
        
        impact["overall_impact"] = sum(impact.values()) / 4
        
        return impact

    async def _apply_elder_wisdom(self, proposal: str, decision_type: DecisionType,
                                stakeholders: List[CommunityStakeholder]) -> List[str]:
        """Apply relevant elder wisdom to the decision"""
        wisdom_applied = []
        
        # Get relevant wisdom based on decision type
        relevant_categories = {
            DecisionType.BUSINESS_STRATEGY: ["decision_making", "collective_work"],
            DecisionType.RESOURCE_ALLOCATION: ["collective_work", "unity_strength"],
            DecisionType.CONFLICT_RESOLUTION: ["patience_wisdom", "truth_strength"],
            DecisionType.COMMUNITY_DEVELOPMENT: ["unity_strength", "good_deeds"],
            DecisionType.PARTNERSHIP_FORMATION: ["collective_work", "unity_strength"],
            DecisionType.CULTURAL_PRESERVATION: ["learning_humility", "good_deeds"]
        }
        
        categories = relevant_categories.get(decision_type, ["decision_making"])
        
        for category in categories:
            if category in self.elder_wisdom:
                wisdom_items = self.elder_wisdom[category]
                if wisdom_items:
                    # Select highest authority wisdom
                    best_wisdom = max(wisdom_items, key=lambda w: w["wisdom_authority"])
                    wisdom_applied.append(best_wisdom["english_text"])
        
        return wisdom_applied

    async def _calculate_cultural_preservation_score(self, ubuntu_assessments: List[UbuntuAssessment]) -> float:
        """Calculate cultural preservation score"""
        cultural_assessment = next(
            (a for a in ubuntu_assessments if a.principle == UbuntuPrinciple.CULTURAL_PRESERVATION),
            None
        )
        
        return cultural_assessment.score if cultural_assessment else 5.0

    async def _calculate_collective_benefit_score(self, ubuntu_assessments: List[UbuntuAssessment]) -> float:
        """Calculate collective benefit score"""
        # Average of community benefit, collective responsibility, and mutual support
        relevant_principles = [
            UbuntuPrinciple.COMMUNITY_BENEFIT,
            UbuntuPrinciple.COLLECTIVE_RESPONSIBILITY,
            UbuntuPrinciple.MUTUAL_SUPPORT
        ]
        
        scores = []
        for principle in relevant_principles:
            assessment = next((a for a in ubuntu_assessments if a.principle == principle), None)
            if assessment:
                scores.append(assessment.score)
        
        return sum(scores) / len(scores) if scores else 5.0

    async def _generate_implementation_guidance(self, ubuntu_assessments: List[UbuntuAssessment],
                                              consensus_process: ConsensusProcess) -> List[str]:
        """Generate Ubuntu-based implementation guidance"""
        guidance = []
        
        # Add guidance based on low-scoring principles
        for assessment in ubuntu_assessments:
            if assessment.score < 8.0:
                guidance.extend(assessment.recommendations[:2])
        
        # Add governance-specific guidance
        governance_guidance = {
            GovernanceStyle.INDABA: "Conduct regular community circles for feedback and adjustment",
            GovernanceStyle.DARE: "Seek elder approval at key implementation milestones",
            GovernanceStyle.PALAVER: "Maintain open dialogue throughout implementation",
            GovernanceStyle.GUURTI: "Follow elder council guidance for major decisions",
            GovernanceStyle.LUKIIKO: "Use formal review processes with community representatives",
            GovernanceStyle.KGOTLA: "Ensure transparent public reporting of progress"
        }
        
        style_guidance = governance_guidance.get(consensus_process.governance_style)
        if style_guidance:
            guidance.append(style_guidance)
        
        return list(set(guidance))  # Remove duplicates

    async def _generate_elder_guidance(self, stakeholders: List[CommunityStakeholder],
                                     decision_type: DecisionType) -> Dict[str, Any]:
        """Generate elder guidance for the decision"""
        elders = [s for s in stakeholders if s.elder_status]
        
        guidance = {
            "elder_count": len(elders),
            "elder_influence": sum(e.influence_level for e in elders) / len(elders) if elders else 0,
            "elder_ubuntu_alignment": sum(e.ubuntu_alignment for e in elders) / len(elders) if elders else 0,
            "guidance_areas": [],
            "traditional_protocols": []
        }
        
        if elders:
            guidance["guidance_areas"] = [
                "traditional_wisdom_application",
                "cultural_authenticity_validation",
                "community_impact_assessment",
                "intergenerational_consideration"
            ]
            
            guidance["traditional_protocols"] = [
                "elder_consultation_required",
                "traditional_blessing_sought",
                "community_announcement_needed",
                "cultural_ceremony_consideration"
            ]
        
        return guidance

    async def _calculate_community_benefit_score_for_process(self, stakeholders: List[CommunityStakeholder],
                                                           decision_type: DecisionType) -> float:
        """Calculate community benefit score for consensus process"""
        # Base score from stakeholder community contribution
        base_score = sum(s.community_contribution for s in stakeholders) / len(stakeholders)
        
        # Adjust based on decision type
        decision_multipliers = {
            DecisionType.COMMUNITY_DEVELOPMENT: 1.2,
            DecisionType.RESOURCE_ALLOCATION: 1.1,
            DecisionType.CULTURAL_PRESERVATION: 1.15,
            DecisionType.PARTNERSHIP_FORMATION: 1.05,
            DecisionType.BUSINESS_STRATEGY: 1.0,
            DecisionType.CONFLICT_RESOLUTION: 1.1
        }
        
        multiplier = decision_multipliers.get(decision_type, 1.0)
        return min(base_score * multiplier, 10.0)

    async def _store_ubuntu_assessment(self, assessments: List[UbuntuAssessment], 
                                     entity_id: str, entity_type: str):
        """Store Ubuntu assessment in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Calculate overall score
            overall_score = sum(a.score for a in assessments) / len(assessments)
            
            # Get individual principle scores
            principle_scores = {a.principle.value: a.score for a in assessments}
            
            cursor.execute('''
                INSERT OR REPLACE INTO ubuntu_assessments 
                (id, entity_id, entity_type, assessment_date, overall_ubuntu_score,
                 humanity_score, collective_responsibility_score, elder_wisdom_score,
                 community_benefit_score, consensus_building_score, cultural_preservation_score,
                 mutual_support_score, harmonious_coexistence_score, recommendations, cultural_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                entity_id,
                entity_type,
                datetime.now(),
                overall_score,
                principle_scores.get("humanity", 0),
                principle_scores.get("collective_responsibility", 0),
                principle_scores.get("elder_wisdom", 0),
                principle_scores.get("community_benefit", 0),
                principle_scores.get("consensus_building", 0),
                principle_scores.get("cultural_preservation", 0),
                principle_scores.get("mutual_support", 0),
                principle_scores.get("harmonious_coexistence", 0),
                json.dumps([r for a in assessments for r in a.recommendations]),
                assessments[0].cultural_context if assessments else "general"
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing Ubuntu assessment: {str(e)}")

    async def _store_ubuntu_decision(self, decision: UbuntuDecision):
        """Store Ubuntu decision in database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Store consensus process first
            cursor.execute('''
                INSERT INTO consensus_processes 
                (id, decision_type, governance_style, stakeholder_count, consensus_level,
                 ubuntu_principles_applied, elder_guidance, community_benefit_score,
                 process_duration, cultural_authenticity, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision.consensus_process.process_id,
                decision.consensus_process.decision_type.value,
                decision.consensus_process.governance_style.value,
                len(decision.consensus_process.stakeholders),
                decision.consensus_process.consensus_level,
                json.dumps([p.value for p in decision.consensus_process.ubuntu_principles_applied]),
                json.dumps(decision.consensus_process.elder_guidance),
                decision.consensus_process.community_benefit_score,
                0.0,  # Process duration (would be calculated in real implementation)
                9.0,  # Cultural authenticity (would be calculated)
                datetime.now()
            ))
            
            # Store decision
            cursor.execute('''
                INSERT INTO ubuntu_decisions 
                (id, original_proposal, ubuntu_enhanced_proposal, decision_type, consensus_process_id,
                 community_impact, elder_wisdom_applied, cultural_preservation_score,
                 collective_benefit_score, implementation_status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision.decision_id,
                decision.original_proposal,
                decision.ubuntu_enhanced_proposal,
                decision.consensus_process.decision_type.value,
                decision.consensus_process.process_id,
                json.dumps(decision.community_impact),
                json.dumps(decision.elder_wisdom_applied),
                decision.cultural_preservation_score,
                decision.collective_benefit_score,
                "pending",
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing Ubuntu decision: {str(e)}")

    async def get_ubuntu_analytics(self) -> Dict[str, Any]:
        """Get comprehensive Ubuntu philosophy analytics"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        # Get assessment statistics
        cursor.execute('''
            SELECT entity_type, COUNT(*) as assessment_count,
                   AVG(overall_ubuntu_score) as avg_ubuntu_score,
                   AVG(humanity_score) as avg_humanity,
                   AVG(collective_responsibility_score) as avg_collective_responsibility,
                   AVG(elder_wisdom_score) as avg_elder_wisdom,
                   AVG(community_benefit_score) as avg_community_benefit,
                   AVG(consensus_building_score) as avg_consensus_building,
                   AVG(cultural_preservation_score) as avg_cultural_preservation,
                   AVG(mutual_support_score) as avg_mutual_support,
                   AVG(harmonious_coexistence_score) as avg_harmonious_coexistence
            FROM ubuntu_assessments 
            GROUP BY entity_type
        ''')
        
        assessment_stats = {}
        for row in cursor.fetchall():
            assessment_stats[row[0]] = {
                "assessment_count": row[1],
                "avg_ubuntu_score": round(row[2], 2) if row[2] else 0,
                "principle_scores": {
                    "humanity": round(row[3], 2) if row[3] else 0,
                    "collective_responsibility": round(row[4], 2) if row[4] else 0,
                    "elder_wisdom": round(row[5], 2) if row[5] else 0,
                    "community_benefit": round(row[6], 2) if row[6] else 0,
                    "consensus_building": round(row[7], 2) if row[7] else 0,
                    "cultural_preservation": round(row[8], 2) if row[8] else 0,
                    "mutual_support": round(row[9], 2) if row[9] else 0,
                    "harmonious_coexistence": round(row[10], 2) if row[10] else 0
                }
            }
        
        # Get consensus process statistics
        cursor.execute('''
            SELECT governance_style, COUNT(*) as process_count,
                   AVG(consensus_level) as avg_consensus,
                   AVG(community_benefit_score) as avg_community_benefit,
                   AVG(cultural_authenticity) as avg_cultural_authenticity
            FROM consensus_processes 
            GROUP BY governance_style
        ''')
        
        consensus_stats = {}
        for row in cursor.fetchall():
            consensus_stats[row[0]] = {
                "process_count": row[1],
                "avg_consensus": round(row[2], 2) if row[2] else 0,
                "avg_community_benefit": round(row[3], 2) if row[3] else 0,
                "avg_cultural_authenticity": round(row[4], 2) if row[4] else 0
            }
        
        conn.close()
        
        return {
            "ubuntu_principles": [p.value for p in UbuntuPrinciple],
            "governance_styles": [g.value for g in GovernanceStyle],
            "assessment_statistics": assessment_stats,
            "consensus_statistics": consensus_stats,
            "cultural_contexts": self.cultural_contexts,
            "elder_wisdom_categories": list(self.elder_wisdom.keys()),
            "total_assessments": sum(stats["assessment_count"] for stats in assessment_stats.values()),
            "total_consensus_processes": sum(stats["process_count"] for stats in consensus_stats.values()),
            "overall_ubuntu_score": sum(stats["avg_ubuntu_score"] for stats in assessment_stats.values()) / len(assessment_stats) if assessment_stats else 0
        }

async def main():
    """Main function for testing Ubuntu Philosophy Agent"""
    agent = UbuntuPhilosophyAgent()
    
    # Test Ubuntu assessment
    test_entities = [
        {
            "id": "business_process_001",
            "description": "Community-centered business development with elder consultation and shared benefits",
            "stakeholders_considered": True,
            "community_impact": 0.8,
            "elder_consultation": True,
            "shared_accountability": True,
            "traditional_knowledge": True,
            "inclusive_decision_making": True,
            "cultural_transmission": True,
            "reciprocal_assistance": True,
            "peaceful_resolution": True,
            "cultural_context": "southern_african_bantu"
        },
        {
            "id": "partnership_002",
            "description": "Individual profit-focused partnership with limited community consideration",
            "stakeholders_considered": False,
            "community_impact": 0.3,
            "elder_consultation": False,
            "shared_accountability": False,
            "traditional_knowledge": False,
            "inclusive_decision_making": False,
            "cultural_transmission": False,
            "reciprocal_assistance": False,
            "peaceful_resolution": True,
            "cultural_context": "modern_ubuntu_application"
        }
    ]
    
    print("🤝 Testing Ubuntu Philosophy Agent")
    print("=" * 60)
    
    for i, entity in enumerate(test_entities, 1):
        print(f"\n📊 Ubuntu Assessment {i}: {entity['id']}")
        print(f"Description: {entity['description']}")
        print(f"Cultural Context: {entity['cultural_context']}")
        
        assessments = await agent.assess_ubuntu_alignment(entity, "business_process")
        
        print(f"\n🎯 Ubuntu Principle Assessments:")
        total_score = 0
        for assessment in assessments:
            print(f"  {assessment.principle.value.replace('_', ' ').title()}: {assessment.score:.1f}/10")
            if assessment.evidence:
                print(f"    Evidence: {', '.join(assessment.evidence)}")
            total_score += assessment.score
        
        avg_score = total_score / len(assessments)
        print(f"\n📈 Overall Ubuntu Score: {avg_score:.1f}/10")
        
        # Show recommendations for low scores
        low_score_assessments = [a for a in assessments if a.score < 7.0]
        if low_score_assessments:
            print(f"\n💡 Recommendations for Improvement:")
            for assessment in low_score_assessments:
                print(f"  {assessment.principle.value.replace('_', ' ').title()}:")
                for rec in assessment.recommendations[:2]:
                    print(f"    - {rec}")
    
    # Test Ubuntu decision facilitation
    print(f"\n🏛️ Testing Ubuntu Decision Facilitation")
    print("=" * 60)
    
    # Create test stakeholders
    stakeholders = [
        CommunityStakeholder(
            stakeholder_id="elder_001",
            name="Mkhulu Mandela",
            role="Community Elder",
            influence_level=9.5,
            ubuntu_alignment=9.8,
            traditional_authority=True,
            elder_status=True,
            community_contribution=9.2
        ),
        CommunityStakeholder(
            stakeholder_id="leader_001",
            name="Mama Wangari",
            role="Community Leader",
            influence_level=8.5,
            ubuntu_alignment=9.0,
            traditional_authority=False,
            elder_status=False,
            community_contribution=8.8
        ),
        CommunityStakeholder(
            stakeholder_id="youth_001",
            name="Kwame Asante",
            role="Youth Representative",
            influence_level=6.5,
            ubuntu_alignment=7.5,
            traditional_authority=False,
            elder_status=False,
            community_contribution=7.2
        )
    ]
    
    proposal = "Establish a community technology center to provide digital skills training and internet access for local entrepreneurs."
    
    print(f"Original Proposal: {proposal}")
    print(f"Stakeholders: {len(stakeholders)} (including {sum(1 for s in stakeholders if s.elder_status)} elders)")
    
    ubuntu_decision = await agent.facilitate_ubuntu_decision(
        proposal, stakeholders, DecisionType.COMMUNITY_DEVELOPMENT, GovernanceStyle.INDABA
    )
    
    print(f"\n✅ Ubuntu-Enhanced Proposal:")
    print(f"{ubuntu_decision.ubuntu_enhanced_proposal}")
    
    print(f"\n🏛️ Consensus Process:")
    print(f"Governance Style: {ubuntu_decision.consensus_process.governance_style.value}")
    print(f"Consensus Level: {ubuntu_decision.consensus_process.consensus_level:.2f}")
    print(f"Community Benefit Score: {ubuntu_decision.consensus_process.community_benefit_score:.1f}/10")
    print(f"Ubuntu Principles Applied: {len(ubuntu_decision.consensus_process.ubuntu_principles_applied)}")
    
    print(f"\n🌍 Community Impact:")
    for impact_type, score in ubuntu_decision.community_impact.items():
        print(f"  {impact_type.replace('_', ' ').title()}: {score:.2f}")
    
    print(f"\n💎 Elder Wisdom Applied:")
    for wisdom in ubuntu_decision.elder_wisdom_applied:
        print(f"  - {wisdom}")
    
    print(f"\n📊 Ubuntu Scores:")
    print(f"Cultural Preservation: {ubuntu_decision.cultural_preservation_score:.1f}/10")
    print(f"Collective Benefit: {ubuntu_decision.collective_benefit_score:.1f}/10")
    
    print(f"\n📋 Implementation Guidance:")
    for guidance in ubuntu_decision.implementation_guidance:
        print(f"  - {guidance}")
    
    # Get analytics
    analytics = await agent.get_ubuntu_analytics()
    print(f"\n📈 Ubuntu Philosophy Analytics:")
    print(f"Ubuntu Principles: {len(analytics['ubuntu_principles'])}")
    print(f"Governance Styles: {len(analytics['governance_styles'])}")
    print(f"Total Assessments: {analytics['total_assessments']}")
    print(f"Total Consensus Processes: {analytics['total_consensus_processes']}")
    print(f"Overall Ubuntu Score: {analytics['overall_ubuntu_score']:.2f}/10")
    print(f"Cultural Contexts: {len(analytics['cultural_contexts'])}")
    print(f"Elder Wisdom Categories: {len(analytics['elder_wisdom_categories'])}")
    
    print("\n🎉 Ubuntu Philosophy Agent testing completed!")

if __name__ == "__main__":
    asyncio.run(main())

