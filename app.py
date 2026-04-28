<<<<<<< HEAD
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

# ===== MODELS (ONLY TOKENS INCREASED) =====
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    max_output_tokens=800   # 🔥 increased
)

groq = ChatGroq(
    model="llama-3.1-8b-instant",  # SAME as yours
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=800   # 🔥 increased
)

# ===== SESSION =====
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

messages = st.session_state.chats[st.session_state.current_chat]

# ===== PAGE =====
st.set_page_config(page_title="CleverQ", layout="wide")

# ===== UI STYLE (FONT FIXED + CLEAR) =====
st.markdown("""
<style>

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
}

/* FORCE WHITE TEXT */
html, body, [class*="css"], p, span, div {
    color: #ffffff !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}

/* TITLES */
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
}
.tagline {
    text-align: center;
    color: #cbd5f5;
    font-size: 15px;
}

/* CHAT BOX */
.stChatMessage {
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    font-weight: 500;
}

/* USER MESSAGE */
.stChatMessage[data-testid="stChatMessage-user"] {
    background-color: #1e293b;
}

/* BOT MESSAGE */
.stChatMessage[data-testid="stChatMessage-assistant"] {
    background-color: #020617;
    border: 1px solid #334155;
}

/* INPUT BOX */
.stTextInput input {
    color: white !important;
}

/* EXPANDER */
.stExpander {
    color: white !important;
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
        return res.content.strip() if res.content else "Error: Empty response"
    except Exception as e:
        return f"Error: {str(e)}"

def safe(x):
    return x and "Error" not in x

def score(ans):
    if not ans or "Error" in ans:
        return 0

    score = 0
    if len(ans) > 50:
        score += 3
    if any(x in ans for x in ["•", "-", "\n-"]):
        score += 3
    if "definition" in ans.lower():
        score += 2
    if len(ans.split("\n")) >= 3:
        score += 2

    return min(score, 10)

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

    # 🔥 loading feel
    with st.spinner("Thinking... 🤖"):
        g1 = ask(gemini, prompt)
        g2 = ask(groq, prompt)

    s1 = score(g1)
    s2 = score(g2)

    # ===== BEST MODEL =====
    if not safe(g1):
        best_model = "Groq"
        reason = "Gemini unavailable"
    elif not safe(g2):
        best_model = "Gemini"
        reason = "Groq unavailable"
    elif s1 >= s2:
        best_model = "Gemini"
        reason = "More structured response"
    else:
        best_model = "Groq"
        reason = "More concise response"

    # ===== FUSION ===== (UNCHANGED)
    if not safe(g1) and not safe(g2):
        final_answer = "Both models failed to generate a response."
    elif not safe(g1):
        final_answer = g2
    elif not safe(g2):
        final_answer = g1
    else:
        fusion_prompt = f"""
Merge both answers into one best short answer.

{g1}

{g2}
"""
        final_answer = ask(groq, fusion_prompt)

    bot_reply = f"""
### Answer
{final_answer}

---

Best Model: {best_model}  
Gemini: {s1}/10 | Groq: {s2}/10  

Reason: {reason}
"""

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    messages.append({"role": "assistant", "content": bot_reply})

    # ===== DEBUG =====
    with st.expander("View Model Responses"):
        st.write("Gemini")
        st.write(g1)

        st.write("Groq")
=======
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

# ===== MODELS (ONLY TOKENS INCREASED) =====
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    max_output_tokens=800   # 🔥 increased
)

groq = ChatGroq(
    model="llama-3.1-8b-instant",  # SAME as yours
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=800   # 🔥 increased
)

# ===== SESSION =====
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

messages = st.session_state.chats[st.session_state.current_chat]

# ===== PAGE =====
st.set_page_config(page_title="CleverQ", layout="wide")

# ===== UI STYLE (FONT FIXED + CLEAR) =====
st.markdown("""
<style>

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
}

/* FORCE WHITE TEXT */
html, body, [class*="css"], p, span, div {
    color: #ffffff !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}

/* TITLES */
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
}
.tagline {
    text-align: center;
    color: #cbd5f5;
    font-size: 15px;
}

/* CHAT BOX */
.stChatMessage {
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    font-weight: 500;
}

/* USER MESSAGE */
.stChatMessage[data-testid="stChatMessage-user"] {
    background-color: #1e293b;
}

/* BOT MESSAGE */
.stChatMessage[data-testid="stChatMessage-assistant"] {
    background-color: #020617;
    border: 1px solid #334155;
}

/* INPUT BOX */
.stTextInput input {
    color: white !important;
}

/* EXPANDER */
.stExpander {
    color: white !important;
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
        return res.content.strip() if res.content else "Error: Empty response"
    except Exception as e:
        return f"Error: {str(e)}"

def safe(x):
    return x and "Error" not in x

def score(ans):
    if not ans or "Error" in ans:
        return 0

    score = 0
    if len(ans) > 50:
        score += 3
    if any(x in ans for x in ["•", "-", "\n-"]):
        score += 3
    if "definition" in ans.lower():
        score += 2
    if len(ans.split("\n")) >= 3:
        score += 2

    return min(score, 10)

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

    # 🔥 loading feel
    with st.spinner("Thinking... 🤖"):
        g1 = ask(gemini, prompt)
        g2 = ask(groq, prompt)

    s1 = score(g1)
    s2 = score(g2)

    # ===== BEST MODEL =====
    if not safe(g1):
        best_model = "Groq"
        reason = "Gemini unavailable"
    elif not safe(g2):
        best_model = "Gemini"
        reason = "Groq unavailable"
    elif s1 >= s2:
        best_model = "Gemini"
        reason = "More structured response"
    else:
        best_model = "Groq"
        reason = "More concise response"

    # ===== FUSION ===== (UNCHANGED)
    if not safe(g1) and not safe(g2):
        final_answer = "Both models failed to generate a response."
    elif not safe(g1):
        final_answer = g2
    elif not safe(g2):
        final_answer = g1
    else:
        fusion_prompt = f"""
Merge both answers into one best short answer.

{g1}

{g2}
"""
        final_answer = ask(groq, fusion_prompt)

    bot_reply = f"""
### Answer
{final_answer}

---

Best Model: {best_model}  
Gemini: {s1}/10 | Groq: {s2}/10  

Reason: {reason}
"""

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    messages.append({"role": "assistant", "content": bot_reply})

    # ===== DEBUG =====
    with st.expander("View Model Responses"):
        st.write("Gemini")
        st.write(g1)

        st.write("Groq")
>>>>>>> c0e6503dcceb4a19cad9ca3a3137a85019bee44f
        st.write(g2)