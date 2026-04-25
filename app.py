import gradio as gr
from multi_agent_system import build_graph, TravelState

# ─────────────────────────────────────────────────────────────────────────────
# Worker Function for the UI
# ─────────────────────────────────────────────────────────────────────────────
def plan_trip(user_input: str):
    """
    Invokes the LangGraph pipeline from the multi_agent_system.py file.
    Returns strings for 5 distinct output boxes.
    """
    if not user_input or not user_input.strip():
        return (
            "⚠️ Please enter a travel request.", 
            "", "", "", ""
        )

    # Compile the graph
    try:
        graph = build_graph()
    except Exception as e:
        return (f"❌ Failed to build agent graph: {str(e)}", "", "", "", "")

    # Define the initial state (matching backend.py structure)
    initial_state: TravelState = {
        "user_input": user_input.strip(),
        "places":     "",
        "budget":     "",
        "schedule":   "",
        "final_plan": "",
        "summary":    "",
    }

    # Execute the LangGraph workflow
    try:
        final_state = graph.invoke(initial_state)

        # Extract values
        places   = final_state.get("places", "No places generated.")
        budget   = final_state.get("budget", "No budget generated.")
        schedule = final_state.get("schedule", "No itinerary generated.")
        review   = final_state.get("final_plan", "No travel tips generated.")
        summary  = final_state.get("summary", "No summary generated.")

        return places, budget, schedule, review, summary

    except Exception as e:
        error_msg = f"❌ **Agent pipeline failed:**\n\n```text\n{str(e)}\n```"
        return (error_msg, "Error", "Error", "Error", "Error")


# ─────────────────────────────────────────────────────────────────────────────
# Gradio Interface Definition
# ─────────────────────────────────────────────────────────────────────────────
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate")) as demo:
    
    # Header Section
    gr.Markdown(
        """
        # ✈️ AI Travel Planner
        **A Multi-Agent System powered by LangChain, LangGraph, and Groq.**
        Describe your dream trip, and watch 5 specialized AI agents work together to research places, calculate budget, schedule days, and give final tips!
        """
    )
    
    # Input area
    with gr.Row():
        with gr.Column(scale=4):
            user_input = gr.Textbox(
                lines=2, 
                placeholder="e.g., Plan a 4-day budget trip to Kerala. We love street food and beaches.",
                label="Describe your perfect trip"
            )
        with gr.Column(scale=1, min_width=150):
            submit_btn = gr.Button("🚀 Plan My Trip", variant="primary", size="lg")

    # Example prompts
    gr.Examples(
        examples=[
            ["Plan a 5-day trip to Kyoto. I love street food, historic temples, and nature walks."],
            ["Plan a weekend getaway to Mumbai. Interested in culture, art museums, and nightlife."],
            ["Plan a 3-day budget trip to Vietnam. We enjoy bustling cafes and local markets."]
        ],
        inputs=user_input
    )

    gr.Markdown("---")
    
    # Results Section
    with gr.Row():
        with gr.Column():
            places_out = gr.Markdown(label="Output", value="### 📍 Places to Visit\n*(Waiting for input...)*")
            budget_out = gr.Markdown(label="Output", value="### 💰 Budget Breakdown\n*(Waiting for input...)*")
        with gr.Column():
            schedule_out = gr.Markdown(label="Output", value="### 🗓️ Day-wise Itinerary\n*(Waiting for input...)*")
            review_out   = gr.Markdown(label="Output", value="### ✅ Travel Tips & Precautions\n*(Waiting for input...)*")
    
    with gr.Row():
        summary_out = gr.Markdown(label="Output", value="### 📌 Overall Summary\n*(Waiting for input...)*")

    # Helper function to format the raw text with headers dynamically
    def format_outputs(p, b, s, r, sum_text):
        if p.startswith("❌") or p.startswith("⚠️"):
            return p, "", "", "", ""
        return (
            f"### 📍 Places to Visit\n{p}",
            f"### 💰 Budget Breakdown\n{b}",
            f"### 🗓️ Day-wise Itinerary\n{s}",
            f"### ✅ Travel Tips & Precautions\n{r}",
            f"### 📌 Overall Summary\n{sum_text}",
        )

    # Wire up the button click event (adds loading spinner automatically to outputs)
    submit_btn.click(
        fn=plan_trip,
        inputs=[user_input],
        outputs=[places_out, budget_out, schedule_out, review_out, summary_out]
    ).success(
        fn=format_outputs,
        inputs=[places_out, budget_out, schedule_out, review_out, summary_out],
        outputs=[places_out, budget_out, schedule_out, review_out, summary_out]
    )


# ─────────────────────────────────────────────────────────────────────────────
# Execution
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nStarting Gradio UI... Click the local link below when it's ready.\n")
    # share=True provides a public HuggingFace radio link. 
    # Use share=False if you are behind strict firewalls.
    demo.launch(share=True, debug=True)
