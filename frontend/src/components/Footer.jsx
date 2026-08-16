import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <span className="brand-icon">🏋️</span>
          <span className="brand-name">Praveen Gym Portal</span>
          <p className="footer-tagline">Train Smart. Eat Better. Become Stronger.</p>
        </div>
        <div className="footer-links">
          <div className="footer-col">
            <h4>Portal</h4>
            <Link to="/">Home</Link>
            <Link to="/login">Member Login</Link>
            <Link to="/register">Register</Link>
          </div>
          <div className="footer-col">
            <h4>Membership</h4>
            <p>Standard — Workout Plans</p>
            <p>Premium — Diet & Nutrition</p>
            <p>Payment: Cash at Gym</p>
          </div>
          <div className="footer-col">
            <h4>Contact</h4>
            <p>📍 Praveen Gym, Your City</p>
            <p>📞 +91 00000 00000</p>
            <p>🕐 Mon–Sat: 6AM – 10PM</p>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2024 Praveen Gym Portal. All rights reserved.</p>
        <p className="footer-disclaimer">
          ⚠️ Nutrition information is general guidance only and not medical advice.
        </p>
      </div>
    </footer>
  );
}
