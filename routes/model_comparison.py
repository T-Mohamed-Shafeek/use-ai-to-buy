import streamlit as st
import pandas as pd
from utils.ai import groq_chat_completion
from utils.formatting import colorize_markdown

def model_comparison_page():
    if st.button('← Back to Home', key='back_home_compare'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>🚗 AI Model Comparison</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Compare up to 5 car models with AI-powered insights on value, costs, and recommendations.</div>", unsafe_allow_html=True)

    # Initialize session state for comparison data
    if 'comparison_data' not in st.session_state:
        st.session_state.comparison_data = []
    if 'comparison_result' not in st.session_state:
        st.session_state.comparison_result = None
    if 'comparison_loading' not in st.session_state:
        st.session_state.comparison_loading = False

    # Form for adding a model
    with st.form("add_model_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            make = st.text_input("Make", key="compare_make")
            model = st.text_input("Model", key="compare_model")
        with col2:
            year = st.text_input("Year", key="compare_year")
            price = st.text_input("Price (₹)", key="compare_price")
        with col3:
            variant = st.text_input("Variant", key="compare_variant")
            mileage = st.text_input("Expected Annual Mileage (km)", key="compare_mileage")
        
        add_model = st.form_submit_button("Add Model to Comparison")

    if add_model and make.strip() and model.strip() and year.strip() and price.strip():
        if len(st.session_state.comparison_data) < 5:
            try:
                price_val = float(price.replace(',', ''))
                st.session_state.comparison_data.append({
                    'make': make,
                    'model': model,
                    'year': year,
                    'price': price_val,
                    'variant': variant,
                    'mileage': mileage
                })
                st.rerun()
            except ValueError:
                st.error("Please enter a valid price")
        else:
            st.error("Maximum 5 models can be compared")

    # Display added models
    if st.session_state.comparison_data:
        st.markdown("<h5 style='color:#fff; margin-top:1.5rem;'>Models to Compare</h5>", unsafe_allow_html=True)
        for i, car in enumerate(st.session_state.comparison_data):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"<div style='color:#fff;'>{car['make']} {car['model']} ({car['year']}) - {car['variant']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='color:#a1a1aa;'>₹{car['price']:,.0f}</div>", unsafe_allow_html=True)
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.comparison_data.pop(i)
                    st.rerun()

        # Compare button
        if st.button("Compare Models", use_container_width=True):
            st.session_state.comparison_loading = True
            st.session_state.comparison_result = None
            
            with st.spinner("Analyzing models with AI..."):
                # Prepare comparison data for AI
                comparison_text = "\n\n".join([
                    f"Model {i+1}:\n"
                    f"Make: {car['make']}\n"
                    f"Model: {car['model']}\n"
                    f"Year: {car['year']}\n"
                    f"Price: ₹{car['price']:,.0f}\n"
                    f"Variant: {car['variant']}\n"
                    f"Expected Annual Mileage: {car['mileage'] or 'N/A'}"
                    for i, car in enumerate(st.session_state.comparison_data)
                ])

                comparison_prompt = [
                    {"role": "system", "content": (
                        "You are an expert automotive analyst for the Indian market. "
                        "Compare the following car models and provide: "
                        "1. Future value prediction after 3 years for each model "
                        "2. Depreciation rate analysis "
                        "3. Potential dealer policy caveats to watch for "
                        "4. Monthly ownership cost comparison "
                        "5. Purchase recommendations with clear reasoning "
                        "Format your response as a markdown report with clear sections. "
                        "Use color indicators: 🟢 for positive, 🟡 for neutral, 🔴 for negative. "
                        "Include specific numbers and percentages where relevant."
                    )},
                    {"role": "user", "content": comparison_text}
                ]

                try:
                    result = groq_chat_completion(comparison_prompt)
                    st.session_state.comparison_result = result
                except Exception as e:
                    st.session_state.comparison_result = f"[Error: {e}]"
                
            st.session_state.comparison_loading = False
            st.rerun()

    # Display comparison results
    if st.session_state.comparison_loading:
        st.info("Analyzing models with AI...")
    elif st.session_state.comparison_result:
        st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h5 style='color:#fff;'>AI Comparison Analysis</h5>", unsafe_allow_html=True)
        
        # Colorize the results
        st.markdown(colorize_markdown(st.session_state.comparison_result), unsafe_allow_html=True) 