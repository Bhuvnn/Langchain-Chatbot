import os
from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key,
    temperature=0.9
)

# Page config
st.set_page_config(page_title="Chandler Bing Chat", page_icon="🧠", layout="centered")

# Streamlit dark theme inspired styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600&display=swap');
    
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    .main-container {
        background-color: #262730;
        border: 1px solid;
        border-image: linear-gradient(90deg, #ff4b4b, #ff8700, #ffbd45, #00d4aa, #00c0f2, #1c83e1, #803df5) 1;
        border-radius: 8px;
        margin: 10px auto;
        max-width: 900px;
        height: 85vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background-color: #262730;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #3d4043;
        flex-shrink: 0;
    }
    
    .chat-title {
        font-size: 16px;
        font-weight: 600;
        margin: 0;
        color: #fafafa;
    }
    
    .chat-subtitle {
        font-size: 12px;
        font-weight: 400;
        color: #a6a6a6;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background-color: #0e1117;
        scrollbar-width: thin;
        scrollbar-color: #3d4043 transparent;
    }
    
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #3d4043;
        border-radius: 3px;
    }
    
    .message {
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
        animation: messageSlideIn 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    @keyframes messageSlideIn {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        50% {
            opacity: 0.7;
            transform: translateY(-2px) scale(1.02);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .bot-message {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
        position: relative;
    }
    
    .user-bubble {
        background-color: #3d4043;
        color: #fafafa;
        border: 1px solid #4a4a4a;
    }
    
    .bot-bubble {
        background-color: #1e1e1e;
        color: #fafafa;
        border: 1px solid #333;
    }
    
    .message-label {
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 4px;
        color: #a6a6a6;
    }
    
    .chat-input-container {
        padding: 15px 20px;
        background-color: #262730;
        border-top: 1px solid #3d4043;
        flex-shrink: 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #3d4043 !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 6px !important;
        color: #fafafa !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff4b4b !important;
        box-shadow: 0 0 0 1px #ff4b4b !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a6a6a6 !important;
    }
    
    .stButton > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 20px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background-color: #ff6b6b !important;
        border: none !important;
    }
    
    .stButton > button:active {
        background-color: #e04444 !important;
    }
    
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #a6a6a6;
    }
    
    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.6;
    }
    
    .empty-state h3 {
        color: #fafafa;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .empty-state p {
        color: #a6a6a6;
        font-size: 14px;
    }
    
    .footer {
        text-align: center;
        padding: 12px;
        background-color: #262730;
        color: #a6a6a6;
        font-size: 12px;
        border-top: 1px solid #3d4043;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Form styling */
    .stForm {
        border: none !important;
        background: transparent !important;
    }
    
    /* Column gap */
    .row-widget {
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(
            content="Act like if You are 'Chandler Bing' from Friends. Your each response will be full of sarcasm and humor. Never break character. Always make fun of user and tease them sarcastically."
        )
    ]

# Gemini response function
def get_gemini_message(question):
    st.session_state["messages"].append(HumanMessage(content=question))
    response = llm.invoke(st.session_state["messages"])
    st.session_state["messages"].append(AIMessage(content=response.content))
    return response.content

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="chat-header">
        <div>
            <h1 class="chat-title">🧠 Chandler Bing AI</h1>
        </div>
        <div>
            <p class="chat-subtitle">Could this BE any more sarcastic?</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Chat messages container
st.markdown('<div class="chat-messages" id="chat-messages">', unsafe_allow_html=True)

# Display messages or empty state
if len(st.session_state["messages"]) <= 1:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <h3>Start chatting with Chandler</h3>
            <p>Type a message below to begin the conversation</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state["messages"][1:]:  # Skip system prompt
        if isinstance(msg, HumanMessage):
            st.markdown(f"""
                <div class="message user-message">
                    <div class="message-bubble user-bubble">
                        <div class="message-label">You</div>
                        {msg.content}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"""
                <div class="message bot-message">
                    <div class="message-bubble bot-bubble">
                        <div class="message-label">Chandler</div>
                        {msg.content}
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input at the bottom
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        question = st.text_input(
            "Message", 
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        submitted = st.form_submit_button("Send")

if submitted and question:
    response = get_gemini_message(question)
    st.rerun()  # Refresh to show new messages

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Made with sarcasm and code • Chandler Bing AI Assistant
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll to bottom script
st.markdown("""
    <script>
    function scrollToBottom() {
        var chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    setTimeout(scrollToBottom, 100);
    </script>
""", unsafe_allow_html=True)