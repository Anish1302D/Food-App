import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { profileAPI } from '../api';
import {
  User, Scale, Ruler, Target, Leaf, Dumbbell, Shield,
  Save, ArrowRight, Zap, Activity, ChevronDown, TrendingDown,
} from 'lucide-react';

const goals = [
  { value: 'weight_loss', label: 'Weight Loss', icon: TrendingDown, desc: 'Burn fat & get lean', color: 'text-blue-400' },
  { value: 'muscle_gain', label: 'Muscle Gain', icon: Dumbbell, desc: 'Build strength & mass', color: 'text-amber-400' },
  { value: 'maintenance', label: 'Maintenance', icon: Shield, desc: 'Keep your current form', color: 'text-emerald-400' },
];

const diets = [
  { value: 'veg', label: 'Vegetarian', emoji: '🥬' },
  { value: 'vegan', label: 'Vegan', emoji: '🌱' },
  { value: 'non-veg', label: 'Non-Vegetarian', emoji: '🍗' },
  { value: 'keto', label: 'Keto', emoji: '🥑' },
];

const activityLevels = [
  { value: 'sedentary', label: 'Sedentary', desc: 'Little or no exercise' },
  { value: 'light', label: 'Lightly Active', desc: 'Light exercise 1-3 days/week' },
  { value: 'moderate', label: 'Moderately Active', desc: 'Moderate exercise 3-5 days/week' },
  { value: 'active', label: 'Very Active', desc: 'Hard exercise 6-7 days/week' },
  { value: 'very_active', label: 'Extremely Active', desc: 'Very hard exercise & physical job' },
];

export default function Profile() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [existing, setExisting] = useState(false);
  const [form, setForm] = useState({
    name: '',
    age: '',
    weight: '',
    height: '',
    gender: 'male',
    goal: 'maintenance',
    dietary: 'veg',
    activity_level: 'moderate',
  });

  useEffect(() => {
    profileAPI.get(1).then(p => {
      if (p) {
        setForm({
          name: p.name || '',
          age: String(p.age),
          weight: String(p.weight),
          height: String(p.height),
          gender: p.gender,
          goal: p.goal,
          dietary: p.dietary,
          activity_level: p.activity_level,
        });
        setExisting(true);
      }
    }).catch(() => {});
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await profileAPI.create({
        name: form.name || 'User',
        age: parseInt(form.age),
        weight: parseFloat(form.weight),
        height: parseFloat(form.height),
        gender: form.gender,
        goal: form.goal,
        dietary: form.dietary,
        activity_level: form.activity_level,
      });
      setSaved(true);
      setTimeout(() => {
        navigate('/');
      }, 1500);
    } catch (err) {
      console.error('Failed to save profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const update = (field, value) => setForm(prev => ({ ...prev, [field]: value }));

  return (
    <div className="page-container bg-mesh">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mx-auto mb-4">
            <User size={28} className="text-white" />
          </div>
          <h1 className="page-title text-center">{existing ? 'Update' : 'Set Up'} Your Profile</h1>
          <p className="page-subtitle text-center">Tell us about yourself for personalized recommendations</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Name */}
          <div className="glass-card p-6 animate-slide-up">
            <label className="label flex items-center gap-2">
              <User size={16} className="text-emerald-400" /> Your Name
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="Enter your name"
              value={form.name}
              onChange={(e) => update('name', e.target.value)}
            />
          </div>

          {/* Body Stats */}
          <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '100ms' }}>
            <h3 className="text-white font-semibold mb-5 flex items-center gap-2">
              <Activity size={18} className="text-emerald-400" /> Body Stats
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="label flex items-center gap-2">
                  <span className="text-lg">🎂</span> Age
                </label>
                <input
                  type="number"
                  className="input-field"
                  placeholder="25"
                  min="10"
                  max="120"
                  required
                  value={form.age}
                  onChange={(e) => update('age', e.target.value)}
                />
              </div>
              <div>
                <label className="label flex items-center gap-2">
                  <Scale size={16} className="text-blue-400" /> Weight (kg)
                </label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  placeholder="70"
                  min="20"
                  max="300"
                  required
                  value={form.weight}
                  onChange={(e) => update('weight', e.target.value)}
                />
              </div>
              <div>
                <label className="label flex items-center gap-2">
                  <Ruler size={16} className="text-purple-400" /> Height (cm)
                </label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  placeholder="175"
                  min="100"
                  max="250"
                  required
                  value={form.height}
                  onChange={(e) => update('height', e.target.value)}
                />
              </div>
              <div>
                <label className="label">Gender</label>
                <select
                  className="select-field"
                  value={form.gender}
                  onChange={(e) => update('gender', e.target.value)}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>
            </div>
          </div>

          {/* Goal Selection */}
          <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '200ms' }}>
            <h3 className="text-white font-semibold mb-5 flex items-center gap-2">
              <Target size={18} className="text-emerald-400" /> Your Goal
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {goals.map((g) => {
                const isActive = form.goal === g.value;
                const Icon = g.icon;
                return (
                  <button
                    key={g.value}
                    type="button"
                    onClick={() => update('goal', g.value)}
                    className={`p-5 rounded-xl border text-left transition-all duration-300
                      ${isActive
                        ? 'bg-emerald-500/10 border-emerald-500/30 shadow-lg shadow-emerald-500/5'
                        : 'bg-white/5 border-white/10 hover:bg-white/10'
                      }`}
                  >
                    <Icon size={24} className={isActive ? 'text-emerald-400' : 'text-gray-500'} />
                    <h4 className={`font-semibold mt-3 ${isActive ? 'text-white' : 'text-gray-300'}`}>
                      {g.label}
                    </h4>
                    <p className="text-xs text-gray-500 mt-1">{g.desc}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Dietary Preference */}
          <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '300ms' }}>
            <h3 className="text-white font-semibold mb-5 flex items-center gap-2">
              <Leaf size={18} className="text-emerald-400" /> Dietary Preference
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {diets.map((d) => {
                const isActive = form.dietary === d.value;
                return (
                  <button
                    key={d.value}
                    type="button"
                    onClick={() => update('dietary', d.value)}
                    className={`p-4 rounded-xl border text-center transition-all duration-300
                      ${isActive
                        ? 'bg-emerald-500/10 border-emerald-500/30 shadow-lg'
                        : 'bg-white/5 border-white/10 hover:bg-white/10'
                      }`}
                  >
                    <span className="text-3xl mb-2 block">{d.emoji}</span>
                    <span className={`text-sm font-medium ${isActive ? 'text-emerald-400' : 'text-gray-400'}`}>
                      {d.label}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Activity Level */}
          <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '400ms' }}>
            <h3 className="text-white font-semibold mb-5 flex items-center gap-2">
              <Zap size={18} className="text-emerald-400" /> Activity Level
            </h3>
            <div className="space-y-3">
              {activityLevels.map((a) => {
                const isActive = form.activity_level === a.value;
                return (
                  <button
                    key={a.value}
                    type="button"
                    onClick={() => update('activity_level', a.value)}
                    className={`w-full p-4 rounded-xl border text-left transition-all duration-300 flex items-center justify-between
                      ${isActive
                        ? 'bg-emerald-500/10 border-emerald-500/30'
                        : 'bg-white/5 border-white/10 hover:bg-white/10'
                      }`}
                  >
                    <div>
                      <p className={`font-medium ${isActive ? 'text-white' : 'text-gray-300'}`}>{a.label}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{a.desc}</p>
                    </div>
                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center
                      ${isActive ? 'border-emerald-400' : 'border-gray-600'}`}>
                      {isActive && <div className="w-2.5 h-2.5 rounded-full bg-emerald-400" />}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Submit */}
          <div className="animate-slide-up" style={{ animationDelay: '500ms' }}>
            <button
              type="submit"
              disabled={loading || !form.age || !form.weight || !form.height}
              className="btn-primary w-full flex items-center justify-center gap-2 py-4 text-lg"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : saved ? (
                <>✅ Profile Saved! Redirecting...</>
              ) : (
                <>
                  <Save size={20} />
                  {existing ? 'Update Profile' : 'Save Profile & Get Started'}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
