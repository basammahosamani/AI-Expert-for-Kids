import streamlit as st
from langchain_groq import ChatGroq

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="🤖 AI Expert for Kids")

st.title("🤖 AI Expert for Kids")
st.write("Ask any AI question. The AI explains concepts for kids aged 5–15 years.")

# -----------------------------
# Initialize Groq LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=st.secrets["GROQ_API_KEY"]
)

# -----------------------------
# Chatbot Function
# -----------------------------
def chatbot(message):
    response = llm.invoke(message)
    return response.content

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Ask your question")

if prompt:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.spinner("Thinking..."):
        response = chatbot(prompt)

    # Display AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)
