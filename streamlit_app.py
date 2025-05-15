import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(page_title="Intelligent Customer Support Chatbot", page_icon="🤖", layout="centered")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to fetch response from OpenAI API
def fetch_response_from_openai(user_input, api_key):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except requests.RequestException as e:
        return f"⚠️ API connection failed. Details: {str(e)}"

# Streamlit UI
st.title("🤖 Intelligent Customer Support Chatbot")
st.markdown("Welcome to our automated assistant! Ask your questions below, and I'll assist you promptly.")

# API Key input
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Chat container
chat_container = st.container()

# Input for user message
with st.form(key="user_input_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your question here...", key="user_input")
    submit_button = st.form_submit_button(label="Send")

# Process user input and display chat
if submit_button and user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Fetch response from OpenAI API
    with st.spinner("🤔 Thinking..."):
        bot_response = fetch_response_from_openai(user_input, api_key)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat history
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"**You**: {message['content']}")
        else:
            with st.chat_message("assistant"):
                st.markdown(f"**Assistant**: {message['content']}")

# Sidebar with project info
with st.sidebar:
    st.header("📌 About the Project")
    st.markdown("""
    *Revolutionizing Customer Support with an Intelligent Chatbot*  
    This chatbot uses OpenAI's API to simulate an automated assistant capable of real-time intelligent conversations.
    
    **Features:**
    - Real-time chat interface
    - OpenAI-powered natural language responses
    - Streamlit-based intuitive web interface
    """)
