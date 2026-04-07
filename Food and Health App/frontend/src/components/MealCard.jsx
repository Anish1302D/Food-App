import { Flame, Drumstick, Wheat, Droplets, Plus } from 'lucide-react';

const categoryStyles = {
  breakfast: 'tag-breakfast',
  lunch: 'tag-lunch',
  dinner: 'tag-dinner',
  snack: 'tag-snack',
};

export default function MealCard({ meal, onLog, index = 0, showLogButton = true }) {
  const delay = index * 100;

  return (
    <div
      className="glass-card-hover p-5 animate-slide-up"
      style={{ animationDelay: `${delay}ms`, animationFillMode: 'both' }}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-white font-semibold text-lg leading-tight mb-1">{meal.name}</h3>
          <span className={categoryStyles[meal.category] || 'tag-snack'}>
            {meal.category}
          </span>
        </div>
        <div className="flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20 ml-3">
          <Flame size={14} className="text-emerald-400" />
          <span className="text-emerald-400 font-bold text-sm">{meal.calories}</span>
          <span className="text-emerald-400/60 text-xs">cal</span>
        </div>
      </div>

      {meal.description && (
        <p className="text-gray-400 text-sm mb-4 leading-relaxed">{meal.description}</p>
      )}

      {/* Macro badges */}
      <div className="flex gap-3 mb-4">
        <div className="flex items-center gap-1.5 text-xs">
          <Drumstick size={13} className="text-blue-400" />
          <span className="text-gray-300">
            <span className="text-blue-400 font-semibold">{meal.protein}</span>g protein
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <Wheat size={13} className="text-amber-400" />
          <span className="text-gray-300">
            <span className="text-amber-400 font-semibold">{meal.carbs}</span>g carbs
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <Droplets size={13} className="text-pink-400" />
          <span className="text-gray-300">
            <span className="text-pink-400 font-semibold">{meal.fats}</span>g fats
          </span>
        </div>
      </div>

      {/* Why Explanation */}
      {meal.why ? (
        <div className="bg-emerald-500/5 border border-emerald-500/10 rounded-lg p-3 mb-4">
          <div className="flex items-center gap-2 mb-2 opacity-80">
            <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-widest">Why this recommendation</span>
          </div>
          <ul className="space-y-1.5">
            {meal.why.split(' · ').map((reason, i) => (
              <li key={i} className="text-emerald-300/90 text-sm flex items-start gap-2">
                <span className="mt-0.5 text-emerald-500/50">•</span>
                <span className="leading-snug">{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      ) : meal.ai_note && (
        <div className="bg-emerald-500/5 border border-emerald-500/10 rounded-lg p-3 mb-4">
          <p className="text-emerald-300 text-sm leading-relaxed">🤖 {meal.ai_note}</p>
        </div>
      )}

      {/* Log button */}
      {showLogButton && onLog && (
        <button
          onClick={() => onLog(meal)}
          className="w-full flex items-center justify-center gap-2 py-2.5 bg-white/5 border border-white/10
            rounded-xl text-gray-300 text-sm font-medium transition-all duration-300
            hover:bg-emerald-500/10 hover:border-emerald-500/30 hover:text-emerald-400"
        >
          <Plus size={16} />
          Log This Meal
        </button>
      )}
    </div>
  );
}
