import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from utils.ai import groq_chat_completion
import base64
from io import BytesIO
import streamlit.components.v1 as components
import re

def clean_text_for_tts(text):
    """Clean text for TTS by removing emojis and formatting"""
    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # Code
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    text = re.sub(r'#{1,6}\s', '', text)          # Headers
    text = re.sub(r'[-*+]\s', '', text)           # List items
    text = re.sub(r'>\s', '', text)               # Blockquotes
    
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def text_to_speech(text):
    """Convert text to speech and return audio data"""
    # Clean text for TTS
    clean_text = clean_text_for_tts(text)
    tts = gTTS(text=clean_text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

def create_autoplay_audio(audio_data):
    """Create an HTML audio player with autoplay"""
    audio_base64 = base64.b64encode(audio_data.getvalue()).decode()
    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    components.html(audio_html, height=0)

def ai_assistant_chat():
    if st.button('← Back to Home', key='back_home_ai_assistant'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>🤖 AI Car Shopping Assistant</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Your personal AI guide for car buying, comparisons, and financial advice.</div>", unsafe_allow_html=True)

    # Initialize session state
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = 'text'
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = [
            {"role": "system", "content": (
                "You are an expert AI car shopping assistant specializing in the Indian market. "
                "Your role is to help users with: "
                "1. Car recommendations based on needs and budget "
                "2. Detailed comparisons between models "
                "3. Financial advice and cost analysis "
                "4. Market insights and trends "
                "5. Negotiation strategies "
                "6. Maintenance and ownership advice "
                "Always provide specific, actionable advice and use data to support your recommendations. "
                "Format your responses with clear sections and bullet points for better readability. "
                "Use emojis to highlight key points and make the conversation more engaging."
            )}
        ]
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'budget': '',
            'primary_use': '',
            'family_size': '',
            'fuel_preference': '',
            'transmission': '',
            'location': ''
        }
    if 'voice_system_prompt' not in st.session_state:
        st.session_state.voice_system_prompt = (
            "You are an expert AI car shopping assistant specializing in the Indian market. "
            "Your role is to help users with: "
            "1. Car recommendations based on needs and budget "
            "2. Detailed comparisons between models "
            "3. Financial advice and cost analysis "
            "4. Market insights and trends "
            "5. Negotiation strategies "
            "6. Maintenance and ownership advice "
            "Always provide specific, actionable advice and use data to support your recommendations. "
            "IMPORTANT: Do not use emojis, markdown formatting, or special characters in your responses. "
            "Keep the text clean and natural for text-to-speech conversion. "
            "Use simple punctuation and clear sentence structure."
        )

    # Create two columns for preferences and chat
    pref_col, chat_col = st.columns([1, 2])

    with pref_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Your Preferences</h5>", unsafe_allow_html=True)
        
        with st.form("preferences_form"):
            # Basic Preferences
            st.markdown("<div style='color:#a1a1aa; margin-bottom:0.5rem;'>Basic Details</div>", unsafe_allow_html=True)
            
            budget = st.text_input(
                "Budget Range (₹)",
                value=st.session_state.user_preferences['budget'],
                help="Your total budget including all costs"
            )
            
            primary_use = st.selectbox(
                "Primary Use",
                options=["City Commute", "Highway Travel", "Family Car", "Luxury", "Off-road", "Business"],
                index=["City Commute", "Highway Travel", "Family Car", "Luxury", "Off-road", "Business"].index(st.session_state.user_preferences['primary_use']) if st.session_state.user_preferences['primary_use'] else 0,
                help="Main purpose of the car"
            )
            
            family_size = st.selectbox(
                "Family Size",
                options=["1-2", "3-4", "5-6", "7+"],
                index=["1-2", "3-4", "5-6", "7+"].index(st.session_state.user_preferences['family_size']) if st.session_state.user_preferences['family_size'] else 0,
                help="Number of people who will regularly use the car"
            )

            # Additional Preferences
            st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Additional Details</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                fuel_preference = st.selectbox(
                    "Fuel Preference",
                    options=["Petrol", "Diesel", "Electric", "Hybrid", "CNG", "No Preference"],
                    index=["Petrol", "Diesel", "Electric", "Hybrid", "CNG", "No Preference"].index(st.session_state.user_preferences['fuel_preference']) if st.session_state.user_preferences['fuel_preference'] else 0,
                    help="Preferred fuel type"
                )
            with col2:
                transmission = st.selectbox(
                    "Transmission",
                    options=["Manual", "Automatic", "No Preference"],
                    index=["Manual", "Automatic", "No Preference"].index(st.session_state.user_preferences['transmission']) if st.session_state.user_preferences['transmission'] else 0,
                    help="Preferred transmission type"
                )
            
            location = st.text_input(
                "Location",
                value=st.session_state.user_preferences['location'],
                help="Your city/state for location-specific advice"
            )

            # Submit Button
            submitted = st.form_submit_button("Update Preferences", use_container_width=True)
            
            if submitted:
                st.session_state.user_preferences = {
                    'budget': budget,
                    'primary_use': primary_use,
                    'family_size': family_size,
                    'fuel_preference': fuel_preference,
                    'transmission': transmission,
                    'location': location
                }
                
                # Add preferences to chat history
                preferences_text = (
                    f"User Preferences:\n"
                    f"Budget: ₹{budget}\n"
                    f"Primary Use: {primary_use}\n"
                    f"Family Size: {family_size}\n"
                    f"Fuel Preference: {fuel_preference}\n"
                    f"Transmission: {transmission}\n"
                    f"Location: {location}"
                )
                st.session_state.ai_chat_history.append({"role": "user", "content": f"Please consider these preferences for future recommendations: {preferences_text}"})
                st.rerun()

    with chat_col:
        # Chat mode selector
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 Text Chat", use_container_width=True, type="primary" if st.session_state.chat_mode == 'text' else "secondary"):
                st.session_state.chat_mode = 'text'
                st.rerun()
        with col2:
            if st.button("🎤 Voice Chat", use_container_width=True, type="primary" if st.session_state.chat_mode == 'voice' else "secondary"):
                st.session_state.chat_mode = 'voice'
                st.rerun()

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.ai_chat_history[1:]:  # Skip system prompt
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style='background:#1e40af22; padding:1rem; border-radius:12px; margin-bottom:1rem;'>
                        <div style='color:#60a5fa; font-weight:600; margin-bottom:0.5rem;'>You:</div>
                        <div style='color:#e5e7eb;'>{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    if st.session_state.chat_mode == 'voice':
                        # Generate audio
                        audio_data = text_to_speech(msg['content'])
                        # Create autoplay audio player
                        create_autoplay_audio(audio_data)
                        # Display text
                        st.markdown(f"""
                        <div style='background:#181f2a; padding:1rem; border-radius:12px; margin-bottom:1rem; border:1px solid #232b3b;'>
                            <div style='color:#a78bfa; font-weight:600; margin-bottom:0.5rem;'>AI Assistant:</div>
                            <div style='color:#e5e7eb;'>{msg['content']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Text mode - just display text
                        st.markdown(f"""
                        <div style='background:#181f2a; padding:1rem; border-radius:12px; margin-bottom:1rem; border:1px solid #232b3b;'>
                            <div style='color:#a78bfa; font-weight:600; margin-bottom:0.5rem;'>AI Assistant:</div>
                            <div style='color:#e5e7eb;'>{msg['content']}</div>
                        </div>
                        """, unsafe_allow_html=True)

        # User input based on chat mode
        if st.session_state.chat_mode == 'text':
            with st.form("ai_chat_form", clear_on_submit=True):
                user_input = st.text_input("Type your question...", key="ai_chat_input")
                submitted = st.form_submit_button("Send", use_container_width=True)
                if submitted and user_input.strip():
                    st.session_state.ai_chat_history.append({"role": "user", "content": user_input})
                    try:
                        ai_response = groq_chat_completion(st.session_state.ai_chat_history)
                    except Exception as e:
                        ai_response = f"[Error: {e}]"
                    st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})
                    st.rerun()
        else:  # Voice mode
            st.markdown("<div style='text-align:center; margin-bottom:1rem;'>Click the microphone button to start speaking</div>", unsafe_allow_html=True)
            if st.button("🎤 Start Recording", use_container_width=True):
                try:
                    recognizer = sr.Recognizer()
                    with sr.Microphone() as source:
                        st.markdown("<div style='text-align:center; color:#60a5fa;'>Listening...</div>", unsafe_allow_html=True)
                        audio = recognizer.listen(source)
                        st.markdown("<div style='text-align:center; color:#60a5fa;'>Processing speech...</div>", unsafe_allow_html=True)
                        user_input = recognizer.recognize_google(audio)
                        
                        if user_input.strip():
                            st.session_state.ai_chat_history.append({"role": "user", "content": user_input})
                            try:
                                # Use voice-specific system prompt for voice mode
                                voice_messages = [{"role": "system", "content": st.session_state.voice_system_prompt}]
                                voice_messages.extend(st.session_state.ai_chat_history[1:])  # Skip the text mode system prompt
                                ai_response = groq_chat_completion(voice_messages)
                            except Exception as e:
                                ai_response = f"[Error: {e}]"
                            st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})
                            st.rerun()
                except Exception as e:
                    st.error(f"Error processing voice input: {str(e)}")
                    st.rerun()

            # Add clear chat button
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.ai_chat_history = [st.session_state.ai_chat_history[0]]  # Keep system prompt
                st.rerun() 