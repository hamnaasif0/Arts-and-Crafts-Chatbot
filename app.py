# ============================================================
# Name: Hamna Asif
# Roll No: 16
# Assignment: Part A - Arts & Crafts ELIZA Chatbot (Streamlit)
# ============================================================

import re
import random
import streamlit as st

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="🎨 Arts & Crafts Chatbot",
    page_icon="🎨",
    layout="centered"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp { background-color: #fdf6f0; }

    /* Title */
    .chat-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #6b3f2a;
        margin-bottom: 0rem;
    }
    .chat-subtitle {
        text-align: center;
        font-size: 0.95rem;
        color: #a0735a;
        margin-bottom: 1.2rem;
    }

    /* Chat bubbles */
    .bubble-user {
        background: #6b3f2a;
        color: white;
        padding: 10px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 78%;
        margin-left: auto;
        font-size: 0.93rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .bubble-bot {
        background: #fff3eb;
        color: #3d1f0f;
        padding: 10px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 78%;
        margin-right: auto;
        font-size: 0.93rem;
        line-height: 1.5;
        border: 1px solid #e8c9b0;
        word-wrap: break-word;
    }
    .label-user {
        text-align: right;
        font-size: 0.72rem;
        color: #a0735a;
        margin-bottom: 2px;
    }
    .label-bot {
        text-align: left;
        font-size: 0.72rem;
        color: #a0735a;
        margin-bottom: 2px;
    }

    /* Divider */
    .chat-divider {
        border: none;
        border-top: 1px solid #e8c9b0;
        margin: 0.8rem 0;
    }

    /* Input box styling */
    .stTextInput > div > div > input {
        border-radius: 24px;
        border: 1.5px solid #c9956d;
        padding: 10px 18px;
        background: #fff;
        font-size: 0.93rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6b3f2a;
        box-shadow: 0 0 0 2px #f0d5c0;
    }

    /* Send button */
    .stButton > button {
        border-radius: 24px;
        background: #6b3f2a;
        color: white;
        border: none;
        padding: 10px 28px;
        font-size: 0.93rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background: #a0735a;
    }

    /* Quick suggestion chips */
    .chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0 1rem 0; }
    .chip {
        background: #fff3eb;
        border: 1px solid #c9956d;
        color: #6b3f2a;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.8rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


# ── RULES ────────────────────────────────────────────────────
RULES = [

    # Greetings
    (re.compile(r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b', re.IGNORECASE), [
        "Hello! 🎨 Welcome to the Arts & Crafts assistant. What are you working on today?",
        "Hey there! Ready to get creative? Tell me about your craft project!",
        "Hi! I'm here to help with all things arts and crafts. What can I help you make?"
    ]),

    # Name introduction
    (re.compile(r'my name is ([a-zA-Z]+)', re.IGNORECASE), [
        "Nice to meet you, {0}! 😊 What craft are you interested in today?",
        "Hello {0}! Great to have you here. Are you working on a project or just looking for ideas?"
    ]),

    # What can you do
    (re.compile(r'(what can you (do|help with|help me with)|what do you (know|do)|your (skills|capabilities))', re.IGNORECASE), [
        "I specialise in Arts & Crafts guidance! 🎨 I can help you with:\n• Project ideas (painting, knitting, origami, macramé…)\n• Step-by-step craft instructions\n• Materials and supply lists\n• Painting techniques (acrylics, oils, watercolour, portraits…)\n• Colour theory and mixing tips\n• Budget-friendly ideas\n• Kids' crafts\nWhat would you like help with?"
    ]),

    # Project ideas
    (re.compile(r'(give me|suggest|recommend|what are|any)\s*(some\s*)?(ideas?|projects?|activities?|things to (make|do|craft))', re.IGNORECASE), [
        "Here are some fun project ideas! 🌟\n1. Watercolour greeting cards\n2. Acrylic pour painting\n3. Macramé wall hanging\n4. Paper quilling art\n5. Tie-dye tote bags\n6. Portrait sketching\nWould you like instructions for any of these?",
        "You could try:\n• Decoupage photo frames\n• Friendship bracelet weaving\n• Handmade soy candles\n• Rock painting\n• Linocut printmaking\nWhich one interests you?"
    ]),

    # How-to
    (re.compile(r'how (do i|can i|to)\s+(make|do|create|start|begin|learn|paint|draw|sketch)\s+(.+)', re.IGNORECASE), [
        "Great choice! 🖌️ To get started with {2}, you'll need the right materials first. Are you a beginner, intermediate, or advanced crafter?",
        "I'd love to walk you through {2}! Have you tried anything similar before, or is this brand new for you?"
    ]),

    # Materials
    (re.compile(r'(what|which)\s+(materials?|supplies?|tools?|things?)\s+(do i need|should i (get|buy|use)|are needed)\s*(for\s*(.+))?', re.IGNORECASE), [
        "Great question! The supplies depend on the specific project. Could you tell me which craft you're planning so I can give you a precise list?",
        "For most craft projects you'll need basic tools (scissors, glue, brushes) plus craft-specific materials. What are you making?"
    ]),

    # ── PAINTING — ACRYLICS (before generic painting rule) ──
    (re.compile(r'\b(acrylic(s)?|acrylic paint(ing)?|acrylic colour)\b', re.IGNORECASE), [
        "Acrylics are fantastic — fast-drying, versatile, and beginner-friendly! 🎨\n• Use a palette to mix colours before applying\n• Thin with water for watercolour-like washes, or use a medium for glazing\n• Work light to dark — acrylics dry slightly darker\n• A flat brush for backgrounds, a round brush for details\nAre you doing a specific style — abstract, portrait, landscape?",
        "Great choice with acrylics! Tips for success:\n✓ Keep brushes wet while working so paint doesn't dry on them\n✓ Use gesso to prime your canvas first\n✓ Experiment with palette knives for textured effects\nWhat are you planning to paint?"
    ]),

    # ── PORTRAIT PAINTING ──
    (re.compile(r'\b(portrait(s)?|portrait paint(ing)?|paint(ing)? (a |the )?face|figure paint(ing)?|human figure|face paint(ing)?)\b', re.IGNORECASE), [
        "Portrait painting is so rewarding! 🖼️ Here are the key steps:\n1. Lightly sketch the face proportions first — eyes sit at the midpoint of the head\n2. Block in main shadow and light areas before adding detail\n3. Work on the eyes last — they bring the portrait to life\n4. Use warm tones (yellow ochre, burnt sienna) for skin, cooled with blues in shadow areas\nAre you working from a photo reference or life?",
        "For portraits, the golden rules are:\n• Get the proportions right first — use the 'envelope' sketch method\n• Mix skin tones from red, yellow, white, and a touch of blue (not brown straight from the tube!)\n• Paint loosely — tight overworked portraits lose life\n• Study light direction — one strong light source makes everything easier\nAre you using oil, acrylic, or watercolour for your portrait?"
    ]),

    # ── OIL PAINTING ──
    (re.compile(r'\b(oil paint(ing)?|oils|linseed oil|oil colour)\b', re.IGNORECASE), [
        "Oil painting has a beautiful richness to it! 🖌️ Key things to know:\n• Work 'fat over lean' — earlier layers use less oil, later layers more\n• Drying takes days to weeks — use alkyd mediums to speed it up\n• Use turpentine or odourless solvent to thin paint and clean brushes\n• Titanium white is your best friend for mixing\nAre you a complete beginner with oils or have you painted before?",
        "Oils are the classic master's medium! Tips:\n✓ Start with an underpainting (thinned burnt umber or raw umber)\n✓ Block in big shapes first, refine later\n✓ Keep a limited palette at first: cad yellow, cad red, ultramarine blue, titanium white, burnt umber\nWhat subject are you planning to paint?"
    ]),

    # ── WATERCOLOUR ──
    (re.compile(r'\b(watercolou?r(s)?|watercolou?r paint(ing)?)\b', re.IGNORECASE), [
        "Watercolour is such a beautiful, expressive medium! 💧\n• Always work light to dark — you can't paint light over dark in watercolour\n• Let layers dry fully before adding the next wash\n• Use wet-on-wet for soft blends, wet-on-dry for sharp edges\n• Cold-pressed paper (140 lb / 300 gsm) is the best for beginners\nWhat are you planning to paint — landscapes, florals, portraits?",
        "Watercolour tips:\n✓ Don't overwork a wash — two passes max before it lifts and goes muddy\n✓ Tilt your board at 15° to let washes flow naturally\n✓ Use a large round brush (size 10–12) for washes, a fine liner for details\nAre you just starting out with watercolour?"
    ]),

    # ── SKETCHING / DRAWING ──
    (re.compile(r'\b(sketch(ing)?|draw(ing)?|pencil art|charcoal|graphite|illustration)\b', re.IGNORECASE), [
        "Drawing and sketching are the foundation of all visual art! ✏️\n• Start with basic shapes — everything can be broken into circles, boxes, and cylinders\n• Practice gesture drawing (quick 30-second poses) to build confidence\n• Use light pressure at first, darken gradually\n• HB for general sketching, 2B–6B for shading, 2H for light guidelines\nWhat do you like to draw — figures, landscapes, still life?",
        "Great skill to develop! Sketching tips:\n✓ Draw through objects — sketch the parts you can't see too, it improves accuracy\n✓ Use your whole arm, not just your wrist, for smoother lines\n✓ Blind contour drawing exercises are excellent for training your eye\nAre you interested in realistic drawing or more stylised/illustrative?"
    ]),

    # ── COLOUR THEORY & MIXING ──
    (re.compile(r'\b(colou?r theory|colou?r wheel|mixing colou?rs?|complementary|analogous|palette|shade|hue|tint|tone|colou?r)\b', re.IGNORECASE), [
        "Colour theory is essential for every artist! 🎨\n• Primary colours: Red, Yellow, Blue\n• Mix primaries to get secondaries: orange, green, purple\n• Complementary pairs (opposites on the wheel) create vibrant contrast: red/green, blue/orange, yellow/purple\n• Analogous colours (neighbours) create harmony\nFor mixing tips: add dark to light, not light to dark — it's easier to darken a colour than to lighten it!\nWhat colours are you trying to mix?",
        "Here's a quick mixing cheat sheet:\n🟡 Yellow + Blue = Green\n🔴 Red + Yellow = Orange\n🔵 Blue + Red = Purple\nFor skin tones: start with white + yellow ochre + a tiny touch of red, then cool shadows with blue\nFor grey: mix complementary colours (e.g., orange + blue) — this gives a richer grey than black + white!\nWhat colour are you struggling to mix?"
    ]),

    # ── CANVAS / SURFACE ──
    (re.compile(r'\b(canvas|gesso|priming|surface|paper|board|panel)\b', re.IGNORECASE), [
        "Choosing the right surface makes a big difference! 🖼️\n• Canvas: best for acrylics and oils — always prime with gesso first (2 coats)\n• Watercolour paper: 300 gsm cold-pressed is ideal for beginners\n• Canvas board: more affordable than stretched canvas, great for practice\n• Wood panel: smooth surface, great for detailed realist work\nWhat medium are you using?"
    ]),

    # ── BRUSH TECHNIQUES ──
    (re.compile(r'\b(brush(es)?|brush technique|brushstroke|palette knife|blending|glazing|impasto|scumbling)\b', re.IGNORECASE), [
        "Brush techniques can totally transform your work! 🖌️\n• Impasto: thick paint applied with a palette knife — great for texture and drama\n• Glazing: thin transparent layers built up for luminosity (common in oils)\n• Scumbling: dragging dry, thick paint over a textured surface for broken colour\n• Wet blending: blend while paint is still wet for smooth gradients\nWhich technique are you trying to learn?",
        "Brush care tips:\n✓ Never let brushes dry with paint in the bristles — rinse immediately\n✓ Flat brushes for backgrounds and blocking, round for detail, fan for blending\n✓ Palette knives create great texture in acrylics and oils\nWhat effect are you going for?"
    ]),

    # ── KNITTING / CROCHET ──
    (re.compile(r'\b(knit(ting)?|crochet(ing)?|yarn|needles?|hook|wool|stitch)\b', re.IGNORECASE), [
        "Knitting and crocheting are so relaxing! 🧶 For beginners:\n• Start with chunky yarn (weight 5–6) and large needles (8–10 mm)\n• Learn the cast-on, knit stitch, and purl stitch first\n• A simple scarf is the perfect first project — just knit every row!\nAre you knitting or crocheting?",
        "Yarn crafts are wonderful. Basic stitches to learn:\n• Knitting: knit, purl, cast on, bind off\n• Crochet: chain, single crochet, double crochet\nOnce you have these, you can make almost anything! What do you want to make?"
    ]),

    # ── ORIGAMI ──
    (re.compile(r'\b(origami|paper fold(ing)?|paper crane|paper art)\b', re.IGNORECASE), [
        "Origami — the beautiful Japanese art of paper folding! 🕊️\nBeginner projects: paper boat, frog, fortune teller, and the classic crane.\nYou only need a square sheet of paper. Want me to walk you through the paper crane step by step?",
        "For origami: use crisp, square paper (15×15 cm is standard). Key folds to learn:\n• Valley fold (fold towards you)\n• Mountain fold (fold away from you)\n• Squash fold\nWhich shape would you like to try?"
    ]),

    # ── SCRAPBOOKING ──
    (re.compile(r'\b(scrapbook(ing)?|photo album|memory book|journaling)\b', re.IGNORECASE), [
        "Scrapbooking is a lovely way to preserve memories! 📖\nYou'll need: an album, decorative paper, adhesive, photos, washi tape, and stickers.\nStart by choosing a theme — travel, family, seasons — then build your colour palette around it.\nWhat theme are you thinking of?",
        "Love scrapbooking! Layout tip: follow the 'rule of thirds' — place your focal photo off-centre and surround it with smaller elements. Want more layout design ideas?"
    ]),

    # ── MACRAMÉ ──
    (re.compile(r'\b(macram[eé]|wall hanging|knotting|rope craft)\b', re.IGNORECASE), [
        "Macramé is making a massive comeback! 🪢\nYou'll need: macramé cord (3–5 mm cotton rope), a wooden dowel, and scissors.\nThe two essential knots: square knot and half-hitch.\nBeginner project: cut 8 cords at 2 m each, fold over a dowel, and practice the square knot.\nShall I guide you through it step by step?",
    ]),

    # ── CANDLE MAKING ──
    (re.compile(r'\b(candle(s|making)?|wax|wick|soy wax|beeswax)\b', re.IGNORECASE), [
        "Candle making is so satisfying! 🕯️\nFor beginners, soy wax container candles are the easiest.\nSupplies: soy wax flakes, pre-waxed wicks, heat-safe jars, fragrance oil, thermometer.\nProcess: melt wax to 85°C → add fragrance at 75°C → pour into jars → let cool 24 hours.\nWhat size candle are you planning to make?"
    ]),

    # ── TIE-DYE ──
    (re.compile(r'\b(tie.?dye|tiedye|fabric dye|dyeing)\b', re.IGNORECASE), [
        "Tie-dye is so much fun! 🌈\nYou'll need: white cotton fabric, rubber bands, gloves, and fibre-reactive dyes.\nClassic spiral pattern steps:\n1. Pinch the centre of the fabric and twist into a spiral\n2. Secure with rubber bands in a star pattern\n3. Apply dye to each section\n4. Wrap in plastic and wait 6–8 hours\nWhich pattern would you like to try?"
    ]),

    # ── PRINTMAKING / LINOCUT ──
    (re.compile(r'\b(linocut|printmaking|lino print|woodcut|block print|etching|monoprint)\b', re.IGNORECASE), [
        "Printmaking is such an underrated craft! 🖨️ Linocut is the most beginner-friendly:\n• Carve your design into a linoleum block using lino tools (V-gouge for lines, U-gouge for areas)\n• Remember: what you carve away stays white!\n• Roll water-based ink onto the block with a brayer\n• Press firmly onto paper or fabric\nSafety tip: always cut away from your hands and keep the block on a non-slip surface.\nWhat design are you thinking of printing?"
    ]),

    # ── POTTERY / CLAY ──
    (re.compile(r'\b(potter(y)?|clay|ceramics|sculpt(ing)?|air dry clay|polymer clay|wheel throwing)\b', re.IGNORECASE), [
        "Working with clay is incredibly therapeutic! 🏺\nFor home crafters without a kiln, air-dry clay and polymer clay are perfect.\n• Air-dry clay: great for sculptures and bowls — sand and paint once dry\n• Polymer clay: bakes in a regular oven at 130°C, ideal for jewellery and figures\n• Pottery wheel: best taken as a class first!\nWhat are you planning to make with clay?",
        "Clay tips:\n✓ Keep clay covered with a damp cloth while working to prevent drying\n✓ Score and slip technique for joining pieces (scratch both surfaces, apply liquid clay, press together)\n✓ Smooth with water and a rubber-tipped tool\nAre you hand-building or wheel throwing?"
    ]),

    # ── JEWELLERY MAKING ──
    (re.compile(r'\b(jewellery|jewelry|beading|wire wrap(ping)?|resin|pendant|bracelet|earrings|necklace)\b', re.IGNORECASE), [
        "Jewellery making is such a fun craft! 💎\nGreat beginner options:\n• Beaded bracelets: just need elastic cord and beads\n• Wire-wrapped pendants: 20-gauge wire + a gemstone or bead\n• Resin jewellery: pour resin into moulds with dried flowers or glitter\nFor resin: always use UV resin or two-part epoxy, wear gloves, and work in a ventilated area.\nWhat type of jewellery do you want to make?"
    ]),

    # ── RESIN ART ──
    (re.compile(r'\b(resin|epoxy|resin art|resin pour|geode art)\b', re.IGNORECASE), [
        "Resin art is stunning and very popular right now! ✨\nFor beginners:\n• Use 1:1 ratio epoxy resin (mix by weight, not volume, for accuracy)\n• Add alcohol inks or mica powder for colour\n• Use a heat gun or torch to pop bubbles and create cells\n• Work at room temperature (20–25°C) for best results\n• Always wear gloves and work in a ventilated area!\nAre you making geode art, coasters, jewellery, or something else?"
    ]),

    # ── BEGINNER ──
    (re.compile(r'\b(beginner|easy|simple|starter|first time|never (tried|done)|new to)\b', re.IGNORECASE), [
        "Welcome to crafting! 🌟 Great first projects for absolute beginners:\n• Acrylic painting on canvas (very forgiving — mistakes are easy to paint over!)\n• Origami (just needs paper)\n• Rock painting (therapeutic and cheap)\n• Friendship bracelets\n• Simple watercolour florals\nWhich sounds most appealing to you?",
        "No experience needed! The easiest crafts to start with:\n1. Acrylic pour painting — mix paint and pour, the results are always beautiful\n2. Paper origami — free to try right now\n3. Tie-dye — hard to go wrong!\nWould you like to start with one of these?"
    ]),

    # ── TROUBLESHOOTING ──
    (re.compile(r"(i('m| am)\s+(having trouble|stuck|struggling|confused)|not working|going wrong|ruined|muddy|cracking|peeling|bleeding)", re.IGNORECASE), [
        "Don't worry — craft mishaps happen to everyone! 😊 Could you describe what went wrong? For example:\n• Is the paint muddy or dull?\n• Is something cracking or peeling?\n• Did colours bleed into each other?\nTell me more and I'll help you fix it!",
        "Crafting can be tricky at first! Tell me exactly what happened and I'll help troubleshoot. Most mistakes in art are actually fixable — or can become happy accidents!"
    ]),

    # ── INSPIRATION / ARTIST BLOCK ──
    (re.compile(r'\b(inspiration|inspired|artists? block|stuck|bored|don\'t know what to (make|paint|draw|create))\b', re.IGNORECASE), [
        "Artist's block is real but beatable! 💡 Try these:\n• Paint something in your immediate surroundings — a cup, a plant, your hand\n• Pick two random colours and make something with only those\n• Do a 10-minute speed sketch with no pressure\n• Browse Pinterest or Instagram for 5 minutes then close it and paint from memory\nWhat medium are you working in?",
        "For instant inspiration:\n🎨 Open your window and paint what you see\n✏️ Fill a sketchbook page with random doodles for 5 minutes\n🎭 Pick an emotion and make abstract art that represents it\nSometimes starting with NO plan leads to the best work!"
    ]),

    # ── BUDGET ──
    (re.compile(r'\b(cheap|budget|affordable|cost|expensive|price|spend|free)\b', re.IGNORECASE), [
        "Crafting doesn't have to be expensive! 💰\n• Origami, sketching, and paper crafts are nearly free\n• Acrylic student-grade paints (Reeves, Daler Rowney) are very affordable\n• Thrift shops and dollar stores are great for frames, jars, and fabric\n• Upcycle household items — tin cans as brush holders, cardboard as canvas\nWhat's your rough budget?"
    ]),

    # ── KIDS ──
    (re.compile(r'\b(kids?|child(ren)?|toddler|school|classroom|age \d+)\b', re.IGNORECASE), [
        "Crafts for kids are wonderful! 👶🎨 Safe, fun activities:\n• Finger painting (ages 2+)\n• Salt dough sculptures (ages 4+)\n• Paper plate animals (ages 3+)\n• Tie-dye with food colouring (safe for young kids)\n• Simple origami (ages 6+)\nHow old are the children? I can suggest age-appropriate projects!"
    ]),

    # ── THANK YOU ──
    (re.compile(r'\b(thank(s| you)|thx|appreciate it|helpful|great help)\b', re.IGNORECASE), [
        "You're very welcome! Happy crafting! 🎨 Feel free to come back anytime.",
        "My pleasure! I hope your project turns out beautifully. Have fun creating! 🌟"
    ]),

    # ── GOODBYE ──
    (re.compile(r'\b(bye|goodbye|see you|quit|exit|done|cya)\b', re.IGNORECASE), [
        "Goodbye! Happy crafting! 🎨 Come back anytime you need inspiration.",
        "See you later! I hope your project is a great success! 🌟"
    ]),
]

FALLBACKS = [
    "That's interesting! Could you tell me more about your arts and crafts project? 🎨",
    "I'm not sure I understood that. Could you rephrase? I'm here to help with any crafting questions!",
    "Hmm, I specialise in arts and crafts. Try asking about painting, sketching, origami, or any other craft!",
    "I'd love to help! Could you give me more detail about what you're trying to make or learn? 😊"
]

QUICK_SUGGESTIONS = [
    "Give me project ideas",
    "I'm a beginner",
    "Tell me about acrylics",
    "How do I paint a portrait?",
    "What is colour theory?",
    "I need cheap craft ideas",
]


# ── CHATBOT LOGIC ─────────────────────────────────────────────
def respond(user_input: str) -> str:
    user_input = user_input.strip()
    for pattern, responses in RULES:
        match = pattern.search(user_input)
        if match:
            template = random.choice(responses)
            try:
                groups = match.groups(default='')
                return template.format(*groups)
            except (IndexError, KeyError):
                return template
    return random.choice(FALLBACKS)


# ── SESSION STATE ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hello! 🎨 I'm your Arts & Crafts assistant. Ask me about painting, sketching, origami, acrylics, portraits, colour theory — anything creative! What are you working on today?"}
    ]
if "input_key" not in st.session_state:
    st.session_state.input_key = 0


# ── HEADER ───────────────────────────────────────────────────
st.markdown('<div class="chat-title">🎨 Arts & Crafts Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Your friendly guide to painting, crafting & everything creative</div>', unsafe_allow_html=True)
st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)


# ── QUICK SUGGESTIONS ────────────────────────────────────────
st.markdown("**Try asking:**")
cols = st.columns(3)
for i, suggestion in enumerate(QUICK_SUGGESTIONS):
    if cols[i % 3].button(suggestion, key=f"chip_{i}"):
        st.session_state.messages.append({"role": "user", "text": suggestion})
        st.session_state.messages.append({"role": "bot", "text": respond(suggestion)})
        st.rerun()

st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)


# ── CHAT HISTORY ─────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown('<div class="label-user">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bubble-user">{msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="label-bot">🎨 Bot</div>', unsafe_allow_html=True)
        # Convert newlines to <br> for HTML rendering
        html_text = msg["text"].replace("\n", "<br>")
        st.markdown(f'<div class="bubble-bot">{html_text}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── INPUT ROW ────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "message",
        placeholder="Ask me anything about arts & crafts...",
        label_visibility="collapsed",
        key=f"input_{st.session_state.input_key}"
    )
with col2:
    send = st.button("Send ➤")

if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "text": user_input.strip()})
    st.session_state.messages.append({"role": "bot", "text": respond(user_input.strip())})
    st.session_state.input_key += 1
    st.rerun()

# ── CLEAR BUTTON ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🗑️ Clear chat", use_container_width=False):
    st.session_state.messages = [
        {"role": "bot", "text": "Hello! 🎨 I'm your Arts & Crafts assistant. What are you working on today?"}
    ]
    st.session_state.input_key += 1
    st.rerun()

st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:0.75rem; color:#bbb;">Hamna Asif — Roll No 16 | NLP Assignment Part A</div>', unsafe_allow_html=True)
