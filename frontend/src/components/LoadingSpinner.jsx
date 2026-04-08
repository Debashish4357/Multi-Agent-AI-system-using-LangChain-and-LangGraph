import { useState, useEffect } from 'react';

// LoadingSpinner.jsx — enhanced with step-by-step progress simulation
export default function LoadingSpinner() {
  const steps = [
    { text: "Planner Agent finding destinations...", icon: "🗺️" },
    { text: "Budget Agent calculating costs...", icon: "💰" },
    { text: "Scheduler Agent creating itinerary...", icon: "📅" },
    { text: "Reviewer Agent adding travel tips...", icon: "✅" },
    { text: "Summary Agent finalizing trip overview...", icon: "📋" },
  ];

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // Cycle through steps roughly every 3.5 seconds
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 3500);

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="flex flex-col items-center justify-center py-16 gap-6">
      {/* Spinning element */}
      <div className="relative w-20 h-20">
        <div className="absolute inset-0 rounded-full border-4 border-slate-100 dark:border-slate-800"></div>
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-500 animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center text-3xl transition-all duration-500">
          {steps[currentStep].icon}
        </div>
      </div>
      
      <div className="text-center space-y-2">
        <p className="text-blue-600 dark:text-blue-400 font-semibold text-lg animate-pulse">
          {steps[currentStep].text}
        </p>
        <p className="text-gray-400 text-sm">Our 5 AI agents are collaborating on your perfect trip</p>
      </div>

      {/* Agent progress pills */}
      <div className="flex flex-wrap justify-center gap-2 mt-4 max-w-sm">
        {["🗺️ Planner", "💰 Budget", "📅 Scheduler", "✅ Reviewer", "📋 Summary"].map((agent, i) => {
          const isActive = i === currentStep;
          const isDone = i < currentStep;
          
          return (
            <span
              key={i}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-300 ${
                isActive 
                  ? "bg-blue-100 text-blue-700 border-blue-300 shadow-sm scale-105" 
                  : isDone
                    ? "bg-green-50 text-green-700 border-green-200"
                    : "bg-gray-50 text-gray-400 border-gray-200 opacity-60"
              }`}
            >
              {isDone ? "✓ " : ""}{agent}
            </span>
          );
        })}
      </div>
    </div>
  );
}
