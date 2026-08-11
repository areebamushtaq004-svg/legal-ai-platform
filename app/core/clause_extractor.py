import re

CLAUSE_KEYWORDS = {
    "Payment Clause": ["payment", "fee", "invoice", "pay "],
    "Termination Clause": ["termination", "terminate"],
    "Confidentiality Clause": ["confidential", "non-disclosure", "disclose"],
    "Liability Clause": ["liability", "liable", "damages"],
    "Force Majeure": ["force majeure", "act of god", "natural disaster"],
    "Renewal Terms": ["renewal", "renew", "extend"],
    "Governing Law": ["governing law", "jurisdiction", "laws of"],
    "Arbitration Clause": ["arbitration", "dispute resolution"]
}

def extract_clauses(text):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    found_clauses = []

    for para in paragraphs:
        para_lower = para.lower()
        for clause_type, keywords in CLAUSE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in para_lower:
                    found_clauses.append({
                        "clause_type": clause_type,
                        "clause_text": para
                    })
                    break

    return found_clauses