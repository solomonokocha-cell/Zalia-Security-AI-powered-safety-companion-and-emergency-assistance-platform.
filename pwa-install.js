```javascript
(function () {
  let installPrompt = null;

  const buttons = () =>
    document.querySelectorAll('[data-install-zalia]');

  const status = () =>
    document.querySelectorAll('[data-install-status]');

  function setInstallVisible(message) {
    buttons().forEach(button => {
      button.classList.remove('hidden');
      button.removeAttribute('aria-hidden');
    });

    status().forEach(node => {
      node.textContent =
        message || 'Install Zalia for faster access and offline support.';
    });
  }

  function setInstallHidden() {
    buttons().forEach(button => {
      button.classList.add('hidden');
      button.setAttribute('aria-hidden', 'true');
    });
  }

  function setStatus(message) {
    status().forEach(node => {
      node.textContent = message;
    });
  }

  /*
   * Chrome / Edge / supported browsers fire this event when
   * Zalia satisfies the browser's PWA installation requirements.
   */
  window.addEventListener('beforeinstallprompt', event => {
    console.log('[Zalia PWA] beforeinstallprompt fired');

    // Prevent the browser from showing its automatic prompt.
    // We will show it when the user presses the Zalia install button.
    event.preventDefault();

    installPrompt = event;

    setInstallVisible(
      'Install Zalia on this device for quick access and offline support.'
    );
  });

  /*
   * Fired after Zalia has successfully been installed.
   */
  window.addEventListener('appinstalled', () => {
    console.log('[Zalia PWA] Zalia was installed');

    installPrompt = null;

    setInstallHidden();

    setStatus('Zalia is installed on this device. 🐾💗');
  });

  /*
   * Check whether Zalia is already running as an installed app.
   */
  function isStandalone() {
    return (
      window.matchMedia &&
      window.matchMedia('(display-mode: standalone)').matches
    ) ||
    window.navigator.standalone === true;
  }

  /*
   * Called by the Install Zalia button.
   */
  window.installZaliaPWA = async function () {
    console.log('[Zalia PWA] Install button clicked');

    /*
     * If Zalia is already installed, don't show an installation
     * prompt again.
     */
    if (isStandalone()) {
      setInstallHidden();
      setStatus('Zalia is already installed on this device. 🐾💗');
      return;
    }

    /*
     * If the browser gave us a real installation prompt,
     * launch it.
     */
    if (installPrompt) {
      try {
        installPrompt.prompt();

        const choice = await installPrompt.userChoice;

        console.log(
          '[Zalia PWA] User installation choice:',
          choice.outcome
        );

        /*
         * The beforeinstallprompt event can only be used once.
         */
        installPrompt = null;

        if (choice.outcome === 'accepted') {
          setStatus('Installing Zalia... 🐾📱');
        } else {
          setStatus(
            'No problem! You can install Zalia anytime from your browser menu.'
          );
        }
      } catch (error) {
        console.error(
          '[Zalia PWA] Installation prompt failed:',
          error
        );

        installPrompt = null;

        setStatus(
          'Use your browser menu and choose “Install Zalia” or “Add to Home screen”.'
        );
      }

      return;
    }

    /*
     * Some browsers do not expose beforeinstallprompt.
     * In that situation, guide the user to the browser's
     * built-in installation option.
     */
    setStatus(
      'Use your browser menu and choose “Install Zalia” or “Add to Home screen”.'
    );

    setInstallVisible(
      'Zalia can be installed from your browser menu. 🐾📱'
    );
  };

  /*
   * Set up the page after the HTML has loaded.
   */
  document.addEventListener('DOMContentLoaded', () => {
    /*
     * If the page is already running as an installed PWA,
     * don't show the install button.
     */
    if (isStandalone()) {
      setInstallHidden();
      setStatus('Zalia is installed on this device. 🐾💗');
      return;
    }

    /*
     * Show the button so users can access installation.
     * If beforeinstallprompt fires later, the button will
     * automatically become connected to the native prompt.
     */
    setInstallVisible(
      'Install Zalia for faster access and offline support.'
    );
  });
})();
```
