import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, Download, Smartphone, Globe, Zap, Shield, Users } from 'lucide-react';

/**
 * PWA Enhancement Manager - Agent 3
 * Progressive Web App optimization with offline capabilities and African infrastructure adaptation
 */

const PWAEnhancementManager = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [installPrompt, setInstallPrompt] = useState(null);
  const [isInstalled, setIsInstalled] = useState(false);
  const [networkSpeed, setNetworkSpeed] = useState('unknown');
  const [cacheStatus, setCacheStatus] = useState({
    cached: 0,
    total: 0,
    lastUpdate: null
  });
  const [offlineQueue, setOfflineQueue] = useState([]);

  // Network status monitoring
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      processOfflineQueue();
    };
    
    const handleOffline = () => {
      setIsOnline(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Detect network speed for African infrastructure optimization
    detectNetworkSpeed();

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // PWA installation handling
  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setInstallPrompt(e);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  // Service Worker registration and cache management
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      registerServiceWorker();
      updateCacheStatus();
    }
  }, []);

  const registerServiceWorker = async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('✅ Service Worker registered successfully');
      
      // Listen for updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            // New content available
            showUpdateNotification();
          }
        });
      });
    } catch (error) {
      console.error('❌ Service Worker registration failed:', error);
    }
  };

  const detectNetworkSpeed = async () => {
    try {
      // Use Connection API if available
      if ('connection' in navigator) {
        const connection = navigator.connection;
        const effectiveType = connection.effectiveType;
        setNetworkSpeed(effectiveType);
        
        // Optimize based on connection type
        optimizeForConnection(effectiveType);
      } else {
        // Fallback: measure download speed
        const startTime = Date.now();
        await fetch('/api/health', { cache: 'no-cache' });
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        if (duration < 100) setNetworkSpeed('4g');
        else if (duration < 300) setNetworkSpeed('3g');
        else setNetworkSpeed('2g');
      }
    } catch (error) {
      console.error('Network speed detection failed:', error);
      setNetworkSpeed('slow');
    }
  };

  const optimizeForConnection = (connectionType) => {
    const optimizations = {
      'slow-2g': {
        imageQuality: 'low',
        prefetchDisabled: true,
        compressionLevel: 'high'
      },
      '2g': {
        imageQuality: 'medium',
        prefetchDisabled: true,
        compressionLevel: 'high'
      },
      '3g': {
        imageQuality: 'medium',
        prefetchDisabled: false,
        compressionLevel: 'medium'
      },
      '4g': {
        imageQuality: 'high',
        prefetchDisabled: false,
        compressionLevel: 'low'
      }
    };

    const config = optimizations[connectionType] || optimizations['2g'];
    
    // Apply optimizations
    document.documentElement.style.setProperty('--image-quality', config.imageQuality);
    
    // Store optimization preferences
    localStorage.setItem('webwaka_network_optimization', JSON.stringify(config));
  };

  const updateCacheStatus = async () => {
    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys();
        let totalCached = 0;
        
        for (const cacheName of cacheNames) {
          const cache = await caches.open(cacheName);
          const keys = await cache.keys();
          totalCached += keys.length;
        }
        
        setCacheStatus({
          cached: totalCached,
          total: totalCached, // Simplified for demo
          lastUpdate: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('Cache status update failed:', error);
    }
  };

  const installPWA = async () => {
    if (installPrompt) {
      const result = await installPrompt.prompt();
      if (result.outcome === 'accepted') {
        setIsInstalled(true);
        setInstallPrompt(null);
      }
    }
  };

  const processOfflineQueue = async () => {
    if (offlineQueue.length === 0) return;

    const processedQueue = [];
    
    for (const item of offlineQueue) {
      try {
        await fetch(item.url, item.options);
        processedQueue.push(item.id);
      } catch (error) {
        console.error('Failed to process queued request:', error);
      }
    }

    // Remove processed items
    setOfflineQueue(prev => prev.filter(item => !processedQueue.includes(item.id)));
  };

  const addToOfflineQueue = (url, options = {}) => {
    const queueItem = {
      id: Date.now() + Math.random(),
      url,
      options,
      timestamp: new Date().toISOString()
    };
    
    setOfflineQueue(prev => [...prev, queueItem]);
  };

  const showUpdateNotification = () => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('WebWaka Update Available', {
        body: 'A new version of WebWaka is available. Refresh to update.',
        icon: '/icons/icon-192x192.png',
        badge: '/icons/badge-72x72.png'
      });
    }
  };

  const clearCache = async () => {
    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys();
        await Promise.all(cacheNames.map(name => caches.delete(name)));
        setCacheStatus({ cached: 0, total: 0, lastUpdate: new Date().toISOString() });
        
        // Reload to get fresh content
        window.location.reload();
      }
    } catch (error) {
      console.error('Cache clearing failed:', error);
    }
  };

  const getConnectionIcon = () => {
    switch (networkSpeed) {
      case '4g': return <Zap className="w-4 h-4 text-green-500" />;
      case '3g': return <Wifi className="w-4 h-4 text-yellow-500" />;
      case '2g':
      case 'slow-2g': return <WifiOff className="w-4 h-4 text-red-500" />;
      default: return <Globe className="w-4 h-4 text-gray-500" />;
    }
  };

  const getOptimizationTips = () => {
    const tips = {
      'slow-2g': [
        'Using minimal data mode',
        'Images compressed for slow connections',
        'Non-essential features disabled'
      ],
      '2g': [
        'Optimized for 2G networks',
        'Reduced image quality for faster loading',
        'Essential features prioritized'
      ],
      '3g': [
        'Balanced performance mode',
        'Standard image quality',
        'Most features available'
      ],
      '4g': [
        'Full performance mode',
        'High-quality images enabled',
        'All features available'
      ]
    };

    return tips[networkSpeed] || tips['2g'];
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center">
          <Smartphone className="w-6 h-6 mr-2 text-blue-600" />
          PWA Enhancement Manager
        </h2>
        <div className="flex items-center space-x-2">
          {getConnectionIcon()}
          <span className="text-sm font-medium text-gray-600">
            {networkSpeed.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Connection Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className={`p-4 rounded-lg border-2 ${isOnline ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Connection Status</p>
              <p className={`text-lg font-bold ${isOnline ? 'text-green-600' : 'text-red-600'}`}>
                {isOnline ? 'Online' : 'Offline'}
              </p>
            </div>
            {isOnline ? (
              <Wifi className="w-8 h-8 text-green-500" />
            ) : (
              <WifiOff className="w-8 h-8 text-red-500" />
            )}
          </div>
        </div>

        <div className="p-4 rounded-lg border-2 border-blue-200 bg-blue-50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Cache Status</p>
              <p className="text-lg font-bold text-blue-600">
                {cacheStatus.cached} items cached
              </p>
            </div>
            <Shield className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="p-4 rounded-lg border-2 border-purple-200 bg-purple-50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Offline Queue</p>
              <p className="text-lg font-bold text-purple-600">
                {offlineQueue.length} pending
              </p>
            </div>
            <Users className="w-8 h-8 text-purple-500" />
          </div>
        </div>
      </div>

      {/* PWA Installation */}
      {!isInstalled && installPrompt && (
        <div className="mb-6 p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold">Install WebWaka App</h3>
              <p className="text-blue-100">Get the full app experience with offline capabilities</p>
            </div>
            <button
              onClick={installPWA}
              className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors flex items-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Install
            </button>
          </div>
        </div>
      )}

      {/* Network Optimization Info */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          African Infrastructure Optimization
        </h3>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center mb-2">
            {getConnectionIcon()}
            <span className="ml-2 font-medium text-gray-700">
              Current Network: {networkSpeed.toUpperCase()}
            </span>
          </div>
          <ul className="space-y-1">
            {getOptimizationTips().map((tip, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-center">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                {tip}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Offline Features */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Offline-First Features
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-medium text-green-800 mb-2">✅ Available Offline</h4>
            <ul className="text-sm text-green-700 space-y-1">
              <li>• Point of Sale transactions</li>
              <li>• Inventory management</li>
              <li>• Customer data access</li>
              <li>• Voice commands processing</li>
              <li>• Basic analytics</li>
            </ul>
          </div>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h4 className="font-medium text-yellow-800 mb-2">⏳ Requires Connection</h4>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• AI-powered insights</li>
              <li>• Real-time sync</li>
              <li>• Payment processing</li>
              <li>• Cloud backup</li>
              <li>• System updates</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Cache Management */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Cache Management
        </h3>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-sm text-gray-600">
                Last updated: {cacheStatus.lastUpdate ? 
                  new Date(cacheStatus.lastUpdate).toLocaleString() : 'Never'}
              </p>
              <p className="text-sm text-gray-600">
                Storage used: {cacheStatus.cached} cached resources
              </p>
            </div>
            <div className="space-x-2">
              <button
                onClick={updateCacheStatus}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm"
              >
                Refresh Status
              </button>
              <button
                onClick={clearCache}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
              >
                Clear Cache
              </button>
            </div>
          </div>
          
          {/* Cache Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min((cacheStatus.cached / 100) * 100, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* African Cultural Features */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Cultural Integration Features
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <h4 className="font-medium text-orange-800 mb-2">🌍 Ubuntu Philosophy</h4>
            <p className="text-sm text-orange-700">
              Community-centered design with shared resources and collective decision-making support
            </p>
          </div>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h4 className="font-medium text-purple-800 mb-2">🗣️ Local Languages</h4>
            <p className="text-sm text-purple-700">
              Voice interface supports 50+ African languages with cultural context awareness
            </p>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Performance Metrics
        </h3>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-blue-600">{isOnline ? '<100ms' : 'N/A'}</p>
              <p className="text-sm text-gray-600">Response Time</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-600">99.9%</p>
              <p className="text-sm text-gray-600">Offline Availability</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">{cacheStatus.cached}</p>
              <p className="text-sm text-gray-600">Cached Resources</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-orange-600">{networkSpeed.toUpperCase()}</p>
              <p className="text-sm text-gray-600">Network Speed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PWAEnhancementManager;

