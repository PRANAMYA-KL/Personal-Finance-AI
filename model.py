import pandas as pd
import joblib


# Load trained ML objects
scaler = joblib.load("model/scaler.pkl")
kmeans = joblib.load("model/kmeans_model.pkl")


# Cluster names obtained from our analysis
cluster_names = {
    0: "High Income - Low Spending",
    1: "Lower Income - Higher Spending",
    2: "Moderate Income - Low Spending",
    3: "High Spending"
}


# Insights for each segment
cluster_insights = {
    "High Income - Low Spending":
        "You have a strong income level with relatively low spending. "
        "Your spending pattern indicates good financial control.",

    "Lower Income - Higher Spending":
        "Your expenses take a relatively larger share of your income. "
        "Consider monitoring discretionary spending.",

    "Moderate Income - Low Spending":
        "Your spending is relatively controlled compared with your income. "
        "Continue maintaining this spending pattern.",

    "High Spending":
        "Your expense level and expense ratio are relatively high. "
        "Review your major spending categories and look for opportunities "
        "to reduce unnecessary expenses."
}


def analyze_finances(
    total_income,
    total_expense,
    transaction_count,
    avg_expense
):

    # Calculate derived features
    savings = total_income - total_expense

    expense_ratio = total_expense / total_income

    # Create input in the SAME feature order used during training
    new_data = pd.DataFrame([{
        "total_income": total_income,
        "total_expense": total_expense,
        "transaction_count": transaction_count,
        "avg_expense": avg_expense,
        "expense_ratio": expense_ratio
    }])

    # Apply the same scaler used during training
    new_scaled = scaler.transform(new_data)

    # Predict cluster
    cluster = kmeans.predict(new_scaled)[0]

    # Convert cluster number to meaningful name
    segment = cluster_names[cluster]

    # Get personalized insight
    insight = cluster_insights[segment]

    # Return result
    return {
        "total_income": round(float(total_income), 2),
        "total_expense": round(float(total_expense), 2),
        "savings": round(float(savings), 2),
        "transaction_count": int(transaction_count),
        "avg_expense": round(float(avg_expense), 2),
        "expense_ratio": round(float(expense_ratio * 100), 2),
        "segment": segment,
        "insight": insight
    }