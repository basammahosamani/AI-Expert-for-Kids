import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Expert for Kids",
    page_icon="🤖",
    layout="centered"
)
# 2️⃣ Add Sidebar HERE 👇
with st.sidebar:
    st.title("📚 AI Expert for Kids")

    st.write("### Ask questions about:")
    st.write("✅ Science")
    st.write("✅ Mathematics")
    st.write("✅ Artificial Intelligence")
    st.write("✅ Space")
    st.write("✅ Animals")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
# 3️⃣ Main Page
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
    response = llm.invoke([
        SystemMessage(
            content="""
You are an AI teacher for children aged 5–15.
Explain everything in very simple language.
Use examples and emojis.
Keep answers friendly and easy to understand.
"""
        ),
        HumanMessage(content=message)
    ])

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
