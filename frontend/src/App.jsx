import React, { useState, useEffect } from 'react';
import MobileOptimizedLayout from './components/MobileOptimizedLayout';
import SystemDashboard from './components/SystemDashboard';
import VoiceInterface from './components/VoiceInterface';
import './App.css';

function App() {
  const [currentSystem, setCurrentSystem] = useState('dashboard');
  const [user, setUser] = useState({
    name: 'John Doe',
    role: 'Business Owner',
    region: 'West Africa',
    language: 'en',
    company: 'Sample Business Ltd'
  });
  const [culturalContext, setCulturalContext] = useState({
    region: 'west_africa',
    language: 'en',
    currency: 'GHS',
    timezone: 'GMT',
    business_practices: {
      extended_family_considerations: true,
      community_oriented: true,
      cash_preferred: true,
      mobile_money_primary: true
    }
  });
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [systemData, setSystemData] = useState({});

  // Monitor online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Load system data
  useEffect(() => {
    loadSystemData(currentSystem);
  }, [currentSystem]);

  const loadSystemData = async (system) => {
    try {
      // Simulate API call to backend
      const response = await fetch(`/api/${system}/dashboard`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': user.company,
          'X-User-Language': culturalContext.language
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSystemData(prev => ({
          ...prev,
          [system]: data
        }));
      } else {
        // Fallback to sample data if API not available
        console.log(`API not available for ${system}, using sample data`);
      }
    } catch (error) {
      console.log(`Error loading ${system} data:`, error);
      // Use offline data or sample data
    }
  };

  const handleSystemChange = (systemId) => {
    setCurrentSystem(systemId);
    
    // Update URL without page refresh
    if (window.history.pushState) {
      window.history.pushState(null, null, `#${systemId}`);
    }
  };

  const handleVoiceCommand = async (commandData) => {
    const { command, language, system, confidence } = commandData;
    
    try {
      // Send voice command to backend for processing
      const response = await fetch('/api/voice/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': user.company,
          'X-User-ID': user.id || 'guest'
        },
        body: JSON.stringify({
          command,
          language,
          system: currentSystem,
          confidence,
          cultural_context: culturalContext
        })
      });

      if (response.ok) {
        const result = await response.json();
        
        // Handle system switching commands
        if (result.action === 'switch_system' && result.target_system) {
          handleSystemChange(result.target_system);
        }
        
        // Handle data updates
        if (result.data_updates) {
          setSystemData(prev => ({
            ...prev,
            [currentSystem]: {
              ...prev[currentSystem],
              ...result.data_updates
            }
          }));
        }
        
        return {
          success: true,
          response: result.response || 'Command processed successfully',
          action: result.action
        };
      } else {
        throw new Error('Voice command processing failed');
      }
    } catch (error) {
      console.error('Voice command error:', error);
      
      // Fallback local processing
      return handleLocalVoiceCommand(commandData);
    }
  };

  const handleLocalVoiceCommand = (commandData) => {
    const { command, language } = commandData;
    const commandLower = command.toLowerCase();
    
    // Basic local command processing
    if (commandLower.includes('dashboard') || commandLower.includes('home')) {
      handleSystemChange('dashboard');
      return { success: true, response: 'Switched to dashboard' };
    }
    
    if (commandLower.includes('sales') || commandLower.includes('pos')) {
      handleSystemChange('pos');
      return { success: true, response: 'Switched to point of sale' };
    }
    
    if (commandLower.includes('inventory') || commandLower.includes('stock')) {
      handleSystemChange('inventory');
      return { success: true, response: 'Switched to inventory management' };
    }
    
    if (commandLower.includes('customer') || commandLower.includes('crm')) {
      handleSystemChange('crm');
      return { success: true, response: 'Switched to customer management' };
    }
    
    if (commandLower.includes('employee') || commandLower.includes('hr')) {
      handleSystemChange('hr');
      return { success: true, response: 'Switched to human resources' };
    }
    
    if (commandLower.includes('money') || commandLower.includes('finance')) {
      handleSystemChange('financial');
      return { success: true, response: 'Switched to financial management' };
    }
    
    return { 
      success: false, 
      response: language === 'sw' ? 'Samahani, sikuelewa amri hiyo' : 'Sorry, I did not understand that command' 
    };
  };

  const getSystemTitle = () => {
    const systemTitles = {
      dashboard: 'Business Dashboard',
      pos: 'Point of Sale',
      inventory: 'Inventory Management',
      crm: 'Customer Relations',
      hr: 'Human Resources',
      financial: 'Financial Management',
      supply_chain: 'Supply Chain',
      project: 'Project Management',
      document: 'Document Management',
      asset: 'Asset Management',
      quality: 'Quality Management',
      healthcare: 'Healthcare Management',
      education: 'Education Management',
      agriculture: 'Agriculture Management',
      restaurant: 'Restaurant Management',
      hotel: 'Hotel Management',
      transport: 'Transport Management',
      manufacturing: 'Manufacturing',
      retail: 'Retail Management',
      service: 'Service Management',
      event: 'Event Management'
    };
    
    return systemTitles[currentSystem] || 'WebWaka Digital OS';
  };

  return (
    <div className="App">
      <MobileOptimizedLayout
        title={getSystemTitle()}
        currentSystem={currentSystem}
        onSystemChange={handleSystemChange}
        user={user}
        culturalTheme={culturalContext.region}
        showVoiceInterface={true}
      >
        {/* Desktop Voice Interface */}
        <div className="hidden lg:block fixed top-20 right-4 z-30">
          <VoiceInterface
            onVoiceCommand={handleVoiceCommand}
            currentSystem={currentSystem}
            culturalContext={culturalContext}
            supportedLanguages={['en', 'sw', 'ha', 'yo', 'ig', 'am', 'fr', 'ar']}
          />
        </div>

        {/* Main Content */}
        <SystemDashboard
          currentSystem={currentSystem}
          onSystemChange={handleSystemChange}
          culturalContext={culturalContext}
          user={user}
          systemData={systemData[currentSystem]}
        />

        {/* Offline Banner */}
        {!isOnline && (
          <div className="fixed bottom-24 left-4 right-4 bg-orange-500 text-white px-4 py-3 rounded-lg shadow-lg z-50">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                <span className="font-medium">You're offline</span>
              </div>
              <span className="text-sm">
                Some features may be limited
              </span>
            </div>
          </div>
        )}

        {/* Cultural Context Indicator */}
        {culturalContext.region !== 'default' && (
          <div className="fixed top-20 left-4 bg-purple-100 text-purple-800 px-3 py-2 rounded-lg shadow-sm z-40 hidden lg:block">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
              <span className="text-sm font-medium">
                {culturalContext.region.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())} Context
              </span>
            </div>
          </div>
        )}

        {/* Loading Overlay */}
        {Object.keys(systemData).length === 0 && (
          <div className="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600 font-medium">Loading WebWaka Digital OS...</p>
              <p className="text-gray-400 text-sm mt-2">Initializing all management systems</p>
            </div>
          </div>
        )}
      </MobileOptimizedLayout>
    </div>
  );
}

export default App;

