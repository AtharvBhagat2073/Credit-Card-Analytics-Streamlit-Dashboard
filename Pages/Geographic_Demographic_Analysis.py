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
    page_title="Geographic & Demographic Analysis | Credit Pulse",
    page_icon="🌍",
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
            DEMOGRAPHIC INTELLIGENCE
        </div>

        <div class="brand-title">
            🌍 Geographic & Demographic Analysis
        </div>

        <div class="brand-subtitle">
            Explore customer demographics, income segments,
            education, family profiles and credit behavior.
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
                DEMOGRAPHIC INTELLIGENCE
            </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🔎 Analysis Filters")


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
    # EDUCATION FILTER
    # -------------------------------------------------

    education_options = sorted(
        customers["Education_Level"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_education = st.multiselect(
        "Education Level",
        education_options,
        default=education_options
    )


    # -------------------------------------------------
    # MARITAL STATUS FILTER
    # -------------------------------------------------

    marital_options = sorted(
        customers["Marital_Status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_marital = st.multiselect(
        "Marital Status",
        marital_options,
        default=marital_options
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

    selected_age_range = st.slider(
        "Customer Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )


    st.divider()

    st.caption(
        "Use filters to explore different demographic "
        "customer segments."
    )


# =====================================================
# APPLY FILTERS
# =====================================================

filtered_data = customers[
    (
        customers["Gender"]
        .astype(str)
        .isin(selected_gender)
    )
    &
    (
        customers["Education_Level"]
        .astype(str)
        .isin(selected_education)
    )
    &
    (
        customers["Marital_Status"]
        .astype(str)
        .isin(selected_marital)
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
        "Please adjust your selections."
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

average_dependents = (
    filtered_data["Dependent_Count"]
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


# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Demographic Overview")

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
    "AVG DEPENDENTS",
    f"{average_dependents:.1f}"
)

col4.metric(
    "AVG CREDIT LIMIT",
    f"${average_credit_limit:,.0f}"
)

col5.metric(
    "AVG UTILIZATION",
    f"{average_utilization:.1%}"
)


# =====================================================
# DEMOGRAPHIC INSIGHT
# =====================================================

st.divider()

largest_income_segment = (
    filtered_data["Income_Category"]
    .value_counts()
    .idxmax()
)

largest_income_count = (
    filtered_data["Income_Category"]
    .value_counts()
    .max()
)

st.info(
    f"💡 Demographic Insight: The largest income segment is "
    f"'{largest_income_segment}' with "
    f"{largest_income_count:,} customers."
)


# =====================================================
# GENDER & AGE ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        DEMOGRAPHIC PROFILE
        </div>

    ### 👥 Gender & Age Analysis
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# -----------------------------------------------------
# GENDER DISTRIBUTION
# -----------------------------------------------------

with col1:

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


# -----------------------------------------------------
# AGE DISTRIBUTION
# -----------------------------------------------------

with col2:

    age_data = (
        filtered_data["Customer_Age"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_data.columns = [
        "Customer_Age",
        "Customers"
    ]

    fig = px.bar(
        age_data,
        x="Customer_Age",
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
# DEPENDENT ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        FAMILY PROFILE
    </div>

    ### 👨‍👩‍👧 Dependent Analysis
    """,
    unsafe_allow_html=True
)


dependents_distribution = (
    filtered_data
    .groupby("Dependent_Count")
    .size()
    .reset_index(name="Customers")
    .sort_values("Dependent_Count")
)


fig = px.bar(
    dependents_distribution,
    x="Dependent_Count",
    y="Customers",
    title="Customer Distribution by Number of Dependents",
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
# EDUCATION ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        EDUCATION PROFILE
        </div>

    ### 🎓 Education Level Analysis
    """,
    unsafe_allow_html=True
)


education_data = (
    filtered_data["Education_Level"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

education_data.columns = [
    "Education_Level",
    "Customers"
]


fig = px.bar(
    education_data,
    x="Education_Level",
    y="Customers",
    title="Customer Distribution by Education Level",
    text="Customers"
)

fig.update_traces(
    textposition="outside"
)

fig = chart_layout(
    fig,
    height=420
)

fig.update_xaxes(
    tickangle=-30
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# MARITAL STATUS ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        HOUSEHOLD PROFILE
    </div>

    ### 💍 Marital Status Analysis
    """,
    unsafe_allow_html=True
)


marital_data = (
    filtered_data["Marital_Status"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

marital_data.columns = [
    "Marital_Status",
    "Customers"
]


fig = px.pie(
    marital_data,
    names="Marital_Status",
    values="Customers",
    title="Customer Distribution by Marital Status",
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
# INCOME ANALYSIS
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        INCOME SEGMENTATION
        </div>

    ### 💰 Income Category Analysis
    """,
    unsafe_allow_html=True
)


income_data = (
    filtered_data["Income_Category"]
    .value_counts()
    .reset_index()
)

income_data.columns = [
    "Income_Category",
    "Customers"
]


col1, col2 = st.columns(2)


with col1:

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

    income_credit = (
        filtered_data
        .groupby("Income_Category")
        .agg(
            Average_Credit_Limit=(
                "Credit_Limit",
                "mean"
            ),
            Average_Utilization=(
                "Avg_Utilization_Ratio",
                "mean"
            )
        )
        .reset_index()
    )

    fig = px.bar(
        income_credit,
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
# EDUCATION & CREDIT BEHAVIOR
# =====================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        CREDIT BEHAVIOR
    </div>

    ### 💳 Credit Behavior by Education Level
    """,
    unsafe_allow_html=True
)


education_credit = (
    filtered_data
    .groupby("Education_Level")
    .agg(
        Average_Credit_Limit=(
            "Credit_Limit",
            "mean"
        ),
        Average_Utilization=(
            "Avg_Utilization_Ratio",
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
        education_credit,
        x="Education_Level",
        y="Average_Credit_Limit",
        title="Average Credit Limit by Education Level",
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


with col2:

    fig = px.bar(
        education_credit,
        x="Education_Level",
        y="Average_Utilization",
        title="Average Utilization by Education Level",
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
    """,
    unsafe_allow_html=True
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


age_group_summary = (
    age_group_data
    .groupby(
        "Age_Group",
        observed=False
    )
    .agg(
        Customers=(
            "Client_Num",
            "nunique"
        ),
        Average_Credit_Limit=(
            "Credit_Limit",
            "mean"
        ),
        Average_Utilization=(
            "Avg_Utilization_Ratio",
            "mean"
        )
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        age_group_summary,
        x="Age_Group",
        y="Customers",
        title="Customers by Age Group",
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

    fig = px.line(
        age_group_summary,
        x="Age_Group",
        y="Average_Utilization",
        markers=True,
        title="Average Credit Utilization by Age Group"
    )

    fig.update_layout(
        yaxis_tickformat=".0%"
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
# DEMOGRAPHIC INSIGHTS
# =====================================================

st.divider()

st.subheader("🏆 Key Demographic Insights")


largest_education_segment = (
    education_data
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


largest_marital_segment = (
    marital_data
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


most_common_dependent_count = (
    dependents_distribution
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]
)


highest_income_credit = (
    income_credit
    .sort_values(
        "Average_Credit_Limit",
        ascending=False
    )
    .iloc[0]
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        ### 📊 Key Findings

        **🎓 Largest Education Segment**  
        **{largest_education_segment["Education_Level"]}**
        is the largest education group with
        **{largest_education_segment["Customers"]:,} customers**.

        **💍 Largest Household Segment**  
        **{largest_marital_segment["Marital_Status"]}**
        customers represent the largest marital-status group.

        **👨‍👩‍👧 Common Family Size**  
        The most common customer profile has
        **{most_common_dependent_count["Dependent_Count"]:.0f} dependents**.
        """
    )


with col2:

    st.markdown(
        f"""
        ### 🎯 Business Recommendations

        **1️⃣ Segment-Based Marketing**  
        Create campaigns based on demographic
        and income characteristics.

        **2️⃣ Credit Product Targeting**  
        The **{highest_income_credit["Income_Category"]}**
        segment has the highest average credit limit at
        **${highest_income_credit["Average_Credit_Limit"]:,.0f}**.

        **3️⃣ Family-Based Offers**  
        Use dependent information to design
        relevant financial products.

        **4️⃣ Personalized Engagement**  
        Combine age, income and education insights
        to improve customer targeting.
        """
    )


# =====================================================
# CUSTOMER DATA TABLE
# =====================================================

st.divider()

st.markdown(
    """
        <div class="section-label">
        DEMOGRAPHIC RECORDS
        </div>

    ### 📋 Filtered Customer Data
    """,
    unsafe_allow_html=True
)


display_columns = [
    "Client_Num",
    "Customer_Age",
    "Gender",
    "Dependent_Count",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
    "Credit_Limit",
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

st.divider()


csv = (
    filtered_data[
        available_columns
    ]
    .to_csv(
        index=False
    )
    .encode(
        "utf-8"
    )
)


st.download_button(
    label="⬇️ Download Filtered Demographic Data",
    data=csv,
    file_name="filtered_demographic_data.csv",
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
        Geographic & Demographic Intelligence &nbsp;•&nbsp;
        Built with Streamlit
        </div>
    """,
    unsafe_allow_html=True
)