def normalize(value, max_value):
    return min(value / max_value, 1)

def calculate_health_score(row):
    """
    Aggregate dealer health score from dealership KPIs
    Output: 0–100
    """
    score = (
        0.35 * (row["target_achievement_pct"]) +
        0.25 * (row["sales_csi"]) +
        0.20 * (100 - row["aging_stock_pct"]) +
        0.10 * (100 - normalize(row["outstanding_overdue_days"], 90) * 100) +
        0.10 * (row["training_compliance_pct"])
    )
    return round(score, 2)

def calculate_risk_score(row):
    """
    Predict risk of underperformance/dealer churn
    Output: 0–1
    Higher = worse
    """
    score = (
        0.4 * (1 - row["target_achievement_pct"] / 100) +
        0.2 * normalize(row["aging_stock_pct"], 100) +
        0.15 * normalize(row["outstanding_overdue_days"], 90) +
        0.25 * (max(0, 80 - row["sales_csi"]) / 80)
    )
    return round(score, 3)

def generate_recommendation(row):
    """
    Simple decision engine based on AI scores.
    Replace with ML later.
    """
    if row["risk_score"] > 0.75 and row["aging_stock_pct"] > 40:
        return "Run stock liquidation + retail scheme"
    if row["risk_score"] > 0.75 and row["sales_csi"] < 65:
        return "Urgent: CSI improvement + staff training"
    if row["health_score"] > 75 and row["target_achievement_pct"] < 85:
        return "High potential: Increase model allocation"
    if row["health_score"] < 50:
        return "KAM intervention: Joint action plan"
    return "Maintain regular support"
