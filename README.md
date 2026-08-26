# 💰 Personal Finance AI

An AI-powered personal finance analysis application that analyzes income,
expenses, savings, and spending behavior using data analysis and machine
learning.

The project uses K-Means clustering to segment users into different financial
behavior groups and provides personalized financial insights through a
Streamlit web application.

---

## 📌 Project Overview

Managing personal finances becomes easier when financial behavior can be
understood through data.

This project analyzes user transaction data and generates useful financial
metrics such as:

- Total Income
- Total Expenses
- Savings
- Savings Ratio
- Expense Ratio
- Transaction Count
- Average Expense
- Top Expense Category

Machine learning is then used to identify different financial user segments.

---

## 🎯 Objectives

- Analyze personal transaction data
- Clean and prepare financial data
- Perform exploratory data analysis (EDA)
- Engineer meaningful financial features
- Identify user spending patterns
- Segment users using K-Means clustering
- Generate personalized financial insights
- Build an interactive Streamlit application

---

## 📊 Key Features

### Financial Analysis

The application calculates:

- Total Income
- Total Expenses
- Savings
- Expense Ratio
- Transaction Count
- Average Expense

### User Segmentation

K-Means clustering is used to identify financial behavior patterns.

The current segments are:

| Segment | Description |
|---|---|
| High Income - Low Spending | Users with relatively high income and lower spending |
| Lower Income - Higher Spending | Users with lower income and comparatively higher spending |
| Moderate Income - Low Spending | Users with moderate income and controlled spending |
| High Spending | Users with relatively high expense levels |

### Personalized Insights

The application evaluates the user's financial metrics and provides an
interpretation of their spending behavior.

---

## 🤖 Machine Learning

### Algorithm

**K-Means Clustering**

The following user-level features are used for segmentation:

- `total_income`
- `total_expense`
- `transaction_count`
- `avg_expense`
- `expense_ratio`

The features are standardized before applying K-Means.

### Model Selection

The Elbow Method and Silhouette Score were used to evaluate different values
of K.

The analysis showed that K=2 produced the highest silhouette score, while
K=4 provided more detailed and interpretable financial segments.

Therefore, K=4 was selected for the final user segmentation because the goal
of the project is not only mathematical separation but also meaningful
financial interpretation.

---

## 📈 Exploratory Data Analysis

The project includes analysis of:

- Transaction amount distribution
- Transaction type distribution
- Transaction count by category
- Total transaction amount by category
- Total spending by expense category
- Income vs expense behavior
- Correlation between user-level financial features

### Important Observations

Food and rent are among the most frequent expense categories.

Income transactions are substantially larger than individual expense
transactions.

Users show different spending behaviors despite having similar income
levels, making clustering useful for identifying financial segments.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Joblib
- Streamlit
- Jupyter Notebook

---

## 📂 Project Structure

```text
Personal-Finance-AI/
│
├── app.py
├── model.py
├── README.md
│
├── model/
│   ├── kmeans_model.pkl
│   └── scaler.pkl
│
└── notebook/
    └── Project_HR_Clean.ipynb