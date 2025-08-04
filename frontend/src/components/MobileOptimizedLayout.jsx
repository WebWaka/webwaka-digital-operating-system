import React, { useState, useEffect } from 'react';
import { Menu, X, Wifi, WifiOff, Battery, Signal, Home, Settings, User, Bell } from 'lucide-react';

const MobileOptimizedLayout = ({ 
  children, 
  title = "WebWaka", 
  showVoiceInterface = true,
  currentSystem = "dashboard",
  user = null,
  onSystemChange = () => {},
  culturalTheme = "default"
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [networkSpeed, setNetworkSpeed] = useState('unknown');
  const [batteryLevel, setBatteryLevel] = useState(100);
  const [signalStrength, setSignalStrength] = useState(4);
  const [notifications, setNotifications] = useState([]);

  // Cultural themes for different African regions
  const culturalThemes = {
    default: {
      primary: '#2563eb',
      secondary: '#f59e0b',
      accent: '#10b981',
      background: '#f8fafc',
      text: '#1f2937'
    },
    west_africa: {
      primary: '#dc2626', // Red
      secondary: '#fbbf24', // Gold
      accent: '#059669', // Green
      background: '#fefbf3',
      text: '#1f2937'
    },
    east_africa: {
      primary: '#7c3aed', // Purple
      secondary: '#f59e0b', // Orange
      accent: '#0891b2', // Cyan
      background: '#faf5ff',
      text: '#1f2937'
    },
    southern_africa: {
      primary: '#1f2937', // Dark gray
      secondary: '#fbbf24', // Gold
      accent: '#dc2626', // Red
      background: '#f9fafb',
      text: '#111827'
    }
  };

  const theme = culturalThemes[culturalTheme] || culturalThemes.default;

  // Management systems navigation
  const managementSystems = [
    { id: 'dashboard', name: 'Dashboard', icon: Home },
    { id: 'pos', name: 'Point of Sale', icon: '🛒' },
    { id: 'inventory', name: 'Inventory', icon: '📦' },
    { id: 'crm', name: 'Customers', icon: '👥' },
    { id: 'hr', name: 'HR', icon: '👤' },
    { id: 'financial', name: 'Finance', icon: '💰' },
    { id: 'supply_chain', name: 'Supply Chain', icon: '🚚' },
    { id: 'project', name: 'Projects', icon: '📋' },
    { id: 'document', name: 'Documents', icon: '📄' },
    { id: 'asset', name: 'Assets', icon: '🏢' },
    { id: 'quality', name: 'Quality', icon: '✅' },
    { id: 'healthcare', name: 'Healthcare', icon: '🏥' },
    { id: 'education', name: 'Education', icon: '🎓' },
    { id: 'agriculture', name: 'Agriculture', icon: '🌾' },
    { id: 'restaurant', name: 'Restaurant', icon: '🍽️' },
    { id: 'hotel', name: 'Hotel', icon: '🏨' },
    { id: 'transport', name: 'Transport', icon: '🚌' },
    { id: 'manufacturing', name: 'Manufacturing', icon: '🏭' },
    { id: 'retail', name: 'Retail', icon: '🛍️' },
    { id: 'service', name: 'Services', icon: '🔧' },
    { id: 'event', name: 'Events', icon: '🎉' }
  ];

  // Monitor network status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    // Detect network speed
    if ('connection' in navigator) {
      const connection = navigator.connection;
      setNetworkSpeed(connection.effectiveType || 'unknown');
      
      connection.addEventListener('change', () => {
        setNetworkSpeed(connection.effectiveType || 'unknown');
      });
    }
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Monitor battery status
  useEffect(() => {
    if ('getBattery' in navigator) {
      navigator.getBattery().then(battery => {
        setBatteryLevel(Math.round(battery.level * 100));
        
        battery.addEventListener('levelchange', () => {
          setBatteryLevel(Math.round(battery.level * 100));
        });
      });
    }
  }, []);

  // Simulate signal strength based on network conditions
  useEffect(() => {
    const speedToSignal = {
      'slow-2g': 1,
      '2g': 2,
      '3g': 3,
      '4g': 4
    };
    setSignalStrength(speedToSignal[networkSpeed] || 2);
  }, [networkSpeed]);

  const getNetworkSpeedColor = () => {
    switch (networkSpeed) {
      case 'slow-2g':
      case '2g':
        return 'text-red-500';
      case '3g':
        return 'text-yellow-500';
      case '4g':
        return 'text-green-500';
      default:
        return 'text-gray-500';
    }
  };

  const getBatteryColor = () => {
    if (batteryLevel > 50) return 'text-green-500';
    if (batteryLevel > 20) return 'text-yellow-500';
    return 'text-red-500';
  };

  const handleSystemChange = (systemId) => {
    onSystemChange(systemId);
    setIsMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{ backgroundColor: theme.background }}>
      {/* Status Bar */}
      <div className="bg-black text-white px-4 py-1 flex justify-between items-center text-xs">
        <div className="flex items-center space-x-2">
          <span>WebWaka</span>
          {!isOnline && (
            <span className="bg-red-500 px-1 rounded text-xs">Offline</span>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <div className={`flex items-center ${getNetworkSpeedColor()}`}>
            {isOnline ? <Wifi size={12} /> : <WifiOff size={12} />}
            <span className="ml-1">{networkSpeed.toUpperCase()}</span>
          </div>
          
          <div className="flex items-center">
            {[...Array(4)].map((_, i) => (
              <div
                key={i}
                className={`w-1 h-2 mx-px ${
                  i < signalStrength ? 'bg-white' : 'bg-gray-600'
                }`}
              />
            ))}
          </div>
          
          <div className={`flex items-center ${getBatteryColor()}`}>
            <Battery size={12} />
            <span className="ml-1">{batteryLevel}%</span>
          </div>
        </div>
      </div>

      {/* Header */}
      <header className="bg-white shadow-sm border-b" style={{ borderColor: theme.primary + '20' }}>
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              style={{ color: theme.primary }}
            >
              {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            
            <div>
              <h1 className="font-semibold text-lg" style={{ color: theme.text }}>
                {title}
              </h1>
              <p className="text-xs text-gray-500">
                {managementSystems.find(s => s.id === currentSystem)?.name || 'Dashboard'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {notifications.length > 0 && (
              <button className="relative p-2 rounded-lg hover:bg-gray-100">
                <Bell size={18} style={{ color: theme.primary }} />
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {notifications.length}
                </span>
              </button>
            )}
            
            <button className="p-2 rounded-lg hover:bg-gray-100">
              <User size={18} style={{ color: theme.primary }} />
            </button>
          </div>
        </div>
      </header>

      {/* Slide-out Menu */}
      <div className={`fixed inset-0 z-50 transform transition-transform duration-300 ${
        isMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex">
          {/* Menu Content */}
          <div className="w-80 bg-white h-full shadow-xl overflow-y-auto">
            <div className="p-4 border-b" style={{ borderColor: theme.primary + '20' }}>
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-lg" style={{ color: theme.text }}>
                  Management Systems
                </h2>
                <button
                  onClick={() => setIsMenuOpen(false)}
                  className="p-1 rounded hover:bg-gray-100"
                >
                  <X size={20} />
                </button>
              </div>
            </div>
            
            <div className="p-2">
              {managementSystems.map((system) => (
                <button
                  key={system.id}
                  onClick={() => handleSystemChange(system.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-3 rounded-lg mb-1 transition-colors ${
                    currentSystem === system.id
                      ? 'text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                  style={{
                    backgroundColor: currentSystem === system.id ? theme.primary : 'transparent'
                  }}
                >
                  <span className="text-xl">
                    {typeof system.icon === 'string' ? system.icon : <system.icon size={20} />}
                  </span>
                  <span className="font-medium">{system.name}</span>
                </button>
              ))}
            </div>
            
            {/* User Profile Section */}
            <div className="border-t p-4 mt-4" style={{ borderColor: theme.primary + '20' }}>
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-full flex items-center justify-center" 
                     style={{ backgroundColor: theme.primary + '20' }}>
                  <User size={20} style={{ color: theme.primary }} />
                </div>
                <div>
                  <p className="font-medium" style={{ color: theme.text }}>
                    {user?.name || 'Guest User'}
                  </p>
                  <p className="text-sm text-gray-500">
                    {user?.role || 'Basic User'}
                  </p>
                </div>
              </div>
              
              <button className="w-full mt-3 px-4 py-2 rounded-lg border transition-colors hover:bg-gray-50"
                      style={{ borderColor: theme.primary, color: theme.primary }}>
                <Settings size={16} className="inline mr-2" />
                Settings
              </button>
            </div>
          </div>
          
          {/* Overlay */}
          <div 
            className="flex-1 bg-black bg-opacity-50"
            onClick={() => setIsMenuOpen(false)}
          />
        </div>
      </div>

      {/* Main Content */}
      <main className="pb-20">
        {children}
      </main>

      {/* Bottom Navigation for Quick Access */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg">
        <div className="flex justify-around py-2">
          {managementSystems.slice(0, 5).map((system) => (
            <button
              key={system.id}
              onClick={() => handleSystemChange(system.id)}
              className={`flex flex-col items-center py-2 px-3 rounded-lg transition-colors ${
                currentSystem === system.id ? 'text-white' : 'text-gray-600'
              }`}
              style={{
                backgroundColor: currentSystem === system.id ? theme.primary : 'transparent'
              }}
            >
              <span className="text-lg mb-1">
                {typeof system.icon === 'string' ? system.icon : <system.icon size={18} />}
              </span>
              <span className="text-xs font-medium truncate max-w-16">
                {system.name}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Offline Indicator */}
      {!isOnline && (
        <div className="fixed top-16 left-4 right-4 bg-yellow-500 text-white px-4 py-2 rounded-lg shadow-lg z-40">
          <div className="flex items-center space-x-2">
            <WifiOff size={16} />
            <span className="text-sm font-medium">
              You're offline. Some features may be limited.
            </span>
          </div>
        </div>
      )}

      {/* Low Battery Warning */}
      {batteryLevel < 20 && (
        <div className="fixed top-16 left-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-40">
          <div className="flex items-center space-x-2">
            <Battery size={16} />
            <span className="text-sm font-medium">
              Low battery ({batteryLevel}%). Consider enabling power saving mode.
            </span>
          </div>
        </div>
      )}

      {/* Network Speed Indicator */}
      {networkSpeed === 'slow-2g' || networkSpeed === '2g' ? (
        <div className="fixed bottom-24 right-4 bg-orange-500 text-white px-3 py-2 rounded-lg shadow-lg z-40">
          <div className="flex items-center space-x-2">
            <Wifi size={14} />
            <span className="text-xs font-medium">
              Slow connection - Optimizing for {networkSpeed.toUpperCase()}
            </span>
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default MobileOptimizedLayout;

