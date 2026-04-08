"""
Multi-Agent Travel Planner System
==================================
Built with LangChain + LangGraph

Agents:
  1. Planner Agent     – Suggests top tourist places
  2. Budget Agent      – Estimates trip cost breakdown
  3. Scheduler Agent   – Creates a day-wise itinerary
  4. Reviewer Agent    – Reviews and refines the final plan
  5. Summary Agent     – Produces a clean, concise trip summary

Workflow: user_input → Planner → Budget → Scheduler → Reviewer → Summary → Output
"""

import os
from typing import TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, END

# ─────────────────────────────────────────────────────────────────────────────
# 0.  Environment Setup
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()  # loads GOOGLE_API_KEY from .env (if present)


def get_llm() -> ChatGoogleGenerativeAI:
    """Return a configured Gemini LLM instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "\n[ERROR] GOOGLE_API_KEY is not set.\n"
            "  → Create a .env file in this directory with:\n"
            "      GOOGLE_API_KEY=your_key_here\n"
            "  → Or set it in PowerShell before running:\n"
            "      $env:GOOGLE_API_KEY='your_key_here'\n"
        )
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Shared State Definition (passed between every agent node)
# ─────────────────────────────────────────────────────────────────────────────
class TravelState(TypedDict):
    """Shared context that flows through the entire agent graph."""
    user_input: str    # Raw user request (destination, days, budget, preferences)
    places:     str    # Output of Planner Agent
    budget:     str    # Output of Budget Agent
    schedule:   str    # Output of Scheduler Agent
    final_plan: str    # Output of Reviewer Agent (improved plan + tips)
    summary:    str    # Output of Summary Agent (clean trip summary)


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Agent Node Functions
# ─────────────────────────────────────────────────────────────────────────────

def planner_agent(state: TravelState) -> TravelState:
    """
    Agent 1 – Travel Planner
    Role: Understands the user request and suggests 4–6 best places to visit.
    """
    print("\n🗺️  [Agent 1 / 5]  Planner Agent is thinking...", flush=True)

    planner_prompt = f"""
You are a professional travel planner.

User request:
{state['user_input']}

Your task:
- Understand the destination, number of days, and budget preference
- Suggest 4–6 best places to visit
- Keep it realistic and suitable for the trip duration
- Avoid overcrowding the plan

Output format:
Destination: ...
Trip Duration: ...

Places to Visit:
1. ...
2. ...
3. ...
4. ...
"""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=planner_prompt)])
    state["places"] = response.content.strip()
    return state


def budget_agent(state: TravelState) -> TravelState:
    """
    Agent 2 – Budget Estimator
    Role: Estimates the complete cost breakdown considering user's budget preference.
    """
    print("\n💰  [Agent 2 / 5]  Budget Agent is thinking...", flush=True)

    budget_prompt = f"""
You are a travel budget expert.

Trip details:
{state['places']}

User request:
{state['user_input']}

Your task:
- Estimate the total trip cost
- Consider:
  - Travel (local transport)
  - Accommodation
  - Food
  - Entry fees (if any)
- Adjust budget based on user's preference (low/medium/high if mentioned)

Output format:
Budget Breakdown:
- Travel: ₹...
- Stay: ₹...
- Food: ₹...
- Activities: ₹...

Total Estimated Budget: ₹...
"""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=budget_prompt)])
    state["budget"] = response.content.strip()
    return state


def scheduler_agent(state: TravelState) -> TravelState:
    """
    Agent 3 – Itinerary Scheduler
    Role: Creates a comfortable day-wise travel plan.
    """
    print("\n📅  [Agent 3 / 5]  Scheduler Agent is thinking...", flush=True)

    scheduler_prompt = f"""
You are a travel itinerary planner.

Places to visit:
{state['places']}

Your task:
- Create a day-wise plan
- Distribute places logically across days
- Avoid too much travel in one day
- Keep plan comfortable and practical

Output format:
Day 1:
- ...

Day 2:
- ...

Day 3:
- ...
"""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=scheduler_prompt)])
    state["schedule"] = response.content.strip()
    return state


def reviewer_agent(state: TravelState) -> TravelState:
    """
    Agent 4 – Expert Reviewer
    Role: Reviews the plan, improves it, and adds travel tips and precautions.
    """
    print("\n✅  [Agent 4 / 5]  Reviewer Agent is thinking...", flush=True)

    reviewer_prompt = f"""
You are an expert travel reviewer.

Travel plan:
{state['schedule']}

Budget:
{state['budget']}

Your task:
- Improve the itinerary if needed
- Ensure it is realistic and balanced
- Add useful travel tips
- Suggest best time to visit and precautions

Output format:
Final Improved Plan:
...

Travel Tips:
- ...
- ...
- ...
"""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=reviewer_prompt)])
    state["final_plan"] = response.content.strip()
    return state


def summary_agent(state: TravelState) -> TravelState:
    """
    Agent 5 – Trip Summarizer
    Role: Produces a clean, concise summary of the entire travel plan.
    """
    print("\n📋  [Agent 5 / 5]  Summary Agent is thinking...", flush=True)

    summary_prompt = f"""
You are a travel assistant.

Trip details:
Places: {state['places']}
Budget: {state['budget']}
Schedule: {state['schedule']}

Your task:
- Summarize the entire travel plan in a clean and short format

Output format:
Trip Summary:
- Destination:
- Duration:
- Key Places:
- Budget:
- Highlights:
"""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=summary_prompt)])
    state["summary"] = response.content.strip()
    return state


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Build the LangGraph Workflow
# ─────────────────────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    """
    Constructs the LangGraph with nodes and directed edges.

    Pipeline:
        START → planner → budget → scheduler → reviewer → summary → END
    """
    graph = StateGraph(TravelState)

    # Register all 5 agent nodes
    graph.add_node("planner",   planner_agent)
    graph.add_node("budget",    budget_agent)
    graph.add_node("scheduler", scheduler_agent)
    graph.add_node("reviewer",  reviewer_agent)
    graph.add_node("summary",   summary_agent)

    # Define directed edges (sequential pipeline)
    graph.set_entry_point("planner")
    graph.add_edge("planner",   "budget")
    graph.add_edge("budget",    "scheduler")
    graph.add_edge("scheduler", "reviewer")
    graph.add_edge("reviewer",  "summary")
    graph.add_edge("summary",   END)

    return graph.compile()


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Output Formatter
# ─────────────────────────────────────────────────────────────────────────────

def display_results(state: TravelState) -> None:
    """Pretty-print the outputs from all five agents."""
    divider = "=" * 65

    print(f"\n{divider}")
    print("         🌍  MULTI-AGENT TRAVEL PLANNER RESULTS")
    print(divider)

    print("\n📍  SUGGESTED PLACES  (Planner Agent)")
    print("-" * 65)
    print(state.get("places", "N/A"))

    print("\n💰  BUDGET BREAKDOWN  (Budget Agent)")
    print("-" * 65)
    print(state.get("budget", "N/A"))

    print("\n📅  DAY-WISE SCHEDULE  (Scheduler Agent)")
    print("-" * 65)
    print(state.get("schedule", "N/A"))

    print("\n✅  FINAL IMPROVED PLAN & TIPS  (Reviewer Agent)")
    print("-" * 65)
    print(state.get("final_plan", "N/A"))

    print("\n📋  TRIP SUMMARY  (Summary Agent)")
    print("-" * 65)
    print(state.get("summary", "N/A"))

    print(f"\n{divider}\n")


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Main Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """
    Entry point – collects user input, runs the multi-agent graph,
    and displays the complete travel plan.
    """
    print("=" * 65)
    print("   🌍  Multi-Agent AI Travel Planner  (LangChain + LangGraph)")
    print("=" * 65)
    print("\nThis system uses 5 AI agents to create your perfect trip:")
    print("  Agent 1 → Planner   : Finds the best places to visit")
    print("  Agent 2 → Budget    : Estimates your total trip cost")
    print("  Agent 3 → Scheduler : Builds your day-wise itinerary")
    print("  Agent 4 → Reviewer  : Refines the plan and adds tips")
    print("  Agent 5 → Summary   : Creates a clean trip summary")
    print("-" * 65)

    # ── Collect user input dynamically ──────────────────────────────────────
    print("\nPlease provide your trip details:")
    destination = input("  📍 Destination (e.g., Manali, Goa, Rajasthan): ").strip()
    days        = input("  📆 Number of days (e.g., 3, 5, 7): ").strip()
    budget      = input("  💰 Total budget in ₹ (e.g., 10000, 25000, 50000): ").strip()
    preferences = input("  🎯 Preferences (e.g., adventure, beaches, heritage) [optional]: ").strip()

    # ── Compose a natural-language user request ──────────────────────────────
    user_input = (
        f"I want to travel to {destination} for {days} days "
        f"with a total budget of ₹{budget}."
    )
    if preferences:
        user_input += f" My interests include: {preferences}."

    print(f"\n✈️  Your Request: {user_input}")
    print("\n⏳  Starting the multi-agent pipeline...\n")

    # ── Build and run the LangGraph ──────────────────────────────────────────
    initial_state: TravelState = {
        "user_input": user_input,
        "places":     "",
        "budget":     "",
        "schedule":   "",
        "final_plan": "",
        "summary":    "",
    }

    try:
        graph       = build_graph()
        final_state = graph.invoke(initial_state)
        display_results(final_state)
    except EnvironmentError as e:
        print(e)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred:\n  {e}\n")
        raise


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
