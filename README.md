# AI-Powered Car Shopping Assistant 🚗

An intelligent web application that helps users make informed decisions when buying cars. The application uses AI to provide personalized recommendations, financial analysis, and market insights.

## Features 🌟

- 🤖 **AI Car Shopping Assistant**: Get personalized car recommendations based on your needs and preferences
- 🛡️ **Policy Scanner**: Analyze dealer policies and terms with AI-powered insights
- 💸 **Financial Advisor**: Get comprehensive financial analysis of car purchases
- 📉 **Depreciation Predictor**: Predict your car's value over time with AI-powered market analysis
- 🚗 **Car Browser**: Find your perfect car with advanced filtering system
- 📊 **Model Comparison**: Compare up to 5 car models with detailed insights
- 📄 **Fine Print Analyzer**: Translate complex agreements into clear, actionable insights

## Tech Stack 💻

- **Frontend**: Streamlit
- **AI/ML**: LLaMA 3.3 70B through Groq API
- **Data Visualization**: Plotly
- **Speech Processing**: SpeechRecognition, gTTS
- **Styling**: Custom CSS

## Prerequisites 📋

- Python 3.8+
- pip (Python package installer)
- Groq API key

## Installation 🚀

1. Clone the repository:
```bash
git https://github.com/T-Mohamed-Shafeek/use-ai-to-buy.git
cd use-ai-to-buy
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # On Linux: source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage 🎯

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## Project Structure 📁

```
use-ai-to-buy/
├── pics/ 
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
├── routes/              # Route handlers
│   ├── ai_assistant.py
│   ├── car_browser.py
│   ├── depreciation_predictor.py
│   ├── financial_advisor.py
│   ├── fine_print_analyzer.py
│   ├── model_comparison.py
│   └── policy_scanner.py
└── utils/               # Utility functions
    ├── ai.py
    ├── formatting.py
    ├── sample_data.py
    └── session_state.py
```
3. You can make use of the fake data I have given in `utils/sample_data.py` to test each features.

By Mohamed Shafeek T