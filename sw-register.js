/**
 * Service Worker Registration with Automatic Updates
 * Handles SW registration, updates, and background sync
 */

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    registerServiceWorker();
  });
}

async function registerServiceWorker() {
  try {
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/',
      updateViaCache: 'none' // Always fetch fresh SW file
    });

    console.log('✅ Service Worker registered successfully:', registration.scope);

    // Check for a newer worker as soon as the app opens.
    registration.update().catch(err => {
      console.warn('SW initial update check failed:', err);
    });

    // Check for updates every 24 hours
    setInterval(() => {
      registration.update().catch(err => {
        console.warn('SW update check failed:', err);
      });
    }, 24 * 60 * 60 * 1000);

    // Listen for controller change (SW update installed)
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      console.log('🔄 Service Worker updated - app is using new version');
      showUpdateNotification();
    });

    // Listen for messages from SW
    navigator.serviceWorker.addEventListener('message', event => {
      if (event.data.type === 'SYNC_COMPLETE') {
        console.log('✅ Background sync completed:', event.data.payload);
      }
    });

  } catch (error) {
    console.warn('⚠️ Service Worker registration failed:', error);
  }
}

/**
 * Show notification when app is updated
 */
function showUpdateNotification() {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification('🐾 Zalia Updated!', {
      body: 'A new version is available. Reload the page to get the latest features.',
      icon: '/images/zalia-app-icon.png',
      tag: 'zalia-update'
    });
  }
}

/**
 * Request notification permissions for push alerts
 */
export function requestNotificationPermission() {
  if ('Notification' in window) {
    if (Notification.permission === 'default') {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          console.log('✅ Notifications enabled');
        }
      });
    }
  }
}
