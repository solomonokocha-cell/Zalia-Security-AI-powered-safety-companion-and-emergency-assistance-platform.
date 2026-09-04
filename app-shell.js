(() => {
  function addSimulatorShell() {
    if (document.querySelector('.app-frame')) return;

    const content = document.createElement('div');
    content.className = 'simulator-content';
    while (document.body.firstChild) content.appendChild(document.body.firstChild);

    const shell = document.createElement('div');
    shell.className = 'app-frame universal-app-frame';

    const sidebar = document.createElement('aside');
    sidebar.className = 'desktop-sidebar universal-sidebar';
    sidebar.innerHTML = `
      <div class="universal-sidebar-top">
        <a class="universal-brand" href="index.html">
          <img src="images/zalia-app-icon.png" alt="Zalia">
          <span><strong>ZALIA</strong><small>Safety command centre</small></span>
        </a>
        <p class="universal-sidebar-label">Navigation</p>
        <nav class="universal-nav">
          <a href="index.html">🏠 <span>Home</span></a>
          <a href="simulator.html">⚡ <span>Crisis Simulator</span></a>
          <a href="incidents.html">🚨 <span>Incident Reports</span></a>
          <a href="ZaziAi.html">🤖 <span>Zazi AI</span></a>
          <a href="route-planner.html">🗺️ <span>Route Planner</span></a>
          <a href="about.html">ℹ️ <span>About Zalia</span></a>
          <a href="contact.html">📞 <span>Emergency Contacts</span></a>
        </nav>
      </div>
      <a class="universal-emergency" href="tel:112">☎ <span>Emergency 112</span></a>`;

    shell.append(sidebar, content);
    document.body.appendChild(shell);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addSimulatorShell, { once: true });
  } else {
    addSimulatorShell();
  }
})();
