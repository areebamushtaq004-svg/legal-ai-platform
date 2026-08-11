# Enterprise Legal Intelligence & Contract Reasoning Platform

**Case Study:** AI-234 — Ezitech Engineering Framework
**Team Size:** 2 AI Engineers
**Duration:** 4 Weeks

---

## 1. Project Overview

This project is an AI-powered Legal Intelligence Platform designed to help legal teams automatically analyze contracts, extract key clauses, detect risks, track obligations, check compliance, and answer natural-language questions about legal documents — all through a single web-based dashboard.

The platform addresses common enterprise legal challenges such as manual contract review, missed renewal deadlines, hidden legal risks, and slow legal research, by automating document intelligence using AI/NLP techniques.

---

## 2. Features Implemented

| Module | Description | Status |
|---|---|---|
| **Legal Document Intelligence** | Upload and extract text from PDF/DOCX contracts, NDAs, and agreements | ✅ Complete |
| **Clause Extraction Engine** | Automatically identifies Payment, Termination, Confidentiality, Liability, Force Majeure, Renewal, Governing Law, and Arbitration clauses | ✅ Complete |
| **Contract Risk Intelligence** | Flags high-risk and medium-risk clauses based on risky legal language | ✅ Complete |
| **Obligation Tracking Engine** | Extracts key dates and notice periods from contract text | ✅ Complete |
| **AI Legal Copilot** | Semantic Q&A system — ask natural-language questions about a contract and get the most relevant answer | ✅ Complete |
| **Legal Knowledge Graph** | Builds a graph of relationships between contracts and their clauses | ✅ Complete |
| **Compliance Intelligence** | Checks whether a contract contains all company-required clauses and generates a compliance score | ✅ Complete |
| **Alert Center** | Generates alerts for missing clauses, high-risk terms, and low compliance scores | ✅ Complete |
| **Executive Dashboard** | A web-based UI to upload contracts, view analysis, and interact with the AI Copilot | ✅ Complete |

---

## 3. Technical Architecture

### 3.1 Tech Stack

| Layer | Technology Used |
|---|---|
| Backend Framework | Python, FastAPI |
| Database | SQLite (lightweight relational database) |
| Document Parsing | pypdf, python-docx |
| AI / Semantic Search | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Knowledge Graph | NetworkX |
| Frontend | HTML, CSS, JavaScript (Dashboard) |
| Server | Uvicorn (ASGI server) |

> **Note on technology choices:** The case study's suggested stack references PostgreSQL, Neo4j, and Redis for a full enterprise deployment. For this 4-week prototype, we used SQLite (instead of PostgreSQL) and NetworkX (instead of Neo4j) because they require no separate server installation and are better suited to a small-scale demo. Both are conceptually equivalent — SQLite is a relational database like PostgreSQL, and NetworkX builds the same kind of graph structure as Neo4j. The architecture is modular, so migrating to PostgreSQL/Neo4j in a production environment would only require changes inside the database layer, not the rest of the application.

> **Note on AI approach:** The case study allows either "OpenAI or Open Source LLM." We chose an open-source, locally-run model (Sentence Transformers) instead of a paid API. This was a deliberate choice: legal documents are highly confidential, and enterprises generally prefer not to send sensitive contract data to third-party AI APIs. A local model keeps all data on-premise, requires no API key or ongoing cost, and still demonstrates real semantic search / RAG-style question answering.

### 3.2 Architecture Diagram (High-Level Flow)

```
┌─────────────────┐
│   Dashboard      │  (HTML/CSS/JS - runs in browser)
│  (Upload / Ask)  │
└────────┬─────────┘
         │  HTTP Requests
         ▼
┌─────────────────────────────────────────────┐
│              FastAPI Backend                  │
│  ┌──────────────────────────────────────┐   │
│  │  api/routes.py  (API endpoints)        │   │
│  └───────────────┬──────────────────────┘   │
│                   │                            │
│   ┌───────────────┼────────────────────┐      │
│   ▼               ▼                    ▼      │
│ core/           core/               core/      │
│ document_reader clause_extractor   risk_engine │
│                                                  │
│ core/           core/               core/       │
│ obligation_     rag_pipeline        compliance_ │
│ tracker         (AI Copilot)        engine      │
│                                                  │
│ graph/                                          │
│ knowledge_graph                                 │
│                                                  │
│ core/                                           │
│ alert_engine                                    │
└───────────────────┬─────────────────────────────┘
                     ▼
           ┌───────────────────┐
           │  database/db.py    │
           │  SQLite (legal_ai.db) │
           │  Tables: contracts, │
           │  clauses, risks,    │
           │  obligations        │
           └───────────────────┘
```

### 3.3 Project Folder Structure

```
legal-ai-platform/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── api/
│   │   └── routes.py            # All API endpoints
│   ├── core/
│   │   ├── document_reader.py   # PDF/DOCX text extraction
│   │   ├── clause_extractor.py  # Clause extraction engine
│   │   ├── risk_engine.py       # Risk detection
│   │   ├── obligation_tracker.py# Date/deadline extraction
│   │   ├── rag_pipeline.py      # AI Legal Copilot (semantic Q&A)
│   │   ├── compliance_engine.py # Compliance checking
│   │   └── alert_engine.py      # Alert generation
│   ├── graph/
│   │   └── knowledge_graph.py   # Knowledge graph builder
│   ├── database/
│   │   └── db.py                # Database connection & queries
│   ├── static/
│   │   └── dashboard.html       # Frontend dashboard
│   └── data/                    # Sample contracts for testing
├── legal_ai.db                  # SQLite database file
└── requirements.txt
```

---

## 4. Database Schema

| Table | Columns | Purpose |
|---|---|---|
| `contracts` | id, filename, full_text, upload_date | Stores uploaded contract text |
| `clauses` | id, contract_id, clause_type, clause_text | Stores extracted clauses per contract |
| `risks` | id, contract_id, risk_description, risk_level | Stores flagged risks per contract |
| `obligations` | id, contract_id, obligation_type, due_date | Stores extracted dates/deadlines |

---

## 5. How It Works — Example Flow

1. User uploads a contract (PDF/DOCX) via the Dashboard.
2. `document_reader.py` extracts raw text.
3. Text is saved to the database (`contracts` table).
4. `clause_extractor.py` scans the text and identifies clause types.
5. `risk_engine.py` flags any clauses containing risky legal language.
6. `obligation_tracker.py` extracts dates and notice periods.
7. `compliance_engine.py` compares found clauses against a required-clause checklist and computes a compliance score.
8. `alert_engine.py` generates alerts for missing clauses or high-risk terms.
9. The user can then query the contract via `/ask` — `rag_pipeline.py` uses sentence embeddings to find the most semantically relevant paragraph to answer the question.
10. `/contracts/{id}/graph` returns a Knowledge Graph showing the relationship between the contract and its clauses.
11. All of the above is displayed on the Dashboard.

---

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/upload` | Upload a contract and run full analysis |
| GET | `/contracts/{id}/clauses` | Get extracted clauses |
| GET | `/contracts/{id}/risks` | Get flagged risks |
| GET | `/contracts/{id}/obligations` | Get extracted obligations/dates |
| GET | `/contracts/{id}/compliance` | Get compliance score & missing clauses |
| GET | `/contracts/{id}/graph` | Get the knowledge graph (nodes & edges) |
| GET | `/contracts/{id}/alerts` | Get generated alerts |
| POST | `/ask` | Ask a natural-language question about a contract |

Full interactive API documentation is auto-generated by FastAPI and available at `/docs`.

---

## 7. Deployment Guide (How to Run Locally)

### Prerequisites
- Python 3.11+ installed
- VS Code (or any code editor)

### Steps

```bash
# 1. Navigate to the project folder
cd legal-ai-platform

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install fastapi uvicorn python-multipart pypdf python-docx
pip install langchain langchain-community sentence-transformers chromadb
pip install spacy networkx
python -m spacy download en_core_web_sm

# 4. Run the server
uvicorn app.main:app --reload

# 5. Open the dashboard in a browser
http://127.0.0.1:8000/dashboard/dashboard.html

# 6. (Optional) Open the API documentation
http://127.0.0.1:8000/docs
```

The database (`legal_ai.db`) and all required tables are created automatically the first time the server starts.

---

## 8. Evaluation Criteria Mapping

| Criteria | Weight | How This Project Addresses It |
|---|---|---|
| AI Architecture | 20% | Modular multi-component system: document intelligence, clause extraction, risk engine, RAG, knowledge graph, compliance engine, alert engine — each in its own module |
| Contract Intelligence | 20% | Clause Extraction Engine identifies 8 clause types automatically |
| Legal Reasoning | 20% | Risk Engine + Compliance Engine apply rule-based legal reasoning to flag risk and missing requirements |
| Knowledge Graph | 15% | NetworkX-based graph linking contracts to their clauses, exposed via API |
| Explainable AI | 10% | Every risk/compliance result includes a plain-language reason (which keyword/clause triggered it); AI Copilot returns a confidence score with every answer |
| Documentation | 10% | This README, architecture diagram, and deployment guide |
| Presentation | 5% | Live demo via the Dashboard |

---

## 9. Future Improvements

- Migrate database layer from SQLite to PostgreSQL for multi-user, production-scale deployment
- Migrate knowledge graph from NetworkX to Neo4j for large-scale graph querying
- Add authentication and role-based access control (RBAC)
- Add multi-language contract support
- Add a full audit logging system
- Integrate an optional paid LLM (e.g., OpenAI) as an alternative AI backend for higher-quality summarization

---

## 10. Authors

Developed as part of the Ezitech Engineering Framework (EEF) Industry Case Study AI-234.
