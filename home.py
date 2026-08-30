import streamlit as st
import plotly.express as px

from utils import (
    load_customer_data,
    load_transaction_data,
    chart_layout
)

from style import apply_style


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Credit Pulse",
    page_icon="💳",
    layout="wide"
)

apply_style()


# =====================================================
# LOAD DATA
# =====================================================

customers = load_customer_data()
transactions = load_transaction_data()


# =====================================================
# HEADER
# =====================================================

st.title("💳 Credit Pulse")

st.caption(
    "Credit Card Customer Intelligence & Transaction Analytics"
)

st.markdown(
    "**LIVE ANALYTICS**  |  Executive Overview"
)

st.divider()


# =====================================================
# PAGE DESCRIPTION
# =====================================================

st.subheader("📊 Portfolio Performance")

st.write(
    "Monitor customer activity, transaction performance, "
    "and overall credit exposure."
)


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = customers["Client_Num"].nunique()

total_transactions = transactions["Transaction_ID"].nunique()

total_transaction_amount = transactions[
    "Total_Trans_Amt"
].sum()

avg_transaction_amount = transactions[
    "Total_Trans_Amt"
].mean()

total_credit_limit = customers[
    "Credit_Limit"
].sum()


# =====================================================
# KPI ROW
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

with col3:
    st.metric(
        "Transaction Value",
        f"${total_transaction_amount:,.0f}"
    )

with col4:
    st.metric(
        "Avg Transaction",
        f"${avg_transaction_amount:,.2f}"
    )

with col5:
    st.metric(
        "Total Credit Limit",
        f"${total_credit_limit:,.0f}"
    )


st.divider()


# =====================================================
# QUICK INSIGHT
# =====================================================

average_utilization = customers[
    "Avg_Utilization_Ratio"
].mean()

high_utilization = (
    customers["Avg_Utilization_Ratio"] > 0.50
).mean()


st.subheader("💡 Portfolio Insight")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.metric(
        "Average Credit Utilization",
        f"{average_utilization:.1%}"
    )

with insight_col2:
    st.metric(
        "Customers Above 50% Utilization",
        f"{high_utilization:.1%}"
    )


st.info(
    f"Approximately {high_utilization:.1%} of customers "
    f"have credit utilization above 50%."
)


# =====================================================
# CUSTOMER MIX
# =====================================================

st.divider()

st.subheader("👥 Customer Portfolio")

st.write(
    "Explore the distribution of customers across "
    "card categories and gender."
)


col1, col2 = st.columns(2)


# =====================================================
# CARD CATEGORY
# =====================================================

with col1:

    card_data = (
        customers["Card_Category"]
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
        title="Customers by Card Category",
        hole=0.48
    )

    fig = chart_layout(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# GENDER
# =====================================================

with col2:

    gender_data = (
        customers["Gender"]
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
        title="Customers by Gender",
        text="Customers"
    )

    fig = chart_layout(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# TRANSACTION PERFORMANCE
# =====================================================

st.divider()

st.subheader("💰 Transaction Performance")

st.write(
    "Compare total transaction value across "
    "different transaction types."
)


transaction_type = (
    transactions
    .groupby("Transaction_Type")["Total_Trans_Amt"]
    .sum()
    .reset_index()
)


fig = px.bar(
    transaction_type,
    x="Transaction_Type",
    y="Total_Trans_Amt",
    text_auto=".2s",
    title="Total Transaction Amount by Transaction Type"
)


fig = chart_layout(
    fig,
    height=430
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "💳 Credit Pulse | Credit Card Analytics Dashboard | "
    "Python + Pandas + Plotly + Streamlit"
)