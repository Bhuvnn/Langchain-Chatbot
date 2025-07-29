import os 
from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI 
from langchain.schema import HumanMessage,AIMessage,SystemMessage 
import streamlit as st  
load_dotenv() 
api_key=os.getenv("API_KEY")  
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key,temperature=0.9)  
st.title("Your Personal 'Chandler Bing' Chat Assistant")  
if "messages" not in st.session_state:     
    st.session_state["messages"]=[SystemMessage(content="Act like if You are 'Chandler Bing' from Friends, Your each response will be full of sarcasm and humor and never break the character and also You will always make fun of user and tease them sarcastically")]  

def get_gemini_message(question):     
    st.session_state["messages"].append(HumanMessage(content=question))     
    response=llm.invoke(st.session_state["messages"])     
    st.session_state["messages"].append(AIMessage(content=response.content))     
    return response.content  

question=st.text_input("Enter Your Text") 
button=st.button("You might wanna click me")  
if button:     
    response=get_gemini_message(question=question)     
    st.write(response)    