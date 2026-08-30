# 💳 Credit Pulse — Credit Card Analytics Dashboard

A professional, interactive **Credit Card Analytics Dashboard** built using **Python, Streamlit, Pandas, and Plotly**.

The project analyzes customer demographics, transaction behavior, credit utilization, and customer risk to provide meaningful business insights through an interactive multi-page dashboard.

---

## 📌 Project Overview

Credit Pulse is designed to help analyze and understand a credit card customer portfolio.

The dashboard transforms raw customer and transaction data into actionable insights related to:

- 👥 Customer demographics
- 💳 Credit card categories
- 💰 Transaction performance
- 📈 Credit utilization
- 💤 Customer inactivity
- ⚠️ Credit risk indicators
- 🎯 Executive-level business insights

The goal is to support better **data-driven decision-making**.

---

# 🚀 Dashboard Features

## 🏠 Executive Overview

The main dashboard provides a consolidated overview of the entire credit card portfolio.

Key insights include:

- Total customers
- Total transactions
- Total transaction value
- Average transaction amount
- Total credit limit
- Average credit utilization
- High-risk customer percentage
- Transaction trends
- Card category distribution
- Executive recommendations

---

## 👥 Customer Analysis

Analyze customer characteristics and portfolio behavior.

Features include:

- Customer demographics
- Age analysis
- Gender distribution
- Income categories
- Education levels
- Marital status
- Card categories
- Credit limit analysis

---

## 💰 Transaction Analysis

Explore customer transaction behavior and performance.

Features include:

- Transaction value
- Transaction volume
- Transaction types
- Transaction trends
- Monthly transaction analysis
- Customer transaction activity

---

## 🌍 Geographic & Demographic Analysis

Analyze different customer demographic segments.

Features include:

- Age distribution
- Gender distribution
- Education analysis
- Income analysis
- Marital status analysis
- Dependent analysis
- Credit behavior by demographic segment

---

## ⚠️ Credit Risk Analysis

Identify potential customer risk indicators.

The risk model considers:

- Credit utilization
- Customer inactivity
- Revolving balance
- Credit limit
- Customer contact frequency

Customers are categorized into:

- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data cleaning and analysis |
| Plotly | Interactive visualizations |
| NumPy | Numerical operations |

---

# 📂 Project Structure

```text
Credit Card Analytics Streamlit Dashboard/
│
├── app.py
├── utils.py
├── style.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── credit_card_customers.csv
│   └── credit_card_transactions.csv
│
└── pages/
    ├── Customer_Analysis.py
    ├── Transaction_Analysis.py
    ├── Geographic_Demographic_Analysis.py
    └── Credit_Risk_Analysis.py
```

---

# 📊 Dataset Description

## Customer Dataset

The customer dataset contains information such as:

- Client number
- Customer age
- Gender
- Dependent count
- Education level
- Marital status
- Income category
- Card category
- Credit limit
- Revolving balance
- Average utilization ratio
- Months inactive
- Customer contacts

---

## Transaction Dataset

The transaction dataset includes:

- Transaction ID
- Client number
- Transaction date
- Transaction type
- Transaction amount
- Transaction count

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

Move into the project directory:

```bash
cd "Credit Card Analytics Streamlit Dashboard"
```

---

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### Activate on Windows

```bash
venv\Scripts\activate
```

### Activate on Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the Dashboard

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📈 Key Business Insights

The dashboard can help identify:

### 💳 Customer Portfolio

Understand which card categories have the largest customer base.

### 💰 Transaction Behavior

Identify the transaction categories generating the highest value.

### ⚠️ Customer Risk

Detect customers with high:

- Credit utilization
- Inactivity
- Revolving balances

### 🎯 Customer Segmentation

Use demographic information to create targeted customer engagement strategies.

---

# 💡 Business Recommendations

Based on the analysis, potential business actions include:

1. **Monitor high-risk customers**  
   Prioritize customers with high utilization and inactivity.

2. **Improve customer engagement**  
   Re-engage inactive customers using personalized campaigns.

3. **Segment marketing campaigns**  
   Use demographic and income data for targeted offers.

4. **Optimize credit strategies**  
   Monitor utilization and revolving balances to improve portfolio health.

5. **Focus on valuable transactions**  
   Identify high-performing transaction categories and strengthen engagement.

---

# 🔮 Future Improvements

Potential improvements for the project include:

- Machine learning-based risk prediction
- Customer churn prediction
- Real-time data integration
- Advanced forecasting
- Automated report generation
- Role-based dashboard access
- Database integration
- Deployment on Streamlit Cloud


# 👨‍💻 Author

**Atharv Bhagat**

Data Analytics | Python | SQL | Power BI | Streamlit

---

## ⭐ If you like this project

Please consider giving the repository a **Star ⭐**.