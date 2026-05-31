"""
KisanMitra - AI Crop & Soil Advisory Chatbot
Streamlit Web Version — powered by Groq API (Free)
Created by Tanishka Patel 10th Grade
Version 1.0.0
"""

import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────
#  CONFIG — paste your Groq key here
# ─────────────────────────────────────────────

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="KisanMitra — AI Farming Advisor",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS + JS (Fixed Chat Layout & Simplified Input)
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding-top: 0 !important; padding-bottom: 4rem; max-width: 780px; }

.stApp {
    background: #060713;
    background-image:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(99, 102, 241, 0.15) 0%, transparent 70%),
        radial-gradient(circle at 10% 40%, rgba(6, 182, 212, 0.05) 0%, transparent 40%);
}

/* ── header ── */
.km-header {
    text-align: center;
    padding: 28px 0 16px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.15);
    margin-bottom: 24px;
    position: relative;
}
.km-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(6, 182, 212, 0.08);
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 20px; padding: 4px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: #22d3ee;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 14px;
}
.km-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #22d3ee;
    box-shadow: 0 0 10px #22d3ee;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.km-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem; font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.03em;
    margin-bottom: 6px;
    line-height: 1;
}
.km-title span { 
    background: linear-gradient(135deg, #a855f7, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.km-sub {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.92rem; color: #64748b;
    letter-spacing: 0.02em;
}

/* ── context expander ── */
[data-testid="stExpander"] {
    background: rgba(99, 102, 241, 0.03) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 12px !important;
    margin-bottom: 16px;
}
[data-testid="stExpander"] summary {
    color: #94a3b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stSelectbox label {
    color: #94a3b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput label {
    color: #94a3b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── context pills ── */
.ctx-bar {
    display: flex; flex-wrap: wrap; gap: 8px;
    justify-content: center; margin-bottom: 18px;
}
.ctx-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 20px; padding: 4px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; color: #cbd5e1;
}

/* ── chat messages (FIXED COMPRESSION DISTORTION) ── */
.km-msg-user {
    display: flex; justify-content: flex-end;
    margin: 12px 0; width: 100%;
}
.km-msg-bot {
    display: flex; justify-content: flex-start;
    margin: 12px 0; width: 100%;
}
.km-user-container {
    display: flex; flex-direction: column; align-items: flex-end; width: 85%;
}
.km-bot-container {
    display: flex; flex-direction: column; align-items: flex-start; width: 85%;
}
.km-bubble-user {
    width: 100%; text-align: left;
    background: linear-gradient(135deg, #312e81, #4338ca);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.93rem; color: #f1f5f9;
    line-height: 1.6;
}
.km-bubble-bot {
    width: 100%;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.93rem; color: #e2e8f0;
    line-height: 1.75;
    position: relative;
}
.km-bot-label {
    display: flex; align-items: center; gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; color: #a855f7;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 8px;
}
.km-bot-label-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #a855f7;
}
.km-user-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; color: #818cf8;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 4px; text-align: right;
}

/* ── input area ── */
.km-input-wrap {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 4px 4px 4px 16px;
    display: flex; align-items: flex-end; gap: 8px;
    margin-top: 8px;
    transition: border-color 0.2s;
}
.km-input-wrap:focus-within {
    border-color: rgba(99, 102, 241, 0.5);
}
.stTextArea { flex: 1; }
.stTextArea textarea {
    background: transparent !important;
    color: #f1f5f9 !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 10px 4px !important; /* Added nice inner placeholder text padding */
    resize: none !important;
    box-shadow: none !important;
    min-height: 44px !important;
}
.stTextArea textarea:focus {
    box-shadow: none !important;
    border: none !important;
}
.stTextArea textarea::placeholder { color: #475569 !important; }
.stTextArea label { display: none !important; }

/* ── buttons ── */
.stButton > button {
    background: rgba(99, 102, 241, 0.12) !important;
    color: #818cf8 !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.15s !important;
    letter-spacing: 0.05em !important;
}
.stButton > button:hover {
    background: rgba(99, 102, 241, 0.25) !important;
    border-color: rgba(99, 102, 241, 0.6) !important;
    color: #c7d2fe !important;
}

/* ── form ── */
[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* ── hint ── */
.km-hint {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; color: #334155;
    letter-spacing: 0.05em;
    margin-top: 10px;
}

/* ── spinner ── */
.stSpinner > div { border-top-color: #818cf8 !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.2); border-radius: 2px; }

/* ── credit footer badge ── */
.tanishka-footer {
    position: fixed;
    bottom: 12px;
    right: 16px;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 6px 14px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    color: #94a3b8;
    z-index: 999999;
}
.tanishka-footer span {
    color: #a855f7;
    font-weight: 600;
}
@media (max-width: 768px) {
    .tanishka-footer {
        position: relative;
        display: block;
        text-align: center;
        margin: 20px auto 0;
        right: auto; bottom: auto;
        width: max-content;
    }
}
</style>

<script>
// Intercept text area entries for true Single-Enter Form Submissions
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        const textarea = document.querySelector('textarea');
        if (textarea && document.activeElement === textarea) {
            e.preventDefault();
            // find and click the Send button
            const btns = document.querySelectorAll('button');
            for (let b of btns) {
                if (b.innerText.includes('Send')) {
                    b.click();
                    break;
                }
            }
        }
    }
});
</script>
""", unsafe_allow_html=True)

# Custom Sticky Credits Badge Injection
st.markdown('<div class="tanishka-footer">Created by <span>Tanishka Patel</span> • Grade 10th</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are KisanMitra (किसान मित्र), a friendly and expert agricultural advisor for Indian farmers.

Your role:
- Give practical, simple advice on crops, soil, pests, diseases, weather, and farming techniques
- Always consider the Indian agricultural context (seasons, states, common crops)
- Respond in simple English. If the user writes in Hindi or uses Hindi words, reply in Hindi too.
- When giving advice, be specific and actionable
- Mention government schemes (PM-Kisan, Fasal Bima Yojana, Kisan Credit Card, etc.) when relevant
- Keep responses concise but complete (5-10 lines max)

Soil types: Sandy, Clay, Loamy, Silty, Black (Regur), Red, Alluvial, Laterite
Seasons: Kharif (June-Nov), Rabi (Nov-Apr), Zaid (Apr-Jun)
Key states and crops: Punjab (wheat, rice), Maharashtra (sugarcane, cotton), UP (wheat, sugarcane), AP/Telangana (rice, cotton), Rajasthan (bajra, moth bean), Karnataka (ragi, coffee)

Format responses clearly. Use bullet points for steps or options.
"""

# ─────────────────────────────────────────────
#  GROQ CLIENT
# ─────────────────────────────────────────────

@st.cache_resource
def get_client():
    return Groq(api_key=GROQ_API_KEY)

def ask_groq(history: list, message: str) -> str:
    try:
        client = get_client()
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower() or "401" in err:
            return "❌ Invalid API key. Check the key in app.py."
        elif "rate_limit" in err.lower() or "429" in err:
            return "⚠️ Rate limit hit. Wait a few seconds and try again."
        return f"❌ Error: {err}"

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class="km-header">
    <div class="km-badge"><div class="km-dot"></div> AI Agricultural Advisor</div>
    <div class="km-title">Kisan<span>Mitra</span></div>
    <div class="km-sub">किसान मित्र &nbsp;·&nbsp; Crop & Soil Intelligence for Indian Farmers</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONTEXT BAR
# ─────────────────────────────────────────────

with st.expander("⚙  Set farming context", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        soil = st.selectbox("Soil Type", [
            "Not specified","Sandy","Clay","Loamy",
            "Black (Regur)","Red","Alluvial","Silty","Laterite"
        ])
    with col2:
        season = st.selectbox("Season", [
            "Not specified","Kharif (Jun-Nov)","Rabi (Nov-Apr)","Zaid (Apr-Jun)"
        ])
    with col3:
        state = st.text_input("State", placeholder="e.g. Punjab")

ctx = []
if soil   != "Not specified": ctx.append(f"◈ {soil} soil")
if season != "Not specified": ctx.append(f"◈ {season}")
if state.strip():             ctx.append(f"◈ {state.strip()}")

if ctx:
    pills = "".join([f'<span class="ctx-pill">{c}</span>' for c in ctx])
    st.markdown(f'<div class="ctx-bar">{pills}</div>', unsafe_allow_html=True)

context_prefix = ""
if ctx:
    context_prefix = "[Farmer context: " + " | ".join(ctx) + "]\n\n"

# ─────────────────────────────────────────────
#  AUTO GREETING
# ─────────────────────────────────────────────

if not st.session_state.greeted:
    with st.spinner("Initializing KisanMitra..."):
        greeting = ask_groq(
            [],
            "Hello! Greet me as a farmer warmly and ask what farming problem I need help with today. Max 3 lines."
        )
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.greeted = True

# ─────────────────────────────────────────────
#  CHAT DISPLAY
# ─────────────────────────────────────────────

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="km-msg-user">
            <div class="km-user-container">
                <div class="km-user-label">You</div>
                <div class="km-bubble-user">{msg["content"]}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        content_html = msg["content"].replace("\n", "<br>")
        st.markdown(f"""
        <div class="km-msg-bot">
            <div class="km-bot-container">
                <div class="km-bubble-bot">
                    <div class="km-bot-label"><div class="km-bot-label-dot"></div>KisanMitra</div>
                    {content_html}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT
# ─────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_btn, col_new = st.columns([6, 1, 1])
    with col_input:
        user_input = st.text_area(
            "msg",
            placeholder="Ask about crops, soil, pests, schemes...",
            height=52,
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("Send ➤", use_container_width=True)
    with col_new:
        new_chat = st.form_submit_button("↺ New", use_container_width=True)

st.markdown('<div class="km-hint">Enter to send &nbsp;·&nbsp; Shift+Enter for new line &nbsp;·&nbsp; Hindi supported</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HANDLE ACTIONS
# ─────────────────────────────────────────────

if new_chat:
    st.session_state.messages = []
    st.session_state.greeted = False
    st.rerun()

if submitted and user_input.strip():
    full_message = context_prefix + user_input.strip()
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner(""):
        reply = ask_groq(st.session_state.messages[:-1], full_message)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
