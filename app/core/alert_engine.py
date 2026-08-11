def generate_alerts(clauses, risks, compliance_result):
    """
    Existing data ko check karke alerts banata hai.
    """
    alerts = []

    # Compliance-based alerts
    if not compliance_result["is_compliant"]:
        for missing in compliance_result["missing_clauses"]:
            alerts.append({
                "alert_type": "Missing Clause",
                "severity": "High",
                "message": f"Required clause missing: {missing}"
            })

    # Risk-based alerts
    for risk in risks:
        if risk["risk_level"] == "High":
            alerts.append({
                "alert_type": "High Risk Clause",
                "severity": "High",
                "message": f"{risk['risk_description']}"
            })
        elif risk["risk_level"] == "Medium":
            alerts.append({
                "alert_type": "Medium Risk Clause",
                "severity": "Medium",
                "message": f"{risk['risk_description']}"
            })

    # Compliance score alert
    if compliance_result["compliance_score"] < 70:
        alerts.append({
            "alert_type": "Low Compliance Score",
            "severity": "High",
            "message": f"Compliance score is only {compliance_result['compliance_score']}%"
        })

    if not alerts:
        alerts.append({
            "alert_type": "All Clear",
            "severity": "Low",
            "message": "No issues detected. Contract looks compliant and low-risk."
        })

    return alerts