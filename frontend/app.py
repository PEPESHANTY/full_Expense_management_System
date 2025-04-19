import streamlit as st
from auth_ui import auth_ui
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from analytics_by_month import analytics_by_month_tab


st.markdown("""
    <style>
    .github-footer {
        position: fixed;
        bottom: 55px;
        right: 15px;
        font-size: 15px;
        font-weight: 500;
        color: #f5f5f5;
        z-index: 999;
        background-color: rgba(0, 0, 0, 0.4);
        padding: 6px 10px;
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(0,0,0,0.3);
    }

    .github-footer a {
        text-decoration: none;
        font-weight: 600;
        color: #90caf9;
    }

    .github-footer a:hover {
        text-decoration: underline;
        color: #ffffff;
    }
    </style>

    <div class="github-footer">
        👨‍💻 Created by <a href="https://github.com/PEPESHANTY" target="_blank">Shantanu Bhute</a>
    </div>
""", unsafe_allow_html=True)



# App content
col1, col2 = st.columns([12, 1.9])
with col1:
    st.title("Expense Management System")
with col2:
    # Logout button placed at top-right corner using Streamlit native
    if st.session_state.get("logged_in", False):
        st.markdown("""
            <style>
                .top-right-logout {
                    position: fixed;
                    top: 20px;
                    right: 15px;
                    z-index: 9999;
                }
                .logout-btn {
                    padding: 0.4rem 0.9rem;
                    font-size: 0.9rem;
                    border-radius: 6px;
                    border: none;
                    background-color: #f44336;
                    color: white;
                    cursor: pointer;
                }
                .logout-btn:hover {
                    background-color: #d32f2f;
                }
            </style>
            <div class="top-right-logout">
                <button class="logout-btn" onclick="fetch('', {method: 'POST'}).then(() => window.location.reload());">
                    Logout
                </button>
            </div>
        """, unsafe_allow_html=True)

    # Use a hidden Streamlit button for logout action
    if st.button("Logout", key="logout_internal", help="Directed toward Login Page"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.auth_mode = "login"
        st.rerun()

# Auth check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    auth_ui()
    st.stop()

tab1, tab2, tab3 = st.tabs(["Add/update", "Analytics by Category", "Analytics by Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    analytics_by_month_tab()


