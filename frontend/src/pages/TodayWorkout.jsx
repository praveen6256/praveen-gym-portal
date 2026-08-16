import React, { useEffect, useState } from 'react';
import client from '../api/client';

export default function TodayWorkout() {
  const [workout, setWorkout] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get('/workouts/today')
      .then((r) => setWorkout(r.data))
      .catch(() => setWorkout(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading today's workout...</p></div>;
  }

  if (!workout || workout.is_rest_day) {
    return (
      <div className="page">
        <div className="container" style={{ paddingTop: '40px' }}>
          <div className="rest-day-card">
            <div className="rest-day-emoji">😴</div>
            <h1 className="rest-day-title">Today is Rest Day!</h1>
            <p className="rest-day-text">
              {workout?.message || "Sunday is for recovery. Rest, stay hydrated, and refuel for next week!"}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="container" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
        <div className="card" style={{ borderColor: 'var(--orange)', marginBottom: '32px' }}>
          <div style={{ fontSize: '12px', color: 'var(--orange)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '4px' }}>
            Today's Session — {workout.day.toUpperCase()}
          </div>
          <h1 style={{ fontSize: '32px', fontWeight: 800 }}>{workout.focus}</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '8px', fontSize: '16px' }}>{workout.description}</p>
        </div>

        <h2 style={{ fontSize: '22px', fontWeight: 800, marginBottom: '20px' }}>Exercises ({workout.exercises?.length || 0})</h2>
        
        <div className="exercise-list">
          {workout.exercises?.map((ex, i) => (
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
  );
}
