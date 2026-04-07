import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Recommendations from './pages/Recommendations';
import FoodLog from './pages/FoodLog';
import EatNow from './pages/EatNow';
import './index.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-navy-900">
        <Sidebar />
        {/* Main content area – adjusts for sidebar */}
        <main className="md:ml-64 transition-all duration-300">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/food-log" element={<FoodLog />} />
            <Route path="/eat-now" element={<EatNow />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
