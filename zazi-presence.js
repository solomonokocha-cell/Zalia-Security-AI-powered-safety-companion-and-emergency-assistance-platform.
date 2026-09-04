(function () {
  const FACT_STORAGE_KEY = 'zaliaSeenSafetyFacts';
  const FACT_LAUNCH_KEY = 'zaliaFactLaunchCount';
  const FACT_DAILY_KEY = 'zaliaDailySafetyFact';
  const FACT_SHOWN_KEY = 'zaliaSafetyFactShownDate';
  const FACT_COUNT = 100000;

  const factOpeners = [
    'A simple safety habit:', 'Quick safety fact:', 'Zazi tip:', 'Good to know:',
    'Small step, big difference:', 'Safety brain note:', 'Everyday safety fact:',
    'A calm reminder:'
  ];

  const factActions = [
    'Pause and check your surroundings', 'Tell someone you trust', 'Keep your phone charged',
    'Choose a well-lit public place', 'Verify the information first', 'Keep an exit in mind',
    'Save the important number', 'Trust your instincts and slow down', 'Use a recognised service',
    'Share your plan before leaving'
  ];

  const factContexts = [
    'before travelling at night', 'when receiving an urgent message', 'before using an ATM',
    'when entering a taxi', 'during heavy traffic', 'when meeting someone new',
    'before sharing your location', 'when a situation feels unusual', 'during severe weather',
    'when your battery is running low', 'before opening an unfamiliar link', 'when walking alone',
    'before leaving home', 'when helping another person', 'during an emergency'
  ];

  const factResults = [
    'It gives you more time to make a clear decision.', 'It reduces the chance of being rushed into a mistake.',
    'It helps a trusted person support you quickly.', 'It keeps a safer option available.',
    'It protects your personal information.', 'It makes it easier to get help if plans change.',
    'It helps you notice warning signs early.', 'It keeps your choices calm and practical.'
  ];

  function getFact(index) {
    const opener = factOpeners[Math.floor(index / 12500) % factOpeners.length];
    const action = factActions[Math.floor(index / 1250) % factActions.length];
    const context = factContexts[Math.floor(index / 83) % factContexts.length];
    const result = factResults[index % factResults.length];
    return `${opener} ${action} ${context}. ${result}`;

  }

  function getNextLaunchNumber() {
    const savedCount = Number.parseInt(localStorage.getItem(FACT_LAUNCH_KEY) || '0', 10);
    const launchNumber = Number.isFinite(savedCount) && savedCount >= 0 ? savedCount + 1 : 1;
    localStorage.setItem(FACT_LAUNCH_KEY, String(launchNumber));
    return launchNumber;
  }

  function getNextFact() {
    const today = new Date().toLocaleDateString('en-CA');
    try {
      const dailyFact = JSON.parse(localStorage.getItem(FACT_DAILY_KEY) || 'null');
      if (dailyFact && dailyFact.date === today && Number.isInteger(dailyFact.index)) {
        return { index: dailyFact.index, text: getFact(dailyFact.index), remaining: null };
      }
    } catch (error) {
      localStorage.removeItem(FACT_DAILY_KEY);
    }

    let seen = [];
    try {
      seen = JSON.parse(localStorage.getItem(FACT_STORAGE_KEY) || '[]');
    } catch (error) {
      seen = [];
    }

    if (!Array.isArray(seen)) seen = [];
    const seenSet = new Set(seen);
    if (seenSet.size >= FACT_COUNT) {
      seenSet.clear();
    }

    let index = Math.floor(Math.random() * FACT_COUNT);
    while (seenSet.has(index)) index = (index + 1) % FACT_COUNT;
    seenSet.add(index);
    localStorage.setItem(FACT_STORAGE_KEY, JSON.stringify([...seenSet]));
    localStorage.setItem(FACT_DAILY_KEY, JSON.stringify({ date: today, index }));
    return { index, text: getFact(index), remaining: FACT_COUNT - seenSet.size };
  }

  function showSafetyFact() {
    const fact = getNextFact();
    const launchNumber = getNextLaunchNumber();
    const dialog = document.createElement('div');
    dialog.className = 'zalia-fact-dialog';
    dialog.setAttribute('role', 'dialog');
    dialog.setAttribute('aria-modal', 'true');
    dialog.setAttribute('aria-labelledby', 'zaliaFactTitle');
    dialog.innerHTML = `<div class="zalia-fact-card"><div id="zaliaFactTitle" class="zalia-fact-kicker">Zalia fun fact ${launchNumber}</div><p class="zalia-fact-text">${fact.text}</p><button type="button" class="zalia-fact-close">Got it</button></div>`;
    document.body.appendChild(dialog);

    const close = () => dialog.remove();
    dialog.querySelector('.zalia-fact-close').addEventListener('click', close);
    dialog.addEventListener('click', event => {
      if (event.target === dialog) close();
    });
    document.addEventListener('keydown', function escapeFact(event) {
      if (event.key === 'Escape') {
        close();
        document.removeEventListener('keydown', escapeFact);
      }
    });
  }

  function updateZaziPresence() {
    const hour = new Date().getHours();
    const isLate = hour >= 22 || hour < 6;
    let presence = document.getElementById('zaliaPageZazi');

    if (!presence && !document.querySelector('img[src*="zaziimage"]')) {
      presence = document.createElement('div');
      presence.id = 'zaliaPageZazi';
      presence.className = 'zalia-page-zazi';
      presence.innerHTML = '<img src="images/zaziimage.png" alt="Zazi" class="zalia-page-zazi-avatar"><span class="zalia-page-zazi-badge" aria-label="Zazi is sleepy">😴</span><span class="zalia-page-zazi-label">Zazi is here</span>';
      document.body.appendChild(presence);
    }

    if (!presence) return;
    presence.classList.toggle('zalia-page-zazi-sleepy', isLate);
    const badge = presence.querySelector('.zalia-page-zazi-badge');
    const label = presence.querySelector('.zalia-page-zazi-label');
    if (badge) badge.hidden = !isLate;
    if (label) label.textContent = isLate ? 'Zazi is sleepy' : 'Zazi is here';
  }

  function startZaliaPresence() {
    updateZaziPresence();
    const isHomePage = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html');
    const today = new Date().toLocaleDateString('en-CA');
    if (isHomePage && localStorage.getItem(FACT_SHOWN_KEY) !== today) {
      localStorage.setItem(FACT_SHOWN_KEY, today);
      window.setTimeout(showSafetyFact, 350);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startZaliaPresence, { once: true });
  } else {
    startZaliaPresence();
  }
  window.setInterval(updateZaziPresence, 60000);
}());
