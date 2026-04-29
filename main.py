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

# Example: set language from user input or default
if "language" not in st.session_state:
    st.session_state.language = "English"

language = st.session_state.language

 
# -----------------------

# Page config

# -----------------------

st.set_page_config(page_title="AI Salon Advisor", layout="centered")

st.title("💇 AI Salon Business Advisor")
 
# -----------------------
# Language Selection
# -----------------------
language = st.selectbox(
    "🌐 Select Language",
    ["English", "Hindi", "Kannada", "Tamil", "Telugu", "Malayalam"]
)

 # -----------------------

 # Welcome messages in multiple languages

 # -----------------------
 
welcome_messages = {
    "English": "Hi 👋 I will help you start your salon business.\n\n💰 What is your budget?",
    "Hindi": "नमस्ते 👋 मैं आपके सैलून बिज़नेस में मदद करूंगा।\n\n💰 आपका बजट क्या है?",
    "Kannada": "ನಮಸ್ಕಾರ 👋 ನಿಮ್ಮ ಸಲೂನ್ ವ್ಯವಹಾರ ಆರಂಭಿಸಲು ನಾನು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.\n\n💰 ನಿಮ್ಮ ಬಜೆಟ್ ಎಷ್ಟು?",
    "Tamil": "வணக்கம் 👋 உங்கள் சலூன் தொழிலை தொடங்க நான் உதவுவேன்.\n\n💰 உங்கள் பட்ஜெட் என்ன?",
    "Telugu": "హాయ్ 👋 మీ సలోన్ బిజినెస్ ప్రారంభించడానికి నేను సహాయం చేస్తాను.\n\n💰 మీ బడ్జెట్ ఎంత?",
    "Malayalam": "ഹലോ 👋 നിങ്ങളുടെ സലൂൺ ബിസിനസ് തുടങ്ങാൻ ഞാൻ സഹായിക്കും.\n\n💰 നിങ്ങളുടെ ബജറ്റ് എത്ര?"
}

# -----------------------

# Initialize chat

# -----------------------
if "last_language" not in st.session_state:
    st.session_state.last_language = language

# 4. Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": welcome_messages[language]
        }
    ]


lang_map = {
    "English": "English",
    "Hindi": "Hindi",
    "Kannada": "Kannada",
    "Tamil": "Tamil",
    "Telugu": "Telugu",
    "Malayalam": "Malayalam"
}

selected_lang = lang_map[language]

# -----------------------

# Detect language change

# -----------------------

if st.session_state.last_language != language:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": welcome_messages[language]
        }
    ]
    st.session_state.last_language = language
    st.rerun()

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

IMPORTANT:
-Reply ONLY in {selected_lang}
- Do NOT mix languages
- Keep sentences simple and local-friendly

Understand user input in any language, but reply ONLY in {language}.

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
 