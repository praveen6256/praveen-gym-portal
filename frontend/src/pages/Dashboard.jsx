import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import client from '../api/client';

const DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'];

function getDayLabel(day) {
  return day.charAt(0).toUpperCase() + day.slice(1);
}

function getTodayName() {
  return DAYS[new Date().getDay() === 0 ? 6 : new Date().getDay() - 1];
}

export default function Dashboard() {
  const { user, isPremium } = useAuth();
  const [todayWorkout, setTodayWorkout] = useState(null);
  const [loading, setLoading] = useState(true);
  const todayName = getTodayName();

  useEffect(() => {
    client.get('/workouts/today')
      .then((r) => setTodayWorkout(r.data))
      .catch(() => setTodayWorkout(null))
      .finally(() => setLoading(false));
  }, []);

  const greeting = () => {
    const h = new Date().getHours();
    if (h < 12) return 'Good Morning';
    if (h < 17) return 'Good Afternoon';
    return 'Good Evening';
  };

  return (
    <div className="page">
      <div className="container">
        <div className="dashboard-header">
          <p className="dashboard-greeting">{greeting()}, let's get to work! 💪</p>
          <h1 className="dashboard-name">{user?.name}</h1>
          <div style={{ display: 'flex', gap: '12px', marginTop: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
            <span className={`badge ${user?.membership_type === 'premium' ? 'badge-premium' : 'badge-standard'}`}>
              {user?.membership_type === 'premium' ? '⭐ Premium Member' : 'Standard Member'}
            </span>
            <span className={`badge ${user?.gender === 'male' ? 'badge-male' : 'badge-female'}`}>
              {user?.gender === 'male' ? '♂ Male' : '♀ Female'}
            </span>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="stats-grid" style={{ marginBottom: '40px' }}>
          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-value" style={{ fontSize: '18px', fontWeight: 700 }}>{user?.fitness_goal?.replace('_', ' ')}</div>
            <div className="stat-label">Fitness Goal</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚖️</div>
            <div className="stat-value">{user?.weight}<span style={{ fontSize: '16px' }}>kg</span></div>
            <div className="stat-label">Body Weight</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📏</div>
            <div className="stat-value">{user?.height}<span style={{ fontSize: '16px' }}>cm</span></div>
            <div className="stat-label">Height</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📅</div>
            <div className="stat-value" style={{ fontSize: '18px', fontWeight: 700 }}>{getDayLabel(todayName)}</div>
            <div className="stat-label">Today</div>
          </div>
        </div>

        {/* Today's Workout Preview */}
        <div style={{ marginBottom: '40px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '16px' }}>Today's Workout</h2>
          {loading ? (
            <div className="loading-screen" style={{ minHeight: '120px' }}><div className="spinner" /></div>
          ) : todayWorkout?.is_rest_day ? (
            <div className="rest-day-card" style={{ padding: '40px' }}>
              <div className="rest-day-emoji">😴</div>
              <h3 className="rest-day-title">Rest Day!</h3>
              <p className="rest-day-text">Today is Sunday — your body needs recovery just as much as training.</p>
            </div>
          ) : todayWorkout ? (
            <div className="card" style={{ borderColor: 'var(--orange)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
                <div>
                  <div style={{ fontSize: '12px', color: 'var(--orange)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '4px' }}>
                    {getDayLabel(todayWorkout.day)} — Today
                  </div>
                  <h3 style={{ fontSize: '22px', fontWeight: 800 }}>{todayWorkout.focus}</h3>
                  <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '6px' }}>{todayWorkout.description}</p>
                  <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '6px' }}>
                    {todayWorkout.exercises?.length} exercises
                  </p>
                </div>
                <Link to="/workouts/today" className="btn btn-primary">Start Workout →</Link>
              </div>
            </div>
          ) : (
            <div className="alert alert-info">No workout plan set for today. Check back later.</div>
          )}
        </div>

        {/* Quick Links */}
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, marginBottom: '16px' }}>Quick Access</h2>
          <div className="feature-grid">
            <Link to="/workouts" style={{ textDecoration: 'none' }}>
              <div className="feature-card" style={{ cursor: 'pointer' }}>
                <div className="feature-icon">📅</div>
                <h3 className="feature-title">Weekly Plan</h3>
                <p className="feature-text">View your full 6-day workout schedule</p>
              </div>
            </Link>
            <Link to="/workouts/today" style={{ textDecoration: 'none' }}>
              <div className="feature-card" style={{ cursor: 'pointer', borderColor: todayWorkout && !todayWorkout.is_rest_day ? 'var(--orange)' : 'var(--border)' }}>
                <div className="feature-icon">💪</div>
                <h3 className="feature-title">Today's Workout</h3>
                <p className="feature-text">Jump straight into today's exercises</p>
              </div>
            </Link>
            <Link to="/profile" style={{ textDecoration: 'none' }}>
              <div className="feature-card" style={{ cursor: 'pointer' }}>
                <div className="feature-icon">👤</div>
                <h3 className="feature-title">My Profile</h3>
                <p className="feature-text">Update your body stats and fitness goals</p>
              </div>
            </Link>
            {isPremium() ? (
              <Link to="/diet" style={{ textDecoration: 'none' }}>
                <div className="feature-card" style={{ cursor: 'pointer', borderColor: 'rgba(255,215,0,0.4)' }}>
                  <div className="feature-icon">🥗</div>
                  <h3 className="feature-title">Diet & Nutrition ⭐</h3>
                  <p className="feature-text">Access your personalised nutrition calculator</p>
                </div>
              </Link>
            ) : (
              <Link to="/membership" style={{ textDecoration: 'none' }}>
                <div className="premium-upsell" style={{ cursor: 'pointer' }}>
                  <div style={{ fontSize: '32px', marginBottom: '12px' }}>⭐</div>
                  <h3>Upgrade to Premium</h3>
                  <p>Visit the gym, pay in cash, and unlock diet & nutrition access.</p>
                  <span className="btn btn-gold btn-sm">Learn How →</span>
                </div>
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
