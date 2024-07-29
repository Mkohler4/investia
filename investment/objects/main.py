import streamlit as st
from datetime import datetime, timedelta
from objects.items.house import House, MortgageCalculator

def manage_objects():
    # Initialize session state for the house object and slider limits
    if "house" not in st.session_state:
        st.session_state.house = House(price=100000, date=datetime.now().date())  # Initial price of 100,000
    if "min_price" not in st.session_state:
        st.session_state.min_price = 0.0
    if "max_price" not in st.session_state:
        st.session_state.max_price = 1000000.0

    # Input boxes to set min and max price
    min_price = st.number_input(
        "Set minimum price",  
        value=float(st.session_state.min_price), 
        step=1000.0,
        key="min_price_input"
    )
    
    max_price = st.number_input(
        "Set maximum price", 
        value=float(st.session_state.max_price), 
        step=1000.0, 
        key="max_price_input"
    )
    
    # Update session state with valid inputs
    st.session_state.min_price = min_price
    st.session_state.max_price = max_price

    st.write("House")
    price = st.slider(
        "Price for House", 
        min_value=st.session_state.min_price, 
        max_value=st.session_state.max_price, 
        value=float(st.session_state.house.price), 
        step=1000.0, 
        key="price"
    )
    
    current_date = datetime.fromisoformat(st.session_state.house.date.isoformat()).date()
    new_date = st.date_input(
        "Date for House", 
        value=current_date, 
        min_value=datetime.now().date(), 
        max_value=(datetime.now() + timedelta(days=365*10)).date(), 
        key="date"
    )
    
    # Update the house price and date in the session state
    st.session_state.house.price = price
    st.session_state.house.date = new_date

    # Display the down payment
    st.write(f"Down payment for House: ${st.session_state.house.calculate_down_payment():.2f}")

    # Create a temporary MortgageCalculator instance for calculations
    mortgage_calculator = MortgageCalculator(
        price=st.session_state.house.price,
        annual_interest_rate=5,  # Example interest rate
        term_years=30,  # Example term in years
        down_payment_percentage=st.session_state.house.calculate_down_payment() / st.session_state.house.price
    )

    # Display the morgage rate
    st.write(f"The morgage rate for the House: ${mortgage_calculator.calculate_monthly_payment():.2f}")