import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { foodLogAPI, feedbackAPI, recommendAPI, profileAPI, healthScoreAPI } from '../api';
import CalorieRing from '../components/CalorieRing';
import MacroBar from '../components/MacroBar';
import FeedbackBanner from '../components/FeedbackBanner';
import MealCard from '../components/MealCard';
import HealthScoreCard from '../components/HealthScoreCard';
import {
  TrendingUp, Utensils, Sparkles, ArrowRight, Clock,
  Target, Flame, Activity,
} from 'lucide-react';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [todayLogs, setTodayLogs] = useState([]);
  const [quickMeal, setQuickMeal] = useState(null);
  const [profile, setProfile] = useState(null);
  const [healthScore, setHealthScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const prof = await profileAPI.get(1);
      setProfile(prof);

      const [sum, fb, logs, hs] = await Promise.all([
        foodLogAPI.getSummary(1),
        feedbackAPI.get(1),
        foodLogAPI.getToday(1),
        healthScoreAPI.get(1).catch(() => null),
      ]);

      setSummary(sum);
      setFeedback(fb);
      setTodayLogs(logs);
      setHealthScore(hs);
    } catch (err) {
      if (err.message.includes('Profile not found')) {
        setError('profile');
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleGetQuickMeal = async () => {
    try {
      const meal = await recommendAPI.getInstant(1);
      setQuickMeal(meal);
    } catch (err) {
      console.error('Failed to get quick meal:', err);
    }
  };

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
      loadData();
      setQuickMeal(null);
    } catch (err) {
      console.error('Failed to log meal:', err);
    }
  };

  // No profile yet
  if (error === 'profile') {
    return (
      <div className="page-container flex items-center justify-center min-h-[80vh]">
        <div className="glass-card p-10 text-center max-w-md animate-scale-in">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mx-auto mb-6">
            <Sparkles size={36} className="text-white" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-3">Welcome to SmartBite AI!</h2>
          <p className="text-gray-400 mb-6">
            Let's set up your profile to get personalized meal recommendations.
          </p>
          <button onClick={() => navigate('/profile')} className="btn-primary w-full flex items-center justify-center gap-2">
            Get Started <ArrowRight size={18} />
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="glass-card h-48 shimmer rounded-2xl" />
          ))}
        </div>
      </div>
    );
  }

  if (error && error !== 'profile') {
    return (
      <div className="page-container flex items-center justify-center min-h-[80vh]">
        <div className="glass-card p-8 text-center max-w-md">
          <p className="text-red-400 mb-4">⚠️ {error}</p>
          <button onClick={loadData} className="btn-primary">Retry</button>
        </div>
      </div>
    );
  }

  const macroTargets = summary ? {
    protein: summary.calorie_target * 0.3 / 4,
    carbs: summary.calorie_target * 0.4 / 4,
    fats: summary.calorie_target * 0.3 / 9,
  } : { protein: 150, carbs: 200, fats: 65 };

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good Morning' : hour < 17 ? 'Good Afternoon' : 'Good Evening';

  return (
    <div className="page-container bg-mesh">
      {/* Header */}
      <div className="mb-8">
        <h1 className="page-title">
          {greeting}, <span className="gradient-text">{profile?.name || 'User'}</span> 👋
        </h1>
        <p className="page-subtitle">Here's your nutrition overview for today</p>
      </div>

      {/* Quick Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="glass-card p-4 animate-slide-up" style={{ animationDelay: '0ms' }}>
          <div className="flex items-center gap-2 mb-2">
            <Flame size={16} className="text-emerald-400" />
            <span className="text-xs text-gray-400">Calories</span>
          </div>
          <p className="text-2xl font-bold text-white">{Math.round(summary?.total_calories || 0)}</p>
          <p className="text-xs text-gray-500">of {Math.round(summary?.calorie_target || 0)}</p>
        </div>
        <div className="glass-card p-4 animate-slide-up" style={{ animationDelay: '100ms' }}>
          <div className="flex items-center gap-2 mb-2">
            <Utensils size={16} className="text-amber-400" />
            <span className="text-xs text-gray-400">Meals Logged</span>
          </div>
          <p className="text-2xl font-bold text-white">{summary?.meals_count || 0}</p>
          <p className="text-xs text-gray-500">today</p>
        </div>
        <div className="glass-card p-4 animate-slide-up" style={{ animationDelay: '200ms' }}>
          <div className="flex items-center gap-2 mb-2">
            <Target size={16} className="text-blue-400" />
            <span className="text-xs text-gray-400">Goal</span>
          </div>
          <p className="text-lg font-bold text-white capitalize">{profile?.goal?.replace('_', ' ') || '-'}</p>
        </div>
        <div className="glass-card p-4 animate-slide-up" style={{ animationDelay: '300ms' }}>
          <div className="flex items-center gap-2 mb-2">
            <Activity size={16} className="text-purple-400" />
            <span className="text-xs text-gray-400">Remaining</span>
          </div>
          <p className="text-2xl font-bold text-white">{Math.round(summary?.remaining_calories || 0)}</p>
          <p className="text-xs text-gray-500">calories</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
        {/* Health Score */}
        <div className="animate-slide-up" style={{ animationDelay: '50ms' }}>
          <HealthScoreCard data={healthScore} />
        </div>

        {/* Calorie Ring */}
        <div className="glass-card p-6 flex flex-col items-center justify-center animate-slide-up" style={{ animationDelay: '100ms' }}>
          <h3 className="text-gray-400 text-sm font-medium mb-4">Daily Calories</h3>
          <CalorieRing
            consumed={summary?.total_calories || 0}
            target={summary?.calorie_target || 2000}
            size={200}
          />
          <div className="mt-4 text-center">
            <span className="text-sm text-gray-400">
              {Math.round(summary?.percentage_consumed || 0)}% consumed
            </span>
          </div>
        </div>

        {/* Macros */}
        <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '200ms' }}>
          <h3 className="text-gray-400 text-sm font-medium mb-5">Macronutrients</h3>
          <MacroBar
            protein={summary?.total_protein || 0}
            carbs={summary?.total_carbs || 0}
            fats={summary?.total_fats || 0}
            targetProtein={macroTargets.protein}
            targetCarbs={macroTargets.carbs}
            targetFats={macroTargets.fats}
          />
        </div>

        {/* Smart Feedback + Quick Action */}
        <div className="space-y-4 animate-slide-up" style={{ animationDelay: '300ms' }}>
          <FeedbackBanner feedback={feedback} onLogSuggestion={handleLogMeal} />

          {/* Quick Action */}
          <button
            onClick={handleGetQuickMeal}
            className="w-full glass-card-hover p-5 text-left group"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center
                group-hover:shadow-lg group-hover:shadow-emerald-500/25 transition-all">
                <Sparkles size={22} className="text-white" />
              </div>
              <div>
                <h3 className="text-white font-semibold">What Should I Eat Now?</h3>
                <p className="text-gray-400 text-sm">Get an instant AI suggestion</p>
              </div>
              <ArrowRight size={18} className="text-gray-500 ml-auto group-hover:text-emerald-400 transition-colors" />
            </div>
          </button>
        </div>
      </div>

      {/* Quick Meal Popup */}
      {quickMeal && (
        <div className="mb-8 animate-scale-in">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Sparkles size={18} className="text-emerald-400" />
            AI Suggests For You
          </h3>
          <div className="max-w-md">
            <MealCard meal={quickMeal} onLog={handleLogMeal} />
          </div>
        </div>
      )}

      {/* Today's Meals */}
      {todayLogs.length > 0 && (
        <div className="animate-fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Clock size={18} className="text-gray-400" />
              Today's Meals
            </h3>
            <button
              onClick={() => navigate('/food-log')}
              className="text-sm text-emerald-400 hover:text-emerald-300 transition-colors flex items-center gap-1"
            >
              View All <ArrowRight size={14} />
            </button>
          </div>
          <div className="space-y-3">
            {todayLogs.slice(0, 4).map((log) => (
              <div key={log.id} className="glass-card p-4 flex items-center justify-between">
                <div>
                  <p className="text-white font-medium">{log.meal_name}</p>
                  <p className="text-gray-500 text-xs mt-0.5 capitalize">{log.category}</p>
                </div>
                <div className="text-right">
                  <p className="text-emerald-400 font-semibold">{Math.round(log.calories)} cal</p>
                  <p className="text-gray-500 text-xs mt-0.5">
                    {new Date(log.logged_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
