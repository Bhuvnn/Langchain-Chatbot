#Q&A Chatbot
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate,ChatPromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')

def get_response(question):
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                               api_key=api_key)
    response=llm.invoke(question)
    return response

## Initialize our streamlit
st.title("QnA Chatbot")
st.header("Langchain Application")
input_text=st.text_input("Enter Your Question")
submit=st.button("Ask the Question")


if submit:
    response=get_response(input_text)
    st.subheader("The response is: ")
    st.write(response.content) 
    
    
    




