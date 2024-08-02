import streamlit as st
from datetime import datetime, timedelta, date
from objects.items.house import House
from objects.items.object import BaseObject  # Assuming a BaseObject class exists
from accounts.classes.manager import FinancialManager
import matplotlib.pyplot as plt

def manage_objects():
    # Initialize session state for FinancialManager
    if "financial_manager" not in st.session_state:
        st.session_state.financial_manager = FinancialManager()

    financial_manager = st.session_state.financial_manager

    # Object selection for adding new objects
    object_type = st.radio("Select object type to add", ("House", "Object"))

    if st.button("Add Object"):
        if object_type == "House":
            house = House(price=100000, annual_interest_rate=5, term_years=30, min_price=0, max_price=1000000)
            financial_manager.add_object(house)
        elif object_type == "Object":
            base_object = BaseObject(price=100)
            financial_manager.add_object(base_object)

    # Display all objects
    for idx, obj in enumerate(financial_manager.objects):
        st.subheader(f"Object {idx + 1}: {'House' if isinstance(obj, House) else 'Object'}")

        if isinstance(obj, House):
            # Input boxes to set min and max price for House
            min_price = st.number_input(
                f"Set minimum price for House {idx + 1}",  
                value=float(obj.min_price), 
                step=1000.0,
                key=f"min_price_input_{idx}"
            )

            max_price = st.number_input(
                f"Set maximum price for House {idx + 1}", 
                value=float(obj.max_price), 
                step=1000.0, 
                key=f"max_price_input_{idx}"
            )

            # Update house with valid inputs
            obj.min_price = min_price
            obj.max_price = max_price

            price = st.slider(
                f"Price for House {idx + 1}", 
                min_value=obj.min_price, 
                max_value=obj.max_price, 
                value=float(obj.price), 
                step=1000.0, 
                key=f"price_{idx}"
            )

            current_date = datetime.fromisoformat(obj.date.isoformat()).date()
            new_date = st.date_input(
                f"Date for House {idx + 1}", 
                value=current_date, 
                min_value=datetime.now().date(), 
                max_value=(datetime.now() + timedelta(days=365*10)).date(), 
                key=f"date_{idx}"
            )

            # Update the house price and date
            obj.price = price
            obj.date = new_date

            # Display the down payment
            st.write(f"Down payment for House {idx + 1}: ${obj.calculate_down_payment():.2f}")

            # Display the mortgage rate
            st.write(f"The mortgage rate for House {idx + 1}: ${obj.calculate_monthly_payment():.2f}")

        else:
            # Direct input box to set price for Base Object
            price = st.number_input(
                f"Set price for Object {idx + 1}",  
                value=float(obj.price), 
                step=10.0,
                key=f"price_input_obj_{idx}"
            )

            # Update the base object price
            obj.price = price

            # Date input for when the object will be purchased
            current_date = datetime.fromisoformat(obj.date.isoformat()).date()
            new_date = st.date_input(
                f"Date for Object {idx + 1}", 
                value=current_date, 
                min_value=datetime.now().date(), 
                max_value=(datetime.now() + timedelta(days=365*10)).date(), 
                key=f"date_obj_{idx}"
            )

            # Update the base object date
            obj.date = new_date


            # Display the object price
            st.write(f"Price for Object {idx + 1}: ${obj.price:.2f}")

        # Calculate and display affordability
        total_income = financial_manager.calculate_affordability(obj)
        st.write(f"Total affordability for Object {idx + 1}: ${total_income:.2f}")

    # Select the number of months for balance projection
    months = st.slider("Select number of months for projection", 1, 60, 12)

    st.header(f"Projected Income Over Time: ({months} months)")

    # Plot the projected balances
    financial_manager.plot_projected_balances(months)

    st.header(f"Projected Income with Puchases Over Time: ({months} months)")

    financial_manager.plot_projected_balances_with_objects(months)

    st.header(f"Projected Income with Purchases and Monthly Expenses Over Time: ({months} months)")

    financial_manager.plot_projected_balances_with_objects_and_monthly_expenses(months)

    