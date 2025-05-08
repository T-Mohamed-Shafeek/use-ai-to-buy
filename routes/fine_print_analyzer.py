import streamlit as st
from utils.ai import groq_chat_completion

def fine_print_analyzer_page():
    if st.button('← Back to Home', key='back_home_fineprint'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>📄 Fine Print Analyzer</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Translate complex agreements into clear, actionable insights with AI-powered analysis.</div>", unsafe_allow_html=True)

    # Initialize session state
    if 'fineprint_result' not in st.session_state:
        st.session_state.fineprint_result = None
    if 'fineprint_loading' not in st.session_state:
        st.session_state.fineprint_loading = False
    if 'fineprint_data' not in st.session_state:
        st.session_state.fineprint_data = {
            'contract_type': 'purchase_agreement',
            'contract_text': '',
            'dealer_name': '',
            'car_details': '',
            'additional_context': ''
        }

    # Create two columns for input and results
    input_col, results_col = st.columns([1, 1])

    with input_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Contract Details</h5>", unsafe_allow_html=True)
        
        with st.form("fineprint_form"):
            # Contract Type Selection
            contract_type = st.selectbox(
                "Contract Type",
                options=[
                    "purchase_agreement",
                    "warranty_terms",
                    "financing_agreement",
                    "insurance_policy",
                    "service_agreement",
                    "lease_agreement"
                ],
                format_func=lambda x: {
                    "purchase_agreement": "Purchase Agreement",
                    "warranty_terms": "Warranty Terms",
                    "financing_agreement": "Financing Agreement",
                    "insurance_policy": "Insurance Policy",
                    "service_agreement": "Service Agreement",
                    "lease_agreement": "Lease Agreement"
                }[x],
                index=0
            )

            # Contract Text Input
            contract_text = st.text_area(
                "Paste contract text here",
                height=300,
                help="Paste the complete contract text or agreement you want to analyze"
            )

            # Additional Context
            with st.expander("Additional Context (Optional)"):
                dealer_name = st.text_input("Dealer Name")
                car_details = st.text_area(
                    "Car Details",
                    help="Enter relevant car details (make, model, year, etc.)"
                )
                additional_context = st.text_area(
                    "Additional Context",
                    help="Any other relevant information about the agreement"
                )

            # Submit Button
            submitted = st.form_submit_button("Analyze Contract", use_container_width=True)

            if submitted:
                if not contract_text.strip():
                    st.error("Please paste the contract text to analyze")
                else:
                    st.session_state.fineprint_loading = True
                    st.session_state.fineprint_result = None
                    
                    # Update session state
                    st.session_state.fineprint_data = {
                        'contract_type': contract_type,
                        'contract_text': contract_text,
                        'dealer_name': dealer_name,
                        'car_details': car_details,
                        'additional_context': additional_context
                    }
                    
                    with st.spinner("Analyzing contract with AI..."):
                        try:
                            # Prepare context for AI
                            context = {
                                "Contract Type": contract_type.replace('_', ' ').title(),
                                "Dealer Name": dealer_name,
                                "Car Details": car_details,
                                "Additional Context": additional_context
                            }
                            
                            context_text = "\n".join([f"{k}: {v}" for k, v in context.items() if v])
                            
                            analysis_prompt = [
                                {"role": "system", "content": (
                                    "You are an expert automotive contract analyst specializing in the Indian market. "
                                    "Analyze the following contract text and provide: "
                                    "1. Plain Language Translation: "
                                    "   - Convert legal jargon into clear, simple explanations "
                                    "   - Break down complex clauses into bullet points "
                                    "2. Risk Assessment: "
                                    "   - 🔴 High Risk: Potentially problematic terms "
                                    "   - 🟡 Medium Risk: Terms requiring attention "
                                    "   - 🟢 Low/Positive Risk: Standard or beneficial terms "
                                    "3. Financial Impact Analysis: "
                                    "   - Direct costs and fees "
                                    "   - Hidden or potential costs "
                                    "   - Long-term financial implications "
                                    "4. Key Terms Summary: "
                                    "   - Important deadlines and dates "
                                    "   - Obligations and responsibilities "
                                    "   - Rights and protections "
                                    "5. Recommendations: "
                                    "   - Terms to negotiate "
                                    "   - Points to clarify "
                                    "   - Protective measures to consider "
                                    "Format your response as a markdown report with clear sections. "
                                    "Use bullet points for clarity and include specific quotes from the contract where relevant."
                                )},
                                {"role": "user", "content": f"Context:\n{context_text}\n\nContract Text:\n{contract_text}"}
                            ]

                            result = groq_chat_completion(analysis_prompt)
                            st.session_state.fineprint_result = result
                        except Exception as e:
                            st.session_state.fineprint_result = f"[Error: {e}]"
                        
                    st.session_state.fineprint_loading = False
                    st.rerun()

    with results_col:
        if st.session_state.fineprint_loading:
            st.info("Analyzing contract with AI...")
        elif st.session_state.fineprint_result:
            st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Analysis Results</h5>", unsafe_allow_html=True)
            
            # Colorize the results
            def colorize_analysis(md):
                md = md.replace("🔴", '<span style="color:#f87171;font-weight:700;">🔴</span>')
                md = md.replace("🟡", '<span style="color:#fbbf24;font-weight:700;">🟡</span>')
                md = md.replace("🟢", '<span style="color:#34d399;font-weight:700;">🟢</span>')
                return md
            
            st.markdown(colorize_analysis(st.session_state.fineprint_result), unsafe_allow_html=True)
            
            # Add download button for the analysis
            st.download_button(
                label="Download Analysis",
                data=st.session_state.fineprint_result,
                file_name="contract_analysis.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style='text-align:center; color:#a1a1aa; margin-top:2rem;'>
                <div style='font-size:2rem; margin-bottom:1rem;'>📄</div>
                <div>Paste the contract text on the left to get started</div>
            </div>
            """, unsafe_allow_html=True) 