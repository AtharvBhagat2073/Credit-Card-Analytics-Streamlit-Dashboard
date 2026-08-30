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
    page_title="Customer Analysis | Credit Pulse",
    page_icon="👥",
    layout="wide"
)

apply_style()


# =====================================================
# LOAD DATA
# =====================================================

customers = load_customer_data().copy()


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
        <div class="brand-header">

        <div class="status-badge">
            CUSTOMER INTELLIGENCE
        </div>

        <div class="brand-title">
            👥 Customer Analysis
        </div>

        <div class="brand-subtitle">
            Explore customer demographics, portfolio segments,
            credit exposure and utilization behavior.
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
                CUSTOMER INTELLIGENCE
            </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🔎 Customer Filters")


    # -------------------------
    # Gender Filter
    # -------------------------

    gender_options = sorted(
        customers["Gender"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_gender = st.multiselect(
        "Gender",
        gender_options,
        default=gender_options
    )


    # -------------------------
    # Card Filter
    # -------------------------

    card_options = sorted(
        customers["Card_Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_card = st.multiselect(
        "Card Category",
        card_options,
        default=card_options
    )


    # -------------------------
    # Income Filter
    # -------------------------

    income_options = sorted(
        customers["Income_Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_income = st.multiselect(
        "Income Category",
        income_options,
        default=income_options
    )


    # -------------------------
    # Age Range Filter
    # -------------------------

    min_age = int(
        customers["Customer_Age"].min()
    )

    max_age = int(
        customers["Customer_Age"].max()
    )

    selected_age_range = st.slider(
        "Customer Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )


    st.divider()

    st.caption(
        "Use the filters to explore specific customer segments."
    )


# =====================================================
# FILTER DATA
# =====================================================

filtered_data = customers[
    (
        customers["Gender"].isin(
            selected_gender
        )
    )
    &
    (
        customers["Card_Category"].isin(
            selected_card
        )
    )
    &
    (
        customers["Income_Category"].isin(
            selected_income
        )
    )
    &
    (
        customers["Customer_Age"].between(
            selected_age_range[0],
            selected_age_range[1]
        )
    )
].copy()


# =====================================================
# EMPTY DATA PROTECTION
# =====================================================

if filtered_data.empty:

    st.warning(
        "⚠️ No customers match the selected filters. "
        "Please adjust your filter selection."
    )

    st.stop()


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = (
    filtered_data["Client_Num"]
    .nunique()
)

average_age = (
    filtered_data["Customer_Age"]
    .mean()
)

average_credit_limit = (
    filtered_data["Credit_Limit"]
    .mean()
)

average_utilization = (
    filtered_data["Avg_Utilization_Ratio"]
    .mean()
)

total_credit_limit = (
    filtered_data["Credit_Limit"]
    .sum()
)

high_utilization_customers = (
    filtered_data[
        filtered_data[
            "Avg_Utilization_Ratio"
        ] > 0.50
    ]["Client_Num"]
    .nunique()
)

high_utilization_percentage = (
    high_utilization_customers
    /
    total_customers
)


# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Customer Portfolio Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "TOTAL CUSTOMERS",
    f"{total_customers:,}"
)

col2.metric(
    "AVG AGE",
    f"{average_age:.1f}"
)

col3.metric(
    "AVG CREDIT LIMIT",
    f"${average_credit_limit:,.0f}"
)

col4.metric(
    "AVG UTILIZATION",
    f"{average_utilization:.1%}"
)

col5.metric(
    "TOTAL CREDIT LIMIT",
    f"${total_credit_limit:,.0f}"
)


# =====================================================
# CUSTOMER INSIGHT
# =====================================================

st.divider()

st.markdown(
    f"""
        <div class="insight-card">

        <div class="insight-title">
            💡 Portfolio Insight
        </div>

        <div class="insight-text">
            <b>{high_utilization_percentage:.1%}</b>
            of selected customers have credit utilization above
            <b>50%</b>, representing
            <b>{high_utilization_customers:,} customers</b>.
        </div>

        </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# CUSTOMER DEMOGRAPHICS
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        CUSTOMER DEMOGRAPHICS
    </div>

    ### 👤 Demographic Analysis
    """
)


col1, col2 = st.columns(2)


# =====================================================
# AGE DISTRIBUTION
# =====================================================

with col1:

    age_data = (
        filtered_data["Customer_Age"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_data.columns = [
        "Age",
        "Customers"
    ]

    fig = px.bar(
        age_data,
        x="Age",
        y="Customers",
        title="Customer Distribution by Age"
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
# GENDER DISTRIBUTION
# =====================================================

with col2:

    gender_data = (
        filtered_data["Gender"]
        .value_counts()
        .reset_index()
    )

    gender_data.columns = [
        "Gender",
        "Customers"
    ]

    fig = px.pie(
        gender_data,
        names="Gender",
        values="Customers",
        title="Customer Distribution by Gender",
        hole=0.50
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
# AGE GROUP ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        AGE SEGMENTATION
        </div>

    ### 📈 Customer Age Groups
    """
)


age_group_data = filtered_data.copy()

age_group_data["Age_Group"] = pd.cut(
    age_group_data["Customer_Age"],
    bins=[
        0,
        25,
        35,
        45,
        55,
        65,
        100
    ],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56-65",
        "65+"
    ],
    include_lowest=True
)


age_summary = (
    age_group_data["Age_Group"]
    .value_counts()
    .sort_index()
    .reset_index()
)

age_summary.columns = [
    "Age_Group",
    "Customers"
]


fig = px.bar(
    age_summary,
    x="Age_Group",
    y="Customers",
    title="Customer Portfolio by Age Group",
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
# CUSTOMER SEGMENTATION
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        CUSTOMER SEGMENTATION
    </div>

    ### 💰 Income & Card Portfolio
    """
)


col1, col2 = st.columns(2)


# =====================================================
# INCOME CATEGORY
# =====================================================

with col1:

    income_data = (
        filtered_data["Income_Category"]
        .value_counts()
        .reset_index()
    )

    income_data.columns = [
        "Income_Category",
        "Customers"
    ]

    fig = px.bar(
        income_data,
        x="Income_Category",
        y="Customers",
        title="Customers by Income Category",
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
# CARD CATEGORY
# =====================================================

with col2:

    card_data = (
        filtered_data["Card_Category"]
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
        title="Customer Distribution by Card Category",
        hole=0.50
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
# CREDIT EXPOSURE
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        CREDIT EXPOSURE
    </div>

    ### 💳 Credit Limit Analysis
    """
)


credit_data = (
    filtered_data
    .groupby("Card_Category")
    .agg(
        Average_Credit_Limit=(
            "Credit_Limit",
            "mean"
        ),
        Maximum_Credit_Limit=(
            "Credit_Limit",
            "max"
        ),
        Total_Credit_Limit=(
            "Credit_Limit",
            "sum"
        ),
        Customers=(
            "Client_Num",
            "nunique"
        )
    )
    .reset_index()
)


fig = px.bar(
    credit_data,
    x="Card_Category",
    y="Average_Credit_Limit",
    title="Average Credit Limit by Card Category",
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
# UTILIZATION SEGMENTATION
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        CREDIT UTILIZATION
    </div>

    ### 🛡️ Customer Utilization Segments
    """
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
    title="Customer Distribution by Credit Utilization",
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
# KEY INSIGHTS
# =====================================================

st.divider()

st.subheader("🏆 Customer Insights")


largest_income_segment = (
    income_data
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


largest_card_segment = (
    card_data
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


most_common_age_group = (
    age_summary
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        ### 📊 Portfolio Highlights

        **Largest Income Segment**  
        {largest_income_segment["Income_Category"]}
        represents the largest income group with
        **{largest_income_segment["Customers"]:,} customers**.

        **Largest Card Segment**  
        {largest_card_segment["Card_Category"]}
        is the most common card category with
        **{largest_card_segment["Customers"]:,} customers**.

        **Largest Age Group**  
        The {most_common_age_group["Age_Group"]} segment
        contains the highest number of customers.
        """
    )


with col2:

    st.markdown(
        f"""
        ### 🎯 Recommended Actions

        **1️⃣ Monitor High Utilization**  
        Focus on the **{high_utilization_customers:,}**
        customers with utilization above 50%.

        **2️⃣ Segment-Based Offers**  
        Create personalized offers based on
        income and card categories.

        **3️⃣ Customer Retention**  
        Develop targeted engagement strategies
        for high-value cardholders.

        **4️⃣ Credit Management**  
        Monitor utilization trends to identify
        potential credit exposure risks.
        """
    )


# =====================================================
# CUSTOMER DATA TABLE
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        CUSTOMER RECORDS
    </div>

    ### 📋 Filtered Customer Data
    """
)


display_columns = [
    "Client_Num",
    "Customer_Age",
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
    "Credit_Limit",
    "Avg_Open_To_Buy",
    "Total_Revolving_Bal",
    "Avg_Utilization_Ratio"
]


available_columns = [
    column
    for column in display_columns
    if column in filtered_data.columns
]


st.dataframe(
    filtered_data[
        available_columns
    ],
    use_container_width=True,
    hide_index=True
)


# =====================================================
# DOWNLOAD FILTERED DATA
# =====================================================

csv = (
    filtered_data[
        available_columns
    ]
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    label="⬇️ Download Filtered Customer Data",
    data=csv,
    file_name="filtered_customer_data.csv",
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
        Customer Intelligence &nbsp;•&nbsp;
        Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)