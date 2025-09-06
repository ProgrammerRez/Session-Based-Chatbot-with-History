import os

from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import streamlit as st

def get_model(model_name='gemma2-9b-it', groq_api_key='', temp=0.7, max_tokens=100):
    return ChatGroq(
        model=model_name,
        api_key=groq_api_key,  # type: ignore
        temperature=temp,
        max_tokens=max_tokens,
    )


st.set_page_config(page_title="Conversational Chatbot with Session Based History", initial_sidebar_state="expanded")
st.title("Conversational Chatbot with Session Based History")

# Initialize memory store once
if 'memories' not in st.session_state:
    st.session_state.memories = {}

with st.sidebar:
    
    api_key = st.text_input('Groq API Key:')
    
    model_name = st.selectbox(
        "Select a Model",
        ["qwen/qwen3-32b", "gemma2-9b-it", "openai/gpt-oss-120b"],
        index=0,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.01)
    max_tokens = st.slider("Max Tokens", 50, 300, 150)

    # Handle session selection
    existing_sessions = list(st.session_state.memories.keys())
    session_id = st.selectbox(
        "Select Session",
        options=existing_sessions or ['default'],
        index=len(existing_sessions) - 1 if existing_sessions else 0,
    )

    if st.button("➕ New Session"):
        new_id = f"session_{len(st.session_state.memories) + 1}"
        st.session_state.memories[new_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        session_id = new_id


if not api_key:
    st.error('Please Enter the API Key\n You can get it from the groq console')
else:
    # Ensure the current session exists in memory
    if session_id not in st.session_state.memories:
        st.session_state.memories[session_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    memory = st.session_state.memories[session_id]

    # Define prompt template
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
        HumanMessagePromptTemplate.from_template("{chat_history}\nUser: {text}")
    ])

    # Build chain with memory
    model = get_model(model_name=model_name, temp=temperature, max_tokens=max_tokens, groq_api_key=api_key)
    chain = LLMChain(llm=model, prompt=prompt, memory=memory)


    st.subheader("Chat History")
    if history := memory.chat_memory.messages:
        for msg in history:
            if msg.type == "human":
                with st.chat_message('user'):
                    st.markdown(msg.content)
            elif msg.type == "ai":
                with st.chat_message('assistant'):
                    st.markdown(msg.content)
    else:
        st.write("No history yet.")

    # --- Chat input/output ---


    if user_input := st.chat_input("Type your message..."):
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner(text='Thinking....',show_time=True):
                response = chain.run(text=user_input)
                st.markdown(response)
