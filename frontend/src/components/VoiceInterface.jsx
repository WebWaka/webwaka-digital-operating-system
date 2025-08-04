import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, VolumeX, Settings, Languages } from 'lucide-react';

const VoiceInterface = ({ 
  onVoiceCommand, 
  supportedLanguages = ['en', 'sw', 'ha', 'yo', 'ig', 'am', 'fr', 'ar'],
  currentSystem = 'general',
  culturalContext = {},
  isEnabled = true 
}) => {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [transcript, setTranscript] = useState('');
  const [lastCommand, setLastCommand] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  
  const recognitionRef = useRef(null);
  const synthRef = useRef(null);
  
  // Language configurations with African cultural context
  const languageConfig = {
    'en': { 
      name: 'English', 
      greeting: 'Hello! How can I help you today?',
      commands: [
        'Say "help" for available commands',
        'Say "switch to [language]" to change language'
      ]
    },
    'sw': { 
      name: 'Kiswahili', 
      greeting: 'Hujambo! Ninaweza kukusaidiaje leo?',
      commands: [
        'Sema "msaada" kupata amri zinazopatikana',
        'Sema "badili kwenda [lugha]" kubadili lugha'
      ]
    },
    'ha': { 
      name: 'Hausa', 
      greeting: 'Sannu! Yaya zan iya taimaka muku yau?',
      commands: [
        'Ku ce "taimako" don samun umarni da ake samu',
        'Ku ce "canza zuwa [harshe]" don canza harshe'
      ]
    },
    'yo': { 
      name: 'Yoruba', 
      greeting: 'Bawo! Bawo ni mo se le ran yin lowo loni?',
      commands: [
        'So "iranlowo" fun awon ase to wa',
        'So "yi pada si [ede]" lati yi ede pada'
      ]
    },
    'ig': { 
      name: 'Igbo', 
      greeting: 'Ndewo! Kedu ka m ga-esi nyere gi aka taa?',
      commands: [
        'Kwuo "enyemaka" maka iwu ndi di',
        'Kwuo "gbanwee gaa [asusu]" iji gbanwee asusu'
      ]
    },
    'am': { 
      name: 'አማርኛ', 
      greeting: 'ሰላም! ዛሬ እንዴት ልረዳዎት እችላለሁ?',
      commands: [
        'ለሚገኙ ትዕዛዞች "እርዳታ" ይበሉ',
        'ቋንቋ ለመቀየር "ወደ [ቋንቋ] ቀይር" ይበሉ'
      ]
    },
    'fr': { 
      name: 'Français', 
      greeting: 'Bonjour! Comment puis-je vous aider aujourd\'hui?',
      commands: [
        'Dites "aide" pour les commandes disponibles',
        'Dites "changer vers [langue]" pour changer de langue'
      ]
    },
    'ar': { 
      name: 'العربية', 
      greeting: 'السلام عليكم! كيف يمكنني مساعدتك اليوم؟',
      commands: [
        'قل "مساعدة" للأوامر المتاحة',
        'قل "تغيير إلى [لغة]" لتغيير اللغة'
      ]
    }
  };

  // System-specific voice commands
  const systemCommands = {
    'pos': {
      'en': [
        'Add [quantity] [item] to cart',
        'Remove [item] from cart',
        'Complete sale',
        'Check inventory for [item]'
      ],
      'sw': [
        'Ongeza [idadi] [bidhaa] kwenye mkoba',
        'Ondoa [bidhaa] kutoka mkoba',
        'Maliza mauzo',
        'Angalia hisa ya [bidhaa]'
      ]
    },
    'inventory': {
      'en': [
        'Check stock for [item]',
        'Add [quantity] [item] to inventory',
        'Create purchase order',
        'Show low stock items'
      ],
      'sw': [
        'Angalia hisa ya [bidhaa]',
        'Ongeza [idadi] [bidhaa] kwenye hisa',
        'Unda agizo la ununuzi',
        'Onyesha bidhaa za hisa ndogo'
      ]
    },
    'crm': {
      'en': [
        'Find customer [name]',
        'Create new customer',
        'Schedule follow-up with [name]',
        'Show customer analytics'
      ],
      'sw': [
        'Tafuta mteja [jina]',
        'Unda mteja mpya',
        'Panga ufuatiliaji na [jina]',
        'Onyesha uchambuzi wa wateja'
      ]
    },
    'hr': {
      'en': [
        'Find employee [name]',
        'Request [days] days leave',
        'Check leave balance',
        'Schedule performance review'
      ],
      'sw': [
        'Tafuta mfanyakazi [jina]',
        'Omba likizo ya siku [idadi]',
        'Angalia salio la likizo',
        'Panga tathmini ya utendaji'
      ]
    },
    'financial': {
      'en': [
        'Record expense of [amount]',
        'Record income of [amount]',
        'Check account balance',
        'Create invoice for [amount]'
      ],
      'sw': [
        'Rekodi gharama ya [kiasi]',
        'Rekodi mapato ya [kiasi]',
        'Angalia salio la akaunti',
        'Unda ankara ya [kiasi]'
      ]
    }
  };

  // Initialize speech recognition
  useEffect(() => {
    if (!isEnabled || !('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    
    const recognition = recognitionRef.current;
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = getLanguageCode(selectedLanguage);
    
    recognition.onstart = () => {
      setIsListening(true);
      setTranscript('');
    };
    
    recognition.onresult = (event) => {
      let finalTranscript = '';
      let interimTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        const confidence = event.results[i][0].confidence;
        
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
          setConfidence(confidence);
        } else {
          interimTranscript += transcript;
        }
      }
      
      setTranscript(finalTranscript || interimTranscript);
      
      if (finalTranscript) {
        handleVoiceCommand(finalTranscript, confidence);
      }
    };
    
    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      setIsProcessing(false);
    };
    
    recognition.onend = () => {
      setIsListening(false);
    };

    // Initialize speech synthesis
    synthRef.current = window.speechSynthesis;
    
    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, [selectedLanguage, isEnabled]);

  const getLanguageCode = (lang) => {
    const langCodes = {
      'en': 'en-US',
      'sw': 'sw-KE',
      'ha': 'ha-NG',
      'yo': 'yo-NG',
      'ig': 'ig-NG',
      'am': 'am-ET',
      'fr': 'fr-FR',
      'ar': 'ar-SA'
    };
    return langCodes[lang] || 'en-US';
  };

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.lang = getLanguageCode(selectedLanguage);
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const handleVoiceCommand = async (command, confidence) => {
    setIsProcessing(true);
    setLastCommand(command);
    
    try {
      // Process the voice command
      const result = await onVoiceCommand({
        command,
        language: selectedLanguage,
        system: currentSystem,
        confidence,
        culturalContext
      });
      
      // Provide voice feedback if enabled
      if (voiceEnabled && result.response) {
        speak(result.response);
      }
      
    } catch (error) {
      console.error('Voice command processing error:', error);
      const errorMessage = languageConfig[selectedLanguage]?.name === 'English' 
        ? 'Sorry, I could not process that command.'
        : 'Samahani, sikuweza kuchakata amri hiyo.'; // Swahili fallback
      
      if (voiceEnabled) {
        speak(errorMessage);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const speak = (text) => {
    if (synthRef.current && voiceEnabled) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = getLanguageCode(selectedLanguage);
      utterance.rate = 0.9;
      utterance.pitch = 1.0;
      
      // Try to find a voice for the selected language
      const voices = synthRef.current.getVoices();
      const voice = voices.find(v => v.lang.startsWith(selectedLanguage)) || 
                   voices.find(v => v.lang.startsWith('en'));
      
      if (voice) {
        utterance.voice = voice;
      }
      
      synthRef.current.speak(utterance);
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setSelectedLanguage(newLanguage);
    const greeting = languageConfig[newLanguage]?.greeting;
    if (greeting && voiceEnabled) {
      setTimeout(() => speak(greeting), 500);
    }
  };

  const getSystemCommands = () => {
    return systemCommands[currentSystem]?.[selectedLanguage] || 
           systemCommands[currentSystem]?.['en'] || 
           [];
  };

  if (!isEnabled) {
    return null;
  }

  return (
    <div className="voice-interface bg-white rounded-lg shadow-lg border border-gray-200 p-4 max-w-md mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isListening ? 'bg-red-500 animate-pulse' : isProcessing ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
          <span className="text-sm font-medium text-gray-700">
            {isListening ? 'Listening...' : isProcessing ? 'Processing...' : 'Ready'}
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setVoiceEnabled(!voiceEnabled)}
            className={`p-2 rounded-full ${voiceEnabled ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-400'}`}
            title={voiceEnabled ? 'Voice feedback enabled' : 'Voice feedback disabled'}
          >
            {voiceEnabled ? <Volume2 size={16} /> : <VolumeX size={16} />}
          </button>
          
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200"
            title="Settings"
          >
            <Settings size={16} />
          </button>
        </div>
      </div>

      {/* Language Selector */}
      {showSettings && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            <Languages size={16} className="text-gray-600" />
            <span className="text-sm font-medium text-gray-700">Language</span>
          </div>
          
          <select
            value={selectedLanguage}
            onChange={(e) => handleLanguageChange(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md text-sm"
          >
            {supportedLanguages.map(lang => (
              <option key={lang} value={lang}>
                {languageConfig[lang]?.name || lang.toUpperCase()}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Voice Control Button */}
      <div className="text-center mb-4">
        <button
          onClick={isListening ? stopListening : startListening}
          disabled={isProcessing}
          className={`w-16 h-16 rounded-full flex items-center justify-center transition-all duration-200 ${
            isListening 
              ? 'bg-red-500 hover:bg-red-600 text-white shadow-lg scale-110' 
              : isProcessing
              ? 'bg-yellow-500 text-white cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 text-white shadow-md hover:shadow-lg'
          }`}
        >
          {isListening ? <MicOff size={24} /> : <Mic size={24} />}
        </button>
        
        <p className="text-xs text-gray-500 mt-2">
          {isListening ? 'Tap to stop' : 'Tap to speak'}
        </p>
      </div>

      {/* Transcript Display */}
      {transcript && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <span className="font-medium">You said:</span> "{transcript}"
          </p>
          {confidence > 0 && (
            <p className="text-xs text-blue-600 mt-1">
              Confidence: {Math.round(confidence * 100)}%
            </p>
          )}
        </div>
      )}

      {/* Last Command */}
      {lastCommand && (
        <div className="mb-4 p-3 bg-green-50 rounded-lg">
          <p className="text-sm text-green-800">
            <span className="font-medium">Last command:</span> "{lastCommand}"
          </p>
        </div>
      )}

      {/* System Commands Help */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">
          {currentSystem.toUpperCase()} Commands:
        </h4>
        <div className="space-y-1">
          {getSystemCommands().slice(0, 3).map((command, index) => (
            <div key={index} className="text-xs text-gray-600 bg-gray-50 rounded px-2 py-1">
              "{command}"
            </div>
          ))}
        </div>
      </div>

      {/* Cultural Context Indicator */}
      {culturalContext.region && (
        <div className="text-xs text-gray-500 text-center">
          <span className="inline-flex items-center px-2 py-1 bg-purple-100 text-purple-700 rounded-full">
            {culturalContext.region} context enabled
          </span>
        </div>
      )}
    </div>
  );
};

export default VoiceInterface;

