import { useState } from "react";
import LoadingSpinner from "./components/LoadingSpinner";
import ResultCard from "./components/ResultCard";

const EXAMPLE_QUERIES = [
  "Plan a 3-day trip to Goa with a low budget",
  "Plan a 5-day trip to Manali with ₹25000 budget, I love adventure",
  "Plan a 4-day heritage trip to Rajasthan with medium budget",
];

export default function App() {
  const [userInput, setUserInput]   = useState("");
  const [loading, setLoading]       = useState(false);
  const [result, setResult]         = useState(null);
  const [error, setError]           = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/plan-trip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userInput.trim() }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Server error. Please try again.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Could not connect to the backend. Make sure it is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleExample = (query) => {
    setUserInput(query);
    setResult(null);
    setError("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 text-white font-sans">

      {/* ── Header ─────────────────────────────────────────────────── */}
      <header className="text-center pt-12 pb-6 px-4">
        <div className="inline-flex items-center gap-3 mb-3">
          <span className="text-4xl">🌍</span>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight bg-gradient-to-r from-blue-300 to-cyan-300 bg-clip-text text-transparent">
            AI Travel Planner
          </h1>
        </div>
        <p className="text-slate-400 text-sm sm:text-base max-w-xl mx-auto">
          Powered by 5 AI agents — LangChain &amp; LangGraph
        </p>

        {/* Agent badges */}
        <div className="flex flex-wrap justify-center gap-2 mt-4">
          {[
            { icon: "🗺️", label: "Planner",   color: "bg-blue-900/60 border-blue-700"   },
            { icon: "💰", label: "Budget",    color: "bg-green-900/60 border-green-700"  },
            { icon: "📅", label: "Scheduler", color: "bg-purple-900/60 border-purple-700"},
            { icon: "✅", label: "Reviewer",  color: "bg-orange-900/60 border-orange-700"},
            { icon: "📋", label: "Summary",   color: "bg-teal-900/60 border-teal-700"   },
          ].map((a) => (
            <span key={a.label} className={`px-3 py-1 rounded-full text-xs font-medium border ${a.color} text-slate-200`}>
              {a.icon} {a.label}
            </span>
          ))}
        </div>
      </header>

      {/* ── Main Content ────────────────────────────────────────────── */}
      <main className="max-w-3xl mx-auto px-4 pb-16">

        {/* Input Card */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 shadow-xl">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <label className="text-slate-300 font-medium text-sm">
              Describe your trip
            </label>
            <textarea
              className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none text-sm leading-relaxed"
              rows={3}
              placeholder='e.g. "Plan a 3-day trip to Goa with low budget and I love beaches"'
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              disabled={loading}
            />

            <button
              type="submit"
              disabled={loading || !userInput.trim()}
              className="w-full py-3 rounded-xl font-bold text-sm tracking-wide transition-all duration-200
                bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-400 hover:to-cyan-400
                disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-blue-500/30"
            >
              {loading ? "Planning..." : "✈️ Plan My Trip"}
            </button>
          </form>

          {/* Example queries */}
          <div className="mt-4">
            <p className="text-slate-400 text-xs mb-2">Try an example:</p>
            <div className="flex flex-col gap-2">
              {EXAMPLE_QUERIES.map((q, i) => (
                <button
                  key={i}
                  onClick={() => handleExample(q)}
                  disabled={loading}
                  className="text-left text-xs text-blue-300 hover:text-blue-200 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg px-3 py-2 transition-all duration-150 disabled:opacity-40"
                >
                  💡 {q}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="mt-8 bg-white rounded-2xl shadow-xl">
            <LoadingSpinner />
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 bg-red-50 border border-red-200 text-red-700 rounded-2xl px-5 py-4 text-sm">
            <p className="font-semibold mb-1">⚠️ Something went wrong</p>
            <p>{error}</p>
            <p className="mt-2 text-xs text-red-500">
              Make sure the backend is running: <code className="bg-red-100 px-1 rounded">uvicorn backend:app --reload</code>
            </p>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="mt-8 space-y-5">
            <h2 className="text-center text-slate-300 text-sm font-medium uppercase tracking-widest">
              Your Personalized Travel Plan
            </h2>

            <ResultCard
              icon="📍"
              title="Places to Visit"
              content={result.places}
              colorScheme="blue"
            />
            <ResultCard
              icon="💰"
              title="Budget Breakdown"
              content={result.budget}
              colorScheme="green"
            />
            <ResultCard
              icon="📅"
              title="Day-wise Itinerary"
              content={result.schedule}
              colorScheme="purple"
            />
            <ResultCard
              icon="✅"
              title="Travel Tips & Improved Plan"
              content={result.review}
              colorScheme="orange"
            />
            <ResultCard
              icon="📋"
              title="Trip Summary"
              content={result.summary}
              colorScheme="teal"
            />

            {/* Start Over */}
            <div className="text-center pt-2">
              <button
                onClick={() => { setResult(null); setUserInput(""); }}
                className="text-sm text-slate-400 hover:text-white underline underline-offset-2 transition-colors"
              >
                Plan another trip →
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
