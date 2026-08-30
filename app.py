import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_customer_data,
    load_transaction_data,
    chart_layout
)

from style import apply_style


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Credit Pulse | Executive Overview",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# APPLY GLOBAL STYLE
# =====================================================

apply_style()


# =====================================================
# LOAD DATA
# =====================================================

customers = load_customer_data().copy()
transactions = load_transaction_data().copy()


# =====================================================
# REQUIRED COLUMN VALIDATION
# =====================================================

customer_required_columns = [
    "Client_Num",
    "Customer_Age",
    "Gender",
    "Income_Category",
    "Card_Category",
    "Credit_Limit",
    "Total_Revolving_Bal",
    "Avg_Utilization_Ratio",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon"
]

transaction_required_columns = [
    "Transaction_ID",
    "Client_Num",
    "Transaction_Date",
    "Transaction_Type",
    "Total_Trans_Amt",
    "Total_Trans_Ct"
]


missing_customer_columns = [
    column
    for column in customer_required_columns
    if column not in customers.columns
]


missing_transaction_columns = [
    column
    for column in transaction_required_columns
    if column not in transactions.columns
]


if missing_customer_columns:

    st.error(
        "Missing customer columns: "
        + ", ".join(missing_customer_columns)
    )

    st.stop()


if missing_transaction_columns:

    st.error(
        "Missing transaction columns: "
        + ", ".join(missing_transaction_columns)
    )

    st.stop()


# =====================================================
# ENSURE TRANSACTION DATE FORMAT
# =====================================================

transactions["Transaction_Date"] = pd.to_datetime(
    transactions["Transaction_Date"],
    errors="coerce",
    dayfirst=True
)


# =====================================================
# SIDEBAR
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
                EXECUTIVE INTELLIGENCE
            </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🎛️ Executive Filters")


    # -------------------------------------------------
    # CARD CATEGORY FILTER
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
    # GENDER FILTER
    # -------------------------------------------------

    gender_options = sorted(
        customers["Gender"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_gender = st.multiselect(
        "Gender",
        gender_options,
        default=gender_options
    )


    # -------------------------------------------------
    # INCOME FILTER
    # -------------------------------------------------

    income_options = sorted(
        customers["Income_Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_income = st.multiselect(
        "Income Category",
        income_options,
        default=income_options
    )


    # -------------------------------------------------
    # AGE FILTER
    # -------------------------------------------------

    min_age = int(
        customers["Customer_Age"].min()
    )

    max_age = int(
        customers["Customer_Age"].max()
    )

    selected_age = st.slider(
        "Customer Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )


    st.divider()

    st.markdown("### 📌 Dashboard Scope")

    st.caption(
        "Customer Portfolio\n\n"
        "Transaction Performance\n\n"
        "Credit Utilization\n\n"
        "Risk Indicators\n\n"
        "Executive Insights"
    )


# =====================================================
# APPLY CUSTOMER FILTERS
# =====================================================

filtered_customers = customers[
    (
        customers["Card_Category"]
        .astype(str)
        .isin(selected_cards)
    )
    &
    (
        customers["Gender"]
        .astype(str)
        .isin(selected_gender)
    )
    &
    (
        customers["Income_Category"]
        .astype(str)
        .isin(selected_income)
    )
    &
    (
        customers["Customer_Age"]
        .between(
            selected_age[0],
            selected_age[1]
        )
    )
].copy()


# =====================================================
# EMPTY DATA PROTECTION
# =====================================================

if filtered_customers.empty:

    st.warning(
        "⚠️ No customers match the selected filters."
    )

    st.stop()


# =====================================================
# FILTER TRANSACTIONS BY SELECTED CUSTOMERS
# =====================================================

selected_customer_ids = (
    filtered_customers["Client_Num"]
    .unique()
)


filtered_transactions = transactions[
    transactions["Client_Num"].isin(
        selected_customer_ids
    )
].copy()


# =====================================================
# CREATE RISK CATEGORY
# =====================================================

def calculate_risk(row):

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
        and row["Total_Revolving_Bal"]
        / row["Credit_Limit"]
        >= 0.50
    ):
        score += 2


    if row["Contacts_Count_12_mon"] >= 5:
        score += 1


    if score >= 5:
        return "High Risk"

    elif score >= 3:
        return "Medium Risk"

    return "Low Risk"


filtered_customers["Risk_Category"] = (
    filtered_customers.apply(
        calculate_risk,
        axis=1
    )
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
        <div class="brand-header">

        <div class="status-badge">
            LIVE EXECUTIVE INTELLIGENCE
        </div>

        <div class="brand-title">
            💳 Credit Pulse
        </div>

        <div class="brand-subtitle">
            Executive overview of customer portfolio,
            transaction performance and credit exposure.
        </div>

        </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = (
    filtered_customers["Client_Num"]
    .nunique()
)


total_transactions = (
    filtered_transactions["Transaction_ID"]
    .nunique()
)


total_transaction_amount = (
    filtered_transactions["Total_Trans_Amt"]
    .sum()
)


average_transaction_amount = (
    filtered_transactions["Total_Trans_Amt"]
    .mean()
    if not filtered_transactions.empty
    else 0
)


total_credit_limit = (
    filtered_customers["Credit_Limit"]
    .sum()
)


average_utilization = (
    filtered_customers[
        "Avg_Utilization_Ratio"
    ]
    .mean()
)


total_revolving_balance = (
    filtered_customers[
        "Total_Revolving_Bal"
    ]
    .sum()
)


high_risk_customers = (
    filtered_customers[
        filtered_customers["Risk_Category"]
        == "High Risk"
    ]["Client_Num"]
    .nunique()
)


high_risk_percentage = (
    high_risk_customers
    / total_customers
    if total_customers > 0
    else 0
)


# =====================================================
# EXECUTIVE KPI SECTION
# =====================================================

st.subheader("📊 Executive Performance Overview")


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "TOTAL CUSTOMERS",
    f"{total_customers:,}"
)


col2.metric(
    "TOTAL TRANSACTIONS",
    f"{total_transactions:,}"
)


col3.metric(
    "TRANSACTION VALUE",
    f"${total_transaction_amount:,.0f}"
)


col4.metric(
    "AVG TRANSACTION",
    f"${average_transaction_amount:,.2f}"
)


col5.metric(
    "TOTAL CREDIT LIMIT",
    f"${total_credit_limit:,.0f}"
)


# =====================================================
# PORTFOLIO HEALTH
# =====================================================

st.divider()

st.subheader("💡 Portfolio Health Snapshot")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "AVG CREDIT UTILIZATION",
    f"{average_utilization:.1%}"
)


col2.metric(
    "HIGH-RISK CUSTOMERS",
    f"{high_risk_customers:,}"
)


col3.metric(
    "HIGH-RISK %",
    f"{high_risk_percentage:.1%}"
)


col4.metric(
    "REVOLVING BALANCE",
    f"${total_revolving_balance:,.0f}"
)


st.info(
    f"📌 Portfolio Insight: {high_risk_percentage:.1%} "
    f"of the selected customer portfolio is currently "
    f"classified as high risk."
)


# =====================================================
# CUSTOMER PORTFOLIO
# =====================================================

st.divider()

st.subheader("👥 Customer Portfolio")


col1, col2 = st.columns(2)


# -----------------------------------------------------
# CARD CATEGORY
# -----------------------------------------------------

with col1:

    card_data = (
        filtered_customers[
            "Card_Category"
        ]
        .value_counts()
        .reset_index()
    )

    card_data.columns = [
        "Card_Category",
        "Customers"
    ]


    fig = px.pie(
        card_data,
        names="Card_Category",
        values="Customers",
        hole=0.50,
        title="Customer Distribution by Card Category"
    )


    fig = chart_layout(
        fig,
        height=420
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------------------------------
# GENDER DISTRIBUTION
# -----------------------------------------------------

with col2:

    gender_data = (
        filtered_customers[
            "Gender"
        ]
        .value_counts()
        .reset_index()
    )

    gender_data.columns = [
        "Gender",
        "Customers"
    ]


    fig = px.bar(
        gender_data,
        x="Gender",
        y="Customers",
        title="Customer Distribution by Gender",
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
# TRANSACTION PERFORMANCE
# =====================================================

st.divider()

st.subheader("💰 Transaction Performance")


if filtered_transactions.empty:

    st.info(
        "No transaction records are available "
        "for the selected customer segment."
    )

else:

    col1, col2 = st.columns(2)


    # -------------------------------------------------
    # TRANSACTION VALUE BY TYPE
    # -------------------------------------------------

    with col1:

        transaction_type = (
            filtered_transactions
            .groupby(
                "Transaction_Type"
            )
            .agg(
                Transaction_Value=(
                    "Total_Trans_Amt",
                    "sum"
                )
            )
            .reset_index()
            .sort_values(
                "Transaction_Value",
                ascending=False
            )
        )


        fig = px.bar(
            transaction_type,
            x="Transaction_Type",
            y="Transaction_Value",
            title="Transaction Value by Type",
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


    # -------------------------------------------------
    # TRANSACTION VOLUME
    # -------------------------------------------------

    with col2:

        transaction_volume = (
            filtered_transactions
            .groupby(
                "Transaction_Type"
            )
            .agg(
                Transaction_Volume=(
                    "Total_Trans_Ct",
                    "sum"
                )
            )
            .reset_index()
            .sort_values(
                "Transaction_Volume",
                ascending=False
            )
        )


        fig = px.bar(
            transaction_volume,
            x="Transaction_Type",
            y="Transaction_Volume",
            title="Transaction Volume by Type",
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
# TRANSACTION TREND
# =====================================================

st.divider()

st.subheader("📈 Transaction Trend Over Time")


trend_data = (
    filtered_transactions
    .dropna(
        subset=[
            "Transaction_Date"
        ]
    )
    .copy()
)


if trend_data.empty:

    st.info(
        "No valid transaction dates are available."
    )

else:

    transaction_trend = (
        trend_data
        .groupby(
            trend_data[
                "Transaction_Date"
            ].dt.to_period("M")
        )
        .agg(
            Transaction_Value=(
                "Total_Trans_Amt",
                "sum"
            ),
            Transactions=(
                "Transaction_ID",
                "nunique"
            )
        )
        .reset_index()
    )


    transaction_trend[
        "Transaction_Date"
    ] = transaction_trend[
        "Transaction_Date"
    ].astype(str)


    fig = px.line(
        transaction_trend,
        x="Transaction_Date",
        y="Transaction_Value",
        markers=True,
        title="Monthly Transaction Value Trend"
    )


    fig.update_traces(
        line=dict(
            width=3
        )
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
# CREDIT UTILIZATION & RISK
# =====================================================

st.divider()

st.subheader("🛡️ Credit Risk & Utilization")


utilization_data = filtered_customers.copy()


utilization_data[
    "Utilization_Segment"
] = pd.cut(
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


col1, col2 = st.columns(2)


with col1:

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


with col2:

    risk_data = (
        filtered_customers[
            "Risk_Category"
        ]
        .value_counts()
        .reset_index()
    )

    risk_data.columns = [
        "Risk_Category",
        "Customers"
    ]


    fig = px.pie(
        risk_data,
        names="Risk_Category",
        values="Customers",
        hole=0.50,
        title="Customer Risk Distribution"
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
# INCOME & UTILIZATION
# =====================================================

st.divider()

st.subheader("💰 Income & Credit Behavior")


income_utilization = (
    filtered_customers
    .groupby(
        "Income_Category"
    )
    .agg(
        Average_Utilization=(
            "Avg_Utilization_Ratio",
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
    .sort_values(
        "Average_Utilization",
        ascending=False
    )
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        income_utilization,
        x="Income_Category",
        y="Average_Utilization",
        title="Average Utilization by Income Category",
        text_auto=".1%"
    )


    fig.update_layout(
        yaxis_tickformat=".0%"
    )


    fig.update_xaxes(
        tickangle=-30
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
        income_utilization,
        x="Income_Category",
        y="Average_Credit_Limit",
        title="Average Credit Limit by Income Category",
        text_auto=".2s"
    )


    fig.update_xaxes(
        tickangle=-30
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
# EXECUTIVE INSIGHTS
# =====================================================

st.divider()

st.subheader("🏆 Executive Insights & Recommendations")


largest_card_category = (
    card_data
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


highest_utilization_income = (
    income_utilization
    .sort_values(
        "Average_Utilization",
        ascending=False
    )
    .iloc[0]
)


if not filtered_transactions.empty:

    top_transaction_type = (
        transaction_type
        .sort_values(
            "Transaction_Value",
            ascending=False
        )
        .iloc[0]
    )

    transaction_type_name = (
        top_transaction_type[
            "Transaction_Type"
        ]
    )

    transaction_type_value = (
        top_transaction_type[
            "Transaction_Value"
        ]
    )

else:

    transaction_type_name = "No transaction data"

    transaction_type_value = 0


insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    st.markdown(
        f"""
        ### 📊 Key Findings

        **💳 Largest Customer Segment**  
        **{largest_card_category["Card_Category"]}**
        represents the largest card category with
        **{largest_card_category["Customers"]:,} customers**.

        **💰 Leading Transaction Type**  
        **{transaction_type_name}** generates the
        highest transaction value at
        **${transaction_type_value:,.0f}**.

        **⚠️ Portfolio Risk**  
        **{high_risk_percentage:.1%}** of the selected
        customer portfolio is classified as high risk.
        """
    )


with insight_col2:

    st.markdown(
        f"""
        ### 🎯 Recommended Actions

        **1️⃣ Monitor High-Risk Customers**  
        Prioritize customers with high utilization
        and extended inactivity.

        **2️⃣ Strengthen High-Value Transactions**  
        Improve engagement in the
        **{transaction_type_name}** segment.

        **3️⃣ Focus on Credit Behavior**  
        The **{highest_utilization_income["Income_Category"]}**
        segment has the highest average utilization
        at **{highest_utilization_income["Average_Utilization"]:.1%}**.

        **4️⃣ Improve Customer Retention**  
        Use demographic and transaction behavior
        to develop personalized engagement strategies.
        """
    )


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.divider()


st.markdown(
    f"""
    ### 📌 Executive Summary

    The selected Credit Pulse portfolio contains
    **{total_customers:,} customers** and
    **{total_transactions:,} transactions**.

    The portfolio has generated
    **${total_transaction_amount:,.0f}**
    in transaction value and currently has a
    total credit limit of
    **${total_credit_limit:,.0f}**.

    The dashboard provides a consolidated view of
    customer behavior, transaction activity,
    credit utilization and potential risk areas
    to support data-driven business decisions.
    """
)


# =====================================================
# DOWNLOAD EXECUTIVE DATA
# =====================================================

st.divider()

st.subheader("⬇️ Export Executive Data")


customer_csv = (
    filtered_customers
    .to_csv(index=False)
    .encode("utf-8")
)


transaction_csv = (
    filtered_transactions
    .to_csv(index=False)
    .encode("utf-8")
)


col1, col2 = st.columns(2)


with col1:

    st.download_button(
        label="⬇️ Download Filtered Customer Data",
        data=customer_csv,
        file_name="executive_customer_data.csv",
        mime="text/csv"
    )


with col2:

    st.download_button(
        label="⬇️ Download Filtered Transaction Data",
        data=transaction_csv,
        file_name="executive_transaction_data.csv",
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
        Executive Intelligence &nbsp;•&nbsp;
        Built with Python, Pandas, Plotly & Streamlit
        </div>
    """,
    unsafe_allow_html=True
)