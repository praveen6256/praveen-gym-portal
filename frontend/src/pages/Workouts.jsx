import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';

const DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'];

function getTodayIdx() {
  const d = new Date().getDay(); // 0=Sun
  return d === 0 ? 6 : d - 1;   // map to 0=Mon...6=Sun
}

export default function Workouts() {
  const [weekData, setWeekData] = useState(null);
  const [selectedDay, setSelectedDay] = useState(DAYS[getTodayIdx()]);
  const [loading, setLoading] = useState(true);
  const todayName = DAYS[getTodayIdx()];

  useEffect(() => {
    client.get('/workouts/week')
      .then((r) => setWeekData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const selectedWorkout = weekData?.workouts?.[selectedDay];

  return (
    <div className="page">
      <div className="container" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
        <div style={{ marginBottom: '32px' }}>
          <h1 style={{ fontSize: '28px', fontWeight: 800 }}>Weekly Workout Plan</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '6px' }}>
            Your personalised {weekData?.gender} workout schedule · Select a day to view exercises
          </p>
        </div>

        {/* Day Tabs */}
        <div className="day-tabs">
          {DAYS.map((day, i) => (
            <button
              key={day}
              className={`day-tab ${selectedDay === day ? 'active' : ''} ${day === todayName ? 'today' : ''} ${day === 'sunday' ? 'rest' : ''}`}
              onClick={() => setSelectedDay(day)}
            >
              {day.slice(0, 3).toUpperCase()}
              {day === todayName && selectedDay !== day && <span style={{ fontSize: '10px', display: 'block', color: 'var(--orange)' }}>Today</span>}
            </button>
          ))}
        </div>

        {/* Content */}
        {loading ? (
          <div className="loading-screen"><div className="spinner" /></div>
        ) : selectedDay === 'sunday' || selectedWorkout?.is_rest_day ? (
          <div className="rest-day-card">
            <div className="rest-day-emoji">😴</div>
            <h2 className="rest-day-title">Sunday — Rest Day</h2>
            <p className="rest-day-text">
              Recovery is a critical part of progress. Rest, hydrate, stretch, and come back stronger on Monday.
            </p>
            <div style={{ marginTop: '24px' }}>
              <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>💡 Rest day tips: walk, foam roll, light yoga, and sleep 8 hours.</p>
            </div>
          </div>
        ) : selectedWorkout ? (
          <div>
            <div style={{ marginBottom: '28px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
                <div>
                  <div style={{ fontSize: '12px', color: 'var(--orange)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '4px' }}>
                    {selectedDay.charAt(0).toUpperCase() + selectedDay.slice(1)}
                    {selectedDay === todayName && <span style={{ marginLeft: '8px', background: 'var(--orange)', color: '#fff', padding: '2px 8px', borderRadius: '20px', fontSize: '10px' }}>TODAY</span>}
                  </div>
                  <h2 style={{ fontSize: '26px', fontWeight: 800 }}>{selectedWorkout.focus}</h2>
                  <p style={{ color: 'var(--text-muted)', marginTop: '6px' }}>{selectedWorkout.description}</p>
                </div>
                {selectedDay === todayName && (
                  <Link to="/workouts/today" className="btn btn-primary">Start Today's Workout →</Link>
                )}
              </div>

              <div className="exercise-list">
                {selectedWorkout.exercises?.map((ex, i) => (
                  <div key={i} className="exercise-card">
                    <img
                      src={ex.image_url}
                      alt={ex.name}
                      className="exercise-img"
                      onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80'; }}
                    />
                    <div className="exercise-body">
                      <div className="exercise-name">{ex.name}</div>
                      {ex.muscle_group && <div className="exercise-muscle">{ex.muscle_group}</div>}
                      <p className="exercise-desc">{ex.description}</p>
                      <div className="exercise-stats">
                        {ex.sets && <div className="exercise-stat"><span className="exercise-stat-val">{ex.sets}</span><span className="exercise-stat-key">Sets</span></div>}
                        {ex.reps && <div className="exercise-stat"><span className="exercise-stat-val">{ex.reps}</span><span className="exercise-stat-key">Reps</span></div>}
                        {ex.duration_minutes && <div className="exercise-stat"><span className="exercise-stat-val">{ex.duration_minutes}</span><span className="exercise-stat-key">Min</span></div>}
                        {ex.rest_seconds != null && <div className="exercise-stat"><span className="exercise-stat-val">{ex.rest_seconds}</span><span className="exercise-stat-key">Rest (s)</span></div>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="alert alert-info">No workout plan set for {selectedDay} yet. Check back soon.</div>
        )}
      </div>
    </div>
  );
}
