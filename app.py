import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Expert for Student",
    page_icon="🤖",
    layout="centered"
)
# 2️⃣ Add Sidebar HERE 👇
with st.sidebar:
    st.title("📚 AI Expert for Students")

    st.write("### Ask questions about:")
    st.write("✅ Natural Language")
    st.write("✅ Deep Learning")
    st.write("✅ Artificial Intelligence")
    st.write("✅ Machine Learning")
    st.write("✅ LLM")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


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
        # -----------------------------
# Edit Last User Message
# -----------------------------
if len(st.session_state.messages) >= 2:
    last_user = None

    # Find the last user message
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            last_user = msg["content"]
            break

    st.divider()
    st.subheader("✏️ Edit Last Question")

    edited_message = st.text_input(
        "Modify your last question:",
        value=last_user
    )

    if st.button("🔄 Regenerate Answer"):
        # Remove last user + assistant messages
        st.session_state.messages = st.session_state.messages[:-2]

        # Add edited user message
        st.session_state.messages.append(
            {"role": "user", "content": edited_message}
        )

        # Generate new response
        with st.spinner("🤖 Thinking..."):
            new_response = chatbot(edited_message)

        st.session_state.messages.append(
            {"role": "assistant", "content": new_response}
        )

        st.rerun()
