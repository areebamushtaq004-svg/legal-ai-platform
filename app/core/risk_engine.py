# Keywords jo high-risk clauses ko identify karte hain
HIGH_RISK_KEYWORDS = [
    "unlimited liability", "sole discretion", "without notice",
    "penalty", "immediate termination", "non-negotiable",
    "waive", "indemnify", "exclusive", "irrevocable"
]

def assess_risk(clauses):
    """
    Har clause ko check karta hai ke usme koi risky keyword hai ya nahi.
    """
    risks = []

    for clause in clauses:
        text_lower = clause["clause_text"].lower()
        matched_keywords = [kw for kw in HIGH_RISK_KEYWORDS if kw in text_lower]

        if matched_keywords:
            risks.append({
                "clause_type": clause["clause_type"],
                "risk_description": f"Contains risky terms: {', '.join(matched_keywords)}",
                "risk_level": "High"
            })
        elif clause["clause_type"] in ["Liability Clause", "Termination Clause"]:
            # Ye clause types by default thodi zyada attention chahte hain
            risks.append({
                "clause_type": clause["clause_type"],
                "risk_description": "Standard risk clause - review recommended",
                "risk_level": "Medium"
            })

    return risks