import streamlit as st
import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

CUSTOMER_FILE = DATA_DIR / "credit_card_customers.csv"

TRANSACTION_FILE = DATA_DIR / "credit_card_transactions.csv"


# =========================================================
# LOAD CUSTOMER DATA
# =========================================================

@st.cache_data
def load_customer_data():

    df = pd.read_csv(CUSTOMER_FILE)

    # Convert important numeric columns safely
    numeric_columns = [
        "Customer_Age",
        "Dependent_Count",
        "Months_on_book",
        "Total_Relationship_Count",
        "Months_Inactive_12_mon",
        "Contacts_Count_12_mon",
        "Credit_Limit",
        "Avg_Open_To_Buy",
        "Total_Revolving_Bal",
        "Avg_Utilization_Ratio"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# =========================================================
# LOAD TRANSACTION DATA
# =========================================================

@st.cache_data
def load_transaction_data():

    df = pd.read_csv(TRANSACTION_FILE)

    # Convert transaction date
    if "Transaction_Date" in df.columns:

        df["Transaction_Date"] = pd.to_datetime(
            df["Transaction_Date"],
            errors="coerce"
        )

    # Convert important numeric columns
    numeric_columns = [
        "Total_Trans_Amt",
        "Total_Trans_Ct",
        "Total_Amt_Chng_Q4_Q1",
        "Total_Ct_Chng_Q4_Q1"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# =========================================================
# COMMON PLOTLY STYLE
# =========================================================

def chart_layout(fig, height=420):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#CBD5E1",
            family="Arial"
        ),

        title_font=dict(
            size=18,
            color="#F8FAFC"
        ),

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),

        hoverlabel=dict(
            bgcolor="#0F172A",
            font_color="#F8FAFC"
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.15)"
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.15)"
    )

    return fig


# =========================================================
# FORMAT CURRENCY
# =========================================================

def format_currency(value):

    if pd.isna(value):

        return "$0"

    return f"${value:,.0f}"


# =========================================================
# FORMAT NUMBER
# =========================================================

def format_number(value):

    if pd.isna(value):

        return "0"

    return f"{value:,.0f}"