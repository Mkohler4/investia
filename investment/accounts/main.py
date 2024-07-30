import streamlit as st

def add_account():
    st.session_state.num_accounts += 1
    st.session_state.account_names.append(f"Account {st.session_state.num_accounts}")
    st.session_state.account_values.append(0)

def rename_account(i, new_name):
    st.session_state.account_names[i] = new_name

def manage_accounts():
    # Initialize session state for the number of accounts
    if "num_accounts" not in st.session_state:
        st.session_state.num_accounts = 1

    # Initialize session state for account names
    if "account_names" not in st.session_state:
        st.session_state.account_names = ["Account 1"]

    # Initialize session state for account values
    if "account_values" not in st.session_state:
        st.session_state.account_values = [0] * st.session_state.num_accounts

    for i in range(st.session_state.num_accounts):
        current_name = st.session_state.account_names[i]
        st.subheader(current_name)
        new_name = st.text_input(f"Rename Account {i + 1}", value=current_name, key=f"rename_{i}")
        
        if new_name != current_name:
            rename_account(i, new_name)
        
        account_value = st.number_input(f"{st.session_state.account_names[i]} $", min_value=0, step=10, key=f"account_{i}", value=st.session_state.account_values[i])
        st.session_state.account_values[i] = account_value

    st.button("Add Account", on_click=add_account)

    net_worth = sum(st.session_state.account_values)
    st.header(f"Net Worth: ${net_worth:,.2f}")