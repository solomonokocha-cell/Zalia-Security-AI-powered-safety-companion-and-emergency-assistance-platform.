import os
import logging
import time
import uuid
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    ENV_FILE,
    override=True
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    static_folder=".",
    static_url_path=""
)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-in-production"
)

app.config["GEMINI_API_KEY"] = os.getenv(
    "GEMINI_API_KEY"
)

app.config["GEMINI_MODEL"] = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

app.config["GEMINI_TEMPERATURE"] = float(
    os.getenv(
        "GEMINI_TEMPERATURE",
        "0.7"
    )
)

app.config["GEMINI_MAX_OUTPUT_TOKENS"] = int(
    os.getenv(
        "GEMINI_MAX_OUTPUT_TOKENS",
        "600"
    )
)

app.config["API_TIMEOUT"] = int(
    os.getenv(
        "API_TIMEOUT",
        "15"
    )
)

app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

app.config["JSON_SORT_KEYS"] = False


# ============================================================
# GEMINI
# ============================================================

API_KEY = app.config["GEMINI_API_KEY"]

client = None

if API_KEY:

    logger.info(
        "Gemini API key loaded successfully."
    )

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        logger.info(
            "Gemini client initialized successfully."
        )

    except Exception as e:

        logger.exception(
            "Failed to initialize Gemini client: %s",
            e
        )

        client = None

else:

    logger.warning(
        "GEMINI_API_KEY is not configured. "
        "Zazi AI features will be unavailable."
    )


# ============================================================
# CORS
# ============================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost",
                "http://127.0.0.1",
                "http://localhost:5000",
                "http://127.0.0.1:5000",
                "http://localhost:5500",
                "http://127.0.0.1:5500",
                "https://adel1aokocha.pythonanywhere.com"
            ],
            "methods": [
                "GET",
                "POST",
                "OPTIONS"
            ],
            "allow_headers": [
                "Content-Type",
                "X-Request-ID"
            ],
            "max_age": 3600
        }
    }
)


# ============================================================
# REQUEST ID
# ============================================================

@app.before_request
def attach_request_id():

    g.request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())
    )[:80]


# ============================================================
# SECURITY HEADERS
# ============================================================

@app.after_request
def set_security_headers(response):

    response.headers["X-Request-ID"] = getattr(
        g,
        "request_id",
        "unknown"
    )

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    response.headers["X-XSS-Protection"] = (
        "1; mode=block"
    )

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://cdn.tailwindcss.com "
        "https://unpkg.com "
        "https://www.gstatic.com "
        "https://www.googletagmanager.com; "
        "style-src 'self' 'unsafe-inline' "
        "https://cdn.tailwindcss.com; "
        "img-src 'self' data: blob: https:; "
        "font-src 'self' data: https:; "
        "connect-src 'self' "
        "https://adel1aokocha.pythonanywhere.com "
        "https:;"
    )

    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    return response


# ============================================================
# RATE LIMITING
# ============================================================

def rate_limit(
    max_requests=20,
    window_seconds=60
):

    requests_log = {}

    def decorator(func):

        @wraps(func)
        def wrapped(*args, **kwargs):

            client_ip = request.headers.get(
                "X-Forwarded-For",
                request.remote_addr or "unknown"
            ).split(",")[0].strip()

            now = time.time()

            if client_ip not in requests_log:
                requests_log[client_ip] = []

            requests_log[client_ip] = [
                request_time
                for request_time
                in requests_log[client_ip]
                if now - request_time < window_seconds
            ]

            if len(
                requests_log[client_ip]
            ) >= max_requests:

                logger.warning(
                    "Rate limit exceeded for %s",
                    client_ip
                )

                return jsonify({
                    "error": (
                        "Too many requests. "
                        "Please try again later."
                    ),
                    "request_id": g.request_id
                }), 429

            requests_log[
                client_ip
            ].append(now)

            return func(
                *args,
                **kwargs
            )

        return wrapped

    return decorator


# ============================================================
# ZAZI SYSTEM INSTRUCTION
# ============================================================

ZAZI_SYSTEM_INSTRUCTION = """
You are Zazi 🐾✨, the friendly AI safety companion inside
the Zalia Security application.

Your personality is:

- bubbly
- warm
- intelligent
- conversational
- helpful
- calm during emergencies
- safety-focused
- natural rather than robotic

You can discuss both safety topics and normal everyday topics.

IMPORTANT:

Never use generic fallback responses such as:

"My brain is wearing its curious little hat."

"Tell me a little more about what you mean."

"What are we exploring?"

"I haven't learned that one yet."

when the user's question is already clear.

Answer the actual question.

============================================================
WHAT ZALIA IS
============================================================

Zalia Security is a technology-based safety platform.

Its purpose is to bring useful safety tools and information
together in one accessible platform.

Zalia includes:

🐾 Zazi AI
AI-powered conversational safety assistance.

🚨 Emergency assistance
Access to emergency information and emergency resources.

📰 Incident reporting
Users can report and view security incidents through the
application's incident system.

🗺️ Smart navigation
Route-planning functionality designed to help users make
safer travel decisions.

🎯 Crisis simulation
Interactive scenarios that allow users to practice responses
to dangerous situations.

🔐 Online and scam safety
Information about phishing, scams, fraud, suspicious links,
ATM safety, POS safety and account security.

📱 Progressive Web App functionality
Zalia is designed to work across devices and can provide
an app-like experience through PWA technology.

🌐 Offline functionality
The application uses service-worker and caching technology
to provide offline access to supported parts of the platform.

============================================================
CURRENT INCIDENT DATA
============================================================

Zalia may provide you with incident information retrieved
from its Firebase Firestore incident system.

When CURRENT INCIDENT DATA is supplied:

- Use it when it is relevant to the user's question.
- Do not invent incident details.
- Clearly distinguish community reports from verified sources.
- Treat community-submitted incidents as reports, not confirmed facts.
- If the data does not contain the incident the user is asking about,
  say that the available Zalia incident feed does not contain
  enough information to verify it.
- Do not claim that an incident is live unless the supplied data
  indicates that it is recent/current.
- Do not pretend that you independently browsed the internet.
- If a user asks about a recent event and the supplied data
  does not verify it, explain that you cannot independently
  verify the latest details.

If an incident contains a source such as ReliefWeb / UN OCHA,
NEMA, FRSC, Nigeria Police or another supplied source, identify
that source when relevant.

============================================================
WHEN THE USER ASKS WHAT YOU CAN DO
============================================================

If the user asks:

"What can you do?"

"What can Zazi do?"

"What does Zazi do?"

"What are your features?"

"What can I ask you?"

Answer clearly.

For example:

"Quite a lot 😄🐾✨ I'm Zazi, the AI safety companion inside
Zalia Security.

I can help with:

🚨 Emergency and personal safety
🗺️ Safer travel and route planning
📰 Security and incident information
🎯 Crisis situations and response guidance
🔐 Phishing, scams, ATM and POS safety
🏠 Home and personal safety
🚗 Road and travel safety
📱 Using Zalia's safety features
💬 Normal questions, planning, ideas and everyday conversations

You can ask me about a safety situation, ask how something
works, or simply talk to me. 🐾✨"

Do NOT answer this question with a generic fallback.

============================================================
ZAZI MUST BE HONEST
============================================================

Do not claim that Zalia has a feature unless it actually
exists in the application.

Do not claim to have live information unless live information
has been supplied to you.

Do not pretend to have browsed the internet.

Do not invent current incidents, news, locations, casualties,
weather events or emergency information.

============================================================
EMERGENCY SAFETY
============================================================

If someone is in immediate danger:

1. Prioritize getting away from danger when possible.
2. Encourage contacting appropriate emergency services.
3. In Nigeria, the national emergency number is 112.
4. Keep instructions short, calm and practical.

Do not encourage dangerous behaviour.

============================================================
STYLE
============================================================

Keep normal answers reasonably concise.

Use emojis naturally.

Do not overuse headings.

Do not repeatedly introduce yourself.

Do not repeatedly say "I'm here to help."

Do not end every response with
"What else can I help you with?"

Sound like Zazi, not a customer-service bot.

You are Zazi 🐾✨ —
a smart, friendly companion who takes safety seriously.
"""


# ============================================================
# INPUT HELPERS
# ============================================================

def sanitize_input(
    text,
    max_length=2000
):

    if not isinstance(
        text,
        str
    ):
        return ""

    text = text.strip()

    return text[:max_length]


def normalize_history(history):

    if not isinstance(
        history,
        list
    ):
        return []

    normalized = []

    for item in history[-10:]:

        if not isinstance(
            item,
            dict
        ):
            continue

        if item.get("role") not in {
            "user",
            "assistant"
        }:
            continue

        content = sanitize_input(
            item.get(
                "content",
                ""
            )
        )

        if content:

            normalized.append({
                "role": item["role"],
                "content": content
            })

    return normalized


# ============================================================
# FIREBASE INCIDENT CONTEXT
# ============================================================

def normalize_incident_context(
    incident_context
):

    """
    Safely clean incident information received from
    ZaziAi.html.

    Firebase itself is accessed from the frontend.
    The backend only receives the relevant incident data.
    """

    if not isinstance(
        incident_context,
        list
    ):
        return []

    cleaned_incidents = []

    for incident in incident_context[:20]:

        if not isinstance(
            incident,
            dict
        ):
            continue

        incident_type = sanitize_input(
            incident.get(
                "type",
                ""
            ),
            150
        )

        location = sanitize_input(
            incident.get(
                "location",
                ""
            ),
            150
        )

        description = sanitize_input(
            incident.get(
                "description",
                ""
            ),
            600
        )

        timestamp = sanitize_input(
            str(
                incident.get(
                    "timestamp",
                    ""
                )
            ),
            100
        )

        source = sanitize_input(
            incident.get(
                "source",
                ""
            ),
            150
        )

        url = sanitize_input(
            incident.get(
                "url",
                ""
            ),
            500
        )

        if not (
            incident_type
            or location
            or description
        ):
            continue

        cleaned_incidents.append({
            "type": incident_type,
            "location": location,
            "description": description,
            "timestamp": timestamp,
            "source": source,
            "url": url
        })

    return cleaned_incidents


def build_incident_context(
    incidents
):

    if not incidents:

        return (
            "No live incident records were supplied by "
            "the Zalia incident system for this request.\n"
            "Do not invent current incident information."
        )

    lines = []

    for index, incident in enumerate(
        incidents,
        start=1
    ):

        line = (
            f"Incident {index}:\n"
            f"Type: {incident['type']}\n"
            f"Location: {incident['location']}\n"
            f"Description: {incident['description']}\n"
            f"Reported time: "
            f"{incident['timestamp'] or 'Unknown'}"
        )

        if incident["source"]:

            line += (
                f"\nSource: "
                f"{incident['source']}"
            )

        if incident["url"]:

            line += (
                f"\nSource URL: "
                f"{incident['url']}"
            )

        lines.append(
            line
        )

    return "\n\n".join(
        lines
    )


# ============================================================
# BUILT-IN ZAZI RESPONSES
# ============================================================

def get_builtin_response(
    message
):

    text = message.lower().strip()

    # --------------------------------------------------------
    # WHAT CAN YOU DO
    # --------------------------------------------------------

    capability_phrases = [
        "what can you do",
        "what can zazi do",
        "what does zazi do",
        "what can zazi help with",
        "what are your features",
        "what can i ask zazi",
        "what can i ask you",
        "what are you able to do",
        "what do you do"
    ]

    if any(
        phrase in text
        for phrase in capability_phrases
    ):

        return """
Quite a lot 😄🐾✨ I'm Zazi, the AI safety companion inside
Zalia Security.

I can help you with:

🚨 Emergency and personal safety
🗺️ Safer travel and route planning
📰 Security and incident information
🎯 Crisis situations and response guidance
🔐 Phishing, scams, ATM and POS safety
🏠 Home and personal safety
🚗 Road and travel safety
📱 Understanding and using Zalia's features
💬 Normal questions, ideas, planning and everyday conversations

Zalia is also a Progressive Web App, which means it can provide
an app-like experience on supported mobile devices, including
installation and offline functionality for supported content.

Basically, you can ask me a question, describe a situation,
or just talk to me. 🐾✨
""".strip()

    # --------------------------------------------------------
    # WHAT IS ZALIA
    # --------------------------------------------------------

    zalia_phrases = [
        "what is zalia",
        "what's zalia",
        "tell me about zalia",
        "explain zalia",
        "what does zalia do"
    ]

    if any(
        phrase in text
        for phrase in zalia_phrases
    ):

        return """
Zalia Security is a technology-based safety platform designed
to bring important safety tools together in one place. 🛡️🐾

It combines Zazi AI, emergency resources, incident reporting,
route planning, crisis simulation, online-safety guidance and
other practical safety tools.

Zalia is also built as a Progressive Web App, so it can provide
an app-like experience across devices and can be installed on
compatible devices. It also uses offline technology so some
supported features can remain available without an internet
connection.

The goal is simple:

Make useful safety information and practical safety tools easier
to access when people need them. 🐾✨
""".strip()

    return None


# ============================================================
# HOME
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    try:

        return send_from_directory(
            ".",
            "index.html"
        )

    except Exception as e:

        logger.error(
            "Error serving home page: %s",
            e
        )

        return jsonify({
            "error": "Page not found"
        }), 404


# ============================================================
# ZAZI PAGE
# ============================================================

@app.route(
    "/zazi",
    methods=["GET"]
)
@app.route(
    "/ZaziAi.html",
    methods=["GET"]
)
def zazi_page():

    try:

        return send_from_directory(
            ".",
            "ZaziAi.html"
        )

    except Exception as e:

        logger.error(
            "Error serving Zazi page: %s",
            e
        )

        return jsonify({
            "error": "Page not found"
        }), 404


# ============================================================
# CHAT API
# ============================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
@rate_limit(
    max_requests=20,
    window_seconds=60
)
def chat():

    try:

        data = request.get_json(
            silent=True
        )

        if data is None:
            data = {}

        if not isinstance(
            data,
            dict
        ):

            return jsonify({
                "error": (
                    "Request body must be a JSON object"
                ),
                "request_id": g.request_id
            }), 400

        # ====================================================
        # USER MESSAGE
        # ====================================================

        user_message = data.get(
            "message",
            ""
        )

        if not isinstance(
            user_message,
            str
        ):

            user_message = ""

        user_message = (
            user_message.strip()[:2000]
        )

        if not user_message:

            return jsonify({
                "reply": (
                    "🐾 Please type a message for Zazi."
                ),
                "type": "text",
                "source": "local",
                "request_id": g.request_id
            }), 200

        # ====================================================
        # CONVERSATION HISTORY
        # ====================================================

        conversation = normalize_history(
            data.get(
                "history",
                []
            )
        )

        # ====================================================
        # LIVE FIREBASE INCIDENT CONTEXT
        # ====================================================

        incident_context = (
            normalize_incident_context(
                data.get(
                    "incident_context",
                    []
                )
            )
        )

        incident_context_text = (
            build_incident_context(
                incident_context
            )
        )

        logger.info(
            "Received %s incident records for Zazi. "
            "Request ID: %s",
            len(incident_context),
            g.request_id
        )

        # ====================================================
        # BUILT-IN RESPONSES FIRST
        # ====================================================

        builtin_reply = get_builtin_response(
            user_message
        )

        if builtin_reply:

            logger.info(
                "Built-in Zazi response used. "
                "Request ID: %s",
                g.request_id
            )

            return jsonify({
                "reply": builtin_reply,
                "type": "text",
                "source": "builtin",
                "incident_context_used": False,
                "request_id": g.request_id
            }), 200

        # ====================================================
        # GEMINI CONFIGURATION CHECK
        # ====================================================

        if not client:

            logger.error(
                "Gemini client is not configured."
            )

            return jsonify({
                "reply": (
                    "⚠️ Zazi's AI connection isn't configured "
                    "right now. Please check the Gemini API key."
                ),
                "request_id": g.request_id
            }), 503

        # ====================================================
        # ZAZI REQUEST
        # ====================================================

        contents = []

        for message in conversation:

            role = message["role"]

            content = message["content"]

            gemini_role = (
                "model"
                if role == "assistant"
                else "user"
            )

            contents.append(
                types.Content(
                    role=gemini_role,
                    parts=[
                        types.Part(
                            text=content
                        )
                    ]
                )
            )

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=user_message
                    )
                ]
            )
        )

        full_system_instruction = (
            ZAZI_SYSTEM_INSTRUCTION
            + "\n\n"
            + "================================================\n"
            + "CURRENT ZALIA INCIDENT DATA\n"
            + "================================================\n\n"
            + "The following incident records were supplied "
            + "by Zalia's Firebase Firestore incident feed.\n\n"
            + incident_context_text
            + "\n\n"
            + "Use these records only when relevant to the "
            + "user's question. Do not invent details that "
            + "are not present in these records."
        )

        response = client.models.generate_content(

            model=app.config[
                "GEMINI_MODEL"
            ],

            contents=contents,

            config=types.GenerateContentConfig(

                system_instruction=(
                    full_system_instruction
                ),

                temperature=app.config[
                    "GEMINI_TEMPERATURE"
                ],

                max_output_tokens=app.config[
                    "GEMINI_MAX_OUTPUT_TOKENS"
                ]
            )
        )

        reply = (
            getattr(
                response,
                "text",
                ""
            )
            or ""
        ).strip()

        if not reply:

            logger.error(
                "Gemini returned an empty response. "
                "Request ID: %s",
                g.request_id
            )

            return jsonify({
                "reply": (
                    "Zazi didn't receive a complete answer. "
                    "Please try again."
                ),
                "request_id": g.request_id
            }), 502

        logger.info(
            "Zazi AI response generated successfully. "
            "Incident records supplied: %s. "
            "Request ID: %s",
            len(incident_context),
            g.request_id
        )

        return jsonify({

            "reply": reply,

            "type": "text",

            "source": "ai",

            "incident_context_used": (
                len(incident_context) > 0
            ),

            "incident_count": len(
                incident_context
            ),

            "request_id": g.request_id

        }), 200

    # ========================================================
    # ERRORS
    # ========================================================

    except Exception as e:

        error_text = str(e).lower()

        logger.exception(
            "Unexpected error in Gemini chat endpoint: %s",
            e
        )

        # ----------------------------------------------------
        # GEMINI RATE LIMIT / QUOTA
        # ----------------------------------------------------

        if (
            "429" in error_text
            or "resource exhausted" in error_text
            or "quota" in error_text
            or "rate limit" in error_text
        ):

            logger.warning(
                "Gemini rate limit or quota reached. "
                "Request ID: %s",
                g.request_id
            )

            return jsonify({
                "reply": (
                    "Zazi's AI service is temporarily busy. 😅🐾 "
                    "Please try again in a moment."
                ),
                "request_id": g.request_id
            }), 503

        # ----------------------------------------------------
        # GEMINI CONNECTION ERROR
        # ----------------------------------------------------

        if (
            "connection" in error_text
            or "connect" in error_text
            or "timeout" in error_text
        ):

            logger.error(
                "Could not connect to Gemini. "
                "Request ID: %s",
                g.request_id
            )

            return jsonify({
                "reply": (
                    "🐾 I can't reach Zazi's AI brain right now. "
                    "Please check your internet connection and "
                    "try again."
                ),
                "request_id": g.request_id
            }), 503

        # ----------------------------------------------------
        # GEMINI API ERROR
        # ----------------------------------------------------

        return jsonify({
            "reply": (
                "Oops! 😭🐾 Zazi had trouble processing that. "
                "Please try again."
            ),
            "request_id": g.request_id
        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health_check():

    return jsonify({

        "status": "healthy",

        "gemini_configured": (
            client is not None
        ),

        "firebase_incident_bridge": True,

        "request_id": g.request_id

    }), 200


# ============================================================
# READINESS CHECK
# ============================================================

@app.route(
    "/api/ready",
    methods=["GET"]
)
def readiness_check():

    ai_ready = client is not None

    return jsonify({

        "status": (
            "ready"
            if ai_ready
            else "degraded"
        ),

        "services": {

            "api": "ready",

            "ai": (
                "ready"
                if ai_ready
                else "not_configured"
            ),

            "incident_context": "ready"

        },

        "request_id": g.request_id

    })


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "error": "Resource not found",

        "request_id": getattr(
            g,
            "request_id",
            "unknown"
        )

    }), 404


# ============================================================
# 500
# ============================================================

@app.errorhandler(500)
def internal_error(error):

    logger.error(
        "Internal server error: %s",
        error
    )

    return jsonify({

        "error": "Internal server error",

        "request_id": getattr(
            g,
            "request_id",
            "unknown"
        )

    }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    host = os.getenv(
        "FLASK_HOST",
        "127.0.0.1"
    )

    port = int(
        os.getenv(
            "FLASK_PORT",
            "5000"
        )
    )

    debug = (
        os.getenv(
            "FLASK_ENV",
            "development"
        )
        == "development"
    )

    logger.info(
        "Starting Zalia app on %s:%s",
        host,
        port
    )

    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )