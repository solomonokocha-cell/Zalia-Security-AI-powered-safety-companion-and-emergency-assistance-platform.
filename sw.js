// Service Worker with enhanced caching and offline support

const CACHE_VERSION = 'v22-pwa-install-fix';
const CACHE_NAME = `zalia-pwa-${CACHE_VERSION}`;

// Core assets that should always be cached
const CORE_ASSETS = [
  '/',
  '/index.html',
  '/ZaziAi.html',
  '/about.html',
  '/contact.html',
  '/incidents.html',
  '/safetyacademy,html',
  '/simulator.html',
  '/route-planner.html',
  '/game.html',
  '/games.html',
  '/manifest.json',
  '/style.css',
  '/zazi-presence.js',
  '/app-shell.js',
  '/sound-effect.js',
  '/lucide-local.js',
  '/images/zalia-app-icon.png',
  '/offline-tailwind.css',
  "/images/Zalia's-final-logo.png",
  '/pwa-install.js',
  '/tailwind-shim.js',
  '/pwa-mobile.css',
  '/images/zazi-image-final.png',
  '/images/shy-zazi.png',
  '/images/zazi-flying.png',
  '/images/loving-zazi.png',
  '/images/sleepy-zazi.png',
  '/images/adventrous-zazi.png',
  '/images/sad-zazi.png',
  '/images/angry-zazi.png',
  '/images/exited-zazi.png',
  '/images/thinking-zazi.png',
  '/images/waving-zazi.png',
  '/images/curious-zazi.png',
  
];

// Install event - cache assets
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching core assets');
        return cache.addAll(CORE_ASSETS);
      })
      .then(() => {
        console.log('[Service Worker] Installation complete');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('[Service Worker] Installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log(`[Service Worker] Deleting old cache: ${cacheName}`);
            return caches.delete(cacheName);
          }
        })
      );
    })
    .then(() => {
      console.log('[Service Worker] Activation complete');
      return self.clients.claim();
    })
  );
});

// Fetch event - implement cache-first strategy for assets, network-first for API calls
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // API calls - network first, fall back to cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Only cache successful responses
          if (response.status === 200) {
            const cache_clone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, cache_clone);
            });
          }
          return response;
        })
        .catch(() => {
          // Return cached response if offline
          return caches.match(request)
            .then(cached => cached || new Response('Offline - API unavailable', { status: 503 }));
        })
    );
    return;
  }

  // HTML navigations check the server first so installed users receive updates.
  if (request.mode === 'navigate' || request.destination === 'document') {
    event.respondWith(
      fetch(request, { cache: 'no-store' })
        .then(response => {
          if (response.ok) {
            const cacheClone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, cacheClone));
          }
          return response;
        })
        .catch(() => caches.match(request).then(cached => cached || new Response('Offline', { status: 503 })))
    );
    return;
  }

  // Other static assets use the cache first, then the network.
  event.respondWith(
    caches.match(request)
      .then(cached => {
        if (cached) {
          return cached;
        }

        return fetch(request)
          .then(response => {
            // Cache successful responses for static assets
            if (response.status === 200 && (
              request.destination === 'script' ||
              request.destination === 'style' ||
              request.destination === 'image' ||
              request.destination === 'font'
            )) {
              const cache_clone = response.clone();
              caches.open(CACHE_NAME).then(cache => {
                cache.put(request, cache_clone);
              });
            }
            return response;
          })
          .catch(() => {
            // Offline fallback
            if (request.destination === 'image') {
              return new Response(
                '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="200" height="200" fill="#e5e7eb"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="#9ca3af" font-family="sans-serif">Offline</text></svg>',
                { headers: { 'Content-Type': 'image/svg+xml' } }
              );
            }
            return new Response('Offline', { status: 503 });
          });
      })
  );
});

// Handle background sync for incident reports
self.addEventListener('sync', event => {
  if (event.tag === 'sync-incident-reports') {
    event.waitUntil(
      // Sync incident reports when connection is restored
      Promise.resolve()
    );
  }
});

// Handle push notifications
self.addEventListener('push', event => {
  if (event.data) {
    const options = {
      body: event.data.text(),
      icon: '/images/zalia-app-icon.png',
      badge: '/images/zalia-app-icon.png',
      tag: 'zalia-notification',
      requireInteraction: true
    };

    event.waitUntil(
      self.registration.showNotification('🐾 Zalia Security Alert', options)
    );
  }
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({ type: 'window' })
      .then(clientList => {
        for (const client of clientList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
  );
});
