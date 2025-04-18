# Import necessary libraries 
import streamlit as st                      # Web app interface
import google.generativeai as genai        # Gemini AI for translation
from dotenv import load_dotenv             # To load API keys securely
import os                                  # For environment variable access
import pyttsx3                             # For text-to-speech (optional)

# Load environment variables from .env 
load_dotenv()

# Configure Gemini AI using your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model 
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Define translation function
def language_translate(text, source_lang, target_lang):
    # Format the prompt for Gemini
    prompt = f"""
    Translate the following text from {source_lang} to {target_lang}:

    {text}

    Please don't add any extra text, only the translated text.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "Translation failed."

# Text-to-Speech function 
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Front end design with Streamlit

# Page setup
st.set_page_config(page_title="Gemini Language Translator", layout="centered")


# Custom CSS
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center;
        color: #0066cc;
        font-size: 36px;
    }
    .stTextArea textarea {
        font-size: 14px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)


# App Title
st.markdown("<div class='title'>🌐 Gemini Language Translator</div>", unsafe_allow_html=True)
st.markdown("---")

# Text input
user_text = st.text_area("✍️ Enter the text you want to translate:")

# List of supported languages
languages = sorted([
    "English", "Spanish", "French", "German", "Urdu", "Hindi", "Chinese", "Japanese", "Korean", "Arabic", 
    "Russian", "Portuguese", "Italian", "Dutch", "Greek", "Polish", "Swedish", "Turkish", "Thai", 
    "Vietnamese", "Indonesian", "Hebrew", "Czech", "Hungarian", "Finnish", "Romanian", "Bulgarian", 
    "Ukrainian", "Malay", "Filipino", "Tamil", "Telugu", "Kannada", "Marathi", "Gujarati", "Bengali", 
    "Pashto", "Farsi", "Sinhala", "Swahili", "Zulu", "Xhosa", "Yoruba", "Igbo", "Hausa", 
    "Somali", "Amharic", "Nepali", "Burmese", "Khmer", "Lao"
])

# Language selectors
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Translate from:", languages, index=languages.index("English"))
with col2:
    target_lang = st.selectbox("Translate to:", languages, index=languages.index("French"))

# Translate button
if st.button("🌍 Translate"):
    if user_text.strip():
        # Call translation function
        translation = language_translate(user_text, source_lang, target_lang)
        
        # Display translation
        st.markdown("#### ✅ Translated Text:")
        st.success(translation)

        # Add text-to-speech playback
        if st.checkbox("🔊 Read Aloud Translated Text"):
            speak_text(translation)
    else:
        st.warning("⚠️ Please enter text to translate.")
