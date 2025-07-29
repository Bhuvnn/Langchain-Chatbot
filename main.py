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

# Streamlit page config
st.set_page_config(page_title="Chandler Bing Chat", page_icon="🧠", layout="centered")

# Title
st.markdown("""
    <h2 style='text-align: center; color: #6C63FF;'>🧠 Your Personal Chandler Bing 🧠</h2>
    <p style='text-align: center;'>A sarcastic chat assistant, could it *be* any funnier?</p>
    <hr style="border:1px solid #ccc;">
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(
            content="Act like if You are 'Chandler Bing' from Friends. Your each response will be full of sarcasm and humor. Never break character. Always make fun of user and tease them sarcastically."
        )
    ]

# Function to get response
def get_gemini_message(question):
    st.session_state["messages"].append(HumanMessage(content=question))
    response = llm.invoke(st.session_state["messages"])
    st.session_state["messages"].append(AIMessage(content=response.content))
    return response.content

# Chat UI
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input("Type something Chandler can mock 👇", placeholder="Could I BE any more sarcastic?")
    submitted = st.form_submit_button("Send 💬")

if submitted and question:
    response = get_gemini_message(question)
    st.session_state.last_response = response

# Display chat history
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("### 💬 Conversation")

for msg in st.session_state["messages"][1:]:  # Skip system message
    if isinstance(msg, HumanMessage):
        st.markdown(f"""
        <div style="background-color:#DCF8C6; padding:10px 15px; border-radius:10px; margin-bottom:10px; max-width:75%; align-self:flex-start;">
            <strong>You:</strong> {msg.content}
        </div>
        """, unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f"""
        <div style="background-color:#F3E8FF; padding:10px 15px; border-radius:10px; margin-bottom:10px; max-width:75%; align-self:flex-end; margin-left:auto;">
            <strong>Chandler:</strong> {msg.content}
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size: 0.85em;'>Made with 🧀 and sarcasm | ©️ Friends Fan Project</p>", unsafe_allow_html=True)
