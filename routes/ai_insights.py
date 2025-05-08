import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.ai import groq_chat_completion

def ai_insights_page():
    if st.button('← Back to Home', key='back_home_insights'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#a78bfa; text-align:center; margin-bottom:1.2rem;'>📊 AI Insights</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Comprehensive market analysis with visual insights for informed car buying decisions.</div>", unsafe_allow_html=True)

    # Initialize session state
    if 'insights_data' not in st.session_state:
        st.session_state.insights_data = {
            'make': '',
            'model': '',
            'year': '',
            'price': '',
            'variant': '',
            'location': '',
            'fuel_type': '',
            'transmission': '',
            'mileage': '',
            'condition': 'Excellent'
        }
    if 'insights_result' not in st.session_state:
        st.session_state.insights_result = None
    if 'insights_loading' not in st.session_state:
        st.session_state.insights_loading = False

    # Create two columns for input and results
    input_col, results_col = st.columns([1, 1])

    with input_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Car Details</h5>", unsafe_allow_html=True)
        
        with st.form("insights_form"):
            # Basic Details
            st.markdown("<div style='color:#a1a1aa; margin-bottom:0.5rem;'>Basic Details</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                make = st.text_input(
                    "Make",
                    value=st.session_state.insights_data['make'],
                    help="Car manufacturer (e.g., Maruti Suzuki, Hyundai)"
                )
                year = st.text_input(
                    "Year",
                    value=st.session_state.insights_data['year'],
                    help="Manufacturing year"
                )
                variant = st.text_input(
                    "Variant",
                    value=st.session_state.insights_data['variant'],
                    help="Car variant/trim level"
                )
            with col2:
                model = st.text_input(
                    "Model",
                    value=st.session_state.insights_data['model'],
                    help="Car model name"
                )
                price = st.text_input(
                    "Price (₹)",
                    value=st.session_state.insights_data['price'],
                    help="Current price"
                )
                location = st.text_input(
                    "Location",
                    value=st.session_state.insights_data['location'],
                    help="City/State for market analysis"
                )

            # Additional Details
            st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Additional Details</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                fuel_type = st.selectbox(
                    "Fuel Type",
                    options=["Petrol", "Diesel", "Electric", "Hybrid", "CNG"],
                    index=["Petrol", "Diesel", "Electric", "Hybrid", "CNG"].index(st.session_state.insights_data['fuel_type']) if st.session_state.insights_data['fuel_type'] else 0,
                    help="Type of fuel the car uses"
                )
                condition = st.selectbox(
                    "Condition",
                    options=["Excellent", "Good", "Fair", "Poor"],
                    index=["Excellent", "Good", "Fair", "Poor"].index(st.session_state.insights_data['condition']),
                    help="Current condition of the car"
                )
            with col2:
                transmission = st.selectbox(
                    "Transmission",
                    options=["Manual", "Automatic", "CVT", "DCT"],
                    index=["Manual", "Automatic", "CVT", "DCT"].index(st.session_state.insights_data['transmission']) if st.session_state.insights_data['transmission'] else 0,
                    help="Type of transmission"
                )
                mileage = st.text_input(
                    "Mileage (km)",
                    value=st.session_state.insights_data['mileage'],
                    help="Current odometer reading"
                )

            # Submit Button
            submitted = st.form_submit_button("Generate Insights", use_container_width=True)

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
                    st.session_state.insights_loading = True
                    st.session_state.insights_result = None
                    
                    # Update session state
                    st.session_state.insights_data = {
                        'make': make,
                        'model': model,
                        'year': year,
                        'price': price,
                        'variant': variant,
                        'location': location,
                        'fuel_type': fuel_type,
                        'transmission': transmission,
                        'mileage': mileage,
                        'condition': condition
                    }
                    
                    with st.spinner("Generating insights with AI..."):
                        try:
                            # Prepare data for AI analysis
                            insights_summary = (
                                f"Make: {make}\n"
                                f"Model: {model}\n"
                                f"Year: {year}\n"
                                f"Variant: {variant}\n"
                                f"Price: ₹{price}\n"
                                f"Location: {location}\n"
                                f"Fuel Type: {fuel_type}\n"
                                f"Transmission: {transmission}\n"
                                f"Mileage: {mileage or 'N/A'}\n"
                                f"Condition: {condition}"
                            )

                            insights_prompt = [
                                {"role": "system", "content": (
                                    "You are an expert automotive market analyst for India. "
                                    "Given the following car details, provide: "
                                    "1. Market Value Assessment: "
                                    "   - Compare with similar vehicles in the market "
                                    "   - Price analysis relative to market average "
                                    "   - Value for money assessment "
                                    "2. Cost Analysis: "
                                    "   - 5-year ownership cost breakdown "
                                    "   - Monthly and annual cost projections "
                                    "   - Maintenance and running costs "
                                    "3. Future Value Projection: "
                                    "   - Expected depreciation rate "
                                    "   - Resale value prediction "
                                    "   - Market trend analysis "
                                    "Format your response as a markdown report with clear sections. "
                                    "Include specific numbers and percentages where relevant."
                                )},
                                {"role": "user", "content": insights_summary}
                            ]

                            analysis = groq_chat_completion(insights_prompt)
                            
                            # Generate visual data
                            price = float(price.replace(',', ''))
                            years = list(range(5))
                            
                            # Depreciation projection
                            base_depr_rate = {
                                "Excellent": 0.12,
                                "Good": 0.15,
                                "Fair": 0.18,
                                "Poor": 0.25
                            }[condition]
                            
                            # Adjust rate based on factors
                            if fuel_type in ["Electric", "Hybrid"]:
                                base_depr_rate *= 0.9  # Better retention
                            if transmission == "Automatic":
                                base_depr_rate *= 1.1  # Slightly worse retention
                            
                            values = [price]
                            for i in range(1, 5):
                                values.append(values[-1] * (1 - base_depr_rate))
                            
                            # Cost breakdown (example percentages)
                            costs = {
                                "Depreciation": values[0] - values[-1],
                                "Maintenance": price * 0.15,
                                "Fuel": price * 0.25,
                                "Insurance": price * 0.10,
                                "Other": price * 0.05
                            }
                            
                            st.session_state.insights_result = {
                                'analysis': analysis,
                                'values': values,
                                'costs': costs
                            }
                        except Exception as e:
                            st.session_state.insights_result = f"[Error: {e}]"
                        
                    st.session_state.insights_loading = False
                    st.rerun()

    with results_col:
        if st.session_state.insights_loading:
            st.info("Generating insights with AI...")
        elif st.session_state.insights_result and isinstance(st.session_state.insights_result, dict):
            st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Market Analysis</h5>", unsafe_allow_html=True)
            
            # Create subplots for visualizations
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=("5-Year Value Projection", "5-Year Cost Breakdown"),
                vertical_spacing=0.2,
                specs=[[{"type": "scatter"}], [{"type": "pie"}]]
            )
            
            # Add value projection line
            fig.add_trace(
                go.Scatter(
                    x=years,
                    y=st.session_state.insights_result['values'],
                    mode='lines+markers',
                    name='Projected Value',
                    line=dict(color='#a78bfa', width=3),
                    marker=dict(size=8)
                ),
                row=1, col=1
            )
            
            # Add cost breakdown pie chart
            fig.add_trace(
                go.Pie(
                    labels=list(st.session_state.insights_result['costs'].keys()),
                    values=list(st.session_state.insights_result['costs'].values()),
                    hole=0.4,
                    marker=dict(colors=['#a78bfa', '#60a5fa', '#34d399', '#fbbf24', '#f87171'])
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=600,
                template="plotly_dark",
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            fig.update_xaxes(title_text="Years", row=1, col=1)
            fig.update_yaxes(title_text="Value (₹)", row=1, col=1)
            fig.update_yaxes(tickformat="₹,.0f", row=1, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display AI analysis
            st.markdown("<h6 style='color:#fff; margin-top:1.5rem; margin-bottom:0.5rem;'>Detailed Analysis</h6>", unsafe_allow_html=True)
            st.markdown(st.session_state.insights_result['analysis'], unsafe_allow_html=True)
            
            # Add download button for the analysis
            st.download_button(
                label="Download Analysis",
                data=st.session_state.insights_result['analysis'],
                file_name="market_analysis.md",
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