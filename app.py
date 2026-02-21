import re
import random
import streamlit as st

RULES = [

    # --- Greetings ---
    (
        re.compile(r'\b(hi|hello|hey|good morning|good afternoon|good evening|assalamualaikum|aoa|assalamoalaikum|yo|helloo)\b.*', re.IGNORECASE),
        [
            "Hello! Welcome to the Arts & Crafts assistant. What are you working on today?",
            "Hey there! Ready to get creative? Tell me about your craft project!",
            "Hi! I'm here to help with all things arts and crafts. What can I help you make?"
        ]
    ),

    # --- User introduces themselves ---
    (
        re.compile(r'my name is ([a-zA-Z]+)', re.IGNORECASE),
        ["Nice to meet you, {0}! What craft project are you working on today?"]
    ),

    # --- Asking for project ideas ---
    (
        re.compile(r'(give me|suggest|recommend|what are|any)\s*(some\s*)?(ideas?|projects?|activities?|things to (make|do|craft))', re.IGNORECASE),
        [
            "Here are some fun project ideas:\n  1. Watercolour greeting cards\n  2. Macrame wall hanging\n  3. Paper quilling art\n  4. Tie-dye tote bags\n  5. Origami animals\nWould you like instructions for any of these?",
            "You could try:\n  • Decoupage photo frames\n  • Friendship bracelet weaving\n  • Handmade candles\n  • Rock painting\n  • DIY journal covers\nWhich one interests you?"
        ]
    ),

    # --- How to / instructions for a specific craft ---
    (
        re.compile(r'how (do i|can i|to)\s+(make|do|create|start|begin|learn)\s+(.+)', re.IGNORECASE),
        [
            "Great choice! To get started with {2}, you will need the right materials first. Could you tell me your experience level: beginner, intermediate, or advanced?",
            "I'd love to walk you through {2}! Are you a complete beginner or have you tried something similar before?"
        ]
    ),

    # --- Painting ---
    (
        re.compile(r'\b(paint(ing)?|watercolou?r|acrylic|oil paint|canvas)\b', re.IGNORECASE),
        [
            "Painting is a wonderful craft! For beginners, acrylic paints are ideal because they dry quickly and are easy to clean up.",
            "Whether you prefer watercolour, acrylic, or oil, the key is to start with basic shapes and build up layers."
        ]
    ),

    # --- Thank you ---
    (
        re.compile(r'\b(thank(s| you)|thx|appreciate it|helpful)\b', re.IGNORECASE),
        [
            "You're very welcome! Happy crafting!",
            "My pleasure! Let me know if you need more help."
        ]
    ),

    # --- Goodbye ---
    (
        re.compile(r'\b(bye|goodbye|see you|quit|exit|done)\b', re.IGNORECASE),
        [
            "Goodbye! Happy crafting!",
            "See you later!"
        ]
    ),
]

# --- Fallback responses (when no pattern matches) ---
FALLBACKS = [
    "That's interesting! Could you tell me more about your arts and crafts project?",
    "I'm not sure I understood that. Could you rephrase?",
    "I'd love to help! Could you give me more detail about what you're trying to make?"
]

def respond(user_input: str) -> str:
    user_input = user_input.strip()

    for pattern, responses in RULES:
        match = pattern.search(user_input)
        if match:
            response_template = random.choice(responses)
            try:
                groups = match.groups(default='')
                response = response_template.format(*groups)
            except (IndexError, KeyError):
                response = response_template
            return response

    return random.choice(FALLBACKS)

st.title("Arts & Crafts ELIZA Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:")

if st.button("Send") and user_input:
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Bot", respond(user_input)))

for speaker, msg in st.session_state.chat:
    st.write(f"{speaker}: {msg}")