"""
SmartBite AI – FastAPI Main Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import profile, recommend, foodlog, feedback, healthscore

app = FastAPI(
    title="SmartBite AI",
    description="Personal Nutrition Coach – AI-powered meal recommendations",
    version="1.0.0",
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(profile.router)
app.include_router(recommend.router)
app.include_router(foodlog.router)
app.include_router(feedback.router)
app.include_router(healthscore.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "SmartBite AI API is running 🚀", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
