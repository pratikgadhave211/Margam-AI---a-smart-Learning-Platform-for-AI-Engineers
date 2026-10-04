import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import questions
from app.api.v1 import autocomplete

app = FastAPI(
    title="Margam AI Backend API",
    description="Backend API for Margam AI - Learning Platform for AI Engineers",
    version="1.0.0"
)

# Configure CORS to allow secure cookies across ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
app.include_router(autocomplete.router, prefix="/api/v1/autocomplete", tags=["Autocomplete"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Margam AI Backend is running."}

# To run the server: uvicorn app.main:app --reload --port 8000
