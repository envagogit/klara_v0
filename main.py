import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

apikey = st.secrets["OPENAI_API_KEY"]
ai_content = "You are a languages teacher. You will chat with the user in the same language that they chat with you. Most importantly, you will correct their spelling and give them tips to improve their grammar and expressions"


def init():
    # setup streamlit page
    st.set_page_config(page_title="Your own ChatGPT", page_icon="🤖")


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content=ai_content)]

    st.header("Your own ChatGPT 🤖")

    # sidebar with user input

    user_input = st.chat_input("Your message: ", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + "_user")
        else:
            message(msg.content, is_user=False, key=str(i) + "_ai")


if __name__ == "__main__":
    main()
