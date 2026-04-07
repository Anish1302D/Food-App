import { Sun, CloudSun, Moon, Coffee } from 'lucide-react';

const times = [
  { value: 'morning', label: 'Morning', icon: Sun, color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/20' },
  { value: 'afternoon', label: 'Afternoon', icon: CloudSun, color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
  { value: 'evening', label: 'Evening', icon: Moon, color: 'text-purple-400', bg: 'bg-purple-500/10', border: 'border-purple-500/20' },
];

export default function TimeSelector({ value, onChange }) {
  return (
    <div className="flex gap-3">
      {times.map((time) => {
        const isActive = value === time.value;
        const Icon = time.icon;
        return (
          <button
            key={time.value}
            onClick={() => onChange(time.value)}
            className={`flex-1 flex flex-col items-center gap-2 py-4 px-3 rounded-xl border transition-all duration-300
              ${isActive
                ? `${time.bg} ${time.border} ${time.color} shadow-lg`
                : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
              }`}
          >
            <Icon size={22} />
            <span className="text-xs font-medium">{time.label}</span>
          </button>
        );
      })}
    </div>
  );
}
