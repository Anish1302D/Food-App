import { useState } from 'react';
import { recommendAPI, foodLogAPI } from '../api';
import MealCard from '../components/MealCard';
import { Sparkles, Wand2, Loader2, RefreshCw, CheckCircle } from 'lucide-react';

export default function EatNow() {
  const [meal, setMeal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [logged, setLogged] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setLogged(false);
    try {
      const result = await recommendAPI.getInstant(1);
      setMeal(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogMeal = async (m) => {
    try {
      await foodLogAPI.log({
        user_id: 1,
        meal_name: m.name,
        calories: m.calories,
        protein: m.protein,
        carbs: m.carbs,
        fats: m.fats,
        category: m.category,
      });
      setLogged(true);
    } catch (err) {
      console.error('Failed to log meal:', err);
    }
  };

  return (
    <div className="page-container bg-mesh min-h-[80vh] flex flex-col items-center justify-center">
      <div className="max-w-lg w-full text-center">
        {/* Hero */}
        {!meal && !loading && (
          <div className="animate-fade-in">
            <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mx-auto mb-8
              animate-pulse-glow">
              <Sparkles size={44} className="text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              What Should I<br/>
              <span className="gradient-text">Eat Now?</span>
            </h1>
            <p className="text-gray-400 text-lg mb-10 max-w-sm mx-auto">
              Let our AI analyze your profile, the time of day, and your nutrition goals to suggest the perfect meal.
            </p>
            <button
              onClick={handleGenerate}
              className="btn-primary text-lg px-10 py-4 flex items-center gap-3 mx-auto animate-bounce-soft"
            >
              <Wand2 size={22} />
              Generate Suggestion
            </button>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="animate-fade-in">
            <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 flex items-center justify-center mx-auto mb-8">
              <Loader2 size={40} className="text-emerald-400 animate-spin" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-3">Analyzing Your Profile...</h2>
            <p className="text-gray-400">Finding the perfect meal for you right now</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="animate-fade-in">
            <div className="glass-card p-6 mb-6 bg-red-500/10 border-red-500/20">
              <p className="text-red-400">⚠️ {error}</p>
            </div>
            <button onClick={handleGenerate} className="btn-primary">Try Again</button>
          </div>
        )}

        {/* Result */}
        {meal && !loading && (
          <div className="animate-scale-in">
            <div className="flex items-center justify-center gap-2 mb-6">
              <Sparkles size={20} className="text-emerald-400" />
              <h2 className="text-xl font-semibold text-white">AI Recommends</h2>
            </div>

            <MealCard meal={meal} onLog={handleLogMeal} showLogButton={!logged} />

            {logged && (
              <div className="mt-4 flex items-center justify-center gap-2 text-emerald-400 animate-fade-in">
                <CheckCircle size={18} />
                <span className="font-medium">Meal logged successfully!</span>
              </div>
            )}

            <button
              onClick={handleGenerate}
              className="mt-6 btn-secondary flex items-center gap-2 mx-auto"
            >
              <RefreshCw size={16} />
              Try Another Suggestion
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
