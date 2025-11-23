import streamlit as st
import pandas as pd
from ai_logic import calculate_health_score, calculate_risk_score, generate_recommendation

st.set_page_config(page_title="OEM–Dealer KAM Dashboard", layout="wide")
st.title("🚗 AI-Powered Key Account Management Dashboard (Automobile OEM)")

uploaded = st.file_uploader("Upload Dealer Performance CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    # Apply AI models
    df["health_score"] = df.apply(calculate_health_score, axis=1)
    df["risk_score"] = df.apply(calculate_risk_score, axis=1)
    df["recommendation"] = df.apply(generate_recommendation, axis=1)

    st.subheader("📈 Dealer Overview")
    st.dataframe(
        df[
            [
                "dealer_name",
                "city",
                "retail_sales",
                "target_achievement_pct",
                "sales_csi",
                "aging_stock_pct",
                "outstanding_overdue_days",
                "health_score",
                "risk_score",
                "recommendation"
            ]
        ].sort_values("risk_score", ascending=False),
        use_container_width=True
    )

    st.subheader("📊 Risk Distribution")
    st.bar_chart(df["risk_score"])

    st.subheader("🏥 Dealer Health Score")
    st.bar_chart(df["health_score"])

    st.success("Analysis generated successfully!")
else:
    st.info("Upload the dealerships.csv file to begin.")
