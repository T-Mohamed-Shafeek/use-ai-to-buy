import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.ai import groq_chat_completion
from utils.formatting import colorize_markdown

def depreciation_predictor_page():
    if st.button('← Back to Home', key='back_home_depr'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#34d399; text-align:center; margin-bottom:1.2rem;'>📉 AI Depreciation Predictor</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Predict your car's value over time with AI-powered market analysis.</div>", unsafe_allow_html=True)

    # Initialize session state
    if 'depr_result' not in st.session_state:
        st.session_state.depr_result = None
    if 'depr_loading' not in st.session_state:
        st.session_state.depr_loading = False
    if 'depr_data' not in st.session_state:
        st.session_state.depr_data = {
            'make': '',
            'model': '',
            'year': '',
            'price': '',
            'variant': '',
            'mileage': '',
            'condition': 'Excellent',
            'location': '',
            'fuel_type': '',
            'transmission': ''
        }

    # Create two columns for input and results
    input_col, results_col = st.columns([1, 1])

    with input_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Car Details</h5>", unsafe_allow_html=True)
        
        with st.form("depr_form"):
            # Basic Details
            st.markdown("<div style='color:#a1a1aa; margin-bottom:0.5rem;'>Basic Details</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                make = st.text_input(
                    "Make",
                    value=st.session_state.depr_data['make'],
                    help="Car manufacturer (e.g., Maruti Suzuki, Hyundai)"
                )
                year = st.text_input(
                    "Year",
                    value=st.session_state.depr_data['year'],
                    help="Manufacturing year"
                )
                variant = st.text_input(
                    "Variant",
                    value=st.session_state.depr_data['variant'],
                    help="Car variant/trim level"
                )
            with col2:
                model = st.text_input(
                    "Model",
                    value=st.session_state.depr_data['model'],
                    help="Car model name"
                )
                price = st.text_input(
                    "Purchase Price (₹)",
                    value=st.session_state.depr_data['price'],
                    help="Original purchase price"
                )
                mileage = st.text_input(
                    "Current Mileage (km)",
                    value=st.session_state.depr_data['mileage'],
                    help="Current odometer reading"
                )

            # Additional Details
            st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Additional Details</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                condition = st.selectbox(
                    "Condition",
                    options=["Excellent", "Good", "Fair", "Poor"],
                    index=["Excellent", "Good", "Fair", "Poor"].index(st.session_state.depr_data['condition']),
                    help="Current condition of the car"
                )
                fuel_type = st.selectbox(
                    "Fuel Type",
                    options=["Petrol", "Diesel", "Electric", "Hybrid", "CNG"],
                    index=["Petrol", "Diesel", "Electric", "Hybrid", "CNG"].index(st.session_state.depr_data['fuel_type']) if st.session_state.depr_data['fuel_type'] else 0,
                    help="Type of fuel the car uses"
                )
            with col2:
                location = st.text_input(
                    "Location",
                    value=st.session_state.depr_data['location'],
                    help="City/State where the car is registered"
                )
                transmission = st.selectbox(
                    "Transmission",
                    options=["Manual", "Automatic", "CVT", "DCT"],
                    index=["Manual", "Automatic", "CVT", "DCT"].index(st.session_state.depr_data['transmission']) if st.session_state.depr_data['transmission'] else 0,
                    help="Type of transmission"
                )

            # Submit Button
            submitted = st.form_submit_button("Predict Depreciation", use_container_width=True)

            if submitted:
                # Validate required fields
                required_fields = {
                    'Make': make,
                    'Model': model,
                    'Year': year,
                    'Price': price
                }
                
                missing_fields = [field for field, value in required_fields.items() if not value.strip()]
                
                if missing_fields:
                    st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
                else:
                    st.session_state.depr_loading = True
                    st.session_state.depr_result = None
                    
                    # Update session state
                    st.session_state.depr_data = {
                        'make': make,
                        'model': model,
                        'year': year,
                        'price': price,
                        'variant': variant,
                        'mileage': mileage,
                        'condition': condition,
                        'location': location,
                        'fuel_type': fuel_type,
                        'transmission': transmission
                    }
                    
                    with st.spinner("Predicting depreciation with AI..."):
                        try:
                            # Calculate base depreciation
                            purchase_price = float(price.replace(',', ''))
                            current_year = int(year)
                            years_old = 2024 - current_year
                            
                            # Base depreciation rates (will be adjusted by AI)
                            base_rates = {
                                "Excellent": 0.12,  # 12% per year
                                "Good": 0.15,      # 15% per year
                                "Fair": 0.18,      # 18% per year
                                "Poor": 0.25       # 25% per year
                            }
                            
                            # Calculate initial values
                            base_rate = base_rates[condition]
                            values = [purchase_price]
                            for i in range(1, 6):
                                values.append(values[-1] * (1 - base_rate))
                            
                            # Prepare data for AI
                            depr_summary = (
                                f"Make: {make}\n"
                                f"Model: {model}\n"
                                f"Year: {year}\n"
                                f"Variant: {variant}\n"
                                f"Purchase Price: ₹{price}\n"
                                f"Current Mileage: {mileage or 'N/A'}\n"
                                f"Condition: {condition}\n"
                                f"Location: {location}\n"
                                f"Fuel Type: {fuel_type}\n"
                                f"Transmission: {transmission}\n"
                                f"Base Depreciation Rate: {base_rate*100:.1f}% per year\n"
                                f"Year-by-year value projection: {', '.join([f'Year {i}: ₹{v:,.0f}' for i, v in enumerate(values)])}"
                            )

                            depr_prompt = [
                                {"role": "system", "content": (
                                    "You are an expert automotive market analyst for India. "
                                    "Given the following car details and base depreciation projection, provide: "
                                    "1. Market Analysis: "
                                    "   - 🟢 Green: Above average resale value "
                                    "   - 🟡 Yellow: Average resale value "
                                    "   - 🔴 Red: Below average resale value "
                                    "2. Adjusted Depreciation Rate: Modify the base rate based on market factors "
                                    "3. Location Impact: How the location affects resale value "
                                    "4. Maintenance Impact: How maintenance affects value retention "
                                    "5. Market Trends: Current market trends for this model "
                                    "6. Recommendations: How to maximize resale value "
                                    "Format your response as a markdown report with clear sections. "
                                    "Include specific numbers and percentages where relevant."
                                )},
                                {"role": "user", "content": depr_summary}
                            ]

                            try:
                                analysis = groq_chat_completion(depr_prompt)
                                st.session_state.depr_result = {
                                    'values': values,
                                    'analysis': analysis,
                                    'summary': depr_summary
                                }
                            except Exception as e:
                                st.session_state.depr_result = f"[Error: {e}]"
                        except Exception as e:
                            st.session_state.depr_result = f"[Error in calculation: {e}]"
                        
                    st.session_state.depr_loading = False
                    st.rerun()

    with results_col:
        if st.session_state.depr_loading:
            st.info("Predicting depreciation with AI...")
        elif st.session_state.depr_result and isinstance(st.session_state.depr_result, dict):
            st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Depreciation Analysis</h5>", unsafe_allow_html=True)
            
            # Create interactive chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(6)),
                y=st.session_state.depr_result['values'],
                mode='lines+markers',
                name='Projected Value',
                line=dict(color='#34d399', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="5-Year Value Projection",
                xaxis_title="Years",
                yaxis_title="Value (₹)",
                template="plotly_dark",
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20),
                height=300
            )
            
            fig.update_xaxes(tickvals=list(range(6)), ticktext=[f"Year {i}" for i in range(6)])
            fig.update_yaxes(tickformat="₹,.0f")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display value table
            st.markdown("<h6 style='color:#fff; margin-top:1.5rem; margin-bottom:0.5rem;'>Year-by-Year Values</h6>", unsafe_allow_html=True)
            value_df = pd.DataFrame({
                'Year': [f"Year {i}" for i in range(6)],
                'Value': [f"₹{v:,.0f}" for v in st.session_state.depr_result['values']]
            })
            st.table(value_df)
            
            # Display AI analysis
            st.markdown("<h6 style='color:#fff; margin-top:1.5rem; margin-bottom:0.5rem;'>Market Analysis</h6>", unsafe_allow_html=True)
            
            # Colorize the results
            st.markdown(colorize_markdown(st.session_state.depr_result['analysis']), unsafe_allow_html=True)
            
            # Add download button for the analysis
            st.download_button(
                label="Download Analysis",
                data=st.session_state.depr_result['analysis'],
                file_name="depreciation_analysis.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style='text-align:center; color:#a1a1aa; margin-top:2rem;'>
                <div style='font-size:2rem; margin-bottom:1rem;'>📊</div>
                <div>Fill in the car details on the left to get started</div>
            </div>
            """, unsafe_allow_html=True) 