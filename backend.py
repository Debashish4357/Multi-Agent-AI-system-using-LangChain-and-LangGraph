"""
FastAPI Backend for Multi-Agent Travel Planner
================================================
Exposes a /plan-trip POST endpoint that runs the LangGraph
multi-agent pipeline and returns structured travel plan data.

Run with:
    uvicorn backend:app --reload --port 8000
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from multi_agent_system import build_graph, TravelState

# ─────────────────────────────────────────────────────────────────────────────
load_dotenv(override=True)

app = FastAPI(
    title="Multi-Agent Travel Planner API",
    description="LangChain + LangGraph powered travel planning backend",
    version="1.0.0",
)

# Allow requests from the React dev server (port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────────────────
# Request / Response Models
# ─────────────────────────────────────────────────────────────────────────────

class TripRequest(BaseModel):
    user_input: str  # e.g. "Plan a 3-day trip to Goa with low budget"


class TripResponse(BaseModel):
    places:   str
    budget:   str
    schedule: str
    review:   str
    summary:  str


# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "🌍 Travel Planner API is running. POST to /plan-trip to start."}


@app.post("/plan-trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    """
    Runs the 5-agent LangGraph pipeline and returns a structured travel plan.
    """
    if not request.user_input.strip():
        raise HTTPException(status_code=400, detail="user_input cannot be empty.")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured on the server."
        )

    initial_state: TravelState = {
        "user_input": request.user_input,
        "places":     "",
        "budget":     "",
        "schedule":   "",
        "final_plan": "",
        "summary":    "",
    }

    try:
        graph       = build_graph()
        final_state = graph.invoke(initial_state)
        
        # Ensure that no fields are entirely missing
        return TripResponse(
            places   = final_state.get("places",     "No places generated."),
            budget   = final_state.get("budget",     "No budget generated."),
            schedule = final_state.get("schedule",   "No schedule generated."),
            review   = final_state.get("final_plan", "No review generated."),
            summary  = final_state.get("summary",    "No summary generated."),
        )
    except Exception as e:
        # Logs the exact error on the backend console for debugging
        print(f"[ERROR] LangGraph Pipeline failed: {str(e)}")
        # Sends a safe 500 error back to the React UI without crashing the server thread
        raise HTTPException(status_code=500, detail=f"Agent pipeline failed during execution: {str(e)}")
