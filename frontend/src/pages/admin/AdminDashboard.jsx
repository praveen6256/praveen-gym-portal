import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get('/admin/dashboard/stats')
      .then((r) => setStats(r.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-screen"><div className="spinner" /><p>Loading Admin Dashboard...</p></div>;

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-title">Admin Navigation</div>
        <Link to="/admin" className="admin-nav-item active">📊 Overview</Link>
        <Link to="/admin/members" className="admin-nav-item">👥 Members Management</Link>
        <Link to="/admin/workouts" className="admin-nav-item">🏋️ Workout Plans</Link>
        <Link to="/admin/foods" className="admin-nav-item">🥗 Food Database</Link>
      </aside>

      <main className="admin-content">
        <h1 className="admin-page-title">Admin Overview</h1>
        <p className="admin-page-sub">Praveen Gym Portal member statistics & activity</p>

        {/* Stats Grid */}
        <div className="stats-grid" style={{ marginBottom: '32px' }}>
          <div className="stat-card">
            <div className="stat-value">{stats?.total_members || 0}</div>
            <div className="stat-label">Total Members</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--gold)' }}>{stats?.premium_members || 0}</div>
            <div className="stat-label">Premium Members</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--text-muted)' }}>{stats?.standard_members || 0}</div>
            <div className="stat-label">Standard Members</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--success)' }}>{stats?.active_members || 0}</div>
            <div className="stat-label">Active Accounts</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: '#60a5fa' }}>{stats?.male_members || 0}</div>
            <div className="stat-label">Male Members</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: '#f472b6' }}>{stats?.female_members || 0}</div>
            <div className="stat-label">Female Members</div>
          </div>
        </div>

        {/* Recent Registrations Table */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Recent Registrations</h2>
            <Link to="/admin/members" className="btn btn-secondary btn-sm">View All Members →</Link>
          </div>

          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Member Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Gender</th>
                  <th>Membership</th>
                  <th>Registered Date</th>
                </tr>
              </thead>
              <tbody>
                {stats?.recent_registrations?.map((m) => (
                  <tr key={m.id}>
                    <td><strong>{m.name}</strong></td>
                    <td>{m.email}</td>
                    <td>{m.phone}</td>
                    <td><span className={`badge ${m.gender === 'male' ? 'badge-male' : 'badge-female'}`}>{m.gender}</span></td>
                    <td>
                      <span className={`badge ${m.membership_type === 'premium' ? 'badge-premium' : 'badge-standard'}`}>
                        {m.membership_type}
                      </span>
                    </td>
                    <td>{new Date(m.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
