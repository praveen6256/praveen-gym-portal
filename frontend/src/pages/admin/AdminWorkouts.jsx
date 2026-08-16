import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';

export default function AdminWorkouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [genderFilter, setGenderFilter] = useState('male');
  const [editingWorkout, setEditingWorkout] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchWorkouts();
  }, [genderFilter]);

  const fetchWorkouts = async () => {
    setLoading(true);
    try {
      const res = await client.get('/admin/workouts', { params: { gender: genderFilter } });
      setWorkouts(res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditExercise = (workoutIndex, exerciseIndex, field, value) => {
    const updated = { ...editingWorkout };
    updated.exercises[exerciseIndex][field] = value;
    setEditingWorkout(updated);
  };

  const handleSaveWorkout = async () => {
    if (!editingWorkout) return;
    setSaving(true);
    try {
      await client.put(`/admin/workouts/${editingWorkout.id}`, {
        focus: editingWorkout.focus,
        description: editingWorkout.description,
        exercises: editingWorkout.exercises,
      });
      await fetchWorkouts();
      setEditingWorkout(null);
      alert("Workout plan updated successfully!");
    } catch (err) {
      alert("Failed to update workout plan.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-title">Admin Navigation</div>
        <Link to="/admin" className="admin-nav-item">📊 Overview</Link>
        <Link to="/admin/members" className="admin-nav-item">👥 Members Management</Link>
        <Link to="/admin/workouts" className="admin-nav-item active">🏋️ Workout Plans</Link>
        <Link to="/admin/foods" className="admin-nav-item">🥗 Food Database</Link>
      </aside>

      <main className="admin-content">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <div>
            <h1 className="admin-page-title">Manage Workout Plans</h1>
            <p className="admin-page-sub">Edit male & female workout routines by day</p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className={`btn btn-sm ${genderFilter === 'male' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setGenderFilter('male')}>♂ Male Plans</button>
            <button className={`btn btn-sm ${genderFilter === 'female' ? 'btn-primary' : 'btn-secondary'}`} onClick={() => setGenderFilter('female')}>♀ Female Plans</button>
          </div>
        </div>

        {loading ? (
          <div className="loading-screen"><div className="spinner" /></div>
        ) : (
          <div className="feature-grid">
            {workouts.map((w) => (
              <div key={w.id} className="card">
                <div style={{ fontSize: '12px', color: 'var(--orange)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px' }}>
                  {w.day} ({w.gender})
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: 800, margin: '8px 0' }}>{w.focus}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginBottom: '16px' }}>{w.description}</p>
                <div style={{ fontSize: '13px', fontWeight: 600, marginBottom: '16px', color: 'var(--text)' }}>
                  📋 {w.exercises?.length || 0} Exercises Configured
                </div>
                <button className="btn btn-secondary btn-sm" style={{ width: '100%' }} onClick={() => setEditingWorkout(w)}>
                  ✏️ Edit Plan & Exercises
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Modal for editing workout plan */}
        {editingWorkout && (
          <div className="modal-overlay">
            <div className="modal" style={{ maxWidth: '720px' }}>
              <div className="modal-header">
                <h2 style={{ fontSize: '20px', fontWeight: 800 }}>Edit Plan: {editingWorkout.day.toUpperCase()} ({editingWorkout.gender})</h2>
                <button className="modal-close" onClick={() => setEditingWorkout(null)}>✕</button>
              </div>

              <div className="form-group">
                <label className="form-label">Focus / Title</label>
                <input className="form-input" value={editingWorkout.focus} onChange={(e) => setEditingWorkout({ ...editingWorkout, focus: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea className="form-input" rows="2" value={editingWorkout.description} onChange={(e) => setEditingWorkout({ ...editingWorkout, description: e.target.value })} />
              </div>

              <h3 style={{ fontSize: '16px', fontWeight: 700, marginTop: '20px', marginBottom: '12px' }}>Exercises</h3>
              <div style={{ maxHeight: '350px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {editingWorkout.exercises?.map((ex, idx) => (
                  <div key={idx} style={{ background: 'var(--bg-card2)', border: '1px solid var(--border)', padding: '14px', borderRadius: 'var(--radius-sm)' }}>
                    <div className="form-grid">
                      <div className="form-group" style={{ marginBottom: '8px' }}>
                        <label className="form-label">Exercise Name</label>
                        <input className="form-input" value={ex.name} onChange={(e) => handleEditExercise(null, idx, 'name', e.target.value)} />
                      </div>
                      <div className="form-group" style={{ marginBottom: '8px' }}>
                        <label className="form-label">Image URL</label>
                        <input className="form-input" value={ex.image_url} onChange={(e) => handleEditExercise(null, idx, 'image_url', e.target.value)} />
                      </div>
                    </div>
                    <div className="form-grid">
                      <div className="form-group" style={{ marginBottom: '8px' }}>
                        <label className="form-label">Sets</label>
                        <input className="form-input" type="number" value={ex.sets || ''} onChange={(e) => handleEditExercise(null, idx, 'sets', parseInt(e.target.value))} />
                      </div>
                      <div className="form-group" style={{ marginBottom: '8px' }}>
                        <label className="form-label">Reps</label>
                        <input className="form-input" type="number" value={ex.reps || ''} onChange={(e) => handleEditExercise(null, idx, 'reps', parseInt(e.target.value))} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '20px' }}>
                <button className="btn btn-secondary" onClick={() => setEditingWorkout(null)}>Cancel</button>
                <button className="btn btn-primary" onClick={handleSaveWorkout} disabled={saving}>
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
