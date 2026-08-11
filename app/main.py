from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import create_tables
from app.api.routes import router

app = FastAPI(title="Enterprise Legal Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_tables()

app.include_router(router)
app.mount("/dashboard", StaticFiles(directory="app/static", html=True), name="dashboard")