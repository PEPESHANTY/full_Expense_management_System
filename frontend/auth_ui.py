import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = "https://full-expense-management-system.onrender.com"

# API_URL =  os.getenv("API_URL", "http://127.0.0.1:8000")
def auth_ui():
    # st.markdown("### 🔐 Expense Management System")

    # Default to login mode
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Switcher between Login and Signup
    if st.session_state.auth_mode == "login":
        st.subheader("🔐 Login")
    else:
        st.subheader("🆕 Sign Up")

    email = st.text_input("Email").strip().lower()
    password = st.text_input("Password", type="password")

    if st.session_state.auth_mode == "login":
        if st.button("Login"):
            try:
                res = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
                if res.status_code == 200:
                    user_id = res.json().get("user_id")
                    st.session_state.user_id = user_id
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                elif res.status_code == 404:
                    st.error("You don't have an account !!  \n 🚫 It seems you are my sister **Sanajana** working as a Senior test Engineering👩🏻‍💻 in SailPoint🚢⚈.  \n Please sign up first 🙇🏻.  \n Fun Fact: Sanjana👧🏻 loves Elephant🐘 !!")
                elif res.status_code == 401:
                    st.error("🔑 Incorrect password. Please try again.")
                elif res.status_code == 422:
                    st.error("🚫 It seems you are my sister **Sanjana** working as a Senior test Engineering👩🏻‍💻 in SailPoint🚢⚈.  \n Please sign up first 🙇🏻.  \n Fun Fact: Sanjana👧🏻 loves Elephant🐘 !!")

                else:
                    st.error(f"⚠️ Login failed with status code {res.status_code}. Try again.")
            except Exception as e:
                st.error(f"Server error: {e}")

        col1, col2 = st.columns([8, 3])
        with col2:
            st.markdown(
                "<div style='text-align:right; margin-right:10px;'>"
                "New user? <a href='#' onClick=\"window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'auth_mode', value: 'signup'}, '*')\">Register now</a>"
                "</div>",
                unsafe_allow_html=True
            )
        col1, col2 = st.columns([8, 1.8])
        with col2:
            if st.button("Register now"):
                st.session_state.auth_mode = "signup"
                st.rerun()

    else:
        if st.button("Sign Up"):
            try:
                res = requests.post(f"{API_URL}/signup", json={"email": email, "password": password})
                if res.status_code == 200:
                    st.success("Signup successful. Please check your email for OTP.")
                    st.session_state.signup_email = email
                    st.session_state.signup_password = password
                    st.session_state.show_otp = True
                else:
                    st.error("Signup failed. User may already exist.")
            except Exception as e:
                st.error(f"Server error: {e}")

        st.markdown(
            "<div style='text-align:right;'>"
            "Already registered? <a href='#'>Login</a>"
            "</div>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns([8, 1.4])
        with col2:
            if st.button("Login now"):
                st.session_state.auth_mode = "login"
                st.session_state.show_otp = False
                st.rerun()

    # OTP verification
    if st.session_state.get("show_otp", False):
        otp = st.text_input("Enter OTP sent to your email")
        if st.button("Verify OTP"):
            try:
                res = requests.post(f"{API_URL}/verify", json={"email": st.session_state.signup_email, "otp": otp})
                if res.status_code == 200:
                    login_res = requests.post(f"{API_URL}/login", json={
                        "email": st.session_state.signup_email,
                        "password": st.session_state.signup_password
                    })
                    if login_res.status_code == 200:
                        st.success("OTP verified. Logged in successfully!")
                        st.session_state.user_id = login_res.json().get("user_id")
                        st.session_state.logged_in = True
                        st.session_state.show_otp = False
                        st.rerun()
                    else:
                        st.error("OTP verified but login failed. Try again.")
                else:
                    st.error("Invalid OTP. Try again.")
            except Exception as e:
                st.error(f"Server error: {e}")
