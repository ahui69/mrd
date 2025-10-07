const CACHE_NAME = 'mordzix-v1';
const ASSETS = [
  '/', '/static/style.css', '/static/app.js', '/static/manifest.webmanifest'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k)))));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (ASSETS.includes(url.pathname)) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
  } else if (url.pathname.startsWith('/static') || url.pathname.startsWith('/uploads')) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      const resp = res.clone(); caches.open(CACHE_NAME).then(c => c.put(e.request, resp)); return res;
    })));
  }
});