import { useState, useEffect, useCallback } from 'react';
import { recommendAPI, foodLogAPI } from '../api';
import MealCard from '../components/MealCard';
import TimeSelector from '../components/TimeSelector';
import MoodSelector from '../components/MoodSelector';
import { Utensils, Search, Loader2, RefreshCw } from 'lucide-react';

export default function Recommendations() {
  const [timeOfDay, setTimeOfDay] = useState(() => {
    const h = new Date().getHours();
    if (h < 11) return 'morning';
    if (h < 16) return 'afternoon';
    return 'evening';
  });
  const [mood, setMood] = useState('energetic');
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searched, setSearched] = useState(false);

  const fetchRecommendations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const results = await recommendAPI.getMeals({
        user_id: 1,
        time_of_day: timeOfDay,
        mood: mood,
        count: 6,
      });
      setMeals(results);
      setSearched(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [timeOfDay, mood]);

  // Ensure recommendations change when inputs change
  useEffect(() => {
    if (searched) {
      fetchRecommendations();
    }
  }, [timeOfDay, mood, searched, fetchRecommendations]);

  const handleLogMeal = async (meal) => {
    try {
      await foodLogAPI.log({
        user_id: 1,
        meal_name: meal.name,
        calories: meal.calories,
        protein: meal.protein,
        carbs: meal.carbs,
        fats: meal.fats,
        category: meal.category,
      });
      // Visual feedback
      alert(`✅ "${meal.name}" logged successfully!`);
    } catch (err) {
      alert('Failed to log meal. ' + err.message);
    }
  };

  return (
    <div className="page-container bg-mesh">
      <h1 className="page-title">
        Meal <span className="gradient-text">Recommendations</span>
      </h1>
      <p className="page-subtitle">Get personalized meal suggestions based on your context</p>

      {/* Context Inputs */}
      <div className="glass-card p-6 mb-8 animate-slide-up">
        <div className="space-y-6">
          <div>
            <label className="label mb-3">⏰ Time of Day</label>
            <TimeSelector value={timeOfDay} onChange={setTimeOfDay} />
          </div>

          <div>
            <label className="label mb-3">😊 How are you feeling?</label>
            <MoodSelector value={mood} onChange={setMood} />
          </div>

          <button
            onClick={fetchRecommendations}
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center gap-2 py-4"
          >
            {loading ? (
              <Loader2 size={20} className="animate-spin" />
            ) : (
              <Search size={20} />
            )}
            {loading ? 'Finding perfect meals...' : 'Get Recommendations'}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="glass-card p-4 mb-6 bg-red-500/10 border-red-500/20">
          <p className="text-red-400">⚠️ {error}</p>
        </div>
      )}

      {/* Results */}
      {meals.length > 0 && (
        <div className="animate-fade-in">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-white flex items-center gap-2">
              <Utensils size={20} className="text-emerald-400" />
              Recommended For You
            </h2>
            <button
              onClick={fetchRecommendations}
              className="btn-secondary flex items-center gap-2 px-4 py-2 text-sm"
            >
              <RefreshCw size={14} />
              Refresh
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {meals.map((meal, i) => (
              <MealCard key={i} meal={meal} index={i} onLog={handleLogMeal} />
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {searched && meals.length === 0 && !loading && (
        <div className="glass-card p-10 text-center">
          <Utensils size={48} className="text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">No meals found</h3>
          <p className="text-gray-400">Try adjusting your filters</p>
        </div>
      )}

      {/* Initial state */}
      {!searched && !loading && (
        <div className="glass-card p-12 text-center animate-fade-in">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-6">
            <Utensils size={36} className="text-emerald-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">Ready to find your perfect meal?</h3>
          <p className="text-gray-400 max-w-md mx-auto">
            Select your time of day and current mood above, then hit "Get Recommendations" for personalized AI suggestions.
          </p>
        </div>
      )}
    </div>
  );
}
