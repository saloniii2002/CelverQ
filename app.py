import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


# ===== LOAD ENV =====
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    load_dotenv(".env")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ===== MODELS =====
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    max_output_tokens=800
)

groq = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=800
)


# ===== SESSION =====
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

messages = st.session_state.chats[st.session_state.current_chat]


# ===== PAGE =====
st.set_page_config(page_title="CleverQ", layout="wide")


st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
}

html, body, [class*="css"], p, span, div {
    color: #ffffff !important;
    font-size: 16px !important;
}

[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}

.tagline {
    text-align: center;
    color: #cbd5f5;
}

.stChatMessage {
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

.stChatMessage[data-testid="stChatMessage-user"] {
    background-color: #1e293b;
}

.stChatMessage[data-testid="stChatMessage-assistant"] {
    background-color: #020617;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)


# ===== HEADER =====
st.markdown("""
<div class="main-title">CleverQ</div>
<div class="tagline">Smart Answers • Multi-Model AI</div>
<hr>
""", unsafe_allow_html=True)


# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## Chats")

    if st.button("New Chat", use_container_width=True):
        new_chat = f"Chat {len(st.session_state.chats)+1}"
        st.session_state.chats[new_chat] = []
        st.session_state.current_chat = new_chat

    st.markdown("---")

    for chat in st.session_state.chats:
        if chat == st.session_state.current_chat:
            st.markdown(f"**{chat}**")
        else:
            if st.button(chat, use_container_width=True):
                st.session_state.current_chat = chat

    st.markdown("---")
    st.caption("CleverQ AI")


# ===== FUNCTIONS =====
def make_prompt(q):
    return f"""
Give a SHORT, exam-ready answer.

- Max 5 bullet points
- 1 line definition
- Clear and concise

Question:
{q}
"""


def ask(model, prompt):
    try:
        res = model.invoke(prompt)
        return res.content.strip() if res.content else "Error"
    except:
        return "Error"


def safe(x):
    return x and "Error" not in x


def score(ans):
    if not ans or "Error" in ans:
        return 0

    s = 0

    if len(ans) > 50:
        s += 3

    if any(x in ans for x in ["•", "-", "\n-"]):
        s += 3

    if len(ans.split("\n")) >= 3:
        s += 2

    if ":" in ans[:60]:
        s += 2

    return min(s, 10)


# ===== DISPLAY CHAT =====
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ===== INPUT =====
if user_input := st.chat_input("Ask anything..."):

    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = make_prompt(user_input)

    with st.spinner("Thinking... 🤖"):
        g1 = ask(gemini, prompt)
        g2 = ask(groq, prompt)

    # ===== STRONG FUSION =====
    if safe(g1) and safe(g2):

        fusion_prompt = f"""
You are an expert answer optimizer.

Combine BOTH answers into ONE BEST answer.

STRICT RULES:
- Start with 1 line definition
- Then 3–5 bullet points
- Use "-" bullets only
- No paragraph
- No repetition
- Keep best points from both

Answer 1:
{g1}

Answer 2:
{g2}
"""

        fusion_raw = ask(groq, fusion_prompt)

        # refinement 
        refine_prompt = f"""
Improve this answer further.

Keep same format.
Make it clearer and sharper.

Answer:
{fusion_raw}
"""

        fusion = ask(groq, refine_prompt)

    else:
        fusion = None

    # ===== SCORING =====
    s1 = score(g1)
    s2 = score(g2)
    s3 = score(fusion) if fusion else 0

    # ===== SELECTION =====
    if s3 >= s1 and s3 >= s2:
        final_answer = fusion
        best_model = "Fusion"
        reason = "Best combined answer"

    elif s1 >= s2:
        final_answer = g1
        best_model = "Gemini"
        reason = "More structured"

    else:
        final_answer = g2
        best_model = "Groq"
        reason = "More concise"

    # ===== OUTPUT =====
    bot_reply = f"""
### Answer
{final_answer}

---

Best Model: {best_model}  
Gemini: {s1}/10 | Groq: {s2}/10 | Fusion: {s3}/10  

Reason: {reason}
"""

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    messages.append({"role": "assistant", "content": bot_reply})