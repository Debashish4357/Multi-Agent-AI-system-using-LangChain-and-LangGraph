import React from 'react';

const schemes = {
  blue:   { bg: "bg-blue-50",   border: "border-blue-200",  header: "bg-blue-500",   badge: "bg-blue-100 text-blue-700"   },
  green:  { bg: "bg-green-50",  border: "border-green-200", header: "bg-green-500",  badge: "bg-green-100 text-green-700" },
  purple: { bg: "bg-purple-50", border: "border-purple-200",header: "bg-purple-500", badge: "bg-purple-100 text-purple-700"},
  orange: { bg: "bg-orange-50", border: "border-orange-200",header: "bg-orange-500", badge: "bg-orange-100 text-orange-700"},
  gray:   { bg: "bg-gray-50",   border: "border-gray-200",  header: "bg-gray-600",   badge: "bg-gray-200 text-gray-800"   },
};

// ResultCard.jsx — Displays a single agent output section
const ResultCard = ({ icon, title, content, colorScheme }) => {
  const s = schemes[colorScheme] || schemes.blue;

  // Format plain text: bold lines starting with "Day", "-", numbered lists
  const formatContent = (text) => {
    if (!text) return null;
    return text.split("\n").map((line, i) => {
      const trimmed = line.trim();
      if (!trimmed) return <div key={i} className="h-2" />;
      if (/^Day \d+/i.test(trimmed) || /^(Destination|Trip Duration|Final Improved Plan|Travel Tips|Trip Summary|Budget Breakdown|Estimated Budget|Improved Plan|Places to Visit):/i.test(trimmed)) {
        return <p key={i} className="font-bold text-gray-800 mt-3 mb-1">{trimmed}</p>;
      }
      if (/^\d+\./.test(trimmed) || trimmed.startsWith("-") || trimmed.startsWith("•")) {
        return <p key={i} className="ml-4 text-gray-700 text-sm leading-relaxed">{trimmed}</p>;
      }
      return <p key={i} className="text-gray-700 text-sm leading-relaxed">{trimmed}</p>;
    });
  };

  return (
    <div className={`rounded-2xl border ${s.border} ${s.bg} overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300`}>
      {/* Card header */}
      <div className={`${s.header} px-5 py-3 flex items-center gap-3`}>
        <span className="text-2xl">{icon}</span>
        <h2 className="text-white font-bold text-base tracking-wide">{title}</h2>
      </div>
      {/* Card body */}
      <div className="px-5 py-4 space-y-1">
        {formatContent(content)}
      </div>
    </div>
  );
};

// Memoize to prevent unnecessary re-renders when parent state changes (e.g. typing in the input box)
export default React.memo(ResultCard);
