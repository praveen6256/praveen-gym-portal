import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const FITNESS_GOALS = [
  { value: 'weight_loss', label: 'Weight Loss' },
  { value: 'muscle_gain', label: 'Muscle Gain' },
  { value: 'maintain', label: 'Maintain Weight' },
  { value: 'endurance', label: 'Improve Endurance' },
];

const DIET_PREFS = [
  { value: 'non_vegetarian', label: 'Non-Vegetarian' },
  { value: 'vegetarian', label: 'Vegetarian' },
  { value: 'vegan', label: 'Vegan' },
];

const ACTIVITY_LEVELS = [
  { value: 'sedentary', label: 'Sedentary (no exercise)' },
  { value: 'light', label: 'Light (1–3 days/week)' },
  { value: 'moderate', label: 'Moderate (3–5 days/week)' },
  { value: 'active', label: 'Active (6–7 days/week)' },
  { value: 'very_active', label: 'Very Active (physical job + exercise)' },
];

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: '', email: '', password: '', confirmPassword: '',
    gender: 'male', age: '', height: '', weight: '', phone: '',
    fitness_goal: 'muscle_gain', dietary_preference: 'non_vegetarian', activity_level: 'moderate',
  });

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError('');
  };

  const validate = () => {
    if (!form.name.trim() || form.name.trim().length < 2) return 'Name must be at least 2 characters.';
    if (!form.email.includes('@')) return 'Please enter a valid email address.';
    if (form.password.length < 6) return 'Password must be at least 6 characters.';
    if (form.password !== form.confirmPassword) return 'Passwords do not match.';
    if (!form.age || form.age < 10 || form.age > 100) return 'Please enter a valid age (10–100).';
    if (!form.height || form.height < 50 || form.height > 300) return 'Please enter a valid height in cm (50–300).';
    if (!form.weight || form.weight < 20 || form.weight > 500) return 'Please enter a valid weight in kg (20–500).';
    if (!form.phone || form.phone.length < 7) return 'Please enter a valid phone number.';
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validate();
    if (validationError) { setError(validationError); return; }

    setLoading(true);
    try {
      const { confirmPassword, ...submitData } = form;
      submitData.age = parseInt(submitData.age);
      submitData.height = parseFloat(submitData.height);
      submitData.weight = parseFloat(submitData.weight);
      const user = await register(submitData);
      navigate(user.role === 'admin' ? '/admin' : '/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card" style={{ maxWidth: '640px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{ fontSize: '40px', marginBottom: '12px' }}>🏋️</div>
          <h1 className="auth-title">Join Praveen Gym</h1>
          <p className="auth-subtitle">Create your free Standard membership account</p>
        </div>

        {error && <div className="alert alert-error">⚠️ {error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Full Name *</label>
              <input className="form-input" name="name" value={form.name} onChange={handleChange} placeholder="Your full name" required />
            </div>
            <div className="form-group">
              <label className="form-label">Phone Number *</label>
              <input className="form-input" name="phone" value={form.phone} onChange={handleChange} placeholder="+91 00000 00000" required />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Email Address *</label>
            <input className="form-input" name="email" type="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required />
          </div>

          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Password *</label>
              <input className="form-input" name="password" type="password" value={form.password} onChange={handleChange} placeholder="Min. 6 characters" required />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm Password *</label>
              <input className="form-input" name="confirmPassword" type="password" value={form.confirmPassword} onChange={handleChange} placeholder="Repeat password" required />
            </div>
          </div>

          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Gender *</label>
              <select className="form-select" name="gender" value={form.gender} onChange={handleChange}>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Age *</label>
              <input className="form-input" name="age" type="number" value={form.age} onChange={handleChange} placeholder="e.g. 25" min="10" max="100" required />
            </div>
          </div>

          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Height (cm) *</label>
              <input className="form-input" name="height" type="number" value={form.height} onChange={handleChange} placeholder="e.g. 175" min="50" max="300" required />
            </div>
            <div className="form-group">
              <label className="form-label">Weight (kg) *</label>
              <input className="form-input" name="weight" type="number" value={form.weight} onChange={handleChange} placeholder="e.g. 70" min="20" max="500" required />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Fitness Goal *</label>
            <select className="form-select" name="fitness_goal" value={form.fitness_goal} onChange={handleChange}>
              {FITNESS_GOALS.map((g) => <option key={g.value} value={g.value}>{g.label}</option>)}
            </select>
          </div>

          <div className="form-grid">
            <div className="form-group">
              <label className="form-label">Dietary Preference *</label>
              <select className="form-select" name="dietary_preference" value={form.dietary_preference} onChange={handleChange}>
                {DIET_PREFS.map((d) => <option key={d.value} value={d.value}>{d.label}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Activity Level *</label>
              <select className="form-select" name="activity_level" value={form.activity_level} onChange={handleChange}>
                {ACTIVITY_LEVELS.map((a) => <option key={a.value} value={a.value}>{a.label}</option>)}
              </select>
            </div>
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '8px' }} disabled={loading}>
            {loading ? '⏳ Creating Account...' : '🏋️ Create Account'}
          </button>
        </form>

        <div className="alert alert-info" style={{ marginTop: '20px', fontSize: '13px' }}>
          ℹ️ Registration gives you <strong>Standard membership</strong>. To upgrade to <strong>Premium</strong>, visit the gym and pay in cash. The admin will activate it for you.
        </div>

        <p style={{ textAlign: 'center', marginTop: '20px', color: 'var(--text-muted)', fontSize: '14px' }}>
          Already have an account? <Link to="/login" style={{ color: 'var(--orange)', fontWeight: 600 }}>Login here</Link>
        </p>
      </div>
    </div>
  );
}
