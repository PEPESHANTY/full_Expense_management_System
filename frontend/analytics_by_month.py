import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import calendar

API_URL = (
    os.getenv("PROD_API_URL")
    if os.getenv("ENV") == "PROD"
    else "http://localhost:8000"
)

def analytics_by_month_tab():
    st.subheader("Expense Breakdown By Month")

    try:
        # Fetch data from API
        response = requests.get(f"{API_URL}/analytics_by_month")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df = df.sort_values("month")

            # Convert '2024-08' to 'Aug 2024' for display
            df["label_month"] = pd.to_datetime(df["month"]).dt.strftime('%b %Y')  # 'Aug 2024', 'Sep 2024', ...

            # Dropdown to choose chart type
            tab1, tab2 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart"])

            #  Bar Chart (Separate Figure)
            with tab1:
                st.bar_chart(data=df.set_index("label_month")["total"], use_container_width=True)

            # Pie Chart (Separate Figure)
            with tab2:
                fig_pie, ax_pie = plt.subplots()
                explode = [0.15 if i == df["total"].idxmax() else 0.05 for i in df.index]
                wedges, texts, autotexts = ax_pie.pie(
                    df["total"],
                    labels=df["label_month"],
                    autopct=lambda pct: f'€{(pct / 100) * df["total"].sum():.2f}',
                    startangle=140,
                    explode= explode

                )
                ax_pie.axis('equal')

                legend_labels = [f"{month}: €{total:.2f}" for month, total in
                                 zip(df["label_month"], df["total"].astype(float))]
                ax_pie.legend(wedges, legend_labels, title="Monthly Expenses", loc="center left",
                              bbox_to_anchor=(1, 0, 0.5, 1))
                st.pyplot(fig_pie)  # Show pie chart


            # Add grand total
            total_spent = df["total"].astype(float).sum()
            st.markdown(f"### 💶 Total Spent Across All Months: €{total_spent:,.2f}")

            # Add € and format
            df["total"] = df["total"].map(lambda x: f"€{x:.2f}")
            df = df.rename(columns={"month": "Month", "total": "Total Spent"})

            # Table
            st.table(df[["Month", "Total Spent"]])


        else:
            st.error("Failed to fetch monthly analytics.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
