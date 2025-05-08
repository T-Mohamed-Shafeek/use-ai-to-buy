import streamlit as st

def initialize_session_state():
    """Initialize all session state variables used across the application."""
    
    # Main navigation
    if 'user_choice' not in st.session_state:
        st.session_state.user_choice = None
    
    # Policy Scanner
    if 'policy_scan_result' not in st.session_state:
        st.session_state.policy_scan_result = None
    if 'policy_scan_loading' not in st.session_state:
        st.session_state.policy_scan_loading = False
    if 'policy_type' not in st.session_state:
        st.session_state.policy_type = "dealer_policy"
    
    # Financial Advisor
    if 'finance_result' not in st.session_state:
        st.session_state.finance_result = None
    if 'finance_loading' not in st.session_state:
        st.session_state.finance_loading = False
    if 'finance_data' not in st.session_state:
        st.session_state.finance_data = {
            'car_price': '',
            'down_payment': '',
            'loan_term': '',
            'interest_rate': '',
            'insurance': '',
            'maintenance': '',
            'fuel': '',
            'resale_value': '',
            'additional_costs': ''
        }
    
    # Model Comparison
    if 'comparison_result' not in st.session_state:
        st.session_state.comparison_result = None
    if 'comparison_loading' not in st.session_state:
        st.session_state.comparison_loading = False
    
    # Car Browser
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'search_loading' not in st.session_state:
        st.session_state.search_loading = False
    
    # AI Assistant
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_loading' not in st.session_state:
        st.session_state.chat_loading = False
        
    # Guide Page
    if 'guide_visited' not in st.session_state:
        st.session_state.guide_visited = False 