from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.document_reader import extract_text
from app.core.clause_extractor import extract_clauses
from app.core.risk_engine import assess_risk
from app.core.obligation_tracker import extract_obligations
from app.database.db import (
    save_contract, save_clauses, get_clauses_by_contract,
    save_risks, save_obligations, get_risks_by_contract, get_obligations_by_contract
)
from app.core.rag_pipeline import answer_question
from app.graph.knowledge_graph import build_graph, graph_to_json
from app.core.compliance_engine import check_compliance
from app.core.alert_engine import generate_alerts

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Legal AI Platform Running"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(file.filename, content)

    contract_id = save_contract(file.filename, text)

    clauses = extract_clauses(text)
    save_clauses(contract_id, clauses)

    risks = assess_risk(clauses)
    save_risks(contract_id, risks)

    obligations = extract_obligations(text)
    save_obligations(contract_id, obligations)

    return {
        "contract_id": contract_id,
        "filename": file.filename,
        "clauses_found": len(clauses),
        "risks_found": len(risks),
        "obligations_found": len(obligations),
        "clauses": clauses,
        "risks": risks,
        "obligations": obligations
    }


@router.get("/contracts/{contract_id}/clauses")
def get_clauses(contract_id: int):
    clauses = get_clauses_by_contract(contract_id)
    if not clauses:
        raise HTTPException(status_code=404, detail="No clauses found for this contract")
    return {"contract_id": contract_id, "clauses": clauses}


@router.get("/contracts/{contract_id}/risks")
def get_risks(contract_id: int):
    risks = get_risks_by_contract(contract_id)
    return {"contract_id": contract_id, "risks": risks}


@router.get("/contracts/{contract_id}/obligations")
def get_obligations(contract_id: int):
    obligations = get_obligations_by_contract(contract_id)
    return {"contract_id": contract_id, "obligations": obligations}

from pydantic import BaseModel

class QuestionRequest(BaseModel):
    contract_id: int
    question: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    from app.database.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT full_text FROM contracts WHERE id = ?", (request.contract_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Contract not found")

    text = row[0]
    result = answer_question(text, request.question)

    return {
        "contract_id": request.contract_id,
        "question": request.question,
        "answer": result["answer"],
        "confidence": result["confidence"]
    }

@router.get("/contracts/{contract_id}/graph")
def get_contract_graph(contract_id: int):
    from app.database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM contracts WHERE id = ?", (contract_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Contract not found")

    filename = row[0]
    clauses = get_clauses_by_contract(contract_id)
    conn.close()

    G = build_graph(contract_id, filename, clauses)
    graph_data = graph_to_json(G)

    return graph_data

@router.get("/contracts/{contract_id}/compliance")
def get_compliance(contract_id: int):
    clauses = get_clauses_by_contract(contract_id)
    if not clauses:
        raise HTTPException(status_code=404, detail="No clauses found for this contract")

    result = check_compliance(clauses)
    return {"contract_id": contract_id, **result}

@router.get("/contracts/{contract_id}/alerts")
def get_alerts(contract_id: int):
    clauses = get_clauses_by_contract(contract_id)
    risks = get_risks_by_contract(contract_id)

    if not clauses:
        raise HTTPException(status_code=404, detail="No data found for this contract")

    compliance_result = check_compliance(clauses)
    alerts = generate_alerts(clauses, risks, compliance_result)

    return {"contract_id": contract_id, "alerts": alerts}