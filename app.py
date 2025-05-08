import streamlit as st
from dotenv import load_dotenv
import os
from routes.policy_scanner import policy_scanner_page
from routes.financial_advisor import financial_advisor_page
from routes.depreciation_predictor import depreciation_predictor_page
from routes.ai_assistant import ai_assistant_chat
from routes.model_comparison import model_comparison_page
from routes.car_browser import car_browser_page
from routes.ai_insights import ai_insights_page
from routes.fine_print_analyzer import fine_print_analyzer_page
from utils.session_state import initialize_session_state

load_dotenv()

# Configure the page with a wide layout and custom theme
st.set_page_config(
    page_title="Use AI to Buy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Custom CSS for dark theme and modern card/button styling
st.markdown("""
    <style>
    body, .stApp {
        background-color: #111827 !important;
        color: #e5e7eb !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    .header {
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .headline {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    .headline .ai {
        color: #60a5fa;
    }
    .subheadline {
        text-align: center;
        color: #a1a1aa;
        font-size: 1.25rem;
        margin-bottom: 2.5rem;
    }
    .card {
        background: #181f2a;
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
        padding: 2.5rem 1.5rem 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        border: 1.5px solid #232b3b;
        transition: border 0.2s, box-shadow 0.2s;
    }
    .card:hover {
        border: 1.5px solid #60a5fa;
        box-shadow: 0 8px 32px rgba(96,165,250,0.10);
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 3.5rem;
        width: 3.5rem;
        border-radius: 50%;
        margin-left: auto;
        margin-right: auto;
    }
    .card-icon.blue { background: #1e40af22; color: #60a5fa; }
    .card-icon.purple { background: #7c3aed22; color: #a78bfa; }
    .card-icon.green { background: #05966922; color: #34d399; }
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    .card-desc {
        color: #a1a1aa;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .card-btn {
        background: #2563eb;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        width: 100%;
        margin-top: 0.5rem;
    }
    .card-btn:hover {
        background: #1d4ed8;
    }
    .cta-btn {
        display: block;
        margin: 2.5rem auto 0 auto;
        background: linear-gradient(90deg, #a78bfa 0%, #818cf8 100%);
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 1.1rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 0 2px 12px #818cf822;
        cursor: pointer;
        transition: background 0.2s;
    }
    .cta-btn:hover {
        background: linear-gradient(90deg, #818cf8 0%, #a78bfa 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# Remove sidebar navigation; use only main content area
st.markdown('<div class="header"></div>', unsafe_allow_html=True)

# Route handling
if st.session_state.user_choice == "policy_scanner":
    policy_scanner_page()
elif st.session_state.user_choice == "financial_advisor":
    financial_advisor_page()
elif st.session_state.user_choice == "depreciation_predictor":
    depreciation_predictor_page()
elif st.session_state.user_choice == "ai_agent":
    ai_agent_page()
elif st.session_state.user_choice == "ai_assistant":
    ai_assistant_chat()
elif st.session_state.user_choice == "model_comparison":
    model_comparison_page()
elif st.session_state.user_choice == "car_browser":
    car_browser_page()
elif st.session_state.user_choice == "ai_insights":
    ai_insights_page()
elif st.session_state.user_choice == "fine_print_analyzer":
    fine_print_analyzer_page()
else:
    # Top headline and subheadline
    st.markdown("""
    <div style='margin-top:2.5rem;'></div>
    <div style='text-align:center;'>
        <span style='font-size:3.2rem; font-weight:800; color:#fff;'>Use <span style='color:#60a5fa;'>AI</span> to Find Your Perfect Car</span>
        <div style='margin-top:1.2rem; color:#a1a1aa; font-size:1.3rem; font-weight:400;'>
            Revolutionizing automotive shopping with AI-powered insights, transparent terms, and personalized recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:2.5rem;'></div>", unsafe_allow_html=True)

    # Main 3 cards row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='card' style='background:#181f2a; border-radius:18px; border:1.5px solid #232b3b; text-align:center;'>
            <div style='font-size:2.2rem; margin-bottom:1.2rem; color:#60a5fa; background:#1e40af22; width:3.5rem; height:3.5rem; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto;'>→</div>
            <div style='font-size:1.25rem; font-weight:700; color:#fff; margin-bottom:0.5rem;'>I Know What I Want</div>
            <div style='color:#a1a1aa; font-size:1rem; margin-bottom:1.5rem;'>Go straight to browsing with our advanced filters to find your exact match.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button('Browse Cars   →', key='browse_btn', use_container_width=True):
            st.session_state.user_choice = 'car_browser'
            st.rerun()
    with col2:
        st.markdown("""
        <div class='card' style='background:#181f2a; border-radius:18px; border:1.5px solid #60a5fa; text-align:center;'>
            <div style='font-size:2.2rem; margin-bottom:1.2rem; color:#a78bfa; background:#7c3aed22; width:3.5rem; height:3.5rem; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto;'>👜</div>
            <div style='font-size:1.25rem; font-weight:700; color:#fff; margin-bottom:0.5rem;'>I Need Your Help</div>
            <div style='color:#a1a1aa; font-size:1rem; margin-bottom:1.5rem;'>Let our AI guide you through the car buying process with personalized recommendations.</div>
        """, unsafe_allow_html=True)
        if st.button('Get AI Guidance   🔍', key='ai_help_btn', use_container_width=True):
            st.session_state.user_choice = 'ai_assistant'
    with col3:
        st.markdown("""
        <div class='card' style='background:#181f2a; border-radius:18px; border:1.5px solid #232b3b; text-align:center;'>
            <div style='font-size:2.2rem; margin-bottom:1.2rem; color:#34d399; background:#05966922; width:3.5rem; height:3.5rem; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto;'>📋</div>
            <div style='font-size:1.25rem; font-weight:700; color:#fff; margin-bottom:0.5rem;'>Compare Models</div>
            <div style='color:#a1a1aa; font-size:1rem; margin-bottom:1.5rem;'>Easily compare up to 5 different models side by side to make an informed decision.</div>
        """, unsafe_allow_html=True)
        if st.button('Compare Cars   →', key='compare_btn', use_container_width=True):
            st.session_state.user_choice = 'model_comparison'
            st.rerun()

    # CTA button
    st.markdown("""
    <div style='display:flex; justify-content:center; margin-top:2.5rem; margin-bottom:2.5rem;'>
        <button style='background:#a78bfa; color:#fff; border:none; border-radius:12px; padding:1.1rem 2.5rem; font-size:1.1rem; font-weight:700; box-shadow:0 2px 12px #818cf822; cursor:pointer;'>
            <span style='font-size:1.2rem; margin-right:0.7rem;'>❓</span>How to Get the Most Out of Our Site
        </button>
    </div>
    """, unsafe_allow_html=True)

    # Four AI tool cards below
    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; font-size:1.1rem; margin-bottom:1.5rem;'>AI Tools</div>", unsafe_allow_html=True)
    
    # Create 5 columns for the AI tools
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <div class='card-icon blue'>🛡️</div>
            <div class='card-title'>AI Policy Scanner</div>
            <div class='card-desc'>Automatically reviews car listings for hidden policy issues, accident history, and ownership red flags.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Scan Policy   →", key="card1", use_container_width=True):
            st.session_state.user_choice = "policy_scanner"
    with col2:
        st.markdown("""
        <div class='card'>
            <div class='card-icon purple'>💸</div>
            <div class='card-title'>AI Financial Advisor</div>
            <div class='card-desc'>Estimates your monthly costs, insurance, and total cost of ownership for confident buying.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Deal   →", key="card2", use_container_width=True):
            st.session_state.user_choice = "financial_advisor"
    with col3:
        st.markdown("""
        <div class='card'>
            <div class='card-icon green'>📉</div>
            <div class='card-title'>Depreciation & Resale Value Predictor</div>
            <div class='card-desc'>Predicts how your car's value will change over time for smarter long-term decisions.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Predict Value   →", key="card3", use_container_width=True):
            st.session_state.user_choice = "depreciation_predictor"
    with col4:
        st.markdown("""
        <div class='card'>
            <div class='card-icon blue'>📄</div>
            <div class='card-title'>Fine Print Analyzer</div>
            <div class='card-desc'>Translates complex agreements, highlights risks, and explains financial impact in plain language.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Fine Print   →", key="card4", use_container_width=True):
            st.session_state.user_choice = "fine_print_analyzer"
    with col5:
        st.markdown("""
        <div class='card'>
            <div class='card-icon purple'>📊</div>
            <div class='card-title'>AI Insights</div>
            <div class='card-desc'>Comprehensive market analysis with visual charts for pricing, costs, and future value projections.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Insights   →", key="card5", use_container_width=True):
            st.session_state.user_choice = "ai_insights"

    # Back button for all routes
    if st.session_state.user_choice:
        if st.button("← Back to Home", key="back_home"):
            st.session_state.user_choice = None
            st.rerun()

# At the end of the file, add the floating chat icon and modal logic
if 'show_ai_chat' not in st.session_state:
    st.session_state.show_ai_chat = False

chat_icon_style = """
    position: fixed;
    bottom: 32px;
    right: 32px;
    z-index: 9999;
    background: linear-gradient(135deg, #60a5fa 60%, #a78bfa 100%);
    color: #fff;
    border-radius: 50%;
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 24px rgba(96,165,250,0.18);
    cursor: pointer;
    font-size: 2.2rem;
    border: none;
"""


# Listen for the open_ai_chat event and toggle session state
import streamlit.components.v1 as components
components.html('''
<script>
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'open_ai_chat') {
        window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'show_ai_chat', value: true}, '*');
    }
});
</script>
''', height=0)

if st.session_state.get('show_ai_chat', False):
    st.markdown("""
    <div style='position:fixed; bottom:110px; right:32px; z-index:10000; width:400px; max-width:90vw; background:#181f2a; border-radius:18px; box-shadow:0 8px 32px rgba(96,165,250,0.18); padding:1.5rem 1rem 1rem 1rem;'>
    """, unsafe_allow_html=True)
    ai_assistant_chat()
    if st.button('Close', key='close_ai_chat'):
        st.session_state.show_ai_chat = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True) 