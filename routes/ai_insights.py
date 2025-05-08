import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.ai import groq_chat_completion
from utils.sample_data import INSIGHTS_SAMPLE
import plotly.express as px

def ai_insights_page():
    if st.button('← Back to Home', key='back_home_insights'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>📊 AI Market Insights</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Comprehensive market analysis with visual charts for pricing, costs, and future value projections.</div>", unsafe_allow_html=True)

    # Create tabs for different insights
    tab1, tab2, tab3 = st.tabs(["Market Trends", "Popular Models", "Price Analysis"])

    with tab1:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Market Trends</h5>", unsafe_allow_html=True)
        
        # Market Trends Chart
        trends_data = INSIGHTS_SAMPLE['market_trends']
        fig = go.Figure()
        
        # Add bars for each trend
        fig.add_trace(go.Bar(
            x=list(trends_data.keys()),
            y=[float(val.replace('%', '').replace(' YoY', '').replace(' increase', '')) for val in trends_data.values()],
            marker_color=['#60a5fa', '#34d399', '#fbbf24', '#f87171'],
            text=[f"{val}" for val in trends_data.values()],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Market Growth Trends",
            xaxis_title="Metrics",
            yaxis_title="Percentage",
            template="plotly_dark",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Popular Models</h5>", unsafe_allow_html=True)
        
        # Popular Models Chart
        models_data = INSIGHTS_SAMPLE['popular_models']
        fig = px.pie(
            models_data,
            values=[float(model['market_share'].replace('%', '')) for model in models_data],
            names=[model['name'] for model in models_data],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            title="Market Share by Model",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Price Analysis</h5>", unsafe_allow_html=True)
        
        # Price Segments Chart
        segments_data = INSIGHTS_SAMPLE['price_segments']
        fig = go.Figure()
        
        # Create a horizontal bar chart for price segments
        fig.add_trace(go.Bar(
            y=list(segments_data.keys()),
            x=[1, 1, 1, 1],  # Equal width for all segments
            orientation='h',
            marker_color=['#60a5fa', '#34d399', '#fbbf24', '#f87171'],
            text=[f"{val}" for val in segments_data.values()],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Price Segments Distribution",
            xaxis_showticklabels=False,
            template="plotly_dark",
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Add AI Analysis Section
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>AI Market Analysis</h5>", unsafe_allow_html=True)
    
    # Prepare data for AI analysis
    analysis_prompt = [
        {"role": "system", "content": (
            "You are an expert automotive market analyst for India. "
            "Based on the following market data, provide: "
            "1. Market Overview: Current trends and their implications "
            "2. Segment Analysis: Performance of different price segments "
            "3. Model Insights: Key factors driving model popularity "
            "4. Future Outlook: Predictions for the next 6-12 months "
            "5. Recommendations: Strategic insights for buyers "
            "Format your response as a markdown report with clear sections. "
            "Use color indicators: 🟢 for positive, 🟡 for neutral, 🔴 for negative."
        )},
        {"role": "user", "content": str(INSIGHTS_SAMPLE)}
    ]

    try:
        analysis = groq_chat_completion(analysis_prompt)
        st.markdown(analysis, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating analysis: {str(e)}")

    # Add download button for the analysis
    if 'analysis' in locals():
        st.download_button(
            label="Download Analysis",
            data=analysis,
            file_name="market_analysis.md",
            mime="text/markdown",
            use_container_width=True
        ) 