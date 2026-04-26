# 🌍 Multi-Agent AI Travel Planner
### Built with LangChain + LangGraph + React + FastAPI

A full-stack AI travel planning system that uses **5 collaborative AI agents** to generate a personalized travel plan from a single user prompt.

---

## 🏗️ Architecture

```
User Input → FastAPI → LangGraph Pipeline → React Frontend
                           ↓
              ┌────────────────────────┐
              │  Agent 1: Planner      │ → Suggests places
              │  Agent 2: Budget       │ → Estimates costs
              │  Agent 3: Scheduler    │ → Day-wise itinerary
              │  Agent 4: Reviewer     │ → Tips & improvements
              │  Agent 5: Summary      │ → Clean trip summary
              └────────────────────────┘
```

---

## 📁 Project Structure

```
├── multi_agent_system.py   # LangGraph multi-agent pipeline (CLI)
├── backend.py              # FastAPI server exposing /plan-trip
├── requirements.txt        # Python dependencies
├── .env.example            # API key template
└── frontend/               # React + Vite + Tailwind CSS UI
    └── src/
        ├── App.jsx
        └── components/
            ├── ResultCard.jsx
            └── LoadingSpinner.jsx
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Debashish4357/Multi-Agent-AI-system-using-LangChain-and-LangGraph.git
cd Multi-Agent-AI-system-using-LangChain-and-LangGraph
```

### 2. Set up Python environment
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file:
```env
Your Api key store here
```

### 4. Start the Backend
```bash
uvicorn backend:app --reload --port 8000
```

### 5. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

### 6. Open in Browser
- **Frontend UI** → http://localhost:5173
- **API Docs** → http://localhost:8000/docs

---

## 🤖 Run CLI Only (no frontend)
```bash
python multi_agent_system.py
```

---

## 🛠️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Agents    | LangChain + LangGraph             |
| LLM       | Google Gemini 1.5 Flash           |
| Backend   | FastAPI + Uvicorn                 |
| Frontend  | React + Vite + Tailwind CSS       |

---

## 📊 Agent Roles

| Agent     | Role                                      | Output Color |
|-----------|-------------------------------------------|--------------|
| Planner   | Suggests 4–6 tourist places               | 🔵 Blue      |
| Budget    | Estimates cost (travel/stay/food/activities) | 🟢 Green  |
| Scheduler | Creates a day-wise itinerary              | 🟣 Purple    |
| Reviewer  | Improves plan + adds travel tips          | 🟠 Orange    |
| Summary   | Clean, concise trip summary               | 🩵 Teal      |
