# Company policy: har contract mein ye clauses zaroor honi chahiye
REQUIRED_CLAUSES = [
    "Payment Clause",
    "Termination Clause",
    "Confidentiality Clause",
    "Governing Law"
]

def check_compliance(clauses):
    """
    Check karta hai ke required clauses mojood hain ya nahi.
    """
    found_clause_types = set(clause["clause_type"] for clause in clauses)
    missing_clauses = [c for c in REQUIRED_CLAUSES if c not in found_clause_types]

    is_compliant = len(missing_clauses) == 0

    compliance_score = round(
        ((len(REQUIRED_CLAUSES) - len(missing_clauses)) / len(REQUIRED_CLAUSES)) * 100, 2
    )

    return {
        "is_compliant": is_compliant,
        "compliance_score": compliance_score,
        "missing_clauses": missing_clauses,
        "total_required": len(REQUIRED_CLAUSES),
        "total_found": len(REQUIRED_CLAUSES) - len(missing_clauses)
    }