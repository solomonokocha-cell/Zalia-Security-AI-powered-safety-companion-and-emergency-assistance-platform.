# Zalia Security - API Documentation

## Overview

Zalia Security provides a REST API for interacting with the Zazi AI assistant and accessing safety features.

**Base URL:** `http://localhost:5000`

---

## Authentication

Currently, no authentication is required. In production, implement API key authentication or OAuth.

---

## Endpoints

### 1. Chat with Zazi AI

**Endpoint:** `POST /api/chat`

**Description:** Send a message to Zazi and receive a safety-focused response.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "How do I stay safe in a taxi?",
  "history": [
    {"role": "user", "content": "I am travelling tonight."},
    {"role": "assistant", "content": "Share your route with someone you trust."}
  ]
}
```

`history` is optional. The API accepts only the last 10 `user` or `assistant` messages and limits each message to 2,000 characters.

**Response (200 OK):**
```json
{
  "reply": "🚕 **TRANSPORT SAFETY!** 🐾🛡️\n\nBefore getting into a vehicle:\n\n👀 Check the vehicle and driver...",
  "type": "text",
  "request_id": "a request trace identifier"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "No message provided"
}
```

**Response (429 Too Many Requests):**
```json
{
  "error": "Too many requests. Please try again later."
}
```

**Response (503 Service Unavailable):**
```json
{
  "reply": "Zazi's OpenAI connection isn't configured. Please set OPENAI_API_KEY."
}
```

**Rate Limiting:**
- Default: 20 requests per 60 seconds per IP address
- Production: 10 requests per 60 seconds

**Example Usage (JavaScript):**
```javascript
async function chatWithZazi(message) {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(data.reply);
  } catch (error) {
    console.error('Chat error:', error);
  }
}

// Usage
chatWithZazi('What should I do in a fire?');
```

**Example Usage (Python):**
```python
import requests

def chat_with_zazi(message):
    url = 'http://localhost:5000/api/chat'
    payload = {'message': message}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        print(data['reply'])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Usage
chat_with_zazi('How do I stay safe during a fire?')
```

**Example Usage (cURL):**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Is phishing dangerous?"}'
```

---

### 2. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if the API is running and if OpenAI is configured.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "openai_configured": true
}
```

### 3. Readiness Check

**Endpoint:** `GET /api/ready`

**Description:** Reports whether the API and optional AI provider are configured.

The endpoint returns `200 OK` for both ready and degraded states so monitoring can distinguish an available API from an unconfigured AI provider:

```json
{
  "status": "ready",
  "services": {
    "api": "ready",
    "ai": "ready"
  },
  "request_id": "a request trace identifier"
}
```

**Example Usage (JavaScript):**
```javascript
async function checkHealth() {
  const response = await fetch('/api/health');
  const data = await response.json();
  console.log(data.status); // "healthy"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": "Error message",
  "status": 400
}
```

### Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check request format and required fields |
| 429 | Rate Limited | Wait before making another request |
| 500 | Server Error | Check server logs, retry later |
| 503 | Service Unavailable | OpenAI API not configured or offline |

---

## Message Categories

Zazi can help with these safety topics:

### Personal Safety
- General safety advice
- Threat assessment
- Emergency protocols

### Travel Safety
- Taxi/transport safety
- Route planning
- Night travel tips

### Phishing & Scams
- Identifying phishing
- Scam prevention
- Online security

### Fire Safety
- Fire extinguisher use
- Evacuation procedures
- Fire prevention

### ATM/POS Safety
- PIN protection
- Card safety
- Transaction security

### Emergency Response
- Gunshot safety
- Medical emergencies
- Natural disasters

### Location Services
- Finding police stations
- Hospital locator
- Pharmacy finder

---

## Response Types

### Text Response
Standard text response from Zazi:
```json
{
  "reply": "Response text",
  "type": "text"
}
```

### Quick Links
Maps links for locations:
```
[MAP:Find Police Stations](https://www.google.com/maps/search/police+stations)
```

---

## Best Practices

1. **Sanitize Input:**
   - Input is automatically sanitized server-side
   - Limit message length to 2000 characters

2. **Error Handling:**
   - Always check response status codes
   - Implement retry logic with exponential backoff

3. **Rate Limiting:**
   - Implement client-side rate limiting
   - Cache frequently asked questions

4. **Offline Support:**
   - Service Worker caches responses
   - Provide fallback responses offline

5. **Security:**
   - Use HTTPS in production
   - Implement API key authentication
   - Add request validation

---

## Webhooks (Future)

Future versions will support webhooks for:
- Emergency alerts
- Incident updates
- User notifications

---

## Version History

### v2.0 (Current)
- ✅ Rate limiting
- ✅ Security headers
- ✅ Input sanitization
- ✅ Health check endpoint
- ✅ Improved error handling
- ✅ Logging system

### v1.0 (Previous)
- Basic chat endpoint
- OpenAI integration

---

## Rate Limit Headers

The API includes rate limit information in response headers:

```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 19
X-RateLimit-Reset: 1234567890
```

---

## Troubleshooting

### "Too many requests" error
- Implement exponential backoff in your client
- Distribute requests over time
- Contact support if limits are too restrictive

### "OpenAI not configured"
- Set `OPENAI_API_KEY` environment variable
- Verify key is valid on OpenAI dashboard

### Connection timeout
- Increase client timeout
- Check server logs for performance issues

---

## Future Enhancements

- [ ] Batch message endpoint
- [ ] Streaming responses
- [ ] User history
- [ ] Conversation context
- [ ] Custom safety profiles
- [ ] Location-based responses
- [ ] Multi-language support
- [ ] Voice API integration

---

## Support

For API issues or questions:
1. Check logs: `tail -f app.log`
2. Verify environment setup
3. Test with cURL or Postman
4. Check GitHub issues
5. Contact support team

---

**Stay safe. Use the API responsibly. 🐾✨**
