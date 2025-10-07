# app.py
import streamlit as st
from queries import run_queries

st.set_page_config(page_title="Food Donation Dashboard", layout="wide")
st.title("🍽️ Food Donation Management Dashboard")
st.markdown("Analyze providers, receivers, and food distribution trends.")

results = run_queries()

tabs = st.tabs(list(results.keys()))

for i, (title, df) in enumerate(results.items()):
    with tabs[i]:
        st.subheader(title)
        if not df.empty:
            st.dataframe(df)
            # Auto charting
            if "City" in df.columns and "Listings" in df.columns:
                st.bar_chart(df.set_index("City"))
            elif "Status" in df.columns and "Percentage" in df.columns:
                st.bar_chart(df.set_index("Status")["Percentage"])
            elif "Provider_Type" in df.columns and "Total_Quantity" in df.columns:
                st.bar_chart(df.set_index("Provider_Type"))
        else:
            st.warning("No data found.")
