import streamlit as st

def guide_page():
    if st.button('← Back to Home', key='back_home_guide'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>📚 How to Get the Most Out of Our Site</h3>", unsafe_allow_html=True)
    
    # AI Features Education
    st.markdown("## 🤖 AI Features Education")
    st.markdown("""
    Our platform leverages advanced AI to transform your car buying experience. Here's how each feature works:

    ### 🛡️ Policy Scanner
    - **How it works**: Analyzes dealer policies and terms using natural language processing
    - **Example**: Paste a dealer's warranty terms, and the AI will:
        - Identify key terms and conditions
        - Flag potential issues (🔴)
        - Highlight standard clauses (🟢)
        - Suggest negotiation points
    - **Accuracy**: Trained on thousands of automotive policies and legal documents

    ### 💸 Financial Advisor
    - **How it works**: Uses machine learning to analyze market trends and financial data
    - **Example**: Input your car details and get:
        - Monthly cost breakdown
        - Interest rate analysis
        - Long-term financial impact
        - Deal quality assessment (🟢/🟡/🔴)
    - **Accuracy**: Continuously updated with current market rates and trends

    ### 📉 Depreciation Predictor
    - **How it works**: Employs predictive analytics based on historical data
    - **Example**: Enter your car's details to receive:
        - 5-year value projection
        - Market trend analysis
        - Maintenance impact assessment
        - Resale value optimization tips
    - **Accuracy**: Based on real market data and historical depreciation patterns

    ### 🚗 Car Browser
    - **How it works**: Uses AI to match your preferences with available options
    - **Example**: Set your filters to get:
        - Personalized recommendations
        - Feature comparisons
        - Price analysis
        - Best variant suggestions
    - **Accuracy**: Updated daily with current market listings

    ### 📊 Model Comparison
    - **How it works**: Employs comparative analysis algorithms
    - **Example**: Compare up to 5 models to see:
        - Side-by-side feature comparison
        - Cost-benefit analysis
        - Long-term value assessment
        - Best match for your needs
    - **Accuracy**: Based on comprehensive market research and user feedback

    ### 📄 Fine Print Analyzer
    - **How it works**: Uses natural language processing to simplify complex terms
    - **Example**: Upload any contract to get:
        - Plain language translation
        - Risk assessment (🔴/🟡/🟢)
        - Key terms summary
        - Actionable recommendations
    - **Accuracy**: Trained on legal documents and automotive contracts
    """)

    # Process Walkthrough
    st.markdown("## 🎯 Process Walkthrough")
    st.markdown("""
    Here's how to use our AI-powered features effectively:

    1. **Start with Preferences**
       - Use the AI Assistant to define your needs
       - Set your budget and requirements
       - Get initial recommendations

    2. **Research and Compare**
       - Use the Car Browser to find matches
       - Compare models side by side
       - Analyze financial implications

    3. **Deep Analysis**
       - Scan dealer policies
       - Analyze fine print
       - Get depreciation predictions

    4. **Final Decision**
       - Review AI recommendations
       - Check financial analysis
       - Make an informed choice

    **Pro Tip**: Use multiple features together for the best results. For example, after finding a car you like, use the Financial Advisor and Policy Scanner to ensure it's a good deal.
    """)

    # FAQ Section
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = {
        "How accurate are the AI predictions?": """
        Our AI models are trained on extensive market data and are regularly updated. 
        While we can't guarantee 100% accuracy, our predictions are based on:
        - Historical market data
        - Current market trends
        - User feedback and outcomes
        - Expert validation
        """,
        
        "How does the AI handle different car markets?": """
        Our AI is specifically trained for the Indian automotive market, considering:
        - Local pricing trends
        - Regional preferences
        - Market-specific features
        - Local regulations and policies
        """,
        
        "Can I trust the AI's financial advice?": """
        The financial analysis is based on:
        - Current market rates
        - Historical data
        - Industry standards
        - Expert validation
        
        However, we recommend consulting with a financial advisor for major decisions.
        """,
        
        "How often is the AI updated?": """
        Our AI models are updated:
        - Daily for market prices
        - Weekly for trend analysis
        - Monthly for major model updates
        - Continuously for user feedback
        """,
        
        "What makes your AI different from other car buying tools?": """
        Our AI stands out because it:
        - Provides comprehensive analysis
        - Considers multiple factors
        - Offers personalized recommendations
        - Integrates multiple features
        - Focuses on the Indian market
        """,
        
        "How do I get the most accurate results?": """
        For best results:
        - Provide complete information
        - Use multiple features together
        - Update your preferences regularly
        - Consider all AI recommendations
        - Review the detailed analysis
        """
    }
    
    for question, answer in faqs.items():
        with st.expander(question):
            st.markdown(answer)
    
    # Additional Tips
    st.markdown("## 💡 Pro Tips")
    st.markdown("""
    - **Start with the AI Assistant**: It helps set your preferences and guides you through the process
    - **Use Voice Chat**: For a more natural interaction with the AI
    - **Save Your Analysis**: Download reports for future reference
    - **Compare Multiple Options**: Don't settle for the first recommendation
    - **Check Fine Print**: Always analyze policies and contracts
    - **Update Regularly**: Market conditions change, so update your analysis periodically
    """) 