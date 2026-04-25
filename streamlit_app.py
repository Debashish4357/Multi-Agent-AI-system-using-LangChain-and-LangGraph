import streamlit as st
import os
from multi_agent_system import build_graph, TravelState
from dotenv import load_dotenv

# Load environment variables (e.g. GROQ_API_KEY)
load_dotenv(override=True)

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------------------------------------------------------
# Main UI Headers
# -----------------------------------------------------------------------------
st.title("✈️ AI Travel Planner")
st.markdown("""
**A Multi-Agent System powered by LangChain, LangGraph, and Groq.**

Describe your dream trip, and watch 5 specialized AI agents work together to research places, calculate budget, schedule days, and give final tips!
""")
st.divider()

# -----------------------------------------------------------------------------
# Input Section
# -----------------------------------------------------------------------------
user_input = st.text_area(
    "Describe your perfect trip:",
    placeholder="e.g., Plan a 4-day budget trip to Kerala. We love street food and beaches.",
    height=100
)

# Define optional example buttons
st.markdown("### Examples")
col1, col2, col3 = st.columns(3)
if col1.button("5-day Kyoto Trip"):
    st.session_state.example_input = "Plan a 5-day trip to Kyoto. I love street food, historic temples, and nature walks."
if col2.button("Weekend in Mumbai"):
    st.session_state.example_input = "Plan a weekend getaway to Mumbai. Interested in culture, art museums, and nightlife."
if col3.button("3-day Vietnam Budget"):
    st.session_state.example_input = "Plan a 3-day budget trip to Vietnam. We enjoy bustling cafes and local markets."

if "example_input" in st.session_state:
    st.info(f"**Click 'Plan My Trip' to use this example:** {st.session_state.example_input}")
    user_input = st.session_state.example_input

generate_btn = st.button("🚀 Plan My Trip", type="primary", use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# Processing Pipeline 
# -----------------------------------------------------------------------------
if generate_btn:
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your trip first.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("🔑 Error: GROQ_API_KEY is not set. Please add it to your environment variables or Streamlit secrets.")
    else:
        with st.spinner("🔄 Building agent graph & planning your trip... This may take a moment."):
            try:
                # 1. Build graph
                graph = build_graph()
                
                # 2. Define Initial State
                initial_state: TravelState = {
                    "user_input": user_input.strip(),
                    "places": "",
                    "budget": "",
                    "schedule": "",
                    "final_plan": "",
                    "summary": "",
                }
                
                # 3. Invoke Pipeline
                final_state = graph.invoke(initial_state)
                
                # 4. Extract data
                places = final_state.get("places", "No places generated.")
                budget = final_state.get("budget", "No budget generated.")
                schedule = final_state.get("schedule", "No itinerary generated.")
                review = final_state.get("final_plan", "No travel tips generated.")
                summary = final_state.get("summary", "No summary generated.")
                
                # -------------------------------------------------------------
                # Render Results Layout
                # -------------------------------------------------------------
                st.success("🎉 Trip planned successfully!")
                
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📍 Places", "💰 Budget", "🗓️ Itinerary", "✅ Tips", "📌 Summary"
                ])
                
                with tab1:
                    st.markdown("### Places to Visit")
                    st.markdown(places)
                with tab2:
                    st.markdown("### Budget Breakdown")
                    st.markdown(budget)
                with tab3:
                    st.markdown("### Day-wise Itinerary")
                    st.markdown(schedule)
                with tab4:
                    st.markdown("### Travel Tips & Precautions")
                    st.markdown(review)
                with tab5:
                    st.markdown("### Overall Summary")
                    st.markdown(summary)
                    
            except Exception as e:
                st.error(f"❌ **Agent pipeline failed:**\n\n```text\n{str(e)}\n```")
