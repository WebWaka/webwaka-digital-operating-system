/**
 * WebWaka Progressive Web App Manager
 * 
 * Manages PWA functionality for WebWaka Digital Operating System:
 * - Service Worker registration and management
 * - Offline-first capabilities
 * - App installation prompts
 * - Background sync
 * - Push notifications
 * - African infrastructure optimization
 */

import React, { useState, useEffect, useContext, createContext } from 'react';
import { Cell } from '../core/CellularArchitecture.js';

// PWA Context for global state management
const PWAContext = createContext();

export const usePWA = () => {
    const context = useContext(PWAContext);
    if (!context) {
        throw new Error('usePWA must be used within a PWAProvider');
    }
    return context;
};

/**
 * PWA Manager Cell - Extends cellular architecture
 */
class PWAManagerCell extends Cell {
    constructor(config = {}) {
        super({
            ...config,
            type: 'pwa-manager',
            capabilities: ['offline-sync', 'background-sync', 'push-notifications', 'app-installation']
        });
        
        this.serviceWorker = null;
        this.installPrompt = null;
        this.isOnline = navigator.onLine;
        this.syncQueue = [];
        this.notificationPermission = 'default';
    }
    
    /**
     * Initialize PWA manager
     */
    async initialize() {
        await super.initialize();
        
        // Register service worker
        await this.registerServiceWorker();
        
        // Setup offline/online listeners
        this.setupNetworkListeners();
        
        // Setup install prompt listener
        this.setupInstallPrompt();
        
        // Request notification permission
        await this.requestNotificationPermission();
        
        // Setup background sync
        this.setupBackgroundSync();
    }
    
    /**
     * Register service worker for offline functionality
     */
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/sw.js');
                this.serviceWorker = registration;
                
                this.emit('service-worker-registered', { registration });
                
                // Listen for service worker updates
                registration.addEventListener('updatefound', () => {
                    this.emit('service-worker-update-available');
                });
                
            } catch (error) {
                this.handleError(error);
            }
        }
    }
    
    /**
     * Setup network status listeners
     */
    setupNetworkListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.emit('network-online');
            this.processSyncQueue();
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.emit('network-offline');
        });
    }
    
    /**
     * Setup app installation prompt
     */
    setupInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (event) => {
            event.preventDefault();
            this.installPrompt = event;
            this.emit('install-prompt-available');
        });
        
        window.addEventListener('appinstalled', () => {
            this.installPrompt = null;
            this.emit('app-installed');
        });
    }
    
    /**
     * Request notification permission
     */
    async requestNotificationPermission() {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission();
            this.notificationPermission = permission;
            this.emit('notification-permission-changed', { permission });
        }
    }
    
    /**
     * Setup background sync for offline operations
     */
    setupBackgroundSync() {
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            navigator.serviceWorker.ready.then((registration) => {
                // Register background sync
                registration.sync.register('background-sync');
            });
        }
    }
    
    /**
     * Add operation to sync queue for offline processing
     */
    addToSyncQueue(operation) {
        this.syncQueue.push({
            ...operation,
            timestamp: new Date(),
            id: this.generateId()
        });
        
        this.emit('operation-queued', { operation, queueLength: this.syncQueue.length });
        
        // Try to sync immediately if online
        if (this.isOnline) {
            this.processSyncQueue();
        }
    }
    
    /**
     * Process sync queue when online
     */
    async processSyncQueue() {
        if (!this.isOnline || this.syncQueue.length === 0) return;
        
        const queue = [...this.syncQueue];
        this.syncQueue = [];
        
        for (const operation of queue) {
            try {
                await this.processQueuedOperation(operation);
                this.emit('operation-synced', { operation });
            } catch (error) {
                // Re-queue failed operations
                this.syncQueue.push(operation);
                this.emit('operation-sync-failed', { operation, error });
            }
        }
    }
    
    /**
     * Process a queued operation
     */
    async processQueuedOperation(operation) {
        // This would integrate with the AI orchestrator or other services
        const response = await fetch(operation.url, {
            method: operation.method || 'POST',
            headers: operation.headers || { 'Content-Type': 'application/json' },
            body: JSON.stringify(operation.data)
        });
        
        if (!response.ok) {
            throw new Error(`Sync failed: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    /**
     * Show app installation prompt
     */
    async showInstallPrompt() {
        if (!this.installPrompt) {
            throw new Error('Install prompt not available');
        }
        
        const result = await this.installPrompt.prompt();
        this.emit('install-prompt-result', { result });
        
        return result;
    }
    
    /**
     * Send push notification
     */
    async sendNotification(title, options = {}) {
        if (this.notificationPermission !== 'granted') {
            throw new Error('Notification permission not granted');
        }
        
        const notification = new Notification(title, {
            icon: '/icons/icon-192x192.png',
            badge: '/icons/badge-72x72.png',
            ...options
        });
        
        this.emit('notification-sent', { title, options });
        
        return notification;
    }
    
    /**
     * Get PWA status
     */
    getStatus() {
        return {
            ...super.getStatus(),
            isOnline: this.isOnline,
            serviceWorkerRegistered: !!this.serviceWorker,
            installPromptAvailable: !!this.installPrompt,
            notificationPermission: this.notificationPermission,
            syncQueueLength: this.syncQueue.length,
            isInstalled: window.matchMedia('(display-mode: standalone)').matches
        };
    }
}

/**
 * PWA Provider Component
 */
export const PWAProvider = ({ children }) => {
    const [pwaManager] = useState(() => new PWAManagerCell());
    const [pwaStatus, setPwaStatus] = useState({
        isOnline: navigator.onLine,
        serviceWorkerRegistered: false,
        installPromptAvailable: false,
        notificationPermission: 'default',
        syncQueueLength: 0,
        isInstalled: false
    });
    
    useEffect(() => {
        // Initialize PWA manager
        pwaManager.initialize();
        
        // Listen for PWA events
        const updateStatus = () => {
            setPwaStatus(pwaManager.getStatus());
        };
        
        pwaManager.on('service-worker-registered', updateStatus);
        pwaManager.on('network-online', updateStatus);
        pwaManager.on('network-offline', updateStatus);
        pwaManager.on('install-prompt-available', updateStatus);
        pwaManager.on('app-installed', updateStatus);
        pwaManager.on('notification-permission-changed', updateStatus);
        pwaManager.on('operation-queued', updateStatus);
        pwaManager.on('operation-synced', updateStatus);
        
        return () => {
            pwaManager.removeAllListeners();
        };
    }, [pwaManager]);
    
    const value = {
        pwaManager,
        pwaStatus,
        addToSyncQueue: (operation) => pwaManager.addToSyncQueue(operation),
        showInstallPrompt: () => pwaManager.showInstallPrompt(),
        sendNotification: (title, options) => pwaManager.sendNotification(title, options)
    };
    
    return (
        <PWAContext.Provider value={value}>
            {children}
        </PWAContext.Provider>
    );
};

/**
 * Network Status Indicator Component
 */
export const NetworkStatusIndicator = () => {
    const { pwaStatus } = usePWA();
    
    return (
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
            pwaStatus.isOnline 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
        }`}>
            <div className={`w-2 h-2 rounded-full ${
                pwaStatus.isOnline ? 'bg-green-500' : 'bg-red-500'
            }`} />
            <span>
                {pwaStatus.isOnline ? 'Online' : 'Offline'}
                {pwaStatus.syncQueueLength > 0 && ` (${pwaStatus.syncQueueLength} pending)`}
            </span>
        </div>
    );
};

/**
 * Install App Prompt Component
 */
export const InstallAppPrompt = () => {
    const { pwaStatus, showInstallPrompt } = usePWA();
    const [isVisible, setIsVisible] = useState(false);
    
    useEffect(() => {
        setIsVisible(pwaStatus.installPromptAvailable && !pwaStatus.isInstalled);
    }, [pwaStatus.installPromptAvailable, pwaStatus.isInstalled]);
    
    if (!isVisible) return null;
    
    const handleInstall = async () => {
        try {
            await showInstallPrompt();
            setIsVisible(false);
        } catch (error) {
            console.error('Install failed:', error);
        }
    };
    
    return (
        <div className="fixed bottom-4 left-4 right-4 bg-blue-600 text-white p-4 rounded-lg shadow-lg z-50 md:left-auto md:right-4 md:max-w-sm">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="font-semibold">Install WebWaka</h3>
                    <p className="text-sm opacity-90">
                        Add WebWaka to your home screen for quick access
                    </p>
                </div>
                <div className="flex space-x-2 ml-4">
                    <button
                        onClick={() => setIsVisible(false)}
                        className="px-3 py-1 text-sm bg-blue-700 rounded hover:bg-blue-800"
                    >
                        Later
                    </button>
                    <button
                        onClick={handleInstall}
                        className="px-3 py-1 text-sm bg-white text-blue-600 rounded hover:bg-gray-100"
                    >
                        Install
                    </button>
                </div>
            </div>
        </div>
    );
};

/**
 * Offline Indicator Component
 */
export const OfflineIndicator = () => {
    const { pwaStatus } = usePWA();
    
    if (pwaStatus.isOnline) return null;
    
    return (
        <div className="fixed top-0 left-0 right-0 bg-yellow-500 text-white text-center py-2 z-50">
            <div className="flex items-center justify-center space-x-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <span>You're offline. Changes will sync when connection is restored.</span>
            </div>
        </div>
    );
};

/**
 * PWA Update Prompt Component
 */
export const PWAUpdatePrompt = () => {
    const { pwaManager } = usePWA();
    const [updateAvailable, setUpdateAvailable] = useState(false);
    
    useEffect(() => {
        const handleUpdate = () => setUpdateAvailable(true);
        pwaManager.on('service-worker-update-available', handleUpdate);
        
        return () => {
            pwaManager.off('service-worker-update-available', handleUpdate);
        };
    }, [pwaManager]);
    
    if (!updateAvailable) return null;
    
    const handleUpdate = () => {
        window.location.reload();
    };
    
    return (
        <div className="fixed bottom-4 left-4 right-4 bg-green-600 text-white p-4 rounded-lg shadow-lg z-50 md:left-auto md:right-4 md:max-w-sm">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="font-semibold">Update Available</h3>
                    <p className="text-sm opacity-90">
                        A new version of WebWaka is available
                    </p>
                </div>
                <div className="flex space-x-2 ml-4">
                    <button
                        onClick={() => setUpdateAvailable(false)}
                        className="px-3 py-1 text-sm bg-green-700 rounded hover:bg-green-800"
                    >
                        Later
                    </button>
                    <button
                        onClick={handleUpdate}
                        className="px-3 py-1 text-sm bg-white text-green-600 rounded hover:bg-gray-100"
                    >
                        Update
                    </button>
                </div>
            </div>
        </div>
    );
};

/**
 * African Infrastructure Optimization Hook
 */
export const useAfricanOptimization = () => {
    const { pwaStatus, addToSyncQueue } = usePWA();
    
    const optimizeForNetwork = (operation) => {
        // Optimize based on network conditions common in Africa
        const optimized = { ...operation };
        
        if (!pwaStatus.isOnline) {
            // Queue for later sync
            addToSyncQueue(operation);
            return { queued: true };
        }
        
        // Apply network-specific optimizations
        optimized.compression = true;
        optimized.timeout = 30000; // 30 second timeout for slow networks
        optimized.retries = 3;
        
        return optimized;
    };
    
    const optimizeForMobile = (data) => {
        // Optimize data for mobile-first African markets
        return {
            ...data,
            compressed: true,
            mobileOptimized: true,
            lowBandwidth: true
        };
    };
    
    return {
        optimizeForNetwork,
        optimizeForMobile,
        isOnline: pwaStatus.isOnline,
        syncQueueLength: pwaStatus.syncQueueLength
    };
};

/**
 * Main PWA Manager Component
 */
export const PWAManager = ({ children }) => {
    return (
        <PWAProvider>
            {children}
            <NetworkStatusIndicator />
            <OfflineIndicator />
            <InstallAppPrompt />
            <PWAUpdatePrompt />
        </PWAProvider>
    );
};

export default PWAManager;

