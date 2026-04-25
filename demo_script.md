# 🎬 Demo Video Script: Multi-Agent AI Travel Planner

**Estimated Video Length:** 4–6 minutes  
**Tone:** Professional, enthusiastic, and educational

---

## 🟢 Part 1: Introduction (0:00 - 0:45)
*(Visual: Show the main home screen of your web app or Gradio UI)*

**Speaker:**
"Hello everyone! Welcome to my demo of the **Multi-Agent AI Travel Planner**. 

Planning a trip can be overwhelming—you have to research places, calculate budgets, and figure out a day-by-day itinerary. To solve this, I built a full-stack, AI-powered web application that automates the entire process. 

Instead of relying on a single AI prompt, this application uses a **Multi-Agent System**. When you submit a travel request, a team of five specialized AI agents work together in a sequence to craft the perfect, customized travel plan for you. 

Let me show you how it works under the hood, and then we’ll jump into a live demo!"

---

## 🟢 Part 2: Tech Stack & Code Walkthrough (0:45 - 2:30)
*(Visual: Switch to your code editor, showing `multi_agent_system.py`)*

**Speaker:**
"First, let's talk about the tech stack. The brain of this application is built in **Python** using **LangChain** and **LangGraph**, and it connects to the incredibly fast **Groq API** running the Llama 3 model. For the interface, I have a React frontend communicating with a **FastAPI** Python backend.

The magic happens right here in `multi_agent_system.py` using **LangGraph**. LangGraph allows us to orchestrate AI workflows by treating each step as a 'Node' on a graph. 

I created a shared variable called `TravelState`. This state flows from one agent to the next, carrying all the accumulated data. 

Here are the 5 specialized agents and their roles:

1. **The Planner Agent:** This agent takes the user’s raw input and outputs the top 4 to 6 places to visit based on their specific vibe and duration.
2. **The Budget Estimator:** Once the places are locked in, this agent calculates a realistic breakdown of costs covering travel, stay, food, and activities.
3. **The Itinerary Builder:** It takes the places and the budget to intelligently structure a logical day-by-day schedule. 
4. **The Reviewer Agent:** This agent acts as a quality check. It reads the full plan, ensures practicality, and adds specific travel tips and safety precautions.
5. **The Summary Agent:** Finally, this agent reads the entire massive output and condenses it into a clean, structured trip summary.

At the bottom of the code, you can see where I wire up the LangGraph pipeline—linking Planner to Budget, Budget to Scheduler, and so on. It is a perfect, uninterrupted flow of data."

---

## 🟢 Part 3: Live Demo (2:30 - 4:00)
*(Visual: Switch back to your Web UI, start typing in the input box)*

**Speaker:**
"Alright, let's see these agents in action. 

I'm going to ask it to: *'Plan a 4-day family trip to Kerala. Kids love beaches and animals.'*

Watch what happens when I click **Plan My Trip**... 
*(Point out the UI loading state or backend terminal logs if visible)*

Behind the scenes, FastAPI triggers our LangGraph pipeline. Because we are using Groq for inference, the multi-agent communication happens blazingly fast.

*(When the results populate on screen)*
And here is our result! As you can see, the data is beautifully broken down into dedicated sections:
* The **Places** section gives us beach and animal spots perfect for kids.
* We have a complete **Budget Breakdown**.
* A highly detailed **Day-wise Itinerary**.
* Highly contextual **Travel Tips**, warning us about local weather or family safety.
* And an **Overall Summary**.

I also implemented a feature where users can click **Download My Plan** to instantly export this entire itinerary cleanly into a text file for offline use."

---

## 🟢 Part 4: Key Learnings & Outro (4:00 - End)
*(Visual: Show the GitHub repository or the final UI screen)*

**Speaker:**
"Building this Multi-Agent system taught me some incredibly valuable lessons:

1. **Agent Specialization is Powerful:** Breaking down one massive LLM prompt into 5 specialized agents resulted in much higher quality, less prone to hallucinations.
2. **State Management:** Learning LangGraph taught me how to securely pass JSON state between distinct LLM calls without losing context.
3. **Optimizing for Speed and Quotas:** During development, I learned how to handle API rate limits by adding a custom retry-wrapper, and I ultimately swapped the backend to use Groq for faster, cheaper inference!

The complete source code is available on my GitHub. Thank you so much for watching, and I hope this inspired you to build your own Multi-Agent AI systems!"
