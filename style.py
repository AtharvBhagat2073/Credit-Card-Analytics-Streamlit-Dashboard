import streamlit as st


def apply_style():

    st.markdown(
        """
<style>

/* =====================================================
   GLOBAL APP
===================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(37, 99, 235, 0.12),
            transparent 25%
        ),

        radial-gradient(
            circle at 90% 20%,
            rgba(6, 182, 212, 0.08),
            transparent 25%
        ),

        #07111f;

    color: #F8FAFC;
}


/* =====================================================
   MAIN CONTAINER
===================================================== */

.main .block-container {

    padding-top: 2rem;

    padding-left: 3rem;

    padding-right: 3rem;

    padding-bottom: 3rem;

    max-width: 1500px;
}


/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #081426 0%,
            #0B1729 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.08);
}


/* =====================================================
   SIDEBAR TEXT
===================================================== */

section[data-testid="stSidebar"] * {

    color: #E2E8F0;
}


/* =====================================================
   HEADINGS
===================================================== */

h1 {

    font-size: 2.5rem !important;

    font-weight: 800 !important;

    letter-spacing: -1px;
}


h2 {

    font-size: 1.7rem !important;

    font-weight: 750 !important;
}


h3 {

    font-size: 1.25rem !important;
}


/* =====================================================
   KPI CARDS
===================================================== */

div[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            rgba(15, 31, 55, 0.96),
            rgba(10, 24, 43, 0.96)
        );

    border:
        1px solid rgba(59, 130, 246, 0.22);

    padding: 20px;

    border-radius: 18px;

    box-shadow:
        0 10px 35px rgba(0,0,0,0.25);

    transition:
        all 0.25s ease;
}


div[data-testid="stMetric"]:hover {

    transform:
        translateY(-4px);

    border-color:
        rgba(34, 211, 238, 0.60);

    box-shadow:
        0 15px 45px rgba(6,182,212,0.15);
}


div[data-testid="stMetricLabel"] {

    color: #94A3B8 !important;

    font-size: 0.78rem !important;

    font-weight: 700 !important;
}


div[data-testid="stMetricValue"] {

    color: #F8FAFC !important;

    font-weight: 800 !important;
}


/* =====================================================
   PLOTLY CHART CONTAINER
===================================================== */

div[data-testid="stPlotlyChart"] {

    background:
        rgba(10, 24, 43, 0.72);

    border:
        1px solid rgba(255,255,255,0.07);

    border-radius: 18px;

    padding: 8px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.18);
}


/* =====================================================
   DATAFRAME
===================================================== */

div[data-testid="stDataFrame"] {

    border-radius: 16px;

    overflow: hidden;

    border:
        1px solid rgba(255,255,255,0.08);
}


/* =====================================================
   SELECT BOX / MULTISELECT
===================================================== */

div[data-baseweb="select"] > div {

    background-color:
        #0D1B2E !important;

    border:
        1px solid rgba(255,255,255,0.10)
        !important;

    border-radius:
        10px !important;
}


/* =====================================================
   BRAND HEADER
===================================================== */

.brand-header {

    background:
        linear-gradient(
            135deg,
            #0F2A4A,
            #0A1B32
        );

    border:
        1px solid rgba(34,211,238,0.18);

    border-radius: 20px;

    padding: 24px 28px;

    margin-bottom: 25px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.25);
}


/* =====================================================
   BRAND TITLE
===================================================== */

.brand-title {

    font-size: 2rem;

    font-weight: 850;

    background:
        linear-gradient(
            90deg,
            #60A5FA,
            #22D3EE
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* =====================================================
   BRAND SUBTITLE
===================================================== */

.brand-subtitle {

    color: #94A3B8;

    font-size: 0.95rem;

    margin-top: 5px;
}


/* =====================================================
   STATUS BADGE
===================================================== */

.status-badge {

    display: inline-block;

    padding: 5px 12px;

    border-radius: 999px;

    background:
        rgba(34,211,238,0.10);

    border:
        1px solid rgba(34,211,238,0.30);

    color: #67E8F9;

    font-size: 0.75rem;

    font-weight: 700;

    letter-spacing: 0.5px;

    margin-bottom: 8px;
}


/* =====================================================
   SIDEBAR BRAND
===================================================== */

.sidebar-brand {

    text-align: center;

    padding:
        10px 5px 20px 5px;
}


.sidebar-icon {

    font-size: 42px;
}


.sidebar-title {

    font-size: 22px;

    font-weight: 800;

    color: #60A5FA !important;
}


.sidebar-subtitle {

    font-size: 11px;

    color: #64748B !important;

    margin-top: 4px;

    letter-spacing: 1px;
}


/* =====================================================
   INSIGHT CARD
===================================================== */

.insight-card {

    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.12),
            rgba(8,145,178,0.08)
        );

    border-left:
        4px solid #22D3EE;

    border-radius: 12px;

    padding: 18px 20px;

    margin:
        10px 0 25px 0;
}


.insight-title {

    color: #67E8F9;

    font-weight: 700;

    font-size: 1rem;
}


.insight-text {

    color: #CBD5E1;

    margin-top: 5px;

    font-size: 0.92rem;
}


/* =====================================================
   SECTION LABEL
===================================================== */

.section-label {

    color: #60A5FA;

    font-size: 0.78rem;

    font-weight: 800;

    letter-spacing: 1px;

    text-transform: uppercase;

    margin-bottom: 5px;
}


/* =====================================================
   DIVIDER
===================================================== */

hr {

    border: none;

    border-top:
        1px solid rgba(255,255,255,0.07);

    margin: 25px 0;
}


/* =====================================================
   FOOTER
===================================================== */

.footer {

    text-align: center;

    color: #64748B;

    font-size: 0.75rem;

    padding: 20px;
}

</style>
""",
        unsafe_allow_html=True
    )