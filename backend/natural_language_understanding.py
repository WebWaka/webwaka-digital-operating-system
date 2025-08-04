"""
WebWaka Natural Language Understanding System
Advanced NLU for African business contexts with cultural intelligence
"""

import os
import json
import re
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import uuid

# Import AI providers and voice recognition
from ai_providers import ai_manager
from voice_recognition import AfricanLanguageConfig, LanguageFamily

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BusinessIntent(Enum):
    """Business intent categories"""
    SELL = "sell"
    BUY = "buy"
    INVENTORY_CHECK = "inventory_check"
    PRICE_INQUIRY = "price_inquiry"
    CUSTOMER_SERVICE = "customer_service"
    PAYMENT = "payment"
    DELIVERY = "delivery"
    RETURN = "return"
    DISCOUNT = "discount"
    GREETING = "greeting"
    GOODBYE = "goodbye"
    HELP = "help"
    UNKNOWN = "unknown"

class EntityType(Enum):
    """Entity types for business NLU"""
    PRODUCT = "product"
    QUANTITY = "quantity"
    PRICE = "price"
    CURRENCY = "currency"
    CUSTOMER = "customer"
    LOCATION = "location"
    TIME = "time"
    PAYMENT_METHOD = "payment_method"
    DISCOUNT_TYPE = "discount_type"
    PERSON = "person"
    ORGANIZATION = "organization"

class CulturalContext(Enum):
    """Cultural context categories"""
    FORMAL = "formal"
    INFORMAL = "informal"
    RESPECTFUL = "respectful"
    URGENT = "urgent"
    POLITE = "polite"
    DIRECT = "direct"
    INDIRECT = "indirect"
    COMMUNITY_ORIENTED = "community_oriented"
    INDIVIDUAL_ORIENTED = "individual_oriented"

@dataclass
class Entity:
    """Named entity with cultural context"""
    text: str
    entity_type: EntityType
    value: Any
    confidence: float
    start_pos: int
    end_pos: int
    language: str
    cultural_context: Optional[CulturalContext] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Intent:
    """Business intent with confidence and context"""
    intent: BusinessIntent
    confidence: float
    entities: List[Entity]
    language: str
    cultural_context: CulturalContext
    sub_intents: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NLUResult:
    """Complete NLU analysis result"""
    text: str
    language: str
    intent: Intent
    entities: List[Entity]
    sentiment: Dict[str, float]
    cultural_analysis: Dict[str, Any]
    business_context: Dict[str, Any]
    processing_time: float
    confidence: float
    alternatives: List[Intent] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class AfricanBusinessVocabulary:
    """Comprehensive African business vocabulary across languages"""
    
    # Extended business vocabulary for major African languages
    BUSINESS_VOCABULARY = {
        # Swahili (East Africa)
        'sw': {
            'products': {
                'sukari': ['sugar', 'sweetener'],
                'mchele': ['rice'],
                'mahindi': ['maize', 'corn'],
                'nazi': ['coconut'],
                'nyama': ['meat'],
                'samaki': ['fish'],
                'maziwa': ['milk'],
                'mkate': ['bread'],
                'chai': ['tea'],
                'kahawa': ['coffee'],
                'mafuta': ['oil', 'cooking oil'],
                'chumvi': ['salt'],
                'vitunguu': ['onions'],
                'nyanya': ['tomatoes'],
                'karoti': ['carrots']
            },
            'quantities': {
                'paketi': ['packet', 'package'],
                'kilo': ['kilogram', 'kg'],
                'lita': ['liter', 'litre'],
                'mfuko': ['bag', 'sack'],
                'sanduku': ['box', 'crate'],
                'chupa': ['bottle'],
                'mkebe': ['tin', 'can'],
                'kipimo': ['measure', 'unit'],
                'fungu': ['bunch', 'bundle'],
                'dozi': ['dozen']
            },
            'actions': {
                'uza': ['sell', 'vend'],
                'nunua': ['buy', 'purchase'],
                'lipa': ['pay', 'payment'],
                'rudisha': ['return', 'refund'],
                'pokea': ['receive', 'collect'],
                'peleka': ['deliver', 'send'],
                'angalia': ['check', 'look'],
                'hesabu': ['count', 'calculate'],
                'pima': ['measure', 'weigh'],
                'funga': ['close', 'pack']
            },
            'money': {
                'pesa': ['money', 'cash'],
                'shilingi': ['shilling'],
                'dola': ['dollar'],
                'bei': ['price', 'cost'],
                'gharama': ['expense', 'cost'],
                'faida': ['profit', 'benefit'],
                'hasara': ['loss'],
                'punguzo': ['discount', 'reduction'],
                'ongeza': ['increase', 'add'],
                'punguza': ['decrease', 'reduce']
            },
            'greetings': {
                'hujambo': ['hello', 'how are you'],
                'habari': ['news', 'how are things'],
                'karibu': ['welcome'],
                'asante': ['thank you'],
                'pole': ['sorry', 'sympathy'],
                'kwaheri': ['goodbye'],
                'tutaonana': ['see you later'],
                'hongera': ['congratulations']
            }
        },
        
        # Zulu (South Africa)
        'zu': {
            'products': {
                'ushukela': ['sugar'],
                'irayisi': ['rice'],
                'umbila': ['maize', 'corn'],
                'inyama': ['meat'],
                'inhlanzi': ['fish'],
                'ubisi': ['milk'],
                'isinkwa': ['bread'],
                'itiye': ['tea'],
                'ikhofi': ['coffee'],
                'amafutha': ['oil'],
                'usawoti': ['salt'],
                'u-anyanisi': ['onions'],
                'utamatisi': ['tomatoes']
            },
            'quantities': {
                'iphakheji': ['packet', 'package'],
                'ikhilogram': ['kilogram'],
                'ilitha': ['liter'],
                'isikhwama': ['bag'],
                'ibhokisi': ['box'],
                'ibhodlela': ['bottle'],
                'itini': ['tin', 'can'],
                'isilinganiso': ['measure'],
                'iqoqo': ['bunch'],
                'idazini': ['dozen']
            },
            'actions': {
                'thengisa': ['sell'],
                'thenga': ['buy'],
                'khokha': ['pay'],
                'buyisela': ['return'],
                'thola': ['receive'],
                'dlulisa': ['deliver'],
                'bheka': ['check'],
                'bala': ['count'],
                'linganisa': ['measure'],
                'vala': ['close']
            },
            'money': {
                'imali': ['money'],
                'irandi': ['rand'],
                'intengo': ['price'],
                'izindleko': ['cost'],
                'inzuzo': ['profit'],
                'ukulahlekelwa': ['loss'],
                'isaphulelo': ['discount'],
                'ukwengeza': ['increase'],
                'ukunciphisa': ['decrease']
            },
            'greetings': {
                'sawubona': ['hello'],
                'unjani': ['how are you'],
                'wamukelekile': ['welcome'],
                'ngiyabonga': ['thank you'],
                'ngiyaxolisa': ['sorry'],
                'sala kahle': ['goodbye'],
                'sizobonana': ['see you later']
            }
        },
        
        # Yoruba (West Africa)
        'yo': {
            'products': {
                'suga': ['sugar'],
                'iresi': ['rice'],
                'agbado': ['maize', 'corn'],
                'eran': ['meat'],
                'eja': ['fish'],
                'wara': ['milk'],
                'buredi': ['bread'],
                'tii': ['tea'],
                'kofi': ['coffee'],
                'epo': ['oil'],
                'iyo': ['salt'],
                'alubosa': ['onions'],
                'tomati': ['tomatoes']
            },
            'quantities': {
                'apoti': ['packet', 'package'],
                'kilo': ['kilogram'],
                'lita': ['liter'],
                'apo': ['bag'],
                'apoti': ['box'],
                'igo': ['bottle'],
                'agolo': ['tin'],
                'iwon': ['measure'],
                'idi': ['bunch'],
                'mejila': ['dozen']
            },
            'actions': {
                'ta': ['sell'],
                'ra': ['buy'],
                'sanwo': ['pay'],
                'pada': ['return'],
                'gba': ['receive'],
                'fi ranṣẹ': ['deliver'],
                'wo': ['check'],
                'ka': ['count'],
                'wọn': ['measure'],
                'ti': ['close']
            },
            'money': {
                'owo': ['money'],
                'naira': ['naira'],
                'idiyẹ': ['price'],
                'owo': ['cost'],
                'ere': ['profit'],
                'ofin': ['loss'],
                'dinku': ['discount'],
                'fi kun': ['increase'],
                'dinku': ['decrease']
            },
            'greetings': {
                'bawo': ['hello'],
                'se daadaa ni': ['how are you'],
                'kaabo': ['welcome'],
                'e se': ['thank you'],
                'ma binu': ['sorry'],
                'o dabo': ['goodbye'],
                'a o ri e laipe': ['see you later']
            }
        },
        
        # Igbo (West Africa)
        'ig': {
            'products': {
                'shuga': ['sugar'],
                'osikapa': ['rice'],
                'oka': ['maize', 'corn'],
                'anu': ['meat'],
                'azu': ['fish'],
                'mmiri ara ehi': ['milk'],
                'achicha': ['bread'],
                'tii': ['tea'],
                'kọfị': ['coffee'],
                'mmanụ': ['oil'],
                'nnu': ['salt'],
                'yabasị': ['onions'],
                'tomato': ['tomatoes']
            },
            'quantities': {
                'akpa': ['packet', 'package'],
                'kilo': ['kilogram'],
                'lita': ['liter'],
                'akpa': ['bag'],
                'igbe': ['box'],
                'karama': ['bottle'],
                'mkpọ': ['tin'],
                'nha': ['measure'],
                'ụyọkọ': ['bunch'],
                'iri na abụọ': ['dozen']
            },
            'actions': {
                'ree': ['sell'],
                'zụta': ['buy'],
                'kwụọ': ['pay'],
                'weghachi': ['return'],
                'nata': ['receive'],
                'bufee': ['deliver'],
                'lee': ['check'],
                'gụọ': ['count'],
                'tụọ': ['measure'],
                'mechie': ['close']
            },
            'money': {
                'ego': ['money'],
                'naira': ['naira'],
                'ọnụ ahịa': ['price'],
                'ego': ['cost'],
                'uru': ['profit'],
                'mfu': ['loss'],
                'mbelata': ['discount'],
                'gbakwunye': ['increase'],
                'belata': ['decrease']
            },
            'greetings': {
                'ndewo': ['hello'],
                'kedu': ['how are you'],
                'nnọọ': ['welcome'],
                'daalụ': ['thank you'],
                'ndo': ['sorry'],
                'ka ọ dị': ['goodbye'],
                'ka anyị hụrụ': ['see you later']
            }
        },
        
        # Hausa (West/North Africa)
        'ha': {
            'products': {
                'sukari': ['sugar'],
                'shinkafa': ['rice'],
                'masara': ['maize', 'corn'],
                'nama': ['meat'],
                'kifi': ['fish'],
                'madara': ['milk'],
                'gurasa': ['bread'],
                'shayi': ['tea'],
                'kofi': ['coffee'],
                'mai': ['oil'],
                'gishiri': ['salt'],
                'albasa': ['onions'],
                'tumatir': ['tomatoes']
            },
            'quantities': {
                'fakiti': ['packet', 'package'],
                'kilo': ['kilogram'],
                'lita': ['liter'],
                'buhun': ['bag'],
                'akwati': ['box'],
                'kwalba': ['bottle'],
                'gwangwani': ['tin'],
                'ma'auni': ['measure'],
                'dambe': ['bunch'],
                'goma sha biyu': ['dozen']
            },
            'actions': {
                'sayar': ['sell'],
                'saya': ['buy'],
                'biya': ['pay'],
                'mayar': ['return'],
                'karba': ['receive'],
                'kai': ['deliver'],
                'duba': ['check'],
                'kirga': ['count'],
                'auna': ['measure'],
                'rufe': ['close']
            },
            'money': {
                'kuɗi': ['money'],
                'naira': ['naira'],
                'farashi': ['price'],
                'kuɗi': ['cost'],
                'riba': ['profit'],
                'hasara': ['loss'],
                'rangwame': ['discount'],
                'ƙara': ['increase'],
                'rage': ['decrease']
            },
            'greetings': {
                'sannu': ['hello'],
                'yaya kake': ['how are you'],
                'maraba': ['welcome'],
                'na gode': ['thank you'],
                'yi hakuri': ['sorry'],
                'sai an jima': ['goodbye'],
                'sai mu hadu': ['see you later']
            }
        }
    }
    
    # Cultural expressions and idioms
    CULTURAL_EXPRESSIONS = {
        'sw': {
            'respect': ['bwana', 'mama', 'mzee', 'dada', 'kaka'],
            'politeness': ['tafadhali', 'asante sana', 'pole sana', 'samahani'],
            'business_courtesy': ['karibu sana', 'umekaribishwa', 'tutakuongoza'],
            'ubuntu_expressions': ['pamoja', 'umoja', 'harambee', 'ujamaa']
        },
        'zu': {
            'respect': ['baba', 'mama', 'gogo', 'mkhulu', 'sisi'],
            'politeness': ['ngicela', 'ngiyabonga kakhulu', 'ngiyaxolisa'],
            'business_courtesy': ['wamukelekile kakhulu', 'sizokusiza'],
            'ubuntu_expressions': ['ubuntu', 'simunye', 'sawubona']
        },
        'yo': {
            'respect': ['baba', 'mama', 'egbon', 'aburo', 'iya'],
            'politeness': ['jọwọ', 'e se pupo', 'ma binu'],
            'business_courtesy': ['kaabo si ile wa', 'a o ran yin lowo'],
            'ubuntu_expressions': ['omoluwabi', 'iwa', 'eniyan']
        },
        'ig': {
            'respect': ['nna', 'nne', 'nna ochie', 'nne ochie', 'nwanne'],
            'politeness': ['biko', 'daalụ nke ukwuu', 'ndo'],
            'business_courtesy': ['nnọọ nke ukwuu', 'anyị ga-enyere gị aka'],
            'ubuntu_expressions': ['igwebuike', 'omenala', 'mmadụ']
        },
        'ha': {
            'respect': ['baba', 'mama', 'kaka', 'yaya', 'dan uwa'],
            'politeness': ['don Allah', 'na gode sosai', 'yi hakuri'],
            'business_courtesy': ['maraba da zuwa', 'za mu taimake ku'],
            'ubuntu_expressions': ['jama\'a', 'haɗin kai', 'mutunci']
        }
    }

class BusinessEntityExtractor:
    """Extract business entities from African language text"""
    
    def __init__(self):
        self.vocabulary = AfricanBusinessVocabulary.BUSINESS_VOCABULARY
        self.cultural_expressions = AfricanBusinessVocabulary.CULTURAL_EXPRESSIONS
        
        # Compile regex patterns for common entities
        self.number_patterns = {
            'sw': r'\b(moja|mbili|tatu|nne|tano|sita|saba|nane|tisa|kumi|\d+)\b',
            'zu': r'\b(kunye|kubili|kuthathu|kune|kuhlanu|isithupha|isikhombisa|isishiyagalombili|isishiyagalolunye|ishumi|\d+)\b',
            'yo': r'\b(ọkan|meji|mẹta|mẹrin|marun|mẹfa|meje|mẹjọ|mẹsan|mẹwa|\d+)\b',
            'ig': r'\b(otu|abụọ|atọ|anọ|ise|isii|asaa|asatọ|itoolu|iri|\d+)\b',
            'ha': r'\b(ɗaya|biyu|uku|huɗu|biyar|shida|bakwai|takwas|tara|goma|\d+)\b'
        }
        
        self.currency_patterns = {
            'sw': r'\b(shilingi|dola|pesa)\b',
            'zu': r'\b(randi|dola|imali)\b',
            'yo': r'\b(naira|dola|owo)\b',
            'ig': r'\b(naira|dola|ego)\b',
            'ha': r'\b(naira|dola|kuɗi)\b'
        }
    
    def extract_entities(self, text: str, language: str) -> List[Entity]:
        """Extract entities from text"""
        entities = []
        text_lower = text.lower()
        
        # Get vocabulary for the language
        lang_vocab = self.vocabulary.get(language, {})
        
        # Extract products
        entities.extend(self._extract_products(text_lower, language, lang_vocab))
        
        # Extract quantities
        entities.extend(self._extract_quantities(text_lower, language, lang_vocab))
        
        # Extract actions
        entities.extend(self._extract_actions(text_lower, language, lang_vocab))
        
        # Extract money-related entities
        entities.extend(self._extract_money_entities(text_lower, language, lang_vocab))
        
        # Extract numbers
        entities.extend(self._extract_numbers(text_lower, language))
        
        # Extract cultural expressions
        entities.extend(self._extract_cultural_expressions(text_lower, language))
        
        return entities
    
    def _extract_products(self, text: str, language: str, vocab: Dict) -> List[Entity]:
        """Extract product entities"""
        entities = []
        products = vocab.get('products', {})
        
        for product_key, product_names in products.items():
            for name in [product_key] + product_names:
                if name.lower() in text:
                    start_pos = text.find(name.lower())
                    entities.append(Entity(
                        text=name,
                        entity_type=EntityType.PRODUCT,
                        value=product_key,
                        confidence=0.9,
                        start_pos=start_pos,
                        end_pos=start_pos + len(name),
                        language=language,
                        metadata={'category': 'product', 'normalized': product_key}
                    ))
        
        return entities
    
    def _extract_quantities(self, text: str, language: str, vocab: Dict) -> List[Entity]:
        """Extract quantity entities"""
        entities = []
        quantities = vocab.get('quantities', {})
        
        for quantity_key, quantity_names in quantities.items():
            for name in [quantity_key] + quantity_names:
                if name.lower() in text:
                    start_pos = text.find(name.lower())
                    entities.append(Entity(
                        text=name,
                        entity_type=EntityType.QUANTITY,
                        value=quantity_key,
                        confidence=0.8,
                        start_pos=start_pos,
                        end_pos=start_pos + len(name),
                        language=language,
                        metadata={'category': 'quantity', 'normalized': quantity_key}
                    ))
        
        return entities
    
    def _extract_actions(self, text: str, language: str, vocab: Dict) -> List[Entity]:
        """Extract action entities"""
        entities = []
        actions = vocab.get('actions', {})
        
        for action_key, action_names in actions.items():
            for name in [action_key] + action_names:
                if name.lower() in text:
                    start_pos = text.find(name.lower())
                    entities.append(Entity(
                        text=name,
                        entity_type=EntityType.PRODUCT,  # Using PRODUCT as general entity
                        value=action_key,
                        confidence=0.9,
                        start_pos=start_pos,
                        end_pos=start_pos + len(name),
                        language=language,
                        metadata={'category': 'action', 'normalized': action_key}
                    ))
        
        return entities
    
    def _extract_money_entities(self, text: str, language: str, vocab: Dict) -> List[Entity]:
        """Extract money-related entities"""
        entities = []
        money_terms = vocab.get('money', {})
        
        for money_key, money_names in money_terms.items():
            for name in [money_key] + money_names:
                if name.lower() in text:
                    start_pos = text.find(name.lower())
                    entities.append(Entity(
                        text=name,
                        entity_type=EntityType.CURRENCY if 'currency' in money_key else EntityType.PRICE,
                        value=money_key,
                        confidence=0.8,
                        start_pos=start_pos,
                        end_pos=start_pos + len(name),
                        language=language,
                        metadata={'category': 'money', 'normalized': money_key}
                    ))
        
        return entities
    
    def _extract_numbers(self, text: str, language: str) -> List[Entity]:
        """Extract number entities"""
        entities = []
        pattern = self.number_patterns.get(language, r'\d+')
        
        import re
        matches = re.finditer(pattern, text)
        for match in matches:
            entities.append(Entity(
                text=match.group(),
                entity_type=EntityType.QUANTITY,
                value=match.group(),
                confidence=0.9,
                start_pos=match.start(),
                end_pos=match.end(),
                language=language,
                metadata={'category': 'number'}
            ))
        
        return entities
    
    def _extract_cultural_expressions(self, text: str, language: str) -> List[Entity]:
        """Extract cultural expressions"""
        entities = []
        expressions = self.cultural_expressions.get(language, {})
        
        for category, terms in expressions.items():
            for term in terms:
                if term.lower() in text:
                    start_pos = text.find(term.lower())
                    entities.append(Entity(
                        text=term,
                        entity_type=EntityType.PERSON,  # Using PERSON for cultural expressions
                        value=term,
                        confidence=0.7,
                        start_pos=start_pos,
                        end_pos=start_pos + len(term),
                        language=language,
                        cultural_context=CulturalContext.RESPECTFUL if category == 'respect' else CulturalContext.POLITE,
                        metadata={'category': 'cultural', 'type': category}
                    ))
        
        return entities

class BusinessIntentClassifier:
    """Classify business intents from African language text"""
    
    def __init__(self):
        self.entity_extractor = BusinessEntityExtractor()
        self.intent_patterns = self._build_intent_patterns()
    
    def _build_intent_patterns(self) -> Dict[BusinessIntent, Dict[str, List[str]]]:
        """Build intent classification patterns"""
        return {
            BusinessIntent.SELL: {
                'sw': ['uza', 'kuuza', 'nataka kuuza', 'nina', 'ninacho'],
                'zu': ['thengisa', 'ukuthengisa', 'ngifuna ukuthengisa', 'nginako'],
                'yo': ['ta', 'mo fẹ ta', 'mo ni'],
                'ig': ['ree', 'ere', 'achọrọ m ire', 'enwere m'],
                'ha': ['sayar', 'ina son sayar', 'ina da']
            },
            BusinessIntent.BUY: {
                'sw': ['nunua', 'kununua', 'nataka kununua', 'nahitaji'],
                'zu': ['thenga', 'ukuthenga', 'ngifuna ukuthenga', 'ngidinga'],
                'yo': ['ra', 'mo fẹ ra', 'mo nilo'],
                'ig': ['zụta', 'zụọ', 'achọrọ m ịzụta', 'achọrọ m'],
                'ha': ['saya', 'siyan', 'ina son saya', 'ina bukata']
            },
            BusinessIntent.PRICE_INQUIRY: {
                'sw': ['bei', 'gharama', 'bei gani', 'ni kiasi gani'],
                'zu': ['intengo', 'malini', 'yimalini'],
                'yo': ['elo ni', 'owo', 'elo lo'],
                'ig': ['ego ole', 'ọnụ ahịa ole', 'ego ole ka ọ'],
                'ha': ['nawa ne', 'farashi nawa', 'kuɗi nawa']
            },
            BusinessIntent.GREETING: {
                'sw': ['hujambo', 'habari', 'mambo', 'vipi'],
                'zu': ['sawubona', 'sanibonani', 'unjani'],
                'yo': ['bawo', 'se daadaa ni', 'ẹ ku aaro'],
                'ig': ['ndewo', 'kedu', 'kedu ka ị mere'],
                'ha': ['sannu', 'yaya kake', 'ina kwana']
            },
            BusinessIntent.GOODBYE: {
                'sw': ['kwaheri', 'tutaonana', 'baadaye'],
                'zu': ['sala kahle', 'sizobonana', 'ngiyahamba'],
                'yo': ['o dabo', 'a o ri e laipe', 'mo n lo'],
                'ig': ['ka ọ dị', 'ka anyị hụrụ', 'ana m aga'],
                'ha': ['sai an jima', 'sai mu hadu', 'zan tafi']
            },
            BusinessIntent.HELP: {
                'sw': ['msaada', 'nisaidie', 'unaweza kunisaidia'],
                'zu': ['usizo', 'ngisiza', 'ungangisiza'],
                'yo': ['iranlowo', 'ran mi lowo', 'se o le ran mi lowo'],
                'ig': ['enyemaka', 'nyere m aka', 'ị nwere ike inyere m aka'],
                'ha': ['taimako', 'ka taimake ni', 'za ka iya taimaka']
            }
        }
    
    def classify_intent(self, text: str, language: str, entities: List[Entity]) -> Intent:
        """Classify business intent from text and entities"""
        text_lower = text.lower()
        
        # Score each intent
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            lang_patterns = patterns.get(language, [])
            
            # Check for pattern matches
            for pattern in lang_patterns:
                if pattern in text_lower:
                    score += 10
            
            # Boost score based on entities
            for entity in entities:
                if intent == BusinessIntent.SELL and entity.metadata.get('category') == 'action' and 'sell' in str(entity.value):
                    score += 15
                elif intent == BusinessIntent.BUY and entity.metadata.get('category') == 'action' and 'buy' in str(entity.value):
                    score += 15
                elif intent == BusinessIntent.PRICE_INQUIRY and entity.entity_type == EntityType.PRICE:
                    score += 10
                elif entity.metadata.get('category') == 'product':
                    score += 5
            
            intent_scores[intent] = score
        
        # Find best intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(1.0, intent_scores[best_intent] / 20.0)
            
            if confidence < 0.3:
                best_intent = BusinessIntent.UNKNOWN
                confidence = 0.1
        else:
            best_intent = BusinessIntent.UNKNOWN
            confidence = 0.1
        
        # Determine cultural context
        cultural_context = self._determine_cultural_context(text, language, entities)
        
        return Intent(
            intent=best_intent,
            confidence=confidence,
            entities=entities,
            language=language,
            cultural_context=cultural_context,
            metadata={
                'intent_scores': intent_scores,
                'pattern_matches': self._get_pattern_matches(text_lower, language)
            }
        )
    
    def _determine_cultural_context(self, text: str, language: str, entities: List[Entity]) -> CulturalContext:
        """Determine cultural context from text and entities"""
        text_lower = text.lower()
        
        # Check for respectful terms
        cultural_entities = [e for e in entities if e.metadata.get('category') == 'cultural']
        
        for entity in cultural_entities:
            if entity.metadata.get('type') == 'respect':
                return CulturalContext.RESPECTFUL
            elif entity.metadata.get('type') == 'politeness':
                return CulturalContext.POLITE
            elif entity.metadata.get('type') == 'ubuntu_expressions':
                return CulturalContext.COMMUNITY_ORIENTED
        
        # Check for formal/informal indicators
        formal_indicators = ['tafadhali', 'ngicela', 'jọwọ', 'biko', 'don allah']
        informal_indicators = ['vipi', 'mambo', 'bawo', 'kedu', 'yaya']
        
        for indicator in formal_indicators:
            if indicator in text_lower:
                return CulturalContext.FORMAL
        
        for indicator in informal_indicators:
            if indicator in text_lower:
                return CulturalContext.INFORMAL
        
        return CulturalContext.POLITE  # Default
    
    def _get_pattern_matches(self, text: str, language: str) -> List[str]:
        """Get all pattern matches for debugging"""
        matches = []
        
        for intent, patterns in self.intent_patterns.items():
            lang_patterns = patterns.get(language, [])
            for pattern in lang_patterns:
                if pattern in text:
                    matches.append(f"{intent.value}: {pattern}")
        
        return matches

class SentimentAnalyzer:
    """Analyze sentiment in African business contexts"""
    
    def __init__(self):
        self.sentiment_lexicon = self._build_sentiment_lexicon()
    
    def _build_sentiment_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Build sentiment lexicon for African languages"""
        return {
            'sw': {
                # Positive
                'asante': 0.8, 'nzuri': 0.7, 'vizuri': 0.7, 'poa': 0.6,
                'furaha': 0.8, 'raha': 0.7, 'karibu': 0.6, 'hongera': 0.9,
                # Negative
                'mbaya': -0.7, 'vibaya': -0.7, 'hasira': -0.8, 'uchungu': -0.6,
                'pole': -0.3, 'huzuni': -0.7, 'tatizo': -0.5,
                # Neutral
                'sawa': 0.1, 'haya': 0.0, 'tu': 0.0
            },
            'zu': {
                # Positive
                'ngiyabonga': 0.8, 'kuhle': 0.7, 'mnandi': 0.7, 'jabulisa': 0.8,
                'wamukelekile': 0.6, 'hongera': 0.9,
                # Negative
                'kubi': -0.7, 'buhlungu': -0.6, 'ngiyaxolisa': -0.3, 'inkinga': -0.5,
                # Neutral
                'kulungile': 0.1, 'yebo': 0.0
            },
            'yo': {
                # Positive
                'e se': 0.8, 'dara': 0.7, 'o dun': 0.7, 'ayo': 0.8,
                'kaabo': 0.6, 'oriire': 0.9,
                # Negative
                'buru': -0.7, 'ibanuje': -0.6, 'ma binu': -0.3, 'wahala': -0.5,
                # Neutral
                'o dara': 0.1, 'beeni': 0.0
            },
            'ig': {
                # Positive
                'daalụ': 0.8, 'ọma': 0.7, 'mma': 0.7, 'ọṅụ': 0.8,
                'nnọọ': 0.6, 'ngọzi': 0.9,
                # Negative
                'ọjọọ': -0.7, 'iwe': -0.8, 'ndo': -0.3, 'nsogbu': -0.5,
                # Neutral
                'ọ dị mma': 0.1, 'ee': 0.0
            },
            'ha': {
                # Positive
                'na gode': 0.8, 'mai kyau': 0.7, 'dadi': 0.7, 'farin ciki': 0.8,
                'maraba': 0.6, 'albarka': 0.9,
                # Negative
                'mummuna': -0.7, 'bacin rai': -0.6, 'yi hakuri': -0.3, 'matsala': -0.5,
                # Neutral
                'to': 0.1, 'i': 0.0
            }
        }
    
    def analyze_sentiment(self, text: str, language: str) -> Dict[str, float]:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        lexicon = self.sentiment_lexicon.get(language, {})
        
        scores = []
        matched_words = []
        
        for word, score in lexicon.items():
            if word in text_lower:
                scores.append(score)
                matched_words.append(word)
        
        if scores:
            avg_score = sum(scores) / len(scores)
            
            # Classify sentiment
            if avg_score > 0.2:
                sentiment = 'positive'
            elif avg_score < -0.2:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            confidence = min(1.0, abs(avg_score))
        else:
            sentiment = 'neutral'
            avg_score = 0.0
            confidence = 0.1
        
        return {
            'sentiment': sentiment,
            'score': avg_score,
            'confidence': confidence,
            'matched_words': matched_words
        }

class CulturalAnalyzer:
    """Analyze cultural context and appropriateness"""
    
    def __init__(self):
        self.cultural_patterns = self._build_cultural_patterns()
    
    def _build_cultural_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Build cultural analysis patterns"""
        return {
            'ubuntu_philosophy': {
                'sw': ['pamoja', 'umoja', 'harambee', 'ujamaa', 'uongozi'],
                'zu': ['ubuntu', 'simunye', 'sawubona'],
                'yo': ['omoluwabi', 'iwa', 'eniyan'],
                'ig': ['igwebuike', 'omenala', 'mmadụ'],
                'ha': ['jama\'a', 'haɗin kai', 'mutunci']
            },
            'respect_hierarchy': {
                'sw': ['mzee', 'bwana', 'mama', 'dada', 'kaka'],
                'zu': ['baba', 'mama', 'gogo', 'mkhulu'],
                'yo': ['baba', 'mama', 'egbon', 'iya'],
                'ig': ['nna', 'nne', 'nna ochie', 'nne ochie'],
                'ha': ['baba', 'mama', 'kaka', 'yaya']
            },
            'business_etiquette': {
                'sw': ['karibu', 'asante', 'tafadhali', 'pole'],
                'zu': ['wamukelekile', 'ngiyabonga', 'ngicela'],
                'yo': ['kaabo', 'e se', 'jọwọ'],
                'ig': ['nnọọ', 'daalụ', 'biko'],
                'ha': ['maraba', 'na gode', 'don allah']
            }
        }
    
    def analyze_cultural_context(self, text: str, language: str, entities: List[Entity]) -> Dict[str, Any]:
        """Analyze cultural context of text"""
        text_lower = text.lower()
        analysis = {
            'ubuntu_score': 0.0,
            'respect_score': 0.0,
            'business_etiquette_score': 0.0,
            'cultural_appropriateness': 'appropriate',
            'recommendations': [],
            'detected_patterns': []
        }
        
        # Check Ubuntu philosophy
        ubuntu_terms = self.cultural_patterns['ubuntu_philosophy'].get(language, [])
        ubuntu_matches = [term for term in ubuntu_terms if term in text_lower]
        analysis['ubuntu_score'] = len(ubuntu_matches) / max(1, len(ubuntu_terms))
        
        # Check respect hierarchy
        respect_terms = self.cultural_patterns['respect_hierarchy'].get(language, [])
        respect_matches = [term for term in respect_terms if term in text_lower]
        analysis['respect_score'] = len(respect_matches) / max(1, len(respect_terms))
        
        # Check business etiquette
        etiquette_terms = self.cultural_patterns['business_etiquette'].get(language, [])
        etiquette_matches = [term for term in etiquette_terms if term in text_lower]
        analysis['business_etiquette_score'] = len(etiquette_matches) / max(1, len(etiquette_terms))
        
        # Overall cultural appropriateness
        total_score = (analysis['ubuntu_score'] + analysis['respect_score'] + analysis['business_etiquette_score']) / 3
        
        if total_score > 0.7:
            analysis['cultural_appropriateness'] = 'highly_appropriate'
        elif total_score > 0.4:
            analysis['cultural_appropriateness'] = 'appropriate'
        elif total_score > 0.2:
            analysis['cultural_appropriateness'] = 'somewhat_appropriate'
        else:
            analysis['cultural_appropriateness'] = 'needs_improvement'
        
        # Generate recommendations
        if analysis['respect_score'] < 0.3:
            analysis['recommendations'].append('Consider using more respectful terms')
        if analysis['business_etiquette_score'] < 0.3:
            analysis['recommendations'].append('Add polite business expressions')
        if analysis['ubuntu_score'] < 0.2:
            analysis['recommendations'].append('Consider community-oriented language')
        
        analysis['detected_patterns'] = ubuntu_matches + respect_matches + etiquette_matches
        
        return analysis

class NLUEngine:
    """Main Natural Language Understanding engine"""
    
    def __init__(self):
        self.entity_extractor = BusinessEntityExtractor()
        self.intent_classifier = BusinessIntentClassifier()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.cultural_analyzer = CulturalAnalyzer()
        self.performance_stats = {
            'total_requests': 0,
            'successful_analyses': 0,
            'average_processing_time': 0,
            'language_distribution': {},
            'intent_distribution': {}
        }
    
    async def analyze(self, text: str, language: str, context: Optional[Dict[str, Any]] = None) -> NLUResult:
        """Perform complete NLU analysis"""
        start_time = datetime.now()
        
        try:
            # Update stats
            self.performance_stats['total_requests'] += 1
            
            # Extract entities
            entities = self.entity_extractor.extract_entities(text, language)
            
            # Classify intent
            intent = self.intent_classifier.classify_intent(text, language, entities)
            
            # Analyze sentiment
            sentiment = self.sentiment_analyzer.analyze_sentiment(text, language)
            
            # Analyze cultural context
            cultural_analysis = self.cultural_analyzer.analyze_cultural_context(text, language, entities)
            
            # Build business context
            business_context = self._build_business_context(intent, entities, context)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Calculate overall confidence
            confidence = (intent.confidence + sentiment['confidence'] + 
                         (cultural_analysis.get('ubuntu_score', 0) + 
                          cultural_analysis.get('respect_score', 0) + 
                          cultural_analysis.get('business_etiquette_score', 0)) / 3) / 3
            
            # Update performance stats
            self.performance_stats['successful_analyses'] += 1
            self._update_stats(processing_time, language, intent.intent)
            
            # Create result
            result = NLUResult(
                text=text,
                language=language,
                intent=intent,
                entities=entities,
                sentiment=sentiment,
                cultural_analysis=cultural_analysis,
                business_context=business_context,
                processing_time=processing_time,
                confidence=confidence,
                metadata={
                    'timestamp': start_time.isoformat(),
                    'context': context,
                    'entity_count': len(entities),
                    'cultural_appropriateness': cultural_analysis.get('cultural_appropriateness')
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"NLU analysis failed: {e}")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            return NLUResult(
                text=text,
                language=language,
                intent=Intent(
                    intent=BusinessIntent.UNKNOWN,
                    confidence=0.0,
                    entities=[],
                    language=language,
                    cultural_context=CulturalContext.POLITE
                ),
                entities=[],
                sentiment={'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.0},
                cultural_analysis={'cultural_appropriateness': 'unknown'},
                business_context={},
                processing_time=processing_time,
                confidence=0.0,
                metadata={'error': str(e)}
            )
    
    def _build_business_context(self, intent: Intent, entities: List[Entity], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Build business context from intent and entities"""
        business_context = {
            'transaction_type': None,
            'products': [],
            'quantities': [],
            'prices': [],
            'customer_info': {},
            'workflow_stage': 'initial',
            'next_actions': []
        }
        
        # Determine transaction type
        if intent.intent == BusinessIntent.SELL:
            business_context['transaction_type'] = 'sale'
            business_context['next_actions'] = ['confirm_product', 'check_inventory', 'calculate_price']
        elif intent.intent == BusinessIntent.BUY:
            business_context['transaction_type'] = 'purchase'
            business_context['next_actions'] = ['confirm_product', 'check_availability', 'provide_price']
        elif intent.intent == BusinessIntent.PRICE_INQUIRY:
            business_context['transaction_type'] = 'inquiry'
            business_context['next_actions'] = ['provide_price', 'suggest_alternatives']
        
        # Extract business entities
        for entity in entities:
            if entity.entity_type == EntityType.PRODUCT:
                business_context['products'].append({
                    'name': entity.value,
                    'text': entity.text,
                    'confidence': entity.confidence
                })
            elif entity.entity_type == EntityType.QUANTITY:
                business_context['quantities'].append({
                    'value': entity.value,
                    'text': entity.text,
                    'confidence': entity.confidence
                })
            elif entity.entity_type == EntityType.PRICE:
                business_context['prices'].append({
                    'value': entity.value,
                    'text': entity.text,
                    'confidence': entity.confidence
                })
        
        # Add context information
        if context:
            business_context['customer_info'] = context.get('customer', {})
            business_context['session_info'] = context.get('session', {})
        
        return business_context
    
    def _update_stats(self, processing_time: float, language: str, intent: BusinessIntent):
        """Update performance statistics"""
        # Update average processing time
        current_avg = self.performance_stats['average_processing_time']
        total_requests = self.performance_stats['total_requests']
        new_avg = ((current_avg * (total_requests - 1)) + processing_time) / total_requests
        self.performance_stats['average_processing_time'] = new_avg
        
        # Update language distribution
        if language not in self.performance_stats['language_distribution']:
            self.performance_stats['language_distribution'][language] = 0
        self.performance_stats['language_distribution'][language] += 1
        
        # Update intent distribution
        intent_name = intent.value
        if intent_name not in self.performance_stats['intent_distribution']:
            self.performance_stats['intent_distribution'][intent_name] = 0
        self.performance_stats['intent_distribution'][intent_name] += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            **self.performance_stats,
            'success_rate': (
                self.performance_stats['successful_analyses'] / 
                max(1, self.performance_stats['total_requests'])
            ) * 100,
            'supported_languages': len(AfricanBusinessVocabulary.BUSINESS_VOCABULARY),
            'supported_intents': len(BusinessIntent)
        }

# Global NLU engine instance
nlu_engine = NLUEngine()

