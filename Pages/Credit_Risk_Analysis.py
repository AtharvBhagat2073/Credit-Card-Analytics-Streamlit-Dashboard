import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os


# =====================================================
# PROJECT ROOT
# =====================================================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


# =====================================================
# PROJECT IMPORTS
# =====================================================

from utils import (
    load_customer_data,
    chart_layout
)

from style import apply_style


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Credit Risk Analysis | Credit Pulse",
    page_icon="⚠️",
    layout="wide"
)

apply_style()


# =====================================================
# LOAD DATA
# =====================================================

customers = load_customer_data().copy()


# =====================================================
# REQUIRED COLUMN CHECK
# =====================================================

required_columns = [
    "Client_Num",
    "Customer_Age",
    "Credit_Limit",
    "Avg_Open_To_Buy",
    "Total_Revolving_Bal",
    "Avg_Utilization_Ratio",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Card_Category"
]

missing_columns = [
    column
    for column in required_columns
    if column not in customers.columns
]

if missing_columns:

    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
        <div class="brand-header">

        <div class="status-badge">
            CREDIT RISK INTELLIGENCE
        </div>

        <div class="brand-title">
            ⚠️ Credit Risk Analysis
        </div>

        <div class="brand-subtitle">
            Identify customer risk patterns using credit utilization,
            inactivity, revolving balance and customer engagement.
        </div>

        </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR FILTERS
# =====================================================

with st.sidebar:

    st.markdown(
        """
            <div class="sidebar-brand">

            <div class="sidebar-icon">
                💳
            </div>

            <div class="sidebar-title">
                CREDIT PULSE
            </div>

            <div class="sidebar-subtitle">
                RISK INTELLIGENCE
            </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🔎 Risk Filters")


    # -------------------------------------------------
    # CARD CATEGORY
    # -------------------------------------------------

    card_options = sorted(
        customers["Card_Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_cards = st.multiselect(
        "Card Category",
        card_options,
        default=card_options
    )


    # -------------------------------------------------
    # UTILIZATION RANGE
    # -------------------------------------------------

    utilization_range = st.slider(
        "Credit Utilization Range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.01
    )


    # -------------------------------------------------
    # INACTIVITY RANGE
    # -------------------------------------------------

    max_inactive_months = int(
        customers["Months_Inactive_12_mon"]
        .max()
    )

    inactivity_range = st.slider(
        "Months Inactive",
        min_value=0,
        max_value=max_inactive_months,
        value=(0, max_inactive_months)
    )


    st.divider()

    st.caption(
        "Adjust the filters to analyze specific "
        "customer risk segments."
    )


# =====================================================
# APPLY FILTERS
# =====================================================

filtered_data = customers[
    (
        customers["Card_Category"]
        .astype(str)
        .isin(selected_cards)
    )
    &
    (
        customers["Avg_Utilization_Ratio"]
        .between(
            utilization_range[0],
            utilization_range[1]
        )
    )
    &
    (
        customers["Months_Inactive_12_mon"]
        .between(
            inactivity_range[0],
            inactivity_range[1]
        )
    )
].copy()


# =====================================================
# EMPTY DATA PROTECTION
# =====================================================

if filtered_data.empty:

    st.warning(
        "⚠️ No customers match the selected risk filters. "
        "Please adjust your selections."
    )

    st.stop()


# =====================================================
# CREATE RISK SEGMENTS
# =====================================================

def calculate_risk(row):

    score = 0

    # High credit utilization
    if row["Avg_Utilization_Ratio"] >= 0.75:
        score += 3

    elif row["Avg_Utilization_Ratio"] >= 0.50:
        score += 2

    elif row["Avg_Utilization_Ratio"] >= 0.30:
        score += 1


    # Customer inactivity
    if row["Months_Inactive_12_mon"] >= 5:
        score += 2

    elif row["Months_Inactive_12_mon"] >= 3:
        score += 1


    # Revolving balance pressure
    if (
        row["Credit_Limit"] > 0
        and
        row["Total_Revolving_Bal"]
        /
        row["Credit_Limit"]
        >= 0.50
    ):
        score += 2


    # High contact count
    if row["Contacts_Count_12_mon"] >= 5:
        score += 1


    if score >= 5:
        return "High Risk"

    elif score >= 3:
        return "Medium Risk"

    return "Low Risk"


filtered_data["Risk_Category"] = (
    filtered_data.apply(
        calculate_risk,
        axis=1
    )
)


# =====================================================
# RISK SCORE
# =====================================================

def calculate_risk_score(row):

    score = 0

    if row["Avg_Utilization_Ratio"] >= 0.75:
        score += 3

    elif row["Avg_Utilization_Ratio"] >= 0.50:
        score += 2

    elif row["Avg_Utilization_Ratio"] >= 0.30:
        score += 1


    if row["Months_Inactive_12_mon"] >= 5:
        score += 2

    elif row["Months_Inactive_12_mon"] >= 3:
        score += 1


    if (
        row["Credit_Limit"] > 0
        and
        row["Total_Revolving_Bal"]
        /
        row["Credit_Limit"]
        >= 0.50
    ):
        score += 2


    if row["Contacts_Count_12_mon"] >= 5:
        score += 1


    return score


filtered_data["Risk_Score"] = (
    filtered_data.apply(
        calculate_risk_score,
        axis=1
    )
)


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = (
    filtered_data["Client_Num"]
    .nunique()
)

high_risk_customers = (
    filtered_data[
        filtered_data["Risk_Category"]
        == "High Risk"
    ]["Client_Num"]
    .nunique()
)

medium_risk_customers = (
    filtered_data[
        filtered_data["Risk_Category"]
        == "Medium Risk"
    ]["Client_Num"]
    .nunique()
)

average_utilization = (
    filtered_data[
        "Avg_Utilization_Ratio"
    ]
    .mean()
)

average_inactivity = (
    filtered_data[
        "Months_Inactive_12_mon"
    ]
    .mean()
)

high_risk_percentage = (
    high_risk_customers
    /
    total_customers
)


# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Credit Risk Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "TOTAL CUSTOMERS",
    f"{total_customers:,}"
)

col2.metric(
    "HIGH RISK",
    f"{high_risk_customers:,}",
    f"{high_risk_percentage:.1%} of customers"
)

col3.metric(
    "MEDIUM RISK",
    f"{medium_risk_customers:,}"
)

col4.metric(
    "AVG UTILIZATION",
    f"{average_utilization:.1%}"
)

col5.metric(
    "AVG INACTIVE MONTHS",
    f"{average_inactivity:.1f}"
)


# =====================================================
# RISK ALERT
# =====================================================

st.divider()

st.markdown(
    f"""
        <div class="insight-card">

        <div class="insight-title">
            ⚠️ Risk Alert
        </div>

        <div class="insight-text">
            <b>{high_risk_customers:,} customers</b>
            are currently classified as
            <b>High Risk</b> based on utilization,
            inactivity, revolving balance and
            customer engagement indicators.
        </div>

        </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# RISK CATEGORY ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        RISK SEGMENTATION
        </div>

    ### ⚠️ Customer Risk Distribution
    """,
    unsafe_allow_html=True
)


risk_distribution = (
    filtered_data[
        "Risk_Category"
    ]
    .value_counts()
    .reset_index()
)

risk_distribution.columns = [
    "Risk_Category",
    "Customers"
]


col1, col2 = st.columns(2)


with col1:

    fig = px.pie(
        risk_distribution,
        names="Risk_Category",
        values="Customers",
        hole=0.50,
        title="Customer Distribution by Risk Category"
    )

    fig = chart_layout(
        fig,
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    risk_score_summary = (
        filtered_data
        .groupby("Risk_Score")
        .size()
        .reset_index(name="Customers")
        .sort_values("Risk_Score")
    )

    fig = px.bar(
        risk_score_summary,
        x="Risk_Score",
        y="Customers",
        title="Customer Distribution by Risk Score",
        text="Customers"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig = chart_layout(
        fig,
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# CREDIT UTILIZATION ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        CREDIT UTILIZATION
        </div>

    ### 💳 Utilization Risk Analysis
    """,
    unsafe_allow_html=True
)


utilization_data = filtered_data.copy()

utilization_data["Utilization_Segment"] = pd.cut(
    utilization_data[
        "Avg_Utilization_Ratio"
    ],
    bins=[
        -0.01,
        0.20,
        0.50,
        0.75,
        1.00
    ],
    labels=[
        "Low (0-20%)",
        "Moderate (21-50%)",
        "High (51-75%)",
        "Very High (76-100%)"
    ]
)


utilization_summary = (
    utilization_data[
        "Utilization_Segment"
    ]
    .value_counts()
    .sort_index()
    .reset_index()
)

utilization_summary.columns = [
    "Utilization_Segment",
    "Customers"
]


fig = px.bar(
    utilization_summary,
    x="Utilization_Segment",
    y="Customers",
    title="Customer Credit Utilization Segments",
    text="Customers"
)

fig.update_traces(
    textposition="outside"
)

fig = chart_layout(
    fig,
    height=420
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# INACTIVITY ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        CUSTOMER ACTIVITY
        </div>

    ### 💤 Customer Inactivity Analysis
    """,
    unsafe_allow_html=True
)


inactivity_summary = (
    filtered_data
    .groupby(
        "Months_Inactive_12_mon"
    )
    .size()
    .reset_index(name="Customers")
    .sort_values(
        "Months_Inactive_12_mon"
    )
)


fig = px.bar(
    inactivity_summary,
    x="Months_Inactive_12_mon",
    y="Customers",
    title="Customer Distribution by Months Inactive",
    text="Customers"
)

fig.update_traces(
    textposition="outside"
)

fig = chart_layout(
    fig,
    height=420
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# REVOLVING BALANCE ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        REVOLVING BALANCE
        </div>

    ### 💰 Revolving Balance Exposure
    """,
    unsafe_allow_html=True
)


balance_data = (
    filtered_data
    .groupby(
        "Risk_Category"
    )
    .agg(
        Average_Revolving_Balance=(
            "Total_Revolving_Bal",
            "mean"
        ),
        Average_Credit_Limit=(
            "Credit_Limit",
            "mean"
        ),
        Customers=(
            "Client_Num",
            "nunique"
        )
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        balance_data,
        x="Risk_Category",
        y="Average_Revolving_Balance",
        title="Average Revolving Balance by Risk Category",
        text_auto=".2s"
    )

    fig = chart_layout(
        fig,
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        balance_data,
        x="Risk_Category",
        y="Average_Credit_Limit",
        title="Average Credit Limit by Risk Category",
        text_auto=".2s"
    )

    fig = chart_layout(
        fig,
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# RISK BY CARD CATEGORY
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        CARD RISK PROFILE
        </div>

    ### 💳 Risk Distribution by Card Category
    """,
    unsafe_allow_html=True
)


card_risk = (
    filtered_data
    .groupby(
        [
            "Card_Category",
            "Risk_Category"
        ]
    )
    .size()
    .reset_index(name="Customers")
)


fig = px.bar(
    card_risk,
    x="Card_Category",
    y="Customers",
    color="Risk_Category",
    barmode="stack",
    title="Customer Risk Profile by Card Category"
)

fig = chart_layout(
    fig,
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# RISK SCATTER ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        RISK CORRELATION
    </div>

    ### 📈 Utilization vs Inactivity
    """,
    unsafe_allow_html=True
)


fig = px.scatter(
    filtered_data,
    x="Avg_Utilization_Ratio",
    y="Months_Inactive_12_mon",
    size="Total_Revolving_Bal",
    color="Risk_Category",
    hover_data=[
        "Client_Num",
        "Credit_Limit",
        "Contacts_Count_12_mon"
    ],
    title="Credit Utilization vs Customer Inactivity"
)

fig.update_xaxes(
    tickformat=".0%"
)

fig = chart_layout(
    fig,
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# HIGH RISK CUSTOMERS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        AT-RISK CUSTOMERS
        </div>

    ### 🚨 High Risk Customer Identification
    """,
    unsafe_allow_html=True
)


high_risk_data = (
    filtered_data[
        filtered_data[
            "Risk_Category"
        ]
        == "High Risk"
    ]
    .sort_values(
        "Risk_Score",
        ascending=False
    )
)


if high_risk_data.empty:

    st.success(
        "🎉 No high-risk customers were identified "
        "with the current filters."
    )

else:

    risk_display_columns = [
        "Client_Num",
        "Card_Category",
        "Credit_Limit",
        "Total_Revolving_Bal",
        "Avg_Utilization_Ratio",
        "Months_Inactive_12_mon",
        "Contacts_Count_12_mon",
        "Risk_Score",
        "Risk_Category"
    ]

    st.dataframe(
        high_risk_data[
            risk_display_columns
        ].style.format(
            {
                "Credit_Limit": "${:,.0f}",
                "Total_Revolving_Bal": "${:,.0f}",
                "Avg_Utilization_Ratio": "{:.1%}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.divider()

st.subheader("🏆 Risk Management Insights")


highest_risk_card = (
    card_risk[
        card_risk["Risk_Category"]
        == "High Risk"
    ]
)


if not highest_risk_card.empty:

    highest_risk_card = (
        highest_risk_card
        .sort_values(
            "Customers",
            ascending=False
        )
        .iloc[0]
    )

    highest_risk_card_name = (
        highest_risk_card[
            "Card_Category"
        ]
    )

else:

    highest_risk_card_name = "No High-Risk Segment"


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        ### 📊 Key Risk Findings

        **⚠️ High-Risk Customers**  
        **{high_risk_customers:,} customers**
        are currently classified as high risk.

        **💳 Highest Risk Card Segment**  
        **{highest_risk_card_name}**
        currently has the highest concentration
        of high-risk customers.

        **📈 Average Utilization**  
        Selected customers have an average
        utilization of
        **{average_utilization:.1%}**.
        """
    )


with col2:

    st.markdown(
        """
        ### 🎯 Recommended Actions

        **1️⃣ Monitor High Utilization**  
        Closely monitor customers approaching
        maximum credit utilization.

        **2️⃣ Re-engage Inactive Customers**  
        Create targeted campaigns for customers
        with extended inactivity.

        **3️⃣ Review High-Risk Accounts**  
        Prioritize high-risk customers for
        proactive credit monitoring.

        **4️⃣ Personalized Risk Strategies**  
        Use customer behavior and credit
        activity to create segment-specific
        risk management strategies.
        """
    )


# =====================================================
# DOWNLOAD DATA
# =====================================================

st.divider()


csv = (
    filtered_data
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    label="⬇️ Download Credit Risk Analysis Data",
    data=csv,
    file_name="credit_risk_analysis.csv",
    mime="text/csv"
)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
        <div class="footer">
        💳 Credit Pulse &nbsp;•&nbsp;
        Credit Risk Intelligence &nbsp;•&nbsp;
        Built with Streamlit
        </div>
    """,
    unsafe_allow_html=True
)