import re

def extract_obligations(text):
    """
    Text mein se dates aur obligation-related jumlay dhoondta hai.
    """
    obligations = []
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    # Date pattern: "January 1, 2026" ya "30 days" jaisi cheezein dhoondta hai
    date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
    days_pattern = r'\b\d+\s+days?\b'

    for para in paragraphs:
        dates_found = re.findall(date_pattern, para)
        days_found = re.findall(days_pattern, para)

        if dates_found:
            for date in dates_found:
                obligations.append({
                    "obligation_type": "Key Date",
                    "due_date": date
                })

        if days_found and ("notice" in para.lower() or "renew" in para.lower() or "terminate" in para.lower()):
            for day in days_found:
                obligations.append({
                    "obligation_type": "Notice Period",
                    "due_date": day
                })

    return obligations