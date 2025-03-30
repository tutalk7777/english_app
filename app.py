import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug: Print environment variable
st.write("API Key loaded:", bool(os.getenv("DEEPSEEK_API_KEY")))

# Initialize the OpenAI client with DeepSeek API
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Set page config
st.set_page_config(
    page_title="English Teacher Chatbot",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are an experienced English teacher. Your role is to:
            1. Help students improve their English speaking and writing skills
            2. Provide clear explanations of grammar concepts
            3. Give constructive feedback on their English usage
            4. Create engaging conversations to practice English
            5. Use simple and clear language when explaining concepts
            6. Provide examples to illustrate your points
            7. Be patient and encouraging
            
            Always respond in English, but if the student writes in Korean, you can provide both English and Korean responses."""
        }
    ]

# Title and description
st.title("📚 English Teacher Chatbot")
st.markdown("""
Welcome to your personal English teacher! I can help you with:
- Grammar explanations
- Speaking practice
- Writing corrections
- Vocabulary building
- Pronunciation tips
- General English questions

Feel free to ask me anything in English or Korean!
""")

# Display chat messages
for message in st.session_state.messages[1:]:  # Skip the system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about English!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages
            )
            response_content = response.choices[0].message.content
            st.markdown(response_content)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_content})

# Sidebar with additional information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This English Teacher Chatbot is powered by DeepSeek AI and designed to help you improve your English skills.
    
    ### Features:
    - Interactive conversations
    - Grammar explanations
    - Writing practice
    - Speaking exercises
    - Vocabulary building
    
    ### Tips:
    1. Be specific in your questions
    2. Practice regularly
    3. Don't be afraid to make mistakes
    4. Ask for clarification when needed
    """)
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep only the system message
        st.rerun() 