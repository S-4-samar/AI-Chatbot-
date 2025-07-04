import streamlit as st
import time
import openai

# ------------------ OpenRouter API Setup ------------------

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)


model = "mistralai/mixtral-8x7b-instruct"

# ------------------ Streamlit Page Setup ------------------
st.set_page_config(page_title="Samar AI • Quantum-Class Chatbot", layout="wide")

# ------------------ Custom CSS ------------------
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

body {
    background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
    font-family: 'Orbitron', sans-serif;
    color: #ffffff;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.glass-container {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 22px;
    padding: 2em;
    margin: 2em auto;
    max-width: 1000px;
    box-shadow: 0 0 40px rgba(0, 255, 255, 0.1);
    animation: zoomIn 1s ease-in-out;
}

.main-title {
    font-size: 3em;
    text-align: center;
    background: linear-gradient(to right, #ff00cc, #333399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    margin-bottom: 0.2em;
    animation: glowPulse 1.2s ease infinite alternate;
}

.subtitle {
    text-align: center;
    font-size: 1.1em;
    color: #cccccc;
    margin-bottom: 2.5em;
}

.message-box {
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1.2em;
    margin: 1em 0;
    width: 100%;
    max-width: 90%;
    line-height: 1.6em;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.04);
    transition: all 0.3s ease-in-out;
    word-wrap: break-word;
}
.user-msg {
    background: linear-gradient(to right, #7f00ff, #e100ff);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 0;
}
.assistant-msg {
    background: rgba(255,255,255,0.05);
    color: #f1f1f1;
    margin-right: auto;
    border-bottom-left-radius: 0;
}
.footer-credit {
    text-align: center;
    font-size: 0.9em;
    color: #888;
    padding: 2em 0 1em;
    margin-top: 3em;
}
input[type="text"] {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #555;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 1em;
    font-family: 'Orbitron', sans-serif;
}
button {
    background: linear-gradient(135deg, #00f2fe, #4facfe);
    color: black;
    border: none;
    padding: 12px 30px;
    border-radius: 15px;
    font-weight: bold;
    font-family: 'Orbitron', sans-serif;
    margin-top: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    letter-spacing: 1px;
}
button:hover {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
}

@keyframes zoomIn {
    from {transform: scale(0.95); opacity: 0;}
    to {transform: scale(1); opacity: 1;}
}

@keyframes glowPulse {
    0% {text-shadow: 0 0 10px #ff00cc, 0 0 20px #ff00cc;}
    100% {text-shadow: 0 0 25px #333399, 0 0 40px #333399;}
}

@media screen and (max-width: 768px) {
    .main-title { font-size: 2.2em; }
    .subtitle { font-size: 0.95em; }
    .glass-container { padding: 1.5em; margin: 1.5em; }
    input[type="text"] { font-size: 0.9em; }
    button { font-size: 0.9em; padding: 10px 20px; }
    .message-box { font-size: 0.9em; padding: 1em; }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.markdown("""
        <h2 style='color:#00f2fe;'>☰ About This App</h2>
        <hr style='border:1px solid #333;'>
        <p><strong>Samar AI</strong> is a next-generation multilingual chatbot assistant designed to simulate human-like conversations with intelligence, speed, and elegance.</p>
        <ul>
            <li>🌍 International-ready</li>
            <li>🔐 Privacy focused</li>
            <li>📧 Email-based sign-in (coming soon)</li>
            <li>🎤 Voice input (in progress)</li>
        </ul>
        <hr>
        <p>🚀 Crafted with ❤️ by <strong>Samar Abbas</strong><br>Vice President • Sports Society<br>University of Narowal</p>
    """, unsafe_allow_html=True)
    st.button("🦤 Clear Chat Session", on_click=lambda: st.session_state.clear())

# ------------------ Title ------------------
st.markdown("""
<div class='glass-container'>
    <h1 class='main-title'>Samar AI: Quantum-Class Chatbot</h1>
    <p class='subtitle'>🚀 Built to be beautiful, fast & intelligent. Experience next-level AI — by Samar Abbas.</p>
</div>
""", unsafe_allow_html=True)

# ------------------ Message Store ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# ------------------ Typing Input + Spinner ------------------
user_input = st.text_input("Speak your thoughts:", key="input")
send = st.button("Engage 🔮")

if send and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("💡 Samar AI is processing..."):
        time.sleep(1.2)
        response = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ------------------ Chat Display ------------------
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.subheader("🧠 Neural Transcript")

for msg in st.session_state.messages[1:]:
    role = msg["role"]
    role_label = "🧑‍🚀 You" if role == "user" else "🤖 Samar AI"
    msg_class = "user-msg" if role == "user" else "assistant-msg"
    st.markdown(f"""
        <div class='message-box {msg_class}'>
            <strong>{role_label}:</strong><br>{msg['content']}
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ Footer ------------------
st.markdown("""
    <div class='footer-credit'>
        🌟 Designed for the World • Built by <strong>Samar Abbas</strong><br>
        Quantum UI • Mistral • OpenRouter • Streamlit • 2025
    </div>
""", unsafe_allow_html=True)
