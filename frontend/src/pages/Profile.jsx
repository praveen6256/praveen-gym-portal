import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import client from '../api/client';

export default function Profile() {
  const { user, refreshUser } = useAuth();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    name: '', age: '', height: '', weight: '', phone: '',
    fitness_goal: 'maintain', dietary_preference: 'non_vegetarian', activity_level: 'moderate',
  });

  useEffect(() => {
    if (user) {
      setForm({
        name: user.name || '',
        age: user.age || '',
        height: user.height || '',
        weight: user.weight || '',
        phone: user.phone || '',
        fitness_goal: user.fitness_goal || 'maintain',
        dietary_preference: user.dietary_preference || 'non_vegetarian',
        activity_level: user.activity_level || 'moderate',
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const updatePayload = {
        ...form,
        age: parseInt(form.age),
        height: parseFloat(form.height),
        weight: parseFloat(form.weight),
      };
      await client.put('/members/profile', updatePayload);
      await refreshUser();
      setMessage('Profile updated successfully!');
      setEditing(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="container-md" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div className="profile-avatar">
                {user?.name?.charAt(0).toUpperCase()}
              </div>
              <div>
                <h1 style={{ fontSize: '24px', fontWeight: 800 }}>{user?.name}</h1>
                <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>{user?.email}</p>
                <div style={{ marginTop: '6px', display: 'flex', gap: '8px' }}>
                  <span className={`badge ${user?.membership_type === 'premium' ? 'badge-premium' : 'badge-standard'}`}>
                    {user?.membership_type === 'premium' ? '⭐ Premium' : 'Standard'}
                  </span>
                  <span className={`badge ${user?.gender === 'male' ? 'badge-male' : 'badge-female'}`}>
                    {user?.gender?.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>
            {!editing && (
              <button className="btn btn-secondary btn-sm" onClick={() => setEditing(true)}>
                ✏️ Edit Profile
              </button>
            )}
          </div>

          {message && <div className="alert alert-success">✅ {message}</div>}
          {error && <div className="alert alert-error">⚠️ {error}</div>}

          {!editing ? (
            <div className="profile-grid">
              <div className="profile-field">
                <div className="profile-field-label">Phone Number</div>
                <div className="profile-field-value">{user?.phone}</div>
              </div>
              <div className="profile-field">
                <div className="profile-field-label">Age</div>
                <div className="profile-field-value">{user?.age} years</div>
              </div>
              <div className="profile-field">
                <div className="profile-field-label">Height</div>
                <div className="profile-field-value">{user?.height} cm</div>
              </div>
              <div className="profile-field">
                <div className="profile-field-label">Weight</div>
                <div className="profile-field-value">{user?.weight} kg</div>
              </div>
              <div className="profile-field">
                <div className="profile-field-label">Fitness Goal</div>
                <div className="profile-field-value" style={{ textTransform: 'capitalize' }}>
                  {user?.fitness_goal?.replace('_', ' ')}
                </div>
              </div>
              <div className="profile-field">
                <div className="profile-field-label">Dietary Preference</div>
                <div className="profile-field-value" style={{ textTransform: 'capitalize' }}>
                  {user?.dietary_preference?.replace('_', ' ')}
                </div>
              </div>
              <div className="profile-field" style={{ gridColumn: 'span 2' }}>
                <div className="profile-field-label">Activity Level</div>
                <div className="profile-field-value" style={{ textTransform: 'capitalize' }}>
                  {user?.activity_level?.replace('_', ' ')}
                </div>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Full Name</label>
                  <input className="form-input" name="name" value={form.name} onChange={handleChange} required />
                </div>
                <div className="form-group">
                  <label className="form-label">Phone Number</label>
                  <input className="form-input" name="phone" value={form.phone} onChange={handleChange} required />
                </div>
              </div>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Age</label>
                  <input className="form-input" type="number" name="age" value={form.age} onChange={handleChange} required />
                </div>
                <div className="form-group">
                  <label className="form-label">Height (cm)</label>
                  <input className="form-input" type="number" name="height" value={form.height} onChange={handleChange} required />
                </div>
              </div>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Weight (kg)</label>
                  <input className="form-input" type="number" name="weight" value={form.weight} onChange={handleChange} required />
                </div>
                <div className="form-group">
                  <label className="form-label">Fitness Goal</label>
                  <select className="form-select" name="fitness_goal" value={form.fitness_goal} onChange={handleChange}>
                    <option value="weight_loss">Weight Loss</option>
                    <option value="muscle_gain">Muscle Gain</option>
                    <option value="maintain">Maintain Weight</option>
                    <option value="endurance">Endurance</option>
                  </select>
                </div>
              </div>
              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Dietary Preference</label>
                  <select className="form-select" name="dietary_preference" value={form.dietary_preference} onChange={handleChange}>
                    <option value="non_vegetarian">Non-Vegetarian</option>
                    <option value="vegetarian">Vegetarian</option>
                    <option value="vegan">Vegan</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Activity Level</label>
                  <select className="form-select" name="activity_level" value={form.activity_level} onChange={handleChange}>
                    <option value="sedentary">Sedentary</option>
                    <option value="light">Light</option>
                    <option value="moderate">Moderate</option>
                    <option value="active">Active</option>
                    <option value="very_active">Very Active</option>
                  </select>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '12px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setEditing(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
