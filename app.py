import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from simulator import generate_bin_data, save_data
from report_generator import generate_pdf_report

st.set_page_config(
    page_title="Smart Waste Management System",
    page_icon="🗑️",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("🗑️ Smart Waste Management & Bin Level Detection System")
st.markdown("Real-Time Waste Bin Monitoring Dashboard")

st.markdown("---")

# =========================
# SIDEBAR
# =========================

st.sidebar.header("Controls")

if st.sidebar.button("Generate Sensor Reading"):

    data = generate_bin_data()
    save_data(data)

    st.sidebar.success("New Data Generated")

# =========================
# LOAD DATA
# =========================

if os.path.exists("data/waste_data.csv"):

    df = pd.read_csv("data/waste_data.csv")

    latest = df.iloc[-1]

    fill = int(latest["Fill Percentage"])

    # =========================
    # STATUS COLORS
    # =========================

    if fill < 30:
        color = "green"
        status_msg = "Bin is Empty"
    elif fill < 70:
        color = "orange"
        status_msg = "Bin is Half Full"
    elif fill < 90:
        color = "darkorange"
        status_msg = "Bin is Nearly Full"
    else:
        color = "red"
        status_msg = "Bin is Full"

    # =========================
    # METRICS
    # =========================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🗑️ Fill Percentage",
        f"{fill}%"
    )

    c2.metric(
        "📊 Bin Status",
        latest["Status"]
    )

    c3.metric(
        "🚨 Alert Status",
        latest["Alert"]
    )

    st.markdown("---")

    # =========================
    # ALERT BOX
    # =========================

    if fill >= 90:
        st.error("🚨 CRITICAL ALERT: Waste Bin is FULL!")
    elif fill >= 70:
        st.warning("⚠️ WARNING: Waste Bin Nearly Full")
    else:
        st.success("✅ Bin Operating Normally")

    # =========================
    # GAUGE CHART
    # =========================

    st.subheader("Bin Fill Gauge")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=fill,
            title={"text": "Fill Percentage"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 30], "color": "lightgreen"},
                    {"range": [30, 70], "color": "yellow"},
                    {"range": [70, 90], "color": "orange"},
                    {"range": [90, 100], "color": "red"},
                ],
            },
        )
    )

    gauge.update_layout(height=350)

    st.plotly_chart(gauge, use_container_width=True)

    # =========================
    # CHARTS
    # =========================

    left, right = st.columns(2)

    with left:

        st.subheader("Waste Fill Trend")

        line_fig = px.line(
            df,
            x="Timestamp",
            y="Fill Percentage",
            markers=True
        )

        line_fig.update_traces(line=dict(width=4))

        line_fig.update_layout(
            height=450,
            yaxis=dict(range=[0, 100]),
            xaxis_title="Time",
            yaxis_title="Fill Percentage (%)"
        )

        st.plotly_chart(line_fig, use_container_width=True)

    with right:

        st.subheader("Current Bin Capacity")

        pie_fig = px.pie(
            values=[fill, 100 - fill],
            names=["Filled", "Remaining"],
            hole=0.65
        )

        pie_fig.update_layout(height=450)

        st.plotly_chart(pie_fig, use_container_width=True)

    # =========================
    # DATA TABLE
    # =========================

    st.markdown("---")

    st.subheader("Waste Monitoring Logs")

    st.dataframe(
        df.sort_index(ascending=False),
        use_container_width=True
    )

    # =========================
    # PDF REPORT
    # =========================

    st.markdown("---")

    if st.button("Generate PDF Report"):

        pdf_file = generate_pdf_report()

        st.success("PDF Report Generated Successfully")

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="waste_report.pdf",
                mime="application/pdf"
            )

else:

    st.info("No sensor data available. Generate readings from the sidebar.")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/679/679720.png",
        width=150
    )