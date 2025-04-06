import streamlit as st
import json
import os

# Load users and investment data from JSON
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def load_investments():
    with open("investments.json", "r") as f:
        return json.load(f)

# Login function
def login(username, password, users):
    return username in users and users[username]["password"] == password

# Dashboard display
def show_dashboard(username, investments):
    if username not in investments:
        st.error("No investment data found.")
        return

    data = investments[username]
    name = data["name"]
    investment = data["investment"]
    current_value = data["current_value"]
    returns = ((current_value - investment) / investment) * 100

    st.title(f"Welcome, {name}")
    st.subheader("📊 Investment Dashboard")

    st.metric("💵 Initial Investment", f"${investment:,.2f}")
    st.metric("📈 Current Value", f"${current_value:,.2f}")
    st.metric("📊 Return (%)", f"{returns:.2f}%")

# Main App
def main():
    st.set_page_config(page_title="Investor Dashboard", layout="centered")
    st.title("🔐 Investor Login")

    users = load_users()
    investments = load_investments()

    # Session state for login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password, users):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")
    else:
        show_dashboard(st.session_state.username, investments)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""

if __name__ == "__main__":
    main()
