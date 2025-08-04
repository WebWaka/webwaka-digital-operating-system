// WebWaka Digital Operating System - Service Worker
// Provides offline-first capabilities for African infrastructure optimization

const CACHE_NAME = 'webwaka-v1.0.0';
const STATIC_CACHE = 'webwaka-static-v1';
const API_CACHE = 'webwaka-api-v1';

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  // Add other static assets as needed
];

// API endpoints to cache
const API_ENDPOINTS = [
  '/api/health',
  '/api/status',
  '/api/sectors',
  '/api/ai/status',
  '/api/partners'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('WebWaka Service Worker: Installing...');
  
  event.waitUntil(
    Promise.all([
      caches.open(STATIC_CACHE).then((cache) => {
        console.log('WebWaka Service Worker: Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      }),
      caches.open(API_CACHE).then((cache) => {
        console.log('WebWaka Service Worker: Pre-caching API endpoints');
        return Promise.all(
          API_ENDPOINTS.map(endpoint => {
            return fetch(endpoint)
              .then(response => {
                if (response.ok) {
                  return cache.put(endpoint, response.clone());
                }
              })
              .catch(error => {
                console.log(`WebWaka Service Worker: Failed to pre-cache ${endpoint}:`, error);
              });
          })
        );
      })
    ])
  );
  
  // Force activation of new service worker
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('WebWaka Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== STATIC_CACHE && cacheName !== API_CACHE) {
            console.log('WebWaka Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  // Take control of all clients
  self.clients.claim();
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }
  
  // Handle static assets
  if (request.method === 'GET') {
    event.respondWith(handleStaticRequest(request));
    return;
  }
});

// Handle API requests with cache-first strategy for offline support
async function handleApiRequest(request) {
  const cache = await caches.open(API_CACHE);
  
  try {
    // Try network first for fresh data
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful responses
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    // If network fails, try cache
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      console.log('WebWaka Service Worker: Serving API from cache (network failed)');
      return cachedResponse;
    }
    
    // Return offline response if no cache available
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'WebWaka is currently offline. Please check your connection.',
      cached: false,
      timestamp: new Date().toISOString()
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    console.log('WebWaka Service Worker: Network error, trying cache:', error);
    
    // Try cache on network error
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      console.log('WebWaka Service Worker: Serving API from cache (offline)');
      return cachedResponse;
    }
    
    // Return offline response
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'WebWaka is currently offline. Please check your connection.',
      cached: false,
      timestamp: new Date().toISOString()
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Handle static requests with cache-first strategy
async function handleStaticRequest(request) {
  const cache = await caches.open(STATIC_CACHE);
  
  // Try cache first
  const cachedResponse = await cache.match(request);
  if (cachedResponse) {
    console.log('WebWaka Service Worker: Serving from cache:', request.url);
    return cachedResponse;
  }
  
  try {
    // Try network if not in cache
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful responses
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    // For navigation requests, return index.html from cache
    if (request.mode === 'navigate') {
      const indexResponse = await cache.match('/index.html');
      if (indexResponse) {
        return indexResponse;
      }
    }
    
    return networkResponse;
    
  } catch (error) {
    console.log('WebWaka Service Worker: Network error for static asset:', error);
    
    // For navigation requests, return index.html from cache
    if (request.mode === 'navigate') {
      const indexResponse = await cache.match('/index.html');
      if (indexResponse) {
        return indexResponse;
      }
    }
    
    // Return offline page or error
    return new Response('WebWaka is currently offline. Please check your connection.', {
      status: 503,
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('WebWaka Service Worker: Background sync triggered:', event.tag);
  
  if (event.tag === 'webwaka-sync') {
    event.waitUntil(syncWebWakaData());
  }
});

// Sync WebWaka data when back online
async function syncWebWakaData() {
  try {
    console.log('WebWaka Service Worker: Syncing data...');
    
    // Refresh API cache with latest data
    const cache = await caches.open(API_CACHE);
    
    for (const endpoint of API_ENDPOINTS) {
      try {
        const response = await fetch(endpoint);
        if (response.ok) {
          await cache.put(endpoint, response.clone());
          console.log(`WebWaka Service Worker: Synced ${endpoint}`);
        }
      } catch (error) {
        console.log(`WebWaka Service Worker: Failed to sync ${endpoint}:`, error);
      }
    }
    
    // Notify clients about sync completion
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'SYNC_COMPLETE',
        message: 'WebWaka data synchronized successfully'
      });
    });
    
  } catch (error) {
    console.log('WebWaka Service Worker: Sync failed:', error);
  }
}

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('WebWaka Service Worker: Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New update from WebWaka',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    tag: 'webwaka-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'open',
        title: 'Open WebWaka'
      },
      {
        action: 'dismiss',
        title: 'Dismiss'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('WebWaka Digital Operating System', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('WebWaka Service Worker: Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handling from main thread
self.addEventListener('message', (event) => {
  console.log('WebWaka Service Worker: Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_REFRESH') {
    event.waitUntil(syncWebWakaData());
  }
});

console.log('WebWaka Service Worker: Loaded successfully');

