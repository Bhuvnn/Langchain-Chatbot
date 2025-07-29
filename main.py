import os
from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import streamlit as st
import time

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
st.set_page_config(
    page_title="Chandler Bing Chat", 
    page_icon="🤦‍♂️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Chandler's personality
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    
    :root {{
        --chandler-dark: #1A1A2E;
        --chandler-purple: #4A3AFF;
        --chandler-teal: #00C6B8;
        --chandler-pink: #FF4B91;
        --chandler-yellow: #FFD166;
        --chandler-light: #F5F5F7;
    }}
    
    * {{
        font-family: 'Montserrat', sans-serif;
        box-sizing: border-box;
    }}
    
    body, .stApp {{
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        margin: 0;
        padding: 0;
        min-height: 100vh;
        color: var(--chandler-light);
        overflow-x: hidden;
    }}
    
    .chandler-container {{
        max-width: 1200px;
        margin: 2rem auto;
        padding: 1.5rem;
        border-radius: 20px;
        background: rgba(26, 26, 46, 0.85);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(74, 58, 255, 0.2);
    }}
    
    .header {{
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(74, 58, 255, 0.3);
        position: relative;
    }}
    
    .header h1 {{
        font-size: 2.8rem;
        margin: 0;
        background: linear-gradient(90deg, var(--chandler-teal), var(--chandler-pink), var(--chandler-yellow));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    
    .header p {{
        font-size: 1.1rem;
        color: rgba(245, 245, 247, 0.7);
        max-width: 600px;
        margin: 0.5rem auto 0;
        font-weight: 500;
    }}
    
    .chat-container {{
        display: flex;
        flex-direction: column;
        height: 65vh;
        background: rgba(30, 30, 50, 0.7);
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(74, 58, 255, 0.15);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }}
    
    .chat-messages {{
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }}
    
    .message {{
        max-width: 80%;
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        position: relative;
        animation: messageAppear 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        line-height: 1.5;
        font-size: 1.05rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    
    @keyframes messageAppear {{
        0% {{
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
    
    .user-message {{
        align-self: flex-end;
        background: linear-gradient(135deg, var(--chandler-purple), #6A5BFF);
        color: white;
        border-bottom-right-radius: 5px;
    }}
    
    .bot-message {{
        align-self: flex-start;
        background: rgba(40, 40, 60, 0.95);
        border: 1px solid rgba(74, 58, 255, 0.25);
        color: var(--chandler-light);
        border-bottom-left-radius: 5px;
    }}
    
    .bot-message::before {{
        content: "";
        position: absolute;
        left: -12px;
        top: 0;
        border: 10px solid transparent;
        border-right-color: rgba(40, 40, 60, 0.95);
        border-left: 0;
    }}
    
    .user-message::after {{
        content: "";
        position: absolute;
        right: -12px;
        top: 0;
        border: 10px solid transparent;
        border-left-color: #6A5BFF;
        border-right: 0;
    }}
    
    .message-header {{
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }}
    
    .user-header {{
        color: var(--chandler-yellow);
    }}
    
    .bot-header {{
        color: var(--chandler-teal);
    }}
    
    .message-icon {{
        margin-right: 0.7rem;
        font-size: 1.3rem;
    }}
    
    .input-container {{
        padding: 1.5rem;
        background: rgba(30, 30, 50, 0.9);
        border-top: 1px solid rgba(74, 58, 255, 0.2);
    }}
    
    .input-area {{
        display: flex;
        gap: 1rem;
    }}
    
    .input-area input {{
        flex: 1;
        padding: 1rem 1.5rem;
        border-radius: 50px;
        border: 2px solid rgba(74, 58, 255, 0.3);
        background: rgba(20, 20, 35, 0.7);
        color: white;
        font-size: 1.05rem;
        outline: none;
        transition: all 0.3s ease;
    }}
    
    .input-area input:focus {{
        border-color: var(--chandler-teal);
        box-shadow: 0 0 0 3px rgba(0, 198, 184, 0.2);
    }}
    
    .input-area button {{
        padding: 1rem 2.5rem;
        border-radius: 50px;
        border: none;
        background: linear-gradient(90deg, var(--chandler-teal), var(--chandler-pink));
        color: white;
        font-weight: 600;
        font-size: 1.05rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 198, 184, 0.3);
    }}
    
    .input-area button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 198, 184, 0.4);
    }}
    
    .input-area button:active {{
        transform: translateY(0);
    }}
    
    .typing-indicator {{
        display: inline-flex;
        align-items: center;
        padding: 0.8rem 1.5rem;
        background: rgba(40, 40, 60, 0.95);
        border-radius: 18px;
        border: 1px solid rgba(74, 58, 255, 0.25);
        color: rgba(245, 245, 247, 0.7);
        font-style: italic;
        margin-top: 0.5rem;
        border-bottom-left-radius: 5px;
    }}
    
    .typing-dots {{
        display: flex;
        margin-left: 0.5rem;
    }}
    
    .typing-dots span {{
        width: 8px;
        height: 8px;
        background: var(--chandler-teal);
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out;
    }}
    
    .typing-dots span:nth-child(1) {{
        animation-delay: 0s;
    }}
    .typing-dots span:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    .typing-dots span:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    
    @keyframes typing {{
        0%, 60%, 100% {{
            transform: translateY(0);
        }}
        30% {{
            transform: translateY(-5px);
        }}
    }}
    
    .empty-state {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 2rem;
        text-align: center;
        opacity: 0.7;
    }}
    
    .empty-state-icon {{
        font-size: 4rem;
        margin-bottom: 1.5rem;
        color: var(--chandler-teal);
    }}
    
    .empty-state h3 {{
        font-size: 1.8rem;
        margin-bottom: 1rem;
        color: var(--chandler-yellow);
    }}
    
    .empty-state p {{
        font-size: 1.1rem;
        max-width: 500px;
        line-height: 1.6;
    }}
    
    .footer {{
        text-align: center;
        padding: 2rem 0 1rem;
        font-size: 0.9rem;
        color: rgba(245, 245, 247, 0.6);
    }}
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {{
        width: 8px;
    }}
    
    .chat-messages::-webkit-scrollbar-track {{
        background: rgba(20, 20, 35, 0.3);
        border-radius: 4px;
    }}
    
    .chat-messages::-webkit-scrollbar-thumb {{
        background: linear-gradient(var(--chandler-purple), var(--chandler-pink));
        border-radius: 4px;
    }}
    
    /* Hide Streamlit elements */
    .stDeployButton {{ display: none; }}
    footer {{ visibility: hidden; }}
    .stApp > header {{ visibility: hidden; }}
    #MainMenu {{ visibility: hidden; }}
    .st-emotion-cache-1dp5vir {{ display: none; }}
    </style>
""", unsafe_allow_html=True)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content="Act like if You are 'Chandler Bing' from Friends. Your each response will be full of sarcasm and humor. Never break character. Always make fun of user and tease them sarcastically."
        )
    ]

if "typing" not in st.session_state:
    st.session_state.typing = False

# Gemini response function with typing simulation
def get_gemini_message(question):
    st.session_state.messages.append(HumanMessage(content=question))
    st.session_state.typing = True
    st.experimental_rerun()
    
    # Simulate typing delay
    time.sleep(1.5)
    
    response = llm.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.typing = False
    return response.content

# Main container
st.markdown('<div class="chandler-container">', unsafe_allow_html=True)

# Header with sarcastic title
st.markdown("""
    <div class="header">
        <h1>🤦‍♂️ Chandler Bing AI</h1>
        <p>Could this BE any more sarcastic? Ask me anything and prepare for maximum snark!</p>
    </div>
""", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages" id="chat-messages">', unsafe_allow_html=True)

# Display messages or empty state
if len(st.session_state.messages) <= 1:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <h3>Could I BE any more ready?</h3>
            <p>Start a conversation below and prepare for my world-class sarcasm.<br>Don't worry, I'll try not to hurt your feelings... much.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages[1:]:  # Skip system prompt
        if isinstance(msg, HumanMessage):
            st.markdown(f"""
                <div class="message user-message">
                    <div class="message-header user-header">
                        <div class="message-icon">👤</div>
                        <div>You</div>
                    </div>
                    {msg.content}
                </div>
            """, unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"""
                <div class="message bot-message">
                    <div class="message-header bot-header">
                        <div class="message-icon">🤦‍♂️</div>
                        <div>Chandler</div>
                    </div>
                    {msg.content}
                </div>
            """, unsafe_allow_html=True)
    
    # Show typing indicator if waiting for response
    if st.session_state.typing:
        st.markdown("""
            <div class="typing-indicator">
                Thinking of something sarcastic to say...
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End chat-messages

# Input area at the bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    input_col, button_col = st.columns([5, 1])
    
    with input_col:
        question = st.text_input(
            "Message", 
            placeholder="Type something... if you dare...",
            label_visibility="collapsed"
        )
    
    with button_col:
        submitted = st.form_submit_button("Sarcasm Me", use_container_width=True)

if submitted and question:
    get_gemini_message(question)

st.markdown('</div>', unsafe_allow_html=True)  # End input-container
st.markdown('</div>', unsafe_allow_html=True)  # End chat-container

# Footer
st.markdown("""
    <div class="footer">
        Made with 99% sarcasm and 1% actual effort • Chandler Bing AI Assistant
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End chandler-container

# Auto-scroll to bottom script
st.markdown("""
    <script>
    function scrollToBottom() {
        var chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Scroll when new messages appear
    setTimeout(scrollToBottom, 100);
    setInterval(scrollToBottom, 500);
    </script>
""", unsafe_allow_html=True)