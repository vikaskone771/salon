import streamlit as st

import google.generativeai as genai

import os

from dotenv import load_dotenv
 
# -----------------------

# Load environment variables

# -----------------------

load_dotenv(dotenv_path=".env")
 
api_key = os.getenv("GOOGLE_API_KEY")
 
if not api_key:

    st.error("❌ GOOGLE_API_KEY not found in .env file")

else:
    genai.configure(api_key=api_key)

    st.success("✅ API key loaded successfully")    
 
# Configure Gemini

genai.configure(api_key=api_key)
 
# Load model

model = genai.GenerativeModel("gemini-2.5-flash")
 
# -----------------------

# Page config

# -----------------------

st.set_page_config(page_title="AI Salon Advisor", layout="centered")

st.title("💇 AI Salon Business Advisor")
 
# -----------------------

# Initialize chat

# -----------------------

if "messages" not in st.session_state:

    st.session_state.messages = [

        {

            "role": "assistant",

            "content": "Hi 👋 I will help you start your salon business.\n\n💰 What is your budget?"

        }

    ]
 
# -----------------------

# Display chat

# -----------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])
 
# -----------------------

# User input

# -----------------------

user_input = st.chat_input("Type your answer...")
 
if user_input:

    # Save user message

    st.session_state.messages.append({"role": "user", "content": user_input})
 
    with st.chat_message("user"):

        st.write(user_input)
 
    # Build conversation history

    conversation = ""

    for msg in st.session_state.messages:

        conversation += f"{msg['role'].capitalize()}: {msg['content']}\n"
 
    # -----------------------

    # AI Prompt

    # -----------------------

    prompt = f"""

You are a professional Salon Business Consultant.
 
Talk like a friendly WhatsApp advisor.
 
Your job:

Ask ONLY ONE question at a time to collect:

- Budget

- Location

- Salon type (Men/Women/Unisex)

- Target customers
 
Rules:

- Do NOT ask multiple questions

- Keep replies short and natural

- Guide step-by-step
 
After collecting all details, provide:

1. Full salon setup plan

2. Cost breakdown

3. Equipment list

4. Marketing ideas

5. Monthly profit estimate
 
Conversation so far:

{conversation}
 
Your next reply:

"""
 
    # -----------------------

    # Call Gemini

    # -----------------------

    try:

        response = model.generate_content(prompt)

        reply = response.text if response.text else "⚠️ No response from AI."
 
    except Exception as e:

        reply = f"❌ Error: {str(e)}"
 
    # Save AI response

    st.session_state.messages.append({"role": "assistant", "content": reply})
 
    with st.chat_message("assistant"):

        st.write(reply)
 
# -----------------------

# Reset button

# -----------------------

if st.button("🔄 Start Over"):

    st.session_state.messages = [

        {

            "role": "assistant",

            "content": "Hi 👋 Let's start again.\n\n💰 What is your budget?"

        }

    ]
 