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

# Inject dark theme styling with chat bubbles
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #EAEAEA;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 20px;
    }
    .user-msg, .bot-msg {
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 15px;
        font-size: 16px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .user-msg {
        background-color: #1E88E5;
        color: white;
        align-self: flex-start;
        border-bottom-left-radius: 0;
    }
    .bot-msg {
        background-color: #8E24AA;
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 0;
    }
    .chat-title {
        text-align: center;
        color: #BB86FC;
    }
    .chat-subtitle {
        text-align: center;
        color: #CCCCCC;
        margin-top: -10px;
    }
    hr {
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 class='chat-title'>🧠 Your Personal Chandler Bing 🧠</h2>", unsafe_allow_html=True)
st.markdown("<p class='chat-subtitle'>A sarcastic chat assistant, could it *BE* any funnier?</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

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

# Chat input form
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input("Type something Chandler can mock 👇", placeholder="Could I BE any more sarcastic?")
    submitted = st.form_submit_button("Send 💬")

if submitted and question:
    response = get_gemini_message(question)
    st.session_state.last_response = response

# Chat history display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state["messages"][1:]:  # Skip system prompt
    if isinstance(msg, HumanMessage):
        st.markdown(f"<div class='user-msg'><strong>You:</strong><br>{msg.content}</div>", unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f"<div class='bot-msg'><strong>Chandler:</strong><br>{msg.content}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size: 0.85em;'>Made with 🧀 and sarcasm | ©️ Friends Fan Project</p>", unsafe_allow_html=True)
