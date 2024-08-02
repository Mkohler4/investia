import streamlit as st
from accounts.classes.manager import FinancialManager
from accounts.classes.account import Account

def add_account():
    account_index = len(st.session_state.financial_manager.accounts) + 1
    account = Account(name=f"Account {account_index}", balance=0, input_rate=0, interest_rate=0)
    st.session_state.financial_manager.add_account(account)

def rename_account(i, new_name):
    st.session_state.financial_manager.accounts[i].name = new_name

def manage_accounts():
    # Initialize session state for FinancialManager
    if "financial_manager" not in st.session_state:
        st.session_state.financial_manager = FinancialManager()
        # Initialize with one default account
        st.session_state.financial_manager.add_account(Account(name="Account 1", balance=0, input_rate=0, interest_rate=0))
    
    financial_manager = st.session_state.financial_manager

    for i, account in enumerate(financial_manager.accounts):
        current_name = account.name
        st.subheader(current_name)
        new_name = st.text_input(f"Rename Account {i + 1}", value=current_name, key=f"rename_{i}")
        
        if new_name != current_name:
            rename_account(i, new_name)
        
        account.balance = st.number_input(f"{account.name} Balance $", min_value=0.0, step=10.0, key=f"balance_{i}", value=float(account.balance))
        account.input_rate = st.number_input(f"{account.name} Monthly Input Rate $", min_value=0.0, step=10.0, key=f"input_rate_{i}", value=float(account.input_rate))
        account.interest_rate = st.number_input(f"{account.name} Annual Interest Rate %", min_value=0.0, step=0.01, key=f"interest_rate_{i}", value=float(account.interest_rate))

    st.button("Add Account", on_click=add_account)

    net_worth = sum(account.balance for account in financial_manager.accounts)
    st.header(f"Net Worth: ${net_worth:,.2f}")