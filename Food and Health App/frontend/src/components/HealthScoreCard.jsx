import { useState, useEffect, useRef } from 'react';
import { Heart, Flame, Clock, Salad } from 'lucide-react';

const SCORE_COLORS = {
  excellent: { ring: '#10b981', glow: 'rgba(16,185,129,0.3)', bg: 'from-emerald-500/20 to-teal-500/10' },
  good:      { ring: '#34d399', glow: 'rgba(52,211,153,0.25)', bg: 'from-emerald-500/15 to-cyan-500/10' },
  fair:      { ring: '#fbbf24', glow: 'rgba(251,191,36,0.25)', bg: 'from-amber-500/15 to-yellow-500/10' },
  needsWork: { ring: '#f97316', glow: 'rgba(249,115,22,0.25)', bg: 'from-orange-500/15 to-amber-500/10' },
  poor:      { ring: '#ef4444', glow: 'rgba(239,68,68,0.25)', bg: 'from-red-500/15 to-orange-500/10' },
};

function getColors(score) {
  if (score >= 85) return SCORE_COLORS.excellent;
  if (score >= 70) return SCORE_COLORS.good;
  if (score >= 50) return SCORE_COLORS.fair;
  if (score >= 30) return SCORE_COLORS.needsWork;
  return SCORE_COLORS.poor;
}

function getGradientId(score) {
  if (score >= 85) return 'scoreGradExcellent';
  if (score >= 70) return 'scoreGradGood';
  if (score >= 50) return 'scoreGradFair';
  if (score >= 30) return 'scoreGradNeedsWork';
  return 'scoreGradPoor';
}

// Animated number counter
function useCountUp(target, duration = 1200) {
  const [value, setValue] = useState(0);
  const rafRef = useRef(null);

  useEffect(() => {
    const start = performance.now();
    const from = 0;

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(Math.round(from + (target - from) * eased));
      if (progress < 1) {
        rafRef.current = requestAnimationFrame(tick);
      }
    }

    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [target, duration]);

  return value;
}

// Breakdown bar component
function BreakdownBar({ icon: Icon, label, score, max, note, delay }) {
  const pct = max > 0 ? (score / max) * 100 : 0;
  const barColor =
    pct >= 80 ? 'bg-emerald-500' :
    pct >= 60 ? 'bg-teal-400' :
    pct >= 40 ? 'bg-amber-400' :
    pct >= 20 ? 'bg-orange-400' :
    'bg-red-400';

  return (
    <div
      className="animate-slide-up"
      style={{ animationDelay: `${delay}ms`, animationFillMode: 'both' }}
    >
      <div className="flex items-center justify-between mb-1.5">
        <div className="flex items-center gap-2">
          <Icon size={13} className="text-gray-400" />
          <span className="text-xs font-medium text-gray-300">{label}</span>
        </div>
        <span className="text-xs font-semibold text-gray-300">
          {Math.round(score)}/{max}
        </span>
      </div>
      <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${barColor} health-bar-fill`}
          style={{ '--bar-width': `${pct}%` }}
        />
      </div>
      <p className="text-[10px] text-gray-500 mt-1 truncate">{note}</p>
    </div>
  );
}

export default function HealthScoreCard({ data }) {
  if (!data) return null;

  const { score, label, emoji, explanation, breakdown } = data;
  const colors = getColors(score);
  const displayScore = useCountUp(score);

  // SVG arc config
  const size = 140;
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const arcLength = circumference * 0.75; // 270° arc
  const offset = arcLength - (arcLength * score) / 100;
  const gradId = getGradientId(score);

  return (
    <div className="glass-card p-6 flex flex-col items-center animate-scale-in health-score-card">
      <h3 className="text-gray-400 text-sm font-medium mb-4 flex items-center gap-1.5">
        <Heart size={14} className="text-emerald-400" />
        Daily Health Score
      </h3>

      {/* Animated Gauge */}
      <div className="relative mb-3">
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          className="health-score-ring"
          style={{ filter: `drop-shadow(0 0 12px ${colors.glow})` }}
        >
          <defs>
            <linearGradient id="scoreGradExcellent" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>
            <linearGradient id="scoreGradGood" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#34d399" />
              <stop offset="100%" stopColor="#10b981" />
            </linearGradient>
            <linearGradient id="scoreGradFair" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#f59e0b" />
            </linearGradient>
            <linearGradient id="scoreGradNeedsWork" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#f97316" />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>
            <linearGradient id="scoreGradPoor" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ef4444" />
              <stop offset="100%" stopColor="#dc2626" />
            </linearGradient>
          </defs>

          {/* Background track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth={strokeWidth}
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeDashoffset={0}
            strokeLinecap="round"
            transform={`rotate(135, ${size / 2}, ${size / 2})`}
          />

          {/* Score arc */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={`url(#${gradId})`}
            strokeWidth={strokeWidth}
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeDashoffset={offset}
            strokeLinecap="round"
            transform={`rotate(135, ${size / 2}, ${size / 2})`}
            className="health-score-arc"
          />
        </svg>

        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="text-4xl font-extrabold text-white tabular-nums"
            style={{ textShadow: `0 0 20px ${colors.glow}` }}
          >
            {displayScore}
          </span>
          <span
            className="text-xs font-semibold mt-0.5 tracking-wide"
            style={{ color: colors.ring }}
          >
            {label} {emoji}
          </span>
        </div>
      </div>

      {/* Explanation */}
      <p className="text-xs text-gray-400 text-center mb-5 leading-relaxed px-2 max-w-[240px]">
        {explanation}
      </p>

      {/* Breakdown */}
      <div className="w-full space-y-3">
        <BreakdownBar
          icon={Flame}
          label="Calorie Balance"
          score={breakdown.calorie_balance.score}
          max={breakdown.calorie_balance.max}
          note={breakdown.calorie_balance.note}
          delay={200}
        />
        <BreakdownBar
          icon={Clock}
          label="Meal Timing"
          score={breakdown.meal_timing.score}
          max={breakdown.meal_timing.max}
          note={breakdown.meal_timing.note}
          delay={350}
        />
        <BreakdownBar
          icon={Salad}
          label="Food Quality"
          score={breakdown.food_quality.score}
          max={breakdown.food_quality.max}
          note={breakdown.food_quality.note}
          delay={500}
        />
      </div>
    </div>
  );
}
