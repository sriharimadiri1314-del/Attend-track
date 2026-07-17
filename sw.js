/* ══════════════════════════════════════════════════
   AttendTrack Service Worker
   - Caches all assets for offline use
   - Serves cached content when network is unavailable
══════════════════════════════════════════════════ */

const CACHE_NAME = 'attendtrack-v2';
const ASSETS = [
  '/attendance-tracker/',
  '/attendance-tracker/index.html',
  '/attendance-tracker/manifest.json',
  '/attendance-tracker/icon-192.png',
  '/attendance-tracker/icon-512.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
];

// Install: cache all core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[SW] Caching app shell');
      return cache.addAll(ASSETS);
    }).catch(err => {
      console.log('[SW] Cache install error:', err);
    })
  );
  self.skipWaiting();
});

// Activate: clear old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request).then(response => {
        // Cache successful responses for future
        if (response && response.status === 200 && response.type !== 'opaque') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        // Offline fallback for navigation
        if (event.request.destination === 'document') {
          return caches.match('/attendance-tracker/index.html');
        }
      });
    })
  );
});
