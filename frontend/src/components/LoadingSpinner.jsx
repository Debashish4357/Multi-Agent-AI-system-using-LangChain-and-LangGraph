// LoadingSpinner.jsx — animated travel-themed loading indicator
export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      {/* Spinning globe */}
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-blue-200"></div>
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-500 animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center text-2xl">✈️</div>
      </div>
      <div className="text-center">
        <p className="text-blue-600 font-semibold text-lg">Planning your trip...</p>
        <p className="text-gray-400 text-sm mt-1">Our 5 AI agents are collaborating</p>
      </div>
      {/* Agent progress pills */}
      <div className="flex flex-wrap justify-center gap-2 mt-2">
        {["🗺️ Planner", "💰 Budget", "📅 Scheduler", "✅ Reviewer", "📋 Summary"].map((agent, i) => (
          <span
            key={i}
            className="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-xs font-medium border border-blue-100 animate-pulse"
            style={{ animationDelay: `${i * 0.2}s` }}
          >
            {agent}
          </span>
        ))}
      </div>
    </div>
  );
}
