import React, { useState, Suspense } from "react";
import LoadingSpinner from "./components/LoadingSpinner";

// Lazy load the ResultCard to optimize initial bundle size
const ResultCard = React.lazy(() => import("./components/ResultCard"));

const EXAMPLE_QUERIES = [
  "Plan a 4-day family trip to Kerala. Kids love beaches and animals.",
  "Plan a 5-day trip to Kyoto. I love street food, historic temples, and nature walks.",
  "Plan a weekend getaway to Mumbai. Interested in culture, art museums, and nightlife.",
  "Plan a 3-day budget trip to Vietnam. We enjoy bustling cafes and local markets."
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
      const response = await fetch("https://ai-travel-backend.onrender.com/plan-trip", {
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
      setError(
        err.message === "Failed to fetch"
          ? "Could not connect to the backend server. Please wait a moment and try again."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  };

  const handleExample = (query) => {
    setUserInput(query);
    setResult(null);
    setError("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDownload = () => {
    if (!result) return;
    
    const content = `
🌍 AI PERSONALIZED TRAVEL PLAN 🌍
=================================

📍 PLACES TO VISIT
---------------------------------
${result.places}

💰 BUDGET BREAKDOWN
---------------------------------
${result.budget}

📅 DAY-WISE ITINERARY
---------------------------------
${result.schedule}

✅ TRAVEL TIPS & PRECAUTIONS
---------------------------------
${result.review}

📋 TRIP SUMMARY
---------------------------------
${result.summary}
    `.trim();

    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "My_Travel_Plan.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 text-white font-sans selection:bg-blue-500/30">

      {/* ── Header ─────────────────────────────────────────────────── */}
      <header className="text-center pt-12 pb-10 px-4">
        <div className="inline-flex items-center gap-3 mb-3 hover:scale-105 transition-transform cursor-default">
          <span className="text-4xl">🌍</span>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight bg-gradient-to-r from-blue-300 to-cyan-300 bg-clip-text text-transparent">
            AI Travel Planner
          </h1>
        </div>
        <p className="text-slate-400 text-sm sm:text-base max-w-xl mx-auto">
          Built with LangChain & LangGraph
        </p>
      </header>

      {/* ── Main Layout (Grid) ──────────────────────────────────────── */}
      <main className="max-w-6xl mx-auto px-4 pb-20 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* LEFT COLUMN: Input & Results (Takes 8 columns) */}
        <div className="lg:col-span-8 flex flex-col gap-8">
          
          {/* Input Card */}
          <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 md:p-8 shadow-2xl transition-all duration-300 hover:border-white/20">
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
              <label className="text-slate-300 font-medium text-sm md:text-base flex items-center justify-between">
                <span>Describe your dream trip</span>
                {userInput.length > 0 && (
                  <span className="text-xs text-slate-400 font-normal">{userInput.length} chars</span>
                )}
              </label>
              <div className="relative">
                <textarea
                  className="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-400 resize-none text-sm leading-relaxed transition-all"
                  rows={3}
                  placeholder='e.g. "Plan a 3-day trip to Goa with low budget and I love beaches"'
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  disabled={loading}
                />
              </div>

              <button
                type="submit"
                disabled={loading || !userInput.trim()}
                className="w-full py-4 rounded-xl font-bold text-sm tracking-wide transition-all duration-300
                  bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500
                  disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-blue-500/25 flex justify-center items-center gap-2"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white placeholder" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Planning...
                  </>
                ) : (
                  <><span className="text-lg">✈️</span> Plan My Trip</>
                )}
              </button>
            </form>

            {/* Example queries */}
            <div className="mt-6 border-t border-white/5 pt-5">
              <p className="text-slate-400 text-xs mb-3 font-medium tracking-wide uppercase">Try an example</p>
              <div className="flex flex-wrap gap-2">
                {EXAMPLE_QUERIES.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => handleExample(q)}
                    disabled={loading}
                    className="text-left text-xs text-blue-200 hover:text-white bg-slate-800/40 hover:bg-slate-700/60 border border-slate-700/50 rounded-lg px-3 py-2 transition-all duration-200 disabled:opacity-40 flex items-center gap-2 max-w-full truncate"
                  >
                    <span className="opacity-70">💡</span>
                    <span className="truncate">{q}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-3xl shadow-2xl p-4 animate-in fade-in zoom-in duration-300">
              <LoadingSpinner />
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-rose-200 rounded-2xl px-6 py-5 text-sm shadow-lg backdrop-blur-sm animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">⚠️</span>
                <p className="font-bold text-base text-rose-300">Oops! Something went wrong</p>
              </div>
              <p className="ml-9 text-rose-100/80">{error}</p>
            </div>
          )}

          {/* Results */}
          {result && !loading && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-500">
              <div className="flex items-center justify-center gap-4 mb-6">
                <div className="h-px bg-gradient-to-r from-transparent via-slate-500 to-transparent flex-1"></div>
                <h2 className="text-center text-slate-300 text-xs font-bold uppercase tracking-[0.2em] whitespace-nowrap">
                  Your Personalized Travel Plan
                </h2>
                <div className="h-px bg-gradient-to-r from-transparent via-slate-500 to-transparent flex-1"></div>
              </div>

              <Suspense fallback={<div className="h-32 bg-slate-800/50 rounded-2xl animate-pulse"></div>}>
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
                  title="Travel Tips"
                  content={result.review}
                  colorScheme="orange"
                />
                <ResultCard
                  icon="📋"
                  title="Trip Summary"
                  content={result.summary}
                  colorScheme="gray"
                />
              </Suspense>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6 pb-2">
                <button
                  onClick={handleDownload}
                  className="inline-flex items-center gap-2 text-sm font-bold text-white bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-full transition-colors shadow-lg shadow-blue-500/20"
                >
                  <span className="text-lg">📥</span> Download My Plan
                </button>
                <button
                  onClick={() => {
                    setResult(null);
                    window.scrollTo({ top: 0, behavior: "smooth" });
                  }}
                  className="inline-flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white px-4 py-3 rounded-full hover:bg-slate-800 transition-colors"
                >
                  <span>↺</span> Plan another trip
                </button>
              </div>
            </div>
          )}

        </div>

        {/* RIGHT COLUMN: Sidebar (Takes 4 columns) */}
        <aside className="lg:col-span-4 space-y-6">
          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-700/50 rounded-2xl p-6 shadow-xl sticky top-6">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-2xl">🤖</span>
              <h2 className="text-lg font-bold text-slate-200">AI Agent System</h2>
            </div>
            
            <p className="text-sm text-slate-400 mb-6 leading-relaxed">
              When you submit a request, 5 specialized AI agents work together in a sequence to craft your perfect trip:
            </p>

            <div className="space-y-5">
              {/* Agent 1 */}
              <div className="flex gap-4 items-start group">
                <div className="w-10 h-10 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-lg shrink-0 group-hover:scale-110 transition-transform">
                  🗺️
                </div>
                <div>
                  <h3 className="text-blue-300 font-semibold mb-1 text-sm">Agent 1: Planner</h3>
                  <p className="text-xs text-slate-400 leading-snug">Extracts destination, dates, budget, and preferences to suggest the best places to visit.</p>
                </div>
              </div>

              {/* Agent 2 */}
              <div className="flex gap-4 items-start group">
                <div className="w-10 h-10 rounded-full bg-green-500/10 border border-green-500/20 flex items-center justify-center text-lg shrink-0 group-hover:scale-110 transition-transform">
                  💰
                </div>
                <div>
                  <h3 className="text-green-300 font-semibold mb-1 text-sm">Agent 2: Budget Estimator</h3>
                  <p className="text-xs text-slate-400 leading-snug">Provides a realistic cost breakdown spanning travel, stay, food, and activities.</p>
                </div>
              </div>

              {/* Agent 3 */}
              <div className="flex gap-4 items-start group">
                <div className="w-10 h-10 rounded-full bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-lg shrink-0 group-hover:scale-110 transition-transform">
                  📅
                </div>
                <div>
                  <h3 className="text-purple-300 font-semibold mb-1 text-sm">Agent 3: Itinerary Builder</h3>
                  <p className="text-xs text-slate-400 leading-snug">Creates a detailed and comfortable day-by-day travel plan based on the selected places.</p>
                </div>
              </div>

              {/* Agent 4 */}
              <div className="flex gap-4 items-start group">
                <div className="w-10 h-10 rounded-full bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-lg shrink-0 group-hover:scale-110 transition-transform">
                  ✅
                </div>
                <div>
                  <h3 className="text-orange-300 font-semibold mb-1 text-sm">Agent 4: Reviewer</h3>
                  <p className="text-xs text-slate-400 leading-snug">Reviews the full plan, ensures practicality, and adds helpful travel tips and precautions.</p>
                </div>
              </div>

              {/* Agent 5 */}
              <div className="flex gap-4 items-start group">
                <div className="w-10 h-10 rounded-full bg-slate-500/10 border border-slate-500/20 flex items-center justify-center text-lg shrink-0 group-hover:scale-110 transition-transform">
                  📋
                </div>
                <div>
                  <h3 className="text-slate-300 font-semibold mb-1 text-sm">Agent 5: Summary</h3>
                  <p className="text-xs text-slate-400 leading-snug">Generates a clean, concise, high-level overview of the entire customized trip.</p>
                </div>
              </div>
            </div>

          </div>
        </aside>

      </main>
    </div>
  );
}
