import streamlit as st
import pandas as pd
from utils.ai import groq_chat_completion
from utils.formatting import colorize_markdown

def financial_advisor_page():
    if st.button('← Back to Home', key='back_home_finance'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#a78bfa; text-align:center; margin-bottom:1.2rem;'>💸 AI Financial Advisor</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Get a comprehensive financial analysis of your car purchase with AI-powered insights.</div>", unsafe_allow_html=True)

    # Create two columns for input and results
    input_col, results_col = st.columns([1, 1])

    with input_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Financial Details</h5>", unsafe_allow_html=True)
        
        with st.form("finance_form"):
            # Basic Details
            st.markdown("<div style='color:#a1a1aa; margin-bottom:0.5rem;'>Basic Details</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                car_price = st.text_input(
                    "Car Price (₹)",
                    value=st.session_state.finance_data['car_price'],
                    help="Total price of the car including all taxes and charges"
                )
                loan_term = st.text_input(
                    "Loan Term (months)",
                    value=st.session_state.finance_data['loan_term'],
                    help="Duration of the loan in months"
                )
                insurance = st.text_input(
                    "Insurance (₹/yr)",
                    value=st.session_state.finance_data['insurance'],
                    help="Annual insurance premium"
                )
            with col2:
                down_payment = st.text_input(
                    "Down Payment (₹)",
                    value=st.session_state.finance_data['down_payment'],
                    help="Initial down payment amount"
                )
                interest_rate = st.text_input(
                    "Interest Rate (%)",
                    value=st.session_state.finance_data['interest_rate'],
                    help="Annual interest rate offered by the dealer"
                )
                maintenance = st.text_input(
                    "Maintenance (₹/yr)",
                    value=st.session_state.finance_data['maintenance'],
                    help="Estimated annual maintenance cost"
                )

            # Additional Costs
            st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Additional Costs</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                fuel = st.text_input(
                    "Fuel Cost (₹/mo)",
                    value=st.session_state.finance_data['fuel'],
                    help="Estimated monthly fuel cost"
                )
            with col2:
                resale_value = st.text_input(
                    "Expected Resale Value (₹)",
                    value=st.session_state.finance_data['resale_value'],
                    help="Expected resale value after loan term"
                )

            # Additional Costs Details
            with st.expander("Additional Costs Details"):
                additional_costs = st.text_area(
                    "Other Costs (one per line)",
                    value=st.session_state.finance_data['additional_costs'],
                    help="Enter any additional costs (e.g., accessories, extended warranty) with amounts"
                )

            # Submit Button
            submitted = st.form_submit_button("Analyze Deal", use_container_width=True)

            if submitted:
                # Validate required fields
                required_fields = {
                    'Car Price': car_price,
                    'Down Payment': down_payment,
                    'Loan Term': loan_term,
                    'Interest Rate': interest_rate
                }
                
                missing_fields = [field for field, value in required_fields.items() if not value.strip()]
                
                if missing_fields:
                    st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
                else:
                    st.session_state.finance_loading = True
                    st.session_state.finance_result = None
                    
                    # Update session state
                    st.session_state.finance_data = {
                        'car_price': car_price,
                        'down_payment': down_payment,
                        'loan_term': loan_term,
                        'interest_rate': interest_rate,
                        'insurance': insurance,
                        'maintenance': maintenance,
                        'fuel': fuel,
                        'resale_value': resale_value,
                        'additional_costs': additional_costs
                    }
                    
                    with st.spinner("Analyzing deal with AI..."):
                        try:
                            # Calculate basic financial metrics
                            P = float(car_price.replace(',', '')) - float(down_payment.replace(',', ''))
                            N = int(loan_term)
                            R = float(interest_rate) / 12 / 100
                            emi = (P * R * (1 + R) ** N) / ((1 + R) ** N - 1) if R > 0 else P / N
                            total_payment = emi * N
                            total_interest = total_payment - P
                            
                            # Calculate additional costs
                            insurance_val = float(insurance.replace(',', '')) if insurance.strip() else 0
                            maintenance_val = float(maintenance.replace(',', '')) if maintenance.strip() else 0
                            fuel_val = float(fuel.replace(',', '')) if fuel.strip() else 0
                            resale_val = float(resale_value.replace(',', '')) if resale_value.strip() else 0
                            
                            # Calculate total cost of ownership
                            tco = total_payment + (insurance_val * (N/12)) + (maintenance_val * (N/12)) + (fuel_val * N)
                            if resale_val:
                                tco -= resale_val

                            # Prepare summary for AI
                            summary = (
                                f"Car Price: ₹{car_price}\n"
                                f"Down Payment: ₹{down_payment}\n"
                                f"Loan Term: {loan_term} months\n"
                                f"Interest Rate: {interest_rate}% per annum\n"
                                f"EMI: ₹{emi:,.2f} per month\n"
                                f"Total Payment (Principal + Interest): ₹{total_payment:,.2f}\n"
                                f"Total Interest Paid: ₹{total_interest:,.2f}\n"
                                f"Insurance: ₹{insurance or 'N/A'} per year\n"
                                f"Maintenance: ₹{maintenance or 'N/A'} per year\n"
                                f"Fuel: ₹{fuel or 'N/A'} per month\n"
                                f"Expected Resale Value: ₹{resale_value or 'N/A'}\n"
                                f"Additional Costs:\n{additional_costs if additional_costs else 'None'}\n"
                                f"Total Cost of Ownership (TCO): ₹{tco:,.2f}"
                            )

                            finance_prompt = [
                                {"role": "system", "content": (
                                    "You are an expert automotive financial advisor for the Indian market. "
                                    "Given the following deal summary, provide: "
                                    "1. Deal Quality Assessment: "
                                    "   - 🟢 Green: Excellent deal "
                                    "   - 🟡 Yellow: Fair deal "
                                    "   - 🔴 Red: Poor deal "
                                    "2. Interest Rate Analysis: Compare with current market rates "
                                    "3. Monthly Budget Impact: Break down monthly costs "
                                    "4. Long-term Financial Impact: 5-year projection "
                                    "5. Negotiation Points: Specific areas to negotiate "
                                    "6. Recommendations: Actionable advice "
                                    "Format your response as a markdown report with clear sections. "
                                    "Include specific numbers and percentages where relevant."
                                )},
                                {"role": "user", "content": summary}
                            ]

                            result = groq_chat_completion(finance_prompt)
                            st.session_state.finance_result = result
                        except Exception as e:
                            st.session_state.finance_result = f"[Error in calculation: {e}]"
                        
                    st.session_state.finance_loading = False
                    st.rerun()

    with results_col:
        if st.session_state.finance_loading:
            st.info("Analyzing deal with AI...")
        elif st.session_state.finance_result:
            st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Financial Analysis</h5>", unsafe_allow_html=True)
            
            # Colorize the results
            st.markdown(colorize_markdown(st.session_state.finance_result), unsafe_allow_html=True)
            
            # Add download button for the analysis
            st.download_button(
                label="Download Analysis",
                data=st.session_state.finance_result,
                file_name="financial_analysis.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style='text-align:center; color:#a1a1aa; margin-top:2rem;'>
                <div style='font-size:2rem; margin-bottom:1rem;'>💰</div>
                <div>Fill in the financial details on the left to get started</div>
            </div>
            """, unsafe_allow_html=True) 