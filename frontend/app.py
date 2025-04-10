import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from analytics_by_month import analytics_by_month_tab

# st.markdown("""
#     <style>
#     /* Full screen animated background */
#     html, body, [data-testid="stApp"] {
#         height: 100%;
#         margin: 0;
#         padding: 0;
#         background: linear-gradient(-45deg, #780206, #061161, #780206, #061161);
#         background-size: 400% 400%;
#         animation: moveBackground 20s ease infinite;
#     }
#
#     @keyframes moveBackground {
#         0% {background-position: 0% 50%;}
#         50% {background-position: 100% 50%;}
#         100% {background-position: 0% 50%;}
#     }
#
#     /* Only background behind app content - clean container style */
#     [data-testid="stApp"]::before {
#         content: "";
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         z-index: -1;
#         background: linear-gradient(-45deg, #780206, #061161, #780206, #061161);
#         background-size: 400% 400%;
#         animation: moveBackground 20s ease infinite;
#     }
#
#     /* Preserve original layout but wrap everything in white content box */
#     .block-container {
#         background-color: white;
#         padding: 3rem 2rem;
#         border-radius: 14px;
#         box-shadow: 0 0 25px rgba(0,0,0,0.1);
#         max-width: 1100px;
#
#         margin: 0rem 2rem;
#     }
#
#     /* GitHub footer */
#     .github-footer {
#         position: fixed;
#         bottom: 15px;
#         right: 25px;
#         font-size: 15px;
#         color: #eee;
#         z-index: 999;
#     }
#
#     .github-footer a {
#         text-decoration: none;
#         font-weight: bold;
#         color: #90caf9;
#     }
#
#     .github-footer a:hover {
#         text-decoration: underline;
#         color: #fff;
#     }
#     </style>
#
#     <div class="github-footer">
#         👨‍💻 Created by <a href="https://github.com/PEPESHANTY" target="_blank">Shantanu Bhute</a>
#     </div>
# """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .github-footer {
        position: fixed;
        bottom: 15px;
        right: 25px;
        font-size: 15px;
        color: #eee;
        z-index: 999;
    }

    .github-footer a {
        text-decoration: none;
        font-weight: bold;
        color: #90caf9;
    }

    .github-footer a:hover {
        text-decoration: underline;
        color: #fff;
    }
    </style>

    <div class="github-footer">
        👨‍💻 Created by <a href="https://github.com/PEPESHANTY" target="_blank">Shantanu Bhute</a>
    </div>
""", unsafe_allow_html=True)


# App content
st.title("Expense Management System")

tab1, tab2, tab3 = st.tabs(["Add/update", "Analytics by Category", "Analytics by Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    analytics_by_month_tab()
