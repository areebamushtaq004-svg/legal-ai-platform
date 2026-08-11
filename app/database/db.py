import sqlite3

DB_NAME = "legal_ai.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        full_text TEXT,
        upload_date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clauses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contract_id INTEGER,
        clause_type TEXT,
        clause_text TEXT,
        FOREIGN KEY (contract_id) REFERENCES contracts (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obligations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contract_id INTEGER,
        obligation_type TEXT,
        due_date TEXT,
        FOREIGN KEY (contract_id) REFERENCES contracts (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contract_id INTEGER,
        risk_description TEXT,
        risk_level TEXT,
        FOREIGN KEY (contract_id) REFERENCES contracts (id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")


def save_contract(filename, full_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contracts (filename, full_text) VALUES (?, ?)",
        (filename, full_text)
    )
    conn.commit()
    contract_id = cursor.lastrowid
    conn.close()
    return contract_id

def save_clauses(contract_id, clauses):
    conn = get_connection()
    cursor = conn.cursor()
    for clause in clauses:
        cursor.execute(
            "INSERT INTO clauses (contract_id, clause_type, clause_text) VALUES (?, ?, ?)",
            (contract_id, clause["clause_type"], clause["clause_text"])
        )
    conn.commit()
    conn.close()


def get_clauses_by_contract(contract_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT clause_type, clause_text FROM clauses WHERE contract_id = ?",
        (contract_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"clause_type": r[0], "clause_text": r[1]} for r in rows]

def save_risks(contract_id, risks):
    conn = get_connection()
    cursor = conn.cursor()
    for risk in risks:
        cursor.execute(
            "INSERT INTO risks (contract_id, risk_description, risk_level) VALUES (?, ?, ?)",
            (contract_id, risk["risk_description"], risk["risk_level"])
        )
    conn.commit()
    conn.close()


def save_obligations(contract_id, obligations):
    conn = get_connection()
    cursor = conn.cursor()
    for ob in obligations:
        cursor.execute(
            "INSERT INTO obligations (contract_id, obligation_type, due_date) VALUES (?, ?, ?)",
            (contract_id, ob["obligation_type"], ob["due_date"])
        )
    conn.commit()
    conn.close()


def get_risks_by_contract(contract_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT risk_description, risk_level FROM risks WHERE contract_id = ?",
        (contract_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"risk_description": r[0], "risk_level": r[1]} for r in rows]


def get_obligations_by_contract(contract_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT obligation_type, due_date FROM obligations WHERE contract_id = ?",
        (contract_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"obligation_type": r[0], "due_date": r[1]} for r in rows]