# 🐾 Zalia Security - Your AI Safety Companion

Welcome to Zalia, a comprehensive safety companion platform for Rivers State and beyond. Zalia combines AI-powered assistance with practical safety tools to keep you secure.

## ✨ Features

### 🤖 Zazi - AI Safety Companion
- 24/7 conversational AI assistant with safety expertise
- Understands 15+ safety domains (personal safety, phishing, fire safety, etc.)
- Friendly, bubbly personality with serious safety focus
- Local response system for offline functionality

### 🗺️ Smart Navigation
- Safer route planning around Port Harcourt
- Real-time traffic and security alerts
- Emergency location finder (police, hospitals, pharmacies)

### 📢 Live Incident Reporting
- Report security incidents in real-time
- View community safety reports
- Integrated incident mapping

### 🌐 Progressive Web App
- Works offline with cached content
- Install on home screen
- Dark/Light theme support
- Responsive design for all devices

### 🛡️ Security Features
- End-to-end support for emergency protocols
- Disguise mode for sensitive situations
- Offline-first architecture

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser with PWA support

### Installation

1. **Clone or download the repository**
   ```bash
   cd "Zalia website"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-key-here
   ```

4. **Run the Flask server**
   ```bash
   # Development mode
   python app.py
   
   # Or with environment variables
   set FLASK_ENV=development
   set OPENAI_API_KEY=your-api-key
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

---

## 📁 Project Structure

```
Zalia website/
├── app.py                  # Flask backend (improved with security & logging)
├── index.html             # Main landing page
├── ZaziAi.html           # Zazi AI chat interface
├── about.html            # About Zalia
├── contact.html          # Contact page
├── incidents.html        # Incident reporting
├── route-planner.html    # Route planner
├── simulator.html        # Safety simulator
├── style.css             # Global styles
├── sw.js                 # Service Worker (upgraded)
├── sw-register.js        # SW registration (enhanced)
├── manifest.json         # PWA manifest (improved)
├── requirements.txt      # Python dependencies (NEW)
├── .env.example         # Environment template (NEW)
└── images/              # Logo and assets
```

---

## 🔧 Configuration

### Backend Configuration

Edit `.env` to configure:
```env
OPENAI_API_KEY=your-key
FLASK_ENV=development
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

### Frontend Configuration

Theme preference is stored in `localStorage`:
- `zalia_theme` - 'light' or 'dark'

---

## 🌙 Features Overview

### Dark Mode
Automatically detects system preference. Toggle with theme button in header.

### Offline Support
Service Worker caches all core assets for offline functionality.

### Network Status
Automatic banner shows when connection is lost.

---

## 🔐 Security Improvements (v2.0)

✅ **Backend:**
- Security headers (CSP, X-Frame-Options, HSTS)
- Input sanitization and validation
- Rate limiting (20 requests/minute default)
- Proper error handling
- Request timeout (10 seconds)
- Logging system

✅ **Frontend:**
- Enhanced PWA meta tags
- Content Security Policy
- Secure external resource loading
- ARIA accessibility improvements

✅ **Service Worker:**
- Versioned caching strategy
- Network-first for APIs
- Cache-first for static assets
- Background sync support
- Push notification handler

---

## 📊 API Endpoints

### Chat Endpoint
```
POST /api/chat
Content-Type: application/json

{
  "message": "How do I stay safe in a taxi?"
}

Response:
{
  "reply": "Zazi's helpful response..."
}
```

### Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "openai_configured": true
}
```

---

## 🐛 Troubleshooting

### OpenAI Connection Issues
1. Verify `OPENAI_API_KEY` is set correctly
2. Check internet connection
3. Verify API key is active on OpenAI dashboard
4. Check rate limits haven't been exceeded

### Service Worker Not Working
1. HTTPS is required in production (not needed for localhost)
2. Clear browser cache and reload
3. Check browser console for registration errors
4. Unregister old versions: `navigator.serviceWorker.getRegistrations()`

### Dark Mode Not Persisting
1. Check if localStorage is enabled
2. Clear `zalia_theme` key and try again
3. Verify browser privacy settings

---

## 🚀 Performance Optimizations (v2.0)

- Resource prefetching for CDNs
- Optimized cache strategies in Service Worker
- Compressed code with Tailwind
- Lazy loading for images
- Minimal JavaScript bundle

---

## 📱 Mobile Optimization

- Mobile-first responsive design
- Touch-friendly interface
- Viewport fit for notch devices
- Native app-like experience

---

## 🎯 Future Roadmap

- [ ] Push notifications for emergency alerts
- [ ] Location-based safety recommendations
- [ ] Community safety heatmap
- [ ] Voice command support
- [ ] Biometric authentication
- [ ] Offline incident syncing
- [ ] Multi-language support
- [ ] Integration with emergency services API

---

## 💬 Support

For issues or questions:
1. Check the FAQ section in the app
2. Review the About page
3. Contact through the Contact page
4. Check GitHub issues (if applicable)

---

## 📄 License

Zalia Security © 2024. All rights reserved.

---

## 🙏 Acknowledgments

- Built with Flask, Tailwind CSS, and Lucide Icons
- AI powered by OpenAI
- Maps integration with Google Maps

---

**Stay safe. Stay smart. Zalia's got your back. 🐾✨**
