(function () {
  const icons = {
    'shield-check': '<path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3v8Z"/><path d="m9 12 2 2 4-4"/>',
    'shield-alert': '<path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3v8Z"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
    'lock': '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
    'moon': '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    'eye-off': '<path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c5 0 8.5 4.5 9 7-.18.9-.82 2-1.75 3"/><path d="M6.61 6.61C4.4 8.03 3.3 10.14 3 12c.5 2.5 4 7 9 7a9.6 9.6 0 0 0 4.39-1.1"/><path d="m3 3 18 18"/>',
    'sparkles': '<path d="m12 3-1.5 5.5L5 10l5.5 1.5L12 17l1.5-5.5L19 10l-5.5-1.5L12 3Z"/><path d="m5 3-.5 2L3 5.5 4.5 6 5 8l.5-2 1.5-.5L5.5 5 5 3ZM19 16l-.5 2-1.5.5 1.5.5.5 2 .5-2 1.5-.5-1.5-.5-.5-2Z"/>',
    'ship': '<path d="M2 20a10 10 0 0 0 20 0"/><path d="m4 18 1.5-7h13L20 18"/><path d="M12 3v8M8 7h8"/>',
    'flame': '<path d="M12 22c4 0 7-2.5 7-6.5 0-3-2-5.5-4.5-7.5.2 2-1 3.5-2.5 4.5.2-3-1.5-6.5-4-8.5.2 4-4 6-4 10.5C4 19 7 22 12 22Z"/>',
    'building-2': '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18M4 22h16M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2"/>',
    'map-pin': '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    'radio': '<path d="M4.9 19.1a10 10 0 0 1 0-14.2M8.5 15.5a5 5 0 0 1 0-7M12 12h.01M15.5 8.5a5 5 0 0 1 0 7M19.1 4.9a10 10 0 0 1 0 14.2"/>',
    'plus-circle': '<circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'car': '<path d="m5 17-1-5 2-5h12l2 5-1 5M4 12h16M7 17v2M17 17v2"/><circle cx="7.5" cy="15" r="1"/><circle cx="16.5" cy="15" r="1"/>',
    'check-circle': '<circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/>',
    'alert-triangle': '<path d="m10.3 3.5-8 14A2 2 0 0 0 4 20.5h16a2 2 0 0 0 1.7-3l-8-14a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    'siren': '<path d="M7 18v-5a5 5 0 0 1 10 0v5M5 18h14M3 22h18M12 2v2M4.2 5.2l1.4 1.4M19.8 5.2l-1.4 1.4"/>',
    'phone-call': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9Z"/>',
    'message-square': '<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4v8Z"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9Z"/>',
    'arrow-right': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'book-open': '<path d="M2 4h6a4 4 0 0 1 4 4v12a4 4 0 0 0-4-4H2V4ZM22 4h-6a4 4 0 0 0-4 4v12a4 4 0 0 1 4-4h6V4Z"/>',
    'activity': '<path d="M3 12h4l3-9 4 18 3-9h4"/>',
    'route': '<circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M8.5 17.5 15.5 6.5"/>',
    'bot': '<rect width="16" height="12" x="4" y="8" rx="2"/><path d="M12 4v4M8 13h.01M16 13h.01M9 17h6"/><path d="M2 12h2M20 12h2"/>',
    'chevron-down': '<path d="m6 9 6 6 6-6"/>',
    'x': '<path d="m6 6 12 12M18 6 6 18"/>'
    ,'zap': '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/>'
    ,'map': '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z"/><path d="M9 3v15M15 6v15"/>'
    ,'external-link': '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
    ,'download': '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>'
  };

  function createIcons() {
    document.querySelectorAll('[data-lucide]').forEach(node => {
      const name = node.getAttribute('data-lucide');
      const content = icons[name] || icons.sparkles;
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      [...node.attributes].forEach(attribute => {
        if (attribute.name !== 'data-lucide') svg.setAttribute(attribute.name, attribute.value);
      });
      svg.setAttribute('data-lucide', name);
      svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      svg.setAttribute('viewBox', '0 0 24 24');
      svg.setAttribute('fill', 'none');
      svg.setAttribute('stroke', 'currentColor');
      svg.setAttribute('stroke-width', '2');
      svg.setAttribute('stroke-linecap', 'round');
      svg.setAttribute('stroke-linejoin', 'round');
      const sizeClass = [...node.classList].find(className => /^w-(?:\d+(?:\.5)?|px)$/.test(className));
      const sizes = { 'w-3': '0.75rem', 'w-3.5': '0.875rem', 'w-4': '1rem', 'w-5': '1.25rem', 'w-6': '1.5rem', 'w-10': '2.5rem', 'w-24': '6rem' };
      if (sizeClass && sizes[sizeClass]) {
        svg.style.width = sizes[sizeClass];
        svg.style.height = sizes[sizeClass];
        svg.style.flexShrink = '0';
      }
      svg.innerHTML = content;
      node.replaceWith(svg);
    });
  }

  window.lucide = window.lucide || { createIcons };
  window.addEventListener('DOMContentLoaded', createIcons);
}());
