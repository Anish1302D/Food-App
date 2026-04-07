import { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  User,
  Utensils,
  BookOpen,
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Leaf,
} from 'lucide-react';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/profile', icon: User, label: 'Profile' },
  { path: '/recommendations', icon: Utensils, label: 'Meals' },
  { path: '/food-log', icon: BookOpen, label: 'Food Log' },
  { path: '/eat-now', icon: Sparkles, label: 'Eat Now' },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const check = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile) setCollapsed(true);
    };
    check();
    window.addEventListener('resize', check);
    return () => window.removeEventListener('resize', check);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
  }, [location]);

  if (isMobile) {
    return (
      <>
        {/* Mobile top bar */}
        <div className="fixed top-0 left-0 right-0 z-50 h-16 bg-navy-800/90 backdrop-blur-md border-b border-white/10 flex items-center px-4">
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <Utensils size={20} className="text-emerald-400" />
          </button>
          <div className="flex items-center gap-2 ml-3">
            <Leaf size={22} className="text-emerald-400" />
            <span className="text-lg font-bold gradient-text">SmartBite AI</span>
          </div>
        </div>

        {/* Mobile overlay */}
        {mobileOpen && (
          <div
            className="fixed inset-0 bg-black/60 z-40"
            onClick={() => setMobileOpen(false)}
          />
        )}

        {/* Mobile drawer */}
        <div
          className={`fixed top-0 left-0 h-full w-64 z-50 bg-navy-800 border-r border-white/10
            transform transition-transform duration-300 ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}`}
        >
          <div className="p-5 border-b border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center">
                <Leaf size={20} className="text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold gradient-text">SmartBite AI</h1>
                <p className="text-xs text-gray-500">Nutrition Coach</p>
              </div>
            </div>
          </div>
          <nav className="p-4 space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200
                  ${isActive
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
                    : 'text-gray-400 hover:bg-white/5 hover:text-white border border-transparent'
                  }`
                }
              >
                <item.icon size={20} />
                <span className="font-medium">{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Spacer for mobile top bar */}
        <div className="h-16" />
      </>
    );
  }

  return (
    <aside
      className={`fixed top-0 left-0 h-full z-40 bg-navy-800/80 backdrop-blur-xl border-r border-white/10
        transition-all duration-300 ${collapsed ? 'w-20' : 'w-64'}`}
    >
      {/* Logo */}
      <div className={`p-5 border-b border-white/10 ${collapsed ? 'px-4' : ''}`}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center flex-shrink-0">
            <Leaf size={20} className="text-white" />
          </div>
          {!collapsed && (
            <div className="animate-fade-in">
              <h1 className="text-lg font-bold gradient-text">SmartBite AI</h1>
              <p className="text-xs text-gray-500">Nutrition Coach</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-3 space-y-1 mt-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            title={item.label}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200
              ${collapsed ? 'justify-center' : ''}
              ${isActive
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 shadow-lg shadow-emerald-500/5'
                : 'text-gray-400 hover:bg-white/5 hover:text-white border border-transparent'
              }`
            }
          >
            <item.icon size={20} className="flex-shrink-0" />
            {!collapsed && <span className="font-medium animate-fade-in">{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute bottom-6 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-white/5 border border-white/10
          flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 transition-all"
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>
    </aside>
  );
}
