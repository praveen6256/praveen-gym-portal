import React from 'react';
import { Link } from 'react-router-dom';

const features = [
  { icon: '💪', title: 'Weekly Workout Plans', text: 'Structured 6-day programs for Monday through Saturday, tailored separately for male and female members. Sunday is always your rest day.' },
  { icon: '🥗', title: 'Premium Diet Guidance', text: 'Premium members unlock personalised nutrition calculations, food recommendations, and meal suggestions based on their body data and fitness goals.' },
  { icon: '🧮', title: 'Nutrition Calculator', text: 'Enter your weight, height, age, and activity level to receive calorie, protein, carbohydrate, fat, fiber, and water estimates.' },
  { icon: '🛡️', title: 'Admin Dashboard', text: 'Gym staff can manage all members, activate Premium memberships, control workout content, and view membership history.' },
  { icon: '📧', title: 'Email Notifications', text: 'Automatic welcome emails on registration and Premium activation notifications to keep members informed.' },
  { icon: '📱', title: 'Mobile Friendly', text: 'Fully responsive design that works seamlessly on smartphones, tablets, and desktops.' },
];

const workoutDays = [
  { day: 'MON', label: 'Chest & Triceps', male: true },
  { day: 'TUE', label: 'Back & Biceps', male: true },
  { day: 'WED', label: 'Legs & Glutes', male: true },
  { day: 'THU', label: 'Shoulders & Core', male: true },
  { day: 'FRI', label: 'Full Body Power', male: true },
  { day: 'SAT', label: 'Arms & Cardio', male: true },
  { day: 'SUN', label: 'Rest Day 😴', rest: true },
];

const steps = [
  { title: 'Register Online', text: 'Create your account on the portal with your personal details and fitness goals.' },
  { title: 'Visit the Gym', text: 'Come to Praveen Gym and choose your Premium membership plan.' },
  { title: 'Pay at Counter', text: 'Pay your membership fee in cash at the gym counter. No online payment required.' },
  { title: 'Admin Activates Premium', text: 'Our staff verifies your payment and activates Premium on your account immediately.' },
  { title: 'Unlock Full Access', text: 'Receive a confirmation email and instantly access all Premium diet and nutrition features.' },
];

export default function Landing() {
  return (
    <div>
      {/* Hero */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <p className="hero-eyebrow">🏋️ Praveen Gym Portal</p>
            <h1 className="hero-title">
              Train Smart.<br />
              <span className="highlight">Eat Better.</span><br />
              Become Stronger.
            </h1>
            <p className="hero-subtitle">
              Your digital portal for professional gym management. Access personalised workout plans, 
              unlock premium diet guidance, and track your fitness journey — all in one place.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-lg">Start Your Journey →</Link>
              <Link to="/login" className="btn btn-secondary btn-lg">Member Login</Link>
            </div>
            <div className="hero-stats">
              <div>
                <div className="hero-stat-num">6</div>
                <div className="hero-stat-label">Workout Days / Week</div>
              </div>
              <div>
                <div className="hero-stat-num">2</div>
                <div className="hero-stat-label">Membership Tiers</div>
              </div>
              <div>
                <div className="hero-stat-num">24/7</div>
                <div className="hero-stat-label">Online Access</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-eyebrow">What's Inside</p>
            <h2 className="section-title">Everything You Need to Succeed</h2>
            <p className="section-subtitle">A complete digital gym experience designed for serious members.</p>
          </div>
          <div className="feature-grid">
            {features.map((f) => (
              <div key={f.title} className="feature-card">
                <div className="feature-icon">{f.icon}</div>
                <h3 className="feature-title">{f.title}</h3>
                <p className="feature-text">{f.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Workout Preview */}
      <section className="section section-dark">
        <div className="container">
          <div className="section-header">
            <p className="section-eyebrow">Workout Schedule</p>
            <h2 className="section-title">6 Days of Structured Training</h2>
            <p className="section-subtitle">Separate plans for male and female members. Workout content managed by our admin team.</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '16px', maxWidth: '900px', margin: '0 auto' }}>
            {workoutDays.map((d) => (
              <div key={d.day} style={{
                background: d.rest ? 'transparent' : 'var(--bg-card)',
                border: `1px solid ${d.rest ? 'var(--border-light)' : 'var(--border)'}`,
                borderStyle: d.rest ? 'dashed' : 'solid',
                borderRadius: 'var(--radius)',
                padding: '20px 16px',
                textAlign: 'center',
                opacity: d.rest ? 0.6 : 1,
              }}>
                <div style={{ fontSize: '20px', fontWeight: '900', color: d.rest ? 'var(--text-muted)' : 'var(--orange)', marginBottom: '8px' }}>{d.day}</div>
                <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>{d.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Membership */}
      <section className="section" id="membership">
        <div className="container">
          <div className="section-header">
            <p className="section-eyebrow">Membership Tiers</p>
            <h2 className="section-title">Standard vs Premium</h2>
            <p className="section-subtitle">Start with Standard, upgrade to Premium after visiting the gym.</p>
          </div>
          <div className="membership-grid">
            {/* Standard */}
            <div className="membership-card">
              <div className="badge badge-standard">Standard</div>
              <div className="membership-price">Free<span style={{ fontSize: '16px', color: 'var(--text-muted)' }}> on registration</span></div>
              <ul className="membership-features">
                <li><span className="check">✓</span> Member registration & login</li>
                <li><span className="check">✓</span> Weekly workout plans (Mon–Sat)</li>
                <li><span className="check">✓</span> Today's workout</li>
                <li><span className="check">✓</span> Gender-specific plans</li>
                <li><span className="check">✓</span> Profile management</li>
                <li><span className="check">✓</span> Membership info</li>
                <li style={{ opacity: 0.4 }}><span>✗</span> Diet & nutrition section</li>
                <li style={{ opacity: 0.4 }}><span>✗</span> Nutrition calculator</li>
                <li style={{ opacity: 0.4 }}><span>✗</span> Meal suggestions</li>
              </ul>
              <div style={{ marginTop: '28px' }}>
                <Link to="/register" className="btn btn-secondary" style={{ width: '100%' }}>Register Free</Link>
              </div>
            </div>
            {/* Premium */}
            <div className="membership-card premium">
              <div className="badge badge-premium">⭐ Premium</div>
              <div className="membership-price">Cash<span style={{ fontSize: '16px', color: 'var(--text-muted)' }}> at gym counter</span></div>
              <ul className="membership-features">
                <li><span className="check">✓</span> Everything in Standard</li>
                <li><span className="check">✓</span> Personalised diet guidance</li>
                <li><span className="check">✓</span> Nutrition calculator</li>
                <li><span className="check">✓</span> Calorie & macro estimates</li>
                <li><span className="check">✓</span> Protein, carbs, fat, fiber</li>
                <li><span className="check">✓</span> Water intake guidance</li>
                <li><span className="check">✓</span> Food recommendations</li>
                <li><span className="check">✓</span> Meal suggestions</li>
                <li><span className="check">✓</span> Priority email support</li>
              </ul>
              <div style={{ marginTop: '28px' }}>
                <Link to="/register" className="btn btn-gold" style={{ width: '100%' }}>Get Started</Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How Premium Activation Works */}
      <section className="section section-dark" id="how-it-works">
        <div className="container">
          <div className="section-header">
            <p className="section-eyebrow">Premium Activation</p>
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">
              There is <strong>no online payment</strong>. Premium is activated by our admin team after you pay in cash at the gym.
            </p>
          </div>
          <div className="steps">
            {steps.map((s, i) => (
              <div key={i} className="step">
                <div className="step-num">{i + 1}</div>
                <div className="step-content">
                  <h4>{s.title}</h4>
                  <p>{s.text}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="alert alert-info" style={{ maxWidth: '600px', margin: '40px auto 0' }}>
            💡 <strong>Important:</strong> Do not attempt to pay online — we do not offer online payments. 
            All membership fees are collected in person at the gym counter.
          </div>
        </div>
      </section>

      {/* Diet Section Preview */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <p className="section-eyebrow">Premium Feature</p>
            <h2 className="section-title">Diet & Nutrition Guidance</h2>
            <p className="section-subtitle">Scientific estimates tailored to your body and fitness goals. Not medical advice.</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', maxWidth: '900px', margin: '0 auto' }}>
            {[
              { icon: '🔥', label: 'Calories', color: 'var(--orange)' },
              { icon: '🥩', label: 'Protein', color: 'var(--success)' },
              { icon: '🌾', label: 'Carbohydrates', color: 'var(--warning)' },
              { icon: '🥑', label: 'Healthy Fats', color: '#3b82f6' },
              { icon: '🥦', label: 'Fiber', color: '#a78bfa' },
              { icon: '💧', label: 'Water Intake', color: '#67e8f9' },
            ].map((m) => (
              <div key={m.label} className="macro-card" style={{ background: 'var(--bg-card)' }}>
                <div className="macro-icon">{m.icon}</div>
                <div className="macro-label" style={{ color: m.color, fontSize: '15px', fontWeight: 700 }}>{m.label}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '6px' }}>Calculated for you</div>
              </div>
            ))}
          </div>
          <div style={{ textAlign: 'center', marginTop: '40px' }}>
            <Link to="/register" className="btn btn-primary btn-lg">Unlock Premium Diet Access →</Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section section-dark">
        <div className="container" style={{ textAlign: 'center' }}>
          <h2 className="section-title">Ready to Start?</h2>
          <p className="section-subtitle" style={{ marginBottom: '32px' }}>
            Join Praveen Gym Portal today. Registration is free and takes less than 2 minutes.
          </p>
          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/register" className="btn btn-primary btn-lg">Create Free Account</Link>
            <Link to="/login" className="btn btn-secondary btn-lg">Already a Member? Login</Link>
          </div>
          <p style={{ color: 'var(--text-dim)', fontSize: '14px', marginTop: '24px' }}>
            📍 Praveen Gym · Your City · Mon–Sat 6AM–10PM
          </p>
        </div>
      </section>
    </div>
  );
}
