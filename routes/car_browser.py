import streamlit as st
import pandas as pd
from utils.ai import groq_chat_completion
from utils.formatting import colorize_markdown

def car_browser_page():
    if st.button('← Back to Home', key='back_home_browser'):
        st.session_state.user_choice = None
        st.rerun()
    
    st.markdown("<h3 style='color:#60a5fa; text-align:center; margin-bottom:1.2rem;'>🚗 Car Browser</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#a1a1aa; margin-bottom:1.5rem;'>Find your perfect car with our advanced filtering system.</div>", unsafe_allow_html=True)

    # Initialize session state for filters
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'price_range': (0, 5000000),
            'year_range': (2020, 2024),
            'body_type': [],
            'fuel_type': [],
            'transmission': [],
            'seating_capacity': [],
            'make': [],
            'sort_by': 'price_low_to_high'
        }
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'search_loading' not in st.session_state:
        st.session_state.search_loading = False

    # Create two columns for filters and results
    filter_col, results_col = st.columns([1, 2])

    with filter_col:
        st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Filters</h5>", unsafe_allow_html=True)
        
        # Price Range
        st.markdown("<div style='color:#a1a1aa; margin-bottom:0.5rem;'>Price Range (₹)</div>", unsafe_allow_html=True)
        price_min, price_max = st.slider(
            "Price Range",
            min_value=0,
            max_value=5000000,
            value=st.session_state.filters['price_range'],
            step=100000,
            format="₹%d",
            key="price_slider"
        )
        st.session_state.filters['price_range'] = (price_min, price_max)

        # Year Range
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Year Range</div>", unsafe_allow_html=True)
        year_min, year_max = st.slider(
            "Year Range",
            min_value=2015,
            max_value=2024,
            value=st.session_state.filters['year_range'],
            step=1,
            key="year_slider"
        )
        st.session_state.filters['year_range'] = (year_min, year_max)

        # Body Type
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Body Type</div>", unsafe_allow_html=True)
        body_types = ["Sedan", "SUV", "Hatchback", "Crossover", "MPV", "Coupe", "Convertible"]
        selected_body_types = st.multiselect(
            "Select Body Types",
            body_types,
            default=st.session_state.filters['body_type'],
            key="body_type_select"
        )
        st.session_state.filters['body_type'] = selected_body_types

        # Fuel Type
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Fuel Type</div>", unsafe_allow_html=True)
        fuel_types = ["Petrol", "Diesel", "Electric", "Hybrid", "CNG"]
        selected_fuel_types = st.multiselect(
            "Select Fuel Types",
            fuel_types,
            default=st.session_state.filters['fuel_type'],
            key="fuel_type_select"
        )
        st.session_state.filters['fuel_type'] = selected_fuel_types

        # Transmission
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Transmission</div>", unsafe_allow_html=True)
        transmission_types = ["Manual", "Automatic", "CVT", "DCT"]
        selected_transmission = st.multiselect(
            "Select Transmission",
            transmission_types,
            default=st.session_state.filters['transmission'],
            key="transmission_select"
        )
        st.session_state.filters['transmission'] = selected_transmission

        # Seating Capacity
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Seating Capacity</div>", unsafe_allow_html=True)
        seating_options = ["2", "4", "5", "6", "7", "8+"]
        selected_seating = st.multiselect(
            "Select Seating Capacity",
            seating_options,
            default=st.session_state.filters['seating_capacity'],
            key="seating_select"
        )
        st.session_state.filters['seating_capacity'] = selected_seating

        # Make
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Make</div>", unsafe_allow_html=True)
        makes = ["Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Toyota", "Honda", "Kia", "Volkswagen", "Skoda", "MG", "Others"]
        selected_makes = st.multiselect(
            "Select Makes",
            makes,
            default=st.session_state.filters['make'],
            key="make_select"
        )
        st.session_state.filters['make'] = selected_makes

        # Sort By
        st.markdown("<div style='color:#a1a1aa; margin-top:1rem; margin-bottom:0.5rem;'>Sort By</div>", unsafe_allow_html=True)
        sort_options = {
            "price_low_to_high": "Price: Low to High",
            "price_high_to_low": "Price: High to Low",
            "year_new_to_old": "Year: Newest First",
            "year_old_to_new": "Year: Oldest First"
        }
        selected_sort = st.selectbox(
            "Sort Results By",
            options=list(sort_options.keys()),
            format_func=lambda x: sort_options[x],
            index=list(sort_options.keys()).index(st.session_state.filters['sort_by']),
            key="sort_select"
        )
        st.session_state.filters['sort_by'] = selected_sort

        # Search Button
        if st.button("Search Cars", use_container_width=True):
            st.session_state.search_loading = True
            st.session_state.search_results = None
            
            with st.spinner("Searching for cars..."):
                # Prepare filter data for AI
                filter_text = (
                    f"Price Range: ₹{price_min:,} - ₹{price_max:,}\n"
                    f"Year Range: {year_min} - {year_max}\n"
                    f"Body Types: {', '.join(selected_body_types) if selected_body_types else 'Any'}\n"
                    f"Fuel Types: {', '.join(selected_fuel_types) if selected_fuel_types else 'Any'}\n"
                    f"Transmission: {', '.join(selected_transmission) if selected_transmission else 'Any'}\n"
                    f"Seating Capacity: {', '.join(selected_seating) if selected_seating else 'Any'}\n"
                    f"Makes: {', '.join(selected_makes) if selected_makes else 'Any'}\n"
                    f"Sort By: {sort_options[selected_sort]}"
                )

                search_prompt = [
                    {"role": "system", "content": (
                        "You are an expert car search assistant for the Indian market. "
                        "Given the following search criteria, provide: "
                        "1. A list of 5-7 best matching car models with their variants "
                        "2. For each car, include: "
                        "   - Price range "
                        "   - Key features "
                        "   - Pros and cons "
                        "   - Best variant recommendation "
                        "3. Sort the results according to the specified sort order "
                        "4. Use color indicators: 🟢 for pros, 🔴 for cons "
                        "Format your response as a markdown report with clear sections for each car."
                    )},
                    {"role": "user", "content": filter_text}
                ]

                try:
                    result = groq_chat_completion(search_prompt)
                    st.session_state.search_results = result
                except Exception as e:
                    st.session_state.search_results = f"[Error: {e}]"
                
            st.session_state.search_loading = False
            st.rerun()

    with results_col:
        if st.session_state.search_loading:
            st.info("Searching for cars...")
        elif st.session_state.search_results:
            st.markdown("<h5 style='color:#fff; margin-bottom:1rem;'>Search Results</h5>", unsafe_allow_html=True)
            
            # Colorize the results
            st.markdown(colorize_markdown(st.session_state.search_results), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center; color:#a1a1aa; margin-top:2rem;'>
                <div style='font-size:2rem; margin-bottom:1rem;'>🔍</div>
                <div>Use the filters on the left to find your perfect car</div>
            </div>
            """, unsafe_allow_html=True) 