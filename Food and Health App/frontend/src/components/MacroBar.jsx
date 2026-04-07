export default function MacroBar({ protein, carbs, fats, targetProtein, targetCarbs, targetFats }) {
  const macros = [
    {
      name: 'Protein',
      value: protein,
      target: targetProtein,
      color: 'bg-blue-500',
      bgColor: 'bg-blue-500/10',
      textColor: 'text-blue-400',
      unit: 'g',
    },
    {
      name: 'Carbs',
      value: carbs,
      target: targetCarbs,
      color: 'bg-amber-500',
      bgColor: 'bg-amber-500/10',
      textColor: 'text-amber-400',
      unit: 'g',
    },
    {
      name: 'Fats',
      value: fats,
      target: targetFats,
      color: 'bg-pink-500',
      bgColor: 'bg-pink-500/10',
      textColor: 'text-pink-400',
      unit: 'g',
    },
  ];

  return (
    <div className="space-y-4">
      {macros.map((macro) => {
        const pct = macro.target ? Math.min((macro.value / macro.target) * 100, 100) : 0;
        return (
          <div key={macro.name}>
            <div className="flex justify-between items-center mb-1.5">
              <span className={`text-sm font-medium ${macro.textColor}`}>{macro.name}</span>
              <span className="text-sm text-gray-400">
                <span className="text-white font-semibold">{Math.round(macro.value)}</span>
                <span className="mx-0.5">/</span>
                {Math.round(macro.target)}{macro.unit}
              </span>
            </div>
            <div className={`h-2.5 rounded-full ${macro.bgColor} overflow-hidden`}>
              <div
                className={`h-full rounded-full ${macro.color} transition-all duration-1000 ease-out`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
