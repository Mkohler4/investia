import streamlit as st
from accounts.main import manage_accounts
from objects.main import manage_objects

# Title of the app
st.title("Investia 🧑‍💻")

# Manage accounts
manage_accounts()

# Manage objects
manage_objects()

