import pandas as pd 
from PIL import Image
import io

import streamlit as st

import google.generativeai as genai

import os

from dotenv import load_dotenv
 
import requests


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
 

 
# Load model

model = genai.GenerativeModel("gemini-2.5-flash")

image_model = genai.GenerativeModel("imagen-4-generate")

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

st.session_state.language = language


# -----------------------

# Initialize chat

# -----------------------
if "last_language" not in st.session_state:
    st.session_state.last_language = language

# 4. Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = "budget"


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
    st.session_state.messages = []
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

    # -----------------------
    # STEP LOGIC
    # -----------------------

    if st.session_state.step == "budget":
        st.session_state.budget = user_input
        reply = "📍 Enter your salon location"
        st.session_state.step = "location"

    elif st.session_state.step == "location":
        st.session_state.location = user_input
        st.session_state.step = "final"
        reply = "✅ Got it! Generating plan..."

    elif st.session_state.step == "final":
        

        # Build conversation (optional)
        conversation = ""
        for msg in st.session_state.messages[-3:]:
            conversation += f"{msg['role']}: {msg['content']}\n"
        
 
    # -----------------------

    # AI Prompt

    # -----------------------

prompt = f"""

You are a professional Salon Business Consultant.
 
Talk like a friendly WhatsApp advisor.

IMPORTANT:
-Reply ONLY in {language}
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


 
Your next reply:

"""
    
with st.spinner("🤖 Generating response..."):
    try:
        response = model.generate_content(prompt)

        if not response or not response.text:
            reply = "⚠️ No response from AI"
        else:
            reply = response.text

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": reply})

with st.chat_message("assistant"):
    st.write(reply)

# -----------------------
# Smart Poster Trigger
# -----------------------
if user_input and any(word in user_input.lower() for word in ["promotion", "poster", "marketing", "ads"]):

    st.divider()
    st.subheader("🎨 Create Your Salon Poster")

    shop_name = st.text_input("Salon Name")
    offer = st.text_input("Offer (e.g., 20% OFF)")

    if st.button("Generate Poster"):

        if not shop_name or not offer:
            st.warning("Please enter Salon Name and Offer")
        else:
            with st.spinner("Creating poster..."):

                poster_prompt = f"""
                Create a high-quality salon advertisement poster.

                Salon Name: {shop_name}
                Offer: {offer}
                Language: {language}

                Style:
                - Modern
                - Attractive
                - Instagram & Google Ads style
                - Bright colors
                - Clean layout

                Include stylish haircut visuals.
                """

                try:
                    response = image_model.generate_content(poster_prompt)
                    image_data = response.candidates[0].content.parts[0].inline_data.data

                    from PIL import Image
                    import io

                    img = Image.open(io.BytesIO(image_data))
                    st.image(img, use_container_width=True)

                except Exception as e:
                    st.error(f"Error: {e}")

 
# -----------------------
# Google Maps Functions
# -----------------------

def get_nearby_salons(location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": f"salon in {location}",
        "key": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        salons = []
        for place in data.get("results", [])[:5]:
            salons.append({
                "name": place.get("name"),
                "rating": place.get("rating", 0),
                "reviews": place.get("user_ratings_total", 0)
            })

        return salons

    except Exception as e:
        print("Google API Error:", e)
        return []


def analyze_competition(salons):
    if not salons:
        return "No data", 0, 0

    total = len(salons)

    ratings = [s["rating"] for s in salons if s["rating"] > 0]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    if total > 15:
        level = "High"
    elif total > 7:
        level = "Medium"
    else:
        level = "Low"

    return level, total, round(avg_rating, 2)

# -----------------------

# Reset button

# -----------------------

if st.button("🔄 Start Over"):
    st.session_state.clear()
    st.rerun()






