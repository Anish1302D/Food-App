import { AlertTriangle, Info, Coffee, TrendingDown, CheckCircle } from 'lucide-react';

const statusConfig = {
  over: {
    icon: AlertTriangle,
    bg: 'bg-red-500/10',
    border: 'border-red-500/20',
    iconColor: 'text-red-400',
    textColor: 'text-red-300',
  },
  warning: {
    icon: AlertTriangle,
    bg: 'bg-amber-500/10',
    border: 'border-amber-500/20',
    iconColor: 'text-amber-400',
    textColor: 'text-amber-300',
  },
  skipped: {
    icon: Coffee,
    bg: 'bg-orange-500/10',
    border: 'border-orange-500/20',
    iconColor: 'text-orange-400',
    textColor: 'text-orange-300',
  },
  under: {
    icon: TrendingDown,
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/20',
    iconColor: 'text-blue-400',
    textColor: 'text-blue-300',
  },
  on_track: {
    icon: CheckCircle,
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/20',
    iconColor: 'text-emerald-400',
    textColor: 'text-emerald-300',
  },
};

export default function FeedbackBanner({ feedback, onLogSuggestion }) {
  if (!feedback) return null;

  const config = statusConfig[feedback.status] || statusConfig.on_track;
  const Icon = config.icon;

  return (
    <div className={`${config.bg} border ${config.border} rounded-2xl p-5 animate-slide-up`}>
      <div className="flex items-start gap-3">
        <div className={`mt-0.5 ${config.iconColor}`}>
          <Icon size={22} />
        </div>
        <div className="flex-1">
          <p className={`${config.textColor} font-medium mb-1`}>
            {feedback.emoji} {feedback.message}
          </p>

          {feedback.suggestion && (
            <div className="mt-3">
              <p className="text-gray-400 text-sm mb-2">{feedback.suggestion.text}</p>
              {feedback.suggestion.meal && (
                <div className="bg-white/5 rounded-xl p-3 flex items-center justify-between">
                  <div>
                    <p className="text-white font-medium text-sm">{feedback.suggestion.meal.name}</p>
                    <p className="text-gray-400 text-xs mt-0.5">{feedback.suggestion.meal.calories} cal</p>
                  </div>
                  {onLogSuggestion && (
                    <button
                      onClick={() => onLogSuggestion(feedback.suggestion.meal)}
                      className="text-xs px-3 py-1.5 bg-emerald-500/20 text-emerald-400 rounded-lg
                        border border-emerald-500/20 hover:bg-emerald-500/25 transition-colors"
                    >
                      Log It
                    </button>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
