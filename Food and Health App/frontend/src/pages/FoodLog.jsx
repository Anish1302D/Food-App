import { useState, useEffect } from 'react';
import { foodLogAPI } from '../api';
import {
  BookOpen, Plus, Trash2, Flame, Clock, X,
  Coffee, Sun, Moon, Cookie
} from 'lucide-react';

const categoryIcons = {
  breakfast: Coffee,
  lunch: Sun,
  dinner: Moon,
  snack: Cookie,
  other: Flame,
};

const categoryColors = {
  breakfast: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
  lunch: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  dinner: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
  snack: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  other: 'text-gray-400 bg-gray-500/10 border-gray-500/20',
};

export default function FoodLog() {
  const [logs, setLogs] = useState([]);
  const [summary, setSummary] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    meal_name: '',
    calories: '',
    protein: '',
    carbs: '',
    fats: '',
    category: 'lunch',
  });

  const loadData = async () => {
    try {
      setLoading(true);
      const [logsData, summaryData] = await Promise.all([
        foodLogAPI.getToday(1),
        foodLogAPI.getSummary(1),
      ]);
      setLogs(logsData);
      setSummary(summaryData);
    } catch (err) {
      console.error('Failed to load food logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await foodLogAPI.log({
        user_id: 1,
        meal_name: form.meal_name,
        calories: parseFloat(form.calories),
        protein: parseFloat(form.protein || 0),
        carbs: parseFloat(form.carbs || 0),
        fats: parseFloat(form.fats || 0),
        category: form.category,
      });
      setForm({ meal_name: '', calories: '', protein: '', carbs: '', fats: '', category: 'lunch' });
      setShowForm(false);
      loadData();
    } catch (err) {
      console.error('Failed to log meal:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (logId) => {
    try {
      await foodLogAPI.delete(logId);
      loadData();
    } catch (err) {
      console.error('Failed to delete log:', err);
    }
  };

  const update = (field, value) => setForm(prev => ({ ...prev, [field]: value }));

  return (
    <div className="page-container bg-mesh">
      <div className="flex items-center justify-between mb-2">
        <h1 className="page-title">
          Food <span className="gradient-text">Log</span>
        </h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center gap-2"
        >
          {showForm ? <X size={18} /> : <Plus size={18} />}
          {showForm ? 'Cancel' : 'Log Meal'}
        </button>
      </div>
      <p className="page-subtitle">Track everything you eat today</p>

      {/* Summary Bar */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8 animate-slide-up">
          <div className="glass-card p-4 text-center">
            <p className="text-xs text-gray-400 mb-1">Consumed</p>
            <p className="text-xl font-bold text-emerald-400">{Math.round(summary.total_calories)}</p>
            <p className="text-xs text-gray-500">cal</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-xs text-gray-400 mb-1">Target</p>
            <p className="text-xl font-bold text-white">{Math.round(summary.calorie_target)}</p>
            <p className="text-xs text-gray-500">cal</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-xs text-gray-400 mb-1">Protein</p>
            <p className="text-xl font-bold text-blue-400">{Math.round(summary.total_protein)}g</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-xs text-gray-400 mb-1">Carbs</p>
            <p className="text-xl font-bold text-amber-400">{Math.round(summary.total_carbs)}g</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-xs text-gray-400 mb-1">Fats</p>
            <p className="text-xl font-bold text-pink-400">{Math.round(summary.total_fats)}g</p>
          </div>
        </div>
      )}

      {/* Add Meal Form */}
      {showForm && (
        <div className="glass-card p-6 mb-8 animate-scale-in">
          <h3 className="text-white font-semibold mb-5 flex items-center gap-2">
            <Plus size={18} className="text-emerald-400" />
            Log a New Meal
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Meal Name</label>
              <input
                type="text"
                className="input-field"
                placeholder="e.g. Grilled Chicken Salad"
                required
                value={form.meal_name}
                onChange={(e) => update('meal_name', e.target.value)}
              />
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <label className="label">Calories *</label>
                <input
                  type="number"
                  className="input-field"
                  placeholder="350"
                  required
                  min="0"
                  value={form.calories}
                  onChange={(e) => update('calories', e.target.value)}
                />
              </div>
              <div>
                <label className="label">Protein (g)</label>
                <input
                  type="number"
                  className="input-field"
                  placeholder="25"
                  min="0"
                  value={form.protein}
                  onChange={(e) => update('protein', e.target.value)}
                />
              </div>
              <div>
                <label className="label">Carbs (g)</label>
                <input
                  type="number"
                  className="input-field"
                  placeholder="30"
                  min="0"
                  value={form.carbs}
                  onChange={(e) => update('carbs', e.target.value)}
                />
              </div>
              <div>
                <label className="label">Fats (g)</label>
                <input
                  type="number"
                  className="input-field"
                  placeholder="12"
                  min="0"
                  value={form.fats}
                  onChange={(e) => update('fats', e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="label">Category</label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {['breakfast', 'lunch', 'dinner', 'snack'].map((cat) => {
                  const isActive = form.category === cat;
                  const Icon = categoryIcons[cat];
                  return (
                    <button
                      key={cat}
                      type="button"
                      onClick={() => update('category', cat)}
                      className={`flex items-center justify-center gap-2 py-3 rounded-xl border transition-all capitalize
                        ${isActive
                          ? `${categoryColors[cat]}`
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
                        }`}
                    >
                      <Icon size={16} />
                      {cat}
                    </button>
                  );
                })}
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="btn-primary w-full flex items-center justify-center gap-2 py-3"
            >
              {submitting ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <><Plus size={18} /> Log Meal</>
              )}
            </button>
          </form>
        </div>
      )}

      {/* Logs List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="glass-card h-20 shimmer rounded-2xl" />
          ))}
        </div>
      ) : logs.length > 0 ? (
        <div className="space-y-3 animate-fade-in">
          {logs.map((log, i) => {
            const Icon = categoryIcons[log.category] || Flame;
            const colors = categoryColors[log.category] || categoryColors.other;
            return (
              <div
                key={log.id}
                className="glass-card p-4 flex items-center gap-4 animate-slide-up"
                style={{ animationDelay: `${i * 50}ms`, animationFillMode: 'both' }}
              >
                <div className={`w-11 h-11 rounded-xl border flex items-center justify-center flex-shrink-0 ${colors}`}>
                  <Icon size={18} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium truncate">{log.meal_name}</p>
                  <div className="flex items-center gap-3 mt-0.5">
                    <span className="text-xs text-gray-500 capitalize">{log.category}</span>
                    <span className="text-xs text-gray-600">•</span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock size={10} />
                      {new Date(log.logged_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-emerald-400 font-semibold">{Math.round(log.calories)} cal</p>
                    <p className="text-xs text-gray-500">
                      P:{Math.round(log.protein)} C:{Math.round(log.carbs)} F:{Math.round(log.fats)}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(log.id)}
                    className="p-2 rounded-lg text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-all"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="glass-card p-12 text-center animate-fade-in">
          <BookOpen size={48} className="text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">No meals logged yet</h3>
          <p className="text-gray-400 mb-6">Start tracking your nutrition by logging your first meal</p>
          <button onClick={() => setShowForm(true)} className="btn-primary">
            <Plus size={18} className="inline mr-2" />
            Log Your First Meal
          </button>
        </div>
      )}
    </div>
  );
}
