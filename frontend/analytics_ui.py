import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        if response.status_code != 200:
            st.error("Failed to fetch data")
            return

        response = response.json()

        data = {
            "Category": list(response.keys()),
            "Total": [response[cat]["total"] for cat in response],
            "Percentage": [response[cat]["percentage"] for cat in response],
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values("Percentage", ascending=False)

        # Create tabs for bar chart and pie chart
        tab1, tab2 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart"])

        with tab1:
            st.subheader("Expense Breakdown By Category")
            st.bar_chart(data=df_sorted.set_index('Category')["Percentage"], use_container_width=True)

        with tab2:
            st.subheader("Category-wise Expense Share")
            fig, ax = plt.subplots()
            explode = [0.05] * len(df_sorted)  # Slightly explode all slices equally

            wedges, texts, autotexts = ax.pie(
                df_sorted["Total"],
                labels=df_sorted["Category"],
                autopct=lambda pct: f'€{(pct / 100) * df_sorted["Total"].sum():.2f}',
                explode=explode,
                startangle=140


            )
            ax.axis('equal')
            legend_labels = [
                f"{category:<15} €{amount:,.2f}"
                for category, amount in zip(df_sorted["Category"], df_sorted["Total"].astype(float))
            ]

            # Add custom legend to the right with monospaced font for clean alignment
            ax.legend(
                wedges,
                legend_labels,
                title="Categories",
                loc="center left",
                bbox_to_anchor=(1, 0.5),
                prop={'family': 'monospace', 'size': 10}
            )
            st.pyplot(fig)

        # Show total spent summary
        total_spent = df_sorted["Total"].sum()
        st.markdown(f"### 💰 Total Spent from {start_date} to {end_date} : €{total_spent:,.2f}")

        # Format and show table
        df_sorted["Total"] = df_sorted["Total"].map(lambda x: f"€{x:.2f}")
        df_sorted["Percentage"] = df_sorted["Percentage"].map(lambda x: f"{x:.2f}%")
        st.table(df_sorted)
