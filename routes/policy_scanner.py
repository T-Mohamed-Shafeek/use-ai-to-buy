import streamlit as st
from utils.ai import groq_chat_completion
from utils.formatting import colorize_markdown

def policy_scanner_page():
    if st.button('← Back to Home', key='back_home_policy'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>🛡️ AI Policy Scanner</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Analyze dealer policies, fine print, and terms with AI-powered insights.</div>", unsafe_allow_html=True)

    # Create two columns for input and results
    input_col, results_col = st.columns([1, 1])

    with input_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Policy Details</h5>", unsafe_allow_html=True)
        
        # Policy Type Selection
        policy_type = st.radio(
            "Select Policy Type",
            options=[
                "dealer_policy",
                "warranty_terms",
                "financing_terms",
                "insurance_terms",
                "service_terms"
            ],
            format_func=lambda x: {
                "dealer_policy": "Dealer Policy",
                "warranty_terms": "Warranty Terms",
                "financing_terms": "Financing Terms",
                "insurance_terms": "Insurance Terms",
                "service_terms": "Service Terms"
            }[x],
            key="policy_type_select"
        )
        st.session_state.policy_type = policy_type

        # Policy Text Input
        policy_text = st.text_area(
            "Paste policy or terms here",
            height=300,
            key="policy_text",
            help="Paste the complete policy text, terms, or fine print you want to analyze."
        )

        # Additional Context
        with st.expander("Add Additional Context (Optional)"):
            dealer_name = st.text_input("Dealer Name", key="dealer_name")
            car_model = st.text_input("Car Model", key="car_model")
            purchase_type = st.selectbox(
                "Purchase Type",
                options=["New", "Used", "Certified Pre-owned"],
                key="purchase_type"
            )
            financing_type = st.selectbox(
                "Financing Type",
                options=["Cash", "Loan", "Lease"],
                key="financing_type"
            )

        # Scan Button
        if st.button("Scan Policy", use_container_width=True):
            if not policy_text.strip():
                st.error("Please paste the policy text to analyze")
            else:
                st.session_state.policy_scan_loading = True
                st.session_state.policy_scan_result = None
                
                with st.spinner("Analyzing policy with AI..."):
                    # Prepare context for AI
                    context = {
                        "policy_type": policy_type,
                        "dealer_name": dealer_name,
                        "car_model": car_model,
                        "purchase_type": purchase_type,
                        "financing_type": financing_type
                    }
                    
                    context_text = "\n".join([f"{k}: {v}" for k, v in context.items() if v])
                    
                    policy_prompt = [
                        {"role": "system", "content": (
                            "You are an expert automotive policy analyst specializing in the Indian market. "
                            "Analyze the following policy text and provide a comprehensive breakdown: "
                            "1. Key Terms and Conditions: List and explain the most important terms "
                            "2. Hidden Fees and Charges: Identify any non-obvious costs or mandatory add-ons "
                            "3. Risk Assessment: "
                            "   - 🟢 Green: Standard/beneficial terms "
                            "   - 🟡 Yellow: Terms requiring attention "
                            "   - 🔴 Red: Potentially problematic terms "
                            "4. Negotiation Points: Suggest terms that could be negotiated "
                            "5. Legal Implications: Highlight any legally significant clauses "
                            "6. Recommendations: Provide actionable advice "
                            "Format your response as a markdown report with clear sections. "
                            "Use bullet points for clarity and include specific quotes from the policy where relevant."
                        )},
                        {"role": "user", "content": f"Context:\n{context_text}\n\nPolicy Text:\n{policy_text}"}
                    ]

                    try:
                        result = groq_chat_completion(policy_prompt)
                        st.session_state.policy_scan_result = result
                    except Exception as e:
                        st.session_state.policy_scan_result = f"[Error: {e}]"
                    
                st.session_state.policy_scan_loading = False
                st.rerun()

    with results_col:
        if st.session_state.policy_scan_loading:
            st.info("Analyzing policy with AI...")
        elif st.session_state.policy_scan_result:
            st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Analysis Results</h5>", unsafe_allow_html=True)
            
            # Colorize the results
            st.markdown(colorize_markdown(st.session_state.policy_scan_result), unsafe_allow_html=True)
            
            # Add download button for the analysis
            st.download_button(
                label="Download Analysis",
                data=st.session_state.policy_scan_result,
                file_name="policy_analysis.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style='text-align:center; color:#a1a1aa; margin-top:2rem;'>
                <div style='font-size:2rem; margin-bottom:1rem;'>📄</div>
                <div>Paste the policy text on the left to get started</div>
            </div>
            """, unsafe_allow_html=True) 