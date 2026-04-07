import { useEffect, useState, useRef } from 'react';

export default function CalorieRing({ consumed, target, size = 180, strokeWidth = 14 }) {
  const [progress, setProgress] = useState(0);
  const animRef = useRef(null);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const percentage = Math.min((consumed / target) * 100, 100);
  const remaining = Math.max(target - consumed, 0);
  const isOver = consumed > target;

  useEffect(() => {
    // Animate the progress
    const start = performance.now();
    const duration = 1200;
    const animate = (now) => {
      const elapsed = now - start;
      const t = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - t, 3);
      setProgress(eased * percentage);
      if (t < 1) {
        animRef.current = requestAnimationFrame(animate);
      }
    };
    animRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animRef.current);
  }, [consumed, target, percentage]);

  const offset = circumference - (progress / 100) * circumference;

  const getColor = () => {
    if (isOver) return { stroke: '#ef4444', glow: 'rgba(239, 68, 68, 0.3)' };
    if (percentage > 85) return { stroke: '#f59e0b', glow: 'rgba(245, 158, 11, 0.3)' };
    return { stroke: '#10b981', glow: 'rgba(16, 185, 129, 0.3)' };
  };

  const color = getColor();

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
        style={{ filter: `drop-shadow(0 0 10px ${color.glow})` }}
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color.stroke}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="ring-progress"
        />
      </svg>
      {/* Center text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-white">
          {Math.round(consumed)}
        </span>
        <span className="text-xs text-gray-400 mt-1">
          of {Math.round(target)} cal
        </span>
        {!isOver && (
          <span className="text-xs text-emerald-400 mt-1 font-medium">
            {Math.round(remaining)} left
          </span>
        )}
        {isOver && (
          <span className="text-xs text-red-400 mt-1 font-medium">
            {Math.round(consumed - target)} over
          </span>
        )}
      </div>
    </div>
  );
}
