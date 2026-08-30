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
    load_transaction_data,
    chart_layout
)

from style import apply_style


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Transaction Analysis | Credit Pulse",
    page_icon="💰",
    layout="wide"
)

apply_style()


# =====================================================
# LOAD DATA
# =====================================================

transactions = load_transaction_data().copy()


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
        <div class="brand-header">

        <div class="status-badge">
            TRANSACTION INTELLIGENCE
        </div>

        <div class="brand-title">
            💰 Transaction Analysis
        </div>

        <div class="brand-subtitle">
            Analyze transaction trends, spending behavior,
            transaction types and customer activity.
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
                TRANSACTION INTELLIGENCE
            </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🔎 Transaction Filters")


    # =================================================
    # TRANSACTION TYPE FILTER
    # =================================================

    transaction_types = sorted(
        transactions[
            "Transaction_Type"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_transaction_types = st.multiselect(
        "Transaction Type",
        transaction_types,
        default=transaction_types
    )


    # =================================================
    # DATE FILTER
    # =================================================

    valid_dates = transactions[
        "Transaction_Date"
    ].dropna()


    if not valid_dates.empty:

        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        selected_dates = st.date_input(
            "Transaction Date",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    else:

        selected_dates = None

        st.warning(
            "Transaction date data is unavailable."
        )


# =====================================================
# APPLY FILTERS
# =====================================================

filtered_data = transactions.copy()


# Transaction Type Filter
if selected_transaction_types:

    filtered_data = filtered_data[
        filtered_data[
            "Transaction_Type"
        ].isin(
            selected_transaction_types
        )
    ]


# Date Filter
if selected_dates and len(selected_dates) == 2:

    start_date = selected_dates[0]
    end_date = selected_dates[1]

    filtered_data = filtered_data[
        (
            filtered_data[
                "Transaction_Date"
            ].dt.date
            >= start_date
        )
        &
        (
            filtered_data[
                "Transaction_Date"
            ].dt.date
            <= end_date
        )
    ]


# =====================================================
# EMPTY DATA PROTECTION
# =====================================================

if filtered_data.empty:

    st.warning(
        "⚠️ No transactions match the selected filters. "
        "Please adjust your filters."
    )

    st.stop()


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_transactions = (
    filtered_data[
        "Transaction_ID"
    ]
    .nunique()
)


total_transaction_value = (
    filtered_data[
        "Total_Trans_Amt"
    ]
    .sum()
)


average_transaction = (
    filtered_data[
        "Total_Trans_Amt"
    ]
    .mean()
)


unique_customers = (
    filtered_data[
        "Client_Num"
    ]
    .nunique()
)


total_transaction_volume = (
    filtered_data[
        "Total_Trans_Ct"
    ]
    .sum()
)


# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Transaction Performance Overview")


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "TOTAL TRANSACTIONS",
    f"{total_transactions:,}"
)


col2.metric(
    "TRANSACTION VALUE",
    f"${total_transaction_value:,.0f}"
)


col3.metric(
    "AVG TRANSACTION",
    f"${average_transaction:,.2f}"
)


col4.metric(
    "ACTIVE CUSTOMERS",
    f"{unique_customers:,}"
)


col5.metric(
    "TRANSACTION VOLUME",
    f"{total_transaction_volume:,.0f}"
)


# =====================================================
# TRANSACTION INSIGHTS
# =====================================================

st.divider()


average_transaction_count = (
    filtered_data[
        "Total_Trans_Ct"
    ]
    .mean()
)


average_amount_change = (
    filtered_data[
        "Total_Amt_Chng_Q4_Q1"
    ]
    .mean()
)


average_count_change = (
    filtered_data[
        "Total_Ct_Chng_Q4_Q1"
    ]
    .mean()
)


st.markdown(
    """
        <div class="section-label">
        TRANSACTION OVERVIEW
        </div>

    ### 💡 Transaction Insights
    """,
    unsafe_allow_html=True
)


insight_col1, insight_col2, insight_col3 = st.columns(3)


insight_col1.metric(
    "AVG TRANSACTION COUNT",
    f"{average_transaction_count:,.1f}"
)


insight_col2.metric(
    "AVG AMOUNT CHANGE",
    f"{average_amount_change:.1%}"
)


insight_col3.metric(
    "AVG COUNT CHANGE",
    f"{average_count_change:.1%}"
)


# =====================================================
# MONTHLY TREND
# =====================================================

st.divider()


st.markdown(
    """
        <div class="section-label">
        TIME SERIES ANALYSIS
        </div>

    ### 📈 Monthly Transaction Trend
    """,
    unsafe_allow_html=True
)


trend_data = filtered_data.dropna(
    subset=[
        "Transaction_Date"
    ]
).copy()


if not trend_data.empty:

    monthly_data = (
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


    monthly_data[
        "Transaction_Date"
    ] = monthly_data[
        "Transaction_Date"
    ].astype(str)


    fig = px.line(
        monthly_data,
        x="Transaction_Date",
        y="Transaction_Value",
        markers=True,
        title="Monthly Transaction Value"
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


    fig.update_xaxes(
        title="Month"
    )


    fig.update_yaxes(
        title="Transaction Value ($)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No valid transaction dates are available "
        "for trend analysis."
    )


# =====================================================
# TRANSACTION TYPE PERFORMANCE
# =====================================================

st.divider()


st.markdown(
    """
        <div class="section-label">
        TRANSACTION TYPES
        </div>

    ### 💳 Transaction Type Performance
    """,
    unsafe_allow_html=True
)


type_value = (
    filtered_data
    .groupby(
        "Transaction_Type"
    )
    .agg(
        Transaction_Value=(
            "Total_Trans_Amt",
            "sum"
        ),
        Transactions=(
            "Transaction_ID",
            "nunique"
        ),
        Customers=(
            "Client_Num",
            "nunique"
        )
    )
    .reset_index()
    .sort_values(
        "Transaction_Value",
        ascending=False
    )
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        type_value,
        x="Transaction_Type",
        y="Transaction_Value",
        text_auto=".2s",
        title="Transaction Value by Type"
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

    fig = px.pie(
        type_value,
        names="Transaction_Type",
        values="Transactions",
        hole=0.50,
        title="Transaction Distribution by Type"
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
# CUSTOMER TRANSACTION BEHAVIOR
# =====================================================

st.divider()


st.markdown(
    """
        <div class="section-label">
        CUSTOMER ACTIVITY
        </div>

    ### 👥 Customer Transaction Behavior
    """,
    unsafe_allow_html=True
)


customer_activity = (
    filtered_data
    .groupby(
        "Client_Num"
    )
    .agg(
        Transaction_Count=(
            "Transaction_ID",
            "nunique"
        ),
        Total_Spent=(
            "Total_Trans_Amt",
            "sum"
        ),
        Average_Transaction=(
            "Total_Trans_Amt",
            "mean"
        )
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    top_customers = (
        customer_activity
        .nlargest(
            10,
            "Total_Spent"
        )
        .sort_values(
            "Total_Spent"
        )
    )


    fig = px.bar(
        top_customers,
        x="Total_Spent",
        y="Client_Num",
        orientation="h",
        text_auto=".2s",
        title="Top 10 Customers by Transaction Value"
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

    fig = px.scatter(
        customer_activity,
        x="Transaction_Count",
        y="Total_Spent",
        size="Average_Transaction",
        hover_data=[
            "Client_Num"
        ],
        title="Transaction Frequency vs Spending"
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
# PERFORMANCE TABLE
# =====================================================

st.divider()


st.markdown(
    """
        <div class="section-label">
        PERFORMANCE DETAILS
        </div>

    ### 📋 Transaction Performance Summary
    """,
    unsafe_allow_html=True
)


summary = (
    filtered_data
    .groupby(
        "Transaction_Type"
    )
    .agg(
        Transactions=(
            "Transaction_ID",
            "nunique"
        ),
        Customers=(
            "Client_Num",
            "nunique"
        ),
        Total_Value=(
            "Total_Trans_Amt",
            "sum"
        ),
        Average_Value=(
            "Total_Trans_Amt",
            "mean"
        ),
        Average_Transaction_Count=(
            "Total_Trans_Ct",
            "mean"
        )
    )
    .reset_index()
)


total_value = summary[
    "Total_Value"
].sum()


if total_value > 0:

    summary[
        "Share_of_Value"
    ] = (
        summary[
            "Total_Value"
        ]
        /
        total_value
    )

else:

    summary[
        "Share_of_Value"
    ] = 0


st.dataframe(
    summary.style.format(
        {
            "Total_Value": "${:,.2f}",
            "Average_Value": "${:,.2f}",
            "Average_Transaction_Count": "{:,.1f}",
            "Share_of_Value": "{:.1%}"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.divider()


st.subheader("🏆 Key Business Insights")


top_transaction_type = (
    type_value.iloc[0][
        "Transaction_Type"
    ]
)


top_transaction_value = (
    type_value.iloc[0][
        "Transaction_Value"
    ]
)


top_customer = (
    customer_activity
    .sort_values(
        "Total_Spent",
        ascending=False
    )
    .iloc[0]
)


top_customer_id = top_customer[
    "Client_Num"
]


top_customer_spending = top_customer[
    "Total_Spent"
]


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        ### 📊 Key Findings

        **💳 Leading Transaction Type**  
        **{top_transaction_type}** generates the
        highest transaction value of
        **${top_transaction_value:,.0f}**.

        **👑 Highest Spending Customer**  
        Customer **{top_customer_id}** generated
        total spending of
        **${top_customer_spending:,.0f}**.

        **📈 Customer Activity**  
        The selected data includes
        **{unique_customers:,} active customers**.
        """
    )


with col2:

    st.markdown(
        """
        ### 🎯 Recommended Actions

        **1️⃣ Strengthen High-Value Transactions**  
        Focus on improving engagement in
        high-performing transaction categories.

        **2️⃣ Retain High-Value Customers**  
        Create personalized offers for
        customers with high spending activity.

        **3️⃣ Monitor Transaction Changes**  
        Track changes in transaction amount
        and transaction frequency.

        **4️⃣ Improve Customer Engagement**  
        Use transaction behavior to create
        targeted marketing strategies.
        """
    )


# =====================================================
# DOWNLOAD FILTERED DATA
# =====================================================

st.divider()


csv = filtered_data.to_csv(
    index=False
).encode(
    "utf-8"
)


st.download_button(
    label="⬇️ Download Filtered Transaction Data",
    data=csv,
    file_name="filtered_transaction_data.csv",
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
        Transaction Intelligence &nbsp;•&nbsp;
        Built with Streamlit
        </div>
    """,
    unsafe_allow_html=True
)