import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';

export default function AdminMembers() {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [membershipFilter, setMembershipFilter] = useState('');
  const [genderFilter, setGenderFilter] = useState('');
  const [actionLoading, setActionLoading] = useState(null);

  useEffect(() => {
    fetchMembers();
  }, [search, membershipFilter, genderFilter]);

  const fetchMembers = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (membershipFilter) params.membership_type = membershipFilter;
      if (genderFilter) params.gender = genderFilter;

      const res = await client.get('/admin/members', { params });
      setMembers(res.data.members || []);
    } catch (err) {
      console.error("Failed to fetch members:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleActivatePremium = async (memberId, name) => {
    if (!window.confirm(`Activate Premium membership for ${name} after cash payment?`)) return;
    setActionLoading(memberId);
    try {
      await client.post(`/admin/members/${memberId}/activate-premium`);
      await fetchMembers();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to activate Premium.");
    } finally {
      setActionLoading(null);
    }
  };

  const handleRemovePremium = async (memberId, name) => {
    if (!window.confirm(`Remove Premium membership for ${name}?`)) return;
    setActionLoading(memberId);
    try {
      await client.post(`/admin/members/${memberId}/remove-premium`);
      await fetchMembers();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to remove Premium.");
    } finally {
      setActionLoading(null);
    }
  };

  const handleToggleActive = async (memberId, name, currentStatus) => {
    const action = currentStatus ? "disable" : "enable";
    if (!window.confirm(`Are you sure you want to ${action} account for ${name}?`)) return;
    setActionLoading(memberId);
    try {
      await client.post(`/admin/members/${memberId}/toggle-active`);
      await fetchMembers();
    } catch (err) {
      alert(err.response?.data?.detail || `Failed to ${action} account.`);
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-title">Admin Navigation</div>
        <Link to="/admin" className="admin-nav-item">📊 Overview</Link>
        <Link to="/admin/members" className="admin-nav-item active">👥 Members Management</Link>
        <Link to="/admin/workouts" className="admin-nav-item">🏋️ Workout Plans</Link>
        <Link to="/admin/foods" className="admin-nav-item">🥗 Food Database</Link>
      </aside>

      <main className="admin-content">
        <h1 className="admin-page-title">Member Management</h1>
        <p className="admin-page-sub">View members, search, filter, and activate Premium after physical cash payment</p>

        {/* Filter Controls */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto auto', gap: '16px', marginBottom: '24px' }}>
          <div className="search-bar">
            <span className="search-icon">🔍</span>
            <input
              className="form-input"
              placeholder="Search by name, email, or phone..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <select className="form-select" value={membershipFilter} onChange={(e) => setMembershipFilter(e.target.value)}>
            <option value="">All Memberships</option>
            <option value="standard">Standard</option>
            <option value="premium">Premium</option>
          </select>
          <select className="form-select" value={genderFilter} onChange={(e) => setGenderFilter(e.target.value)}>
            <option value="">All Genders</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        {/* Members Table */}
        {loading ? (
          <div className="loading-screen"><div className="spinner" /></div>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Contact Info</th>
                  <th>Details</th>
                  <th>Goal / Diet</th>
                  <th>Membership</th>
                  <th>Account Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {members.length === 0 ? (
                  <tr><td colSpan="7" style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>No members found.</td></tr>
                ) : (
                  members.map((m) => (
                    <tr key={m.id}>
                      <td>
                        <strong>{m.name}</strong>
                        <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>ID: {m.id}</div>
                      </td>
                      <td>
                        <div>{m.email}</div>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{m.phone}</div>
                      </td>
                      <td>
                        <span className={`badge ${m.gender === 'male' ? 'badge-male' : 'badge-female'}`} style={{ marginRight: '6px' }}>{m.gender}</span>
                        <span style={{ fontSize: '13px' }}>{m.age}y / {m.height}cm / {m.weight}kg</span>
                      </td>
                      <td>
                        <div style={{ fontSize: '13px', textTransform: 'capitalize' }}>{m.fitness_goal?.replace('_', ' ')}</div>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'capitalize' }}>{m.dietary_preference?.replace('_', ' ')}</div>
                      </td>
                      <td>
                        <span className={`badge ${m.membership_type === 'premium' ? 'badge-premium' : 'badge-standard'}`}>
                          {m.membership_type}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${m.is_active ? 'badge-active' : 'badge-inactive'}`}>
                          {m.is_active ? 'Active' : 'Disabled'}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                          {m.membership_type === 'standard' ? (
                            <button
                              className="btn btn-gold btn-sm"
                              onClick={() => handleActivatePremium(m.id, m.name)}
                              disabled={actionLoading === m.id}
                            >
                              ⭐ Activate Premium
                            </button>
                          ) : (
                            <button
                              className="btn btn-secondary btn-sm"
                              onClick={() => handleRemovePremium(m.id, m.name)}
                              disabled={actionLoading === m.id}
                            >
                              Remove Premium
                            </button>
                          )}
                          <button
                            className={`btn btn-sm ${m.is_active ? 'btn-danger' : 'btn-success'}`}
                            onClick={() => handleToggleActive(m.id, m.name, m.is_active)}
                            disabled={actionLoading === m.id}
                          >
                            {m.is_active ? 'Disable' : 'Enable'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
