# Sample data for testing AI features

# Policy Scanner Sample Data
POLICY_SAMPLE = """
WARRANTY TERMS AND CONDITIONS

1. Coverage Period: 3 years or 100,000 km, whichever comes first
2. Exclusions:
   - Regular maintenance items
   - Wear and tear parts
   - Accidents and damages
   - Modifications without approval
3. Service Requirements:
   - Regular service every 10,000 km
   - Use of authorized service centers
   - Use of genuine parts only
4. Additional Benefits:
   - 24/7 roadside assistance
   - Free towing up to 50 km
   - Courtesy car for major repairs
5. Transfer Conditions:
   - Transferable to second owner
   - Transfer fee: ₹5,000
   - Must be transferred within 30 days
"""

# Financial Advisor Sample Data
FINANCE_SAMPLE = {
    'car_price': '15,00,000',
    'down_payment': '3,00,000',
    'loan_term': '60',
    'interest_rate': '8.5',
    'insurance': '25,000',
    'maintenance': '15,000',
    'fuel': '8,000',
    'resale_value': '7,00,000',
    'additional_costs': """Extended Warranty: ₹25,000
Accessories: ₹50,000
Registration: ₹1,50,000"""
}

# Depreciation Predictor Sample Data
DEPRECIATION_SAMPLE = {
    'make': 'Hyundai',
    'model': 'Creta',
    'year': '2023',
    'price': '16,50,000',
    'variant': 'SX(O)',
    'mileage': '15,000',
    'condition': 'Excellent',
    'location': 'Bangalore',
    'fuel_type': 'Petrol',
    'transmission': 'Automatic'
}

# Car Browser Sample Filters
BROWSER_SAMPLE = {
    'price_range': (10, 20),
    'year_range': (2020, 2024),
    'body_type': ['SUV', 'Sedan'],
    'fuel_type': ['Petrol', 'Hybrid'],
    'transmission': ['Automatic'],
    'seating_capacity': ['5'],
    'make': ['Hyundai', 'Toyota', 'Honda'],
    'sort_by': 'price_low_to_high'
}

# Model Comparison Sample Data
COMPARISON_SAMPLE = [
    {
        'make': 'Hyundai',
        'model': 'Creta',
        'year': '2023',
        'price': '16,50,000',
        'variant': 'SX(O)',
        'mileage': '15,000'
    },
    {
        'make': 'Toyota',
        'model': 'Urban Cruiser',
        'year': '2023',
        'price': '14,50,000',
        'variant': 'Hyryder',
        'mileage': '12,000'
    },
    {
        'make': 'Honda',
        'model': 'Elevate',
        'year': '2023',
        'price': '15,80,000',
        'variant': 'ZX',
        'mileage': '10,000'
    }
]

# Fine Print Analyzer Sample Data
FINE_PRINT_SAMPLE = """
PURCHASE AGREEMENT

1. Vehicle Details:
   Make: Hyundai
   Model: Creta
   Variant: SX(O)
   Price: ₹16,50,000

2. Payment Terms:
   - Down Payment: ₹3,00,000
   - Loan Amount: ₹13,50,000
   - Interest Rate: 8.5% p.a.
   - Term: 60 months
   - Processing Fee: ₹15,000

3. Delivery Terms:
   - Delivery within 7 days of full payment
   - Pre-delivery inspection mandatory
   - Registration charges extra
   - Insurance to be arranged separately

4. Additional Charges:
   - Extended Warranty: Optional
   - Accessories: As per customer choice
   - Road Tax: As per state regulations
   - Handling Charges: ₹5,000

5. Cancellation Policy:
   - 50% refund if cancelled before delivery
   - No refund after delivery
   - Processing fee non-refundable
"""

# AI Assistant Sample Preferences
ASSISTANT_PREFERENCES = {
    'budget': '15,00,000',
    'primary_use': 'Family Car',
    'family_size': '3-4',
    'fuel_preference': 'Petrol',
    'transmission': 'Automatic',
    'location': 'Bangalore'
}

# Sample AI Assistant Chat
ASSISTANT_CHAT_SAMPLE = [
    {"role": "user", "content": "I'm looking for a family car under 15 lakhs. What would you recommend?"},
    {"role": "assistant", "content": """Based on your requirements, here are my top recommendations:

1. 🟢 Hyundai Creta SX(O)
   - Perfect for family use
   - Great fuel efficiency
   - Spacious interior
   - Price: ₹14.5-16.5 lakhs

2. 🟢 Toyota Urban Cruiser Hyryder
   - Hybrid option available
   - Excellent reliability
   - Good resale value
   - Price: ₹13.5-15.5 lakhs

3. 🟡 Honda Elevate
   - New model with modern features
   - Good safety ratings
   - Slightly higher maintenance
   - Price: ₹14.8-16.8 lakhs

Would you like me to provide more details about any of these models?"""}
]

# Sample AI Insights
INSIGHTS_SAMPLE = {
    'market_trends': {
        'suv_growth': '15% YoY',
        'hybrid_adoption': '25% increase',
        'ev_market_share': '5%',
        'price_trends': '3% increase'
    },
    'popular_models': [
        {'name': 'Hyundai Creta', 'market_share': '12%'},
        {'name': 'Toyota Urban Cruiser', 'market_share': '10%'},
        {'name': 'Honda Elevate', 'market_share': '8%'}
    ],
    'price_segments': {
        'budget': '5-10 lakhs',
        'mid_range': '10-15 lakhs',
        'premium': '15-20 lakhs',
        'luxury': '20+ lakhs'
    }
} 