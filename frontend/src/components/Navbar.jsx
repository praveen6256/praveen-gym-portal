import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Navbar() {
  const { user, logout, isAdmin, isPremium } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setMenuOpen(false);
  };

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand" onClick={() => setMenuOpen(false)}>
          <span className="brand-icon">🏋️</span>
          <span className="brand-name">Praveen Gym</span>
        </Link>

        <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle menu">
          <span /><span /><span />
        </button>

        <ul className={`nav-links ${menuOpen ? 'open' : ''}`}>
          {!user && (
            <>
              <li><Link to="/" className={isActive('/')} onClick={() => setMenuOpen(false)}>Home</Link></li>
              <li><Link to="/login" className={`nav-btn ${isActive('/login')}`} onClick={() => setMenuOpen(false)}>Login</Link></li>
              <li><Link to="/register" className="nav-btn primary" onClick={() => setMenuOpen(false)}>Join Now</Link></li>
            </>
          )}

          {user && !isAdmin() && (
            <>
              <li><Link to="/dashboard" className={isActive('/dashboard')} onClick={() => setMenuOpen(false)}>Dashboard</Link></li>
              <li><Link to="/workouts" className={isActive('/workouts')} onClick={() => setMenuOpen(false)}>Workouts</Link></li>
              {isPremium() && (
                <li><Link to="/diet" className={isActive('/diet')} onClick={() => setMenuOpen(false)}>
                  <span className="premium-badge-sm">⭐</span> Diet
                </Link></li>
              )}
              <li><Link to="/profile" className={isActive('/profile')} onClick={() => setMenuOpen(false)}>Profile</Link></li>
              <li><Link to="/membership" className={isActive('/membership')} onClick={() => setMenuOpen(false)}>Membership</Link></li>
              <li>
                <div className="nav-user">
                  <span className={`membership-tag ${user.membership_type}`}>
                    {user.membership_type === 'premium' ? '⭐ Premium' : 'Standard'}
                  </span>
                  <button onClick={handleLogout} className="nav-btn logout">Logout</button>
                </div>
              </li>
            </>
          )}

          {user && isAdmin() && (
            <>
              <li><Link to="/admin" className={isActive('/admin')} onClick={() => setMenuOpen(false)}>Dashboard</Link></li>
              <li><Link to="/admin/members" className={isActive('/admin/members')} onClick={() => setMenuOpen(false)}>Members</Link></li>
              <li><Link to="/admin/workouts" className={isActive('/admin/workouts')} onClick={() => setMenuOpen(false)}>Workouts</Link></li>
              <li><Link to="/admin/foods" className={isActive('/admin/foods')} onClick={() => setMenuOpen(false)}>Foods</Link></li>
              <li>
                <div className="nav-user">
                  <span className="membership-tag admin">🛡️ Admin</span>
                  <button onClick={handleLogout} className="nav-btn logout">Logout</button>
                </div>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}
