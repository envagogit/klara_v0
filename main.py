import streamlit as st
from streamlit_chat import message
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

apikey = st.secrets["OPENAI_API_KEY"]
ai_content = st.secrets["prompt_template1"]


def init():
    # setup streamlit page
    st.set_page_config(page_title="Klara", page_icon="😊")


def titles():
    st.markdown(
        "<h1 style='text-align: center;'>Klara</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h6 style='text-align: center;'>Your personal languages teacher, chat with me 😊</h6>",
        unsafe_allow_html=True,
    )
    st.divider()


def main():
    init()

    chat = ChatOpenAI(temperature=0.3)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content=ai_content)]

    # sidebar with user input

    user_input = st.chat_input("Your message: ", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(
            HumanMessage(content=str(st.secrets["prompt_template2"]) + user_input)
        )
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
    else:
        titles()

    # display message history
    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(
                msg.content.replace(str(st.secrets["prompt_template2"]), ""),
                is_user=True,
                key=str(i) + "_user",
            )
        else:
            message(
                msg.content.replace(str(st.secrets["prompt_template2"]), ""),
                is_user=False,
                key=str(i) + "_ai",
            )


if __name__ == "__main__":
    main()
