import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from model import analyze_finances


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personal Finance AI",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# CSV PROCESSING FUNCTION
# ============================================================

def process_csv(df):

    required_columns = [
        "transaction_type",
        "amount"
    ]

    # Check required columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        return None, (
            f"Missing required columns: "
            f"{', '.join(missing_columns)}"
        )

    # Work on a copy
    df = df.copy()

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Clean transaction type
    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Remove invalid amounts
    df = df.dropna(subset=["amount"])

    # Remove invalid transaction types
    df = df[
        df["transaction_type"].isin(
            ["income", "expense"]
        )
    ]

    # Total income
    total_income = df.loc[
        df["transaction_type"] == "income",
        "amount"
    ].sum()

    # Total expense
    total_expense = df.loc[
        df["transaction_type"] == "expense",
        "amount"
    ].sum()

    # Number of transactions
    transaction_count = len(df)

    # Average expense
    expense_values = df.loc[
        df["transaction_type"] == "expense",
        "amount"
    ]

    if len(expense_values) > 0:
        avg_expense = expense_values.mean()
    else:
        avg_expense = 0

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "transaction_count": int(transaction_count),
        "avg_expense": float(avg_expense)
    }, None


# ============================================================
# DISPLAY RESULTS FUNCTION
# ============================================================

def display_results(result):

    st.success("✅ Financial analysis completed!")

    # --------------------------------------------------------
    # FINANCIAL SUMMARY
    # --------------------------------------------------------

    st.subheader("📊 Your Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💵 Total Income",
            f"₹{result['total_income']:,.0f}"
        )

    with col2:
        st.metric(
            "💸 Total Expense",
            f"₹{result['total_expense']:,.0f}"
        )

    with col3:
        st.metric(
            "💰 Savings",
            f"₹{result['savings']:,.0f}"
        )

    with col4:
        st.metric(
            "📈 Expense Ratio",
            f"{result['expense_ratio']:.2f}%"
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔢 Transactions",
            result["transaction_count"]
        )

    with col2:
        st.metric(
            "🧾 Average Expense",
            f"₹{result['avg_expense']:,.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    st.subheader("📈 Financial Overview")

    chart_col1, chart_col2 = st.columns(2)

    # Income / Expense / Savings
    with chart_col1:

        fig, ax = plt.subplots()

        labels = [
            "Income",
            "Expense",
            "Savings"
        ]

        values = [
            result["total_income"],
            result["total_expense"],
            result["savings"]
        ]

        ax.bar(
            labels,
            values
        )

        ax.set_ylabel("Amount (₹)")
        ax.set_title(
            "Income vs Expense vs Savings"
        )

        st.pyplot(fig)

        plt.close(fig)

    # Expense / Savings
    with chart_col2:

        fig, ax = plt.subplots()

        # result["expense_ratio"] is already percentage
        expense_value = max(
            0,
            min(
                100,
                float(result["expense_ratio"])
            )
        )

        savings_value = 100 - expense_value

        values = [
            expense_value,
            savings_value
        ]

        labels = [
            "Expense",
            "Savings"
        ]

        # Prevent zero-total error
        if sum(values) > 0:

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )

        ax.set_title(
            "Expense vs Savings"
        )

        st.pyplot(fig)

        plt.close(fig)

    st.divider()

    # --------------------------------------------------------
    # ML SEGMENT
    # --------------------------------------------------------

    st.subheader("🤖 Your Financial Segment")

    st.info(
        f"### {result['segment']}"
    )

    # --------------------------------------------------------
    # INSIGHT
    # --------------------------------------------------------

    st.subheader(
        "💡 Personalized Financial Insight"
    )

    st.write(
        result["insight"]
    )


# ============================================================
# TITLE
# ============================================================

st.title("💰 Personal Finance AI")

st.write(
    "Analyze your financial behavior and discover "
    "your personalized financial segment using "
    "Machine Learning."
)

st.divider()


# ============================================================
# INPUT TABS
# ============================================================

manual_tab, csv_tab = st.tabs(
    [
        "✍️ Manual Input",
        "📂 Upload CSV"
    ]
)


# ============================================================
# MANUAL INPUT
# ============================================================

with manual_tab:

    st.subheader(
        "📝 Enter Your Financial Details"
    )

    col1, col2 = st.columns(2)

    with col1:

        total_income = st.number_input(
            "💵 Total Income (₹)",
            min_value=1.0,
            value=60000.0,
            step=1000.0
        )

        total_expense = st.number_input(
            "💸 Total Expenses (₹)",
            min_value=0.0,
            value=12000.0,
            step=500.0
        )

    with col2:

        transaction_count = st.number_input(
            "🔢 Number of Transactions",
            min_value=1,
            value=45,
            step=1
        )

        avg_expense = st.number_input(
            "🧾 Average Expense per Transaction (₹)",
            min_value=0.0,
            value=800.0,
            step=50.0
        )

    st.write("")

    analyze_button = st.button(
        "🔍 Analyze My Finances",
        use_container_width=True
    )

    if analyze_button:

        # Validation
        if total_expense > total_income:

            st.error(
                "⚠️ Your expenses are higher than "
                "your income. Please check the values."
            )

        elif avg_expense > total_expense:

            st.warning(
                "⚠️ Average expense cannot be greater "
                "than total expenses."
            )

        else:

            result = analyze_finances(
                total_income,
                total_expense,
                transaction_count,
                avg_expense
            )

            display_results(result)


# ============================================================
# CSV UPLOAD
# ============================================================

with csv_tab:

    st.subheader(
        "📂 Upload Your Transaction Data"
    )

    st.write(
        "Upload a CSV containing your transaction history."
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            # Read CSV
            user_df = pd.read_csv(
                uploaded_file
            )

            st.success(
                "✅ File uploaded successfully!"
            )

            # ------------------------------------------------
            # PREVIEW
            # ------------------------------------------------

            st.subheader(
                "👀 Data Preview"
            )

            st.dataframe(
                user_df.head(10),
                use_container_width=True
            )

            # ------------------------------------------------
            # PROCESS DATA
            # ------------------------------------------------

            features, error = process_csv(
                user_df
            )

            if error:

                st.error(
                    f"❌ {error}"
                )

            else:

                st.subheader(
                    "📊 Calculated Financial Features"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "💵 Total Income",
                        f"₹{features['total_income']:,.0f}"
                    )

                with col2:

                    st.metric(
                        "💸 Total Expense",
                        f"₹{features['total_expense']:,.0f}"
                    )

                with col3:

                    st.metric(
                        "🔢 Transactions",
                        features["transaction_count"]
                    )

                with col4:

                    st.metric(
                        "🧾 Average Expense",
                        f"₹{features['avg_expense']:,.2f}"
                    )

                st.write("")

                # ------------------------------------------------
                # CSV VALIDATION
                # ------------------------------------------------

                if features["total_income"] <= 0:

                    st.error(
                        "❌ No valid income transactions "
                        "were found in the CSV."
                    )

                elif features["total_expense"] > features["total_income"]:

                    st.warning(
                        "⚠️ Your uploaded data shows "
                        "expenses higher than income."
                    )

                else:

                    analyze_csv_button = st.button(
                        "🤖 Analyze Uploaded Data",
                        use_container_width=True
                    )

                    if analyze_csv_button:

                        result = analyze_finances(
                            features["total_income"],
                            features["total_expense"],
                            features["transaction_count"],
                            features["avg_expense"]
                        )

                        display_results(result)

        except Exception as e:

            st.error(
                f"❌ Unable to process the CSV: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Personal Finance AI • Machine Learning Project"
)