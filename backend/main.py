from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import remittance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nepal Remittance Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(remittance.router)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Nepal Remittance Tracker API is running"}