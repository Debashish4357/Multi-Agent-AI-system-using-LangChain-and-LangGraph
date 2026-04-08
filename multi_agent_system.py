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
import time
from typing import TypedDict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# ─────────────────────────────────────────────────────────────────────────────
# 0.  Environment Setup
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv(override=True)  # forces pulling from .env over terminal cache


def get_llm() -> ChatGroq:
    """Return a configured Groq LLM instance."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "\n[ERROR] GROQ_API_KEY is not set.\n"
            "  → Add it to your .env file:\n"
            "      GROQ_API_KEY=your_key_here\n"
        )
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.7,
    )


def invoke_with_retry(llm, messages, retries=3, wait=12):
    """Call the LLM with automatic retry on quota errors (429)."""
    for attempt in range(retries):
        try:
            return llm.invoke(messages)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < retries - 1:
                    print(f"  ⏳ Rate limit hit. Retrying in {wait}s... (attempt {attempt+1}/{retries})")
                    time.sleep(wait)
                else:
                    raise RuntimeError(
                        "Groq API rate limit exhausted or failed. Please check your token quota."
                    ) from e
            else:
                raise


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Shared State Definition (passed between every agent node)
# ─────────────────────────────────────────────────────────────────────────────
class TravelState(TypedDict):
    """Shared context that flows through the entire agent graph."""
    user_input: str    # Raw user request
    places:     str    # Output of Planner Agent
    budget:     str    # Output of Budget Agent
    schedule:   str    # Output of Scheduler Agent
    final_plan: str    # Output of Reviewer Agent
    summary:    str    # Output of Summary Agent


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Agent Node Functions
# ─────────────────────────────────────────────────────────────────────────────

def planner_agent(state: TravelState) -> TravelState:
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
    response = invoke_with_retry(llm, [HumanMessage(content=planner_prompt)])
    state["places"] = response.content.strip()
    return state


def budget_agent(state: TravelState) -> TravelState:
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
    response = invoke_with_retry(llm, [HumanMessage(content=budget_prompt)])
    state["budget"] = response.content.strip()
    return state


def scheduler_agent(state: TravelState) -> TravelState:
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
    response = invoke_with_retry(llm, [HumanMessage(content=scheduler_prompt)])
    state["schedule"] = response.content.strip()
    return state


def reviewer_agent(state: TravelState) -> TravelState:
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
    response = invoke_with_retry(llm, [HumanMessage(content=reviewer_prompt)])
    state["final_plan"] = response.content.strip()
    return state


def summary_agent(state: TravelState) -> TravelState:
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
    response = invoke_with_retry(llm, [HumanMessage(content=summary_prompt)])
    state["summary"] = response.content.strip()
    return state


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Build the LangGraph Workflow
# ─────────────────────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    """Constructs the LangGraph with nodes and directed edges."""
    graph = StateGraph(TravelState)

    graph.add_node("planner",   planner_agent)
    graph.add_node("budget",    budget_agent)
    graph.add_node("scheduler", scheduler_agent)
    graph.add_node("reviewer",  reviewer_agent)
    graph.add_node("summary",   summary_agent)

    graph.set_entry_point("planner")
    graph.add_edge("planner",   "budget")
    graph.add_edge("budget",    "scheduler")
    graph.add_edge("scheduler", "reviewer")
    graph.add_edge("reviewer",  "summary")
    graph.add_edge("summary",   END)

    return graph.compile()


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Main Entry Point (CLI Fallback)
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("🌍 Starting Multi-Agent Travel Planner Engine (OpenAI)")
    
    user_input = input("Describe your trip: ")
    initial_state = { "user_input": user_input, "places": "", "budget": "", "schedule": "", "final_plan": "", "summary": "" }

    try:
        graph = build_graph()
        final_state = graph.invoke(initial_state)
        print("\n\n--- COMPLETED ---\n")
        print(final_state["summary"])
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}\n")


if __name__ == "__main__":
    main()
