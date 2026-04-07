const moods = [
  { value: 'energetic', emoji: '⚡', label: 'Energetic', color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
  { value: 'happy', emoji: '😊', label: 'Happy', color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
  { value: 'tired', emoji: '😴', label: 'Tired', color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/20' },
  { value: 'stressed', emoji: '😰', label: 'Stressed', color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/20' },
];

export default function MoodSelector({ value, onChange }) {
  return (
    <div className="flex gap-3">
      {moods.map((mood) => {
        const isActive = value === mood.value;
        return (
          <button
            key={mood.value}
            onClick={() => onChange(mood.value)}
            className={`flex-1 flex flex-col items-center gap-2 py-4 px-3 rounded-xl border transition-all duration-300
              ${isActive
                ? `${mood.bg} ${mood.border} ${mood.color} shadow-lg`
                : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
              }`}
          >
            <span className="text-2xl">{mood.emoji}</span>
            <span className="text-xs font-medium">{mood.label}</span>
          </button>
        );
      })}
    </div>
  );
}
