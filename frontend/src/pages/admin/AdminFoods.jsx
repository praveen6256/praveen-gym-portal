import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../../api/client';

export default function AdminFoods() {
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [saving, setSaving] = useState(false);

  const [newFood, setNewFood] = useState({
    name: '', category: 'protein', calories_per_100g: 100,
    protein_g: 10, carbs_g: 10, fat_g: 2, fiber_g: 1,
    description: '', dietary_tags: [],
  });

  useEffect(() => {
    fetchFoods();
  }, []);

  const fetchFoods = async () => {
    setLoading(true);
    try {
      const res = await client.get('/admin/foods');
      setFoods(res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFood = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await client.post('/admin/foods', {
        ...newFood,
        calories_per_100g: parseFloat(newFood.calories_per_100g),
        protein_g: parseFloat(newFood.protein_g),
        carbs_g: parseFloat(newFood.carbs_g),
        fat_g: parseFloat(newFood.fat_g),
        fiber_g: parseFloat(newFood.fiber_g),
      });
      await fetchFoods();
      setShowAddModal(false);
      alert("New food item added to database!");
    } catch (err) {
      alert("Failed to add food item.");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteFood = async (id, name) => {
    if (!window.confirm(`Delete ${name} from food database?`)) return;
    try {
      await client.delete(`/admin/foods/${id}`);
      await fetchFoods();
    } catch (err) {
      alert("Failed to delete food.");
    }
  };

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-title">Admin Navigation</div>
        <Link to="/admin" className="admin-nav-item">📊 Overview</Link>
        <Link to="/admin/members" className="admin-nav-item">👥 Members Management</Link>
        <Link to="/admin/workouts" className="admin-nav-item">🏋️ Workout Plans</Link>
        <Link to="/admin/foods" className="admin-nav-item active">🥗 Food Database</Link>
      </aside>

      <main className="admin-content">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <div>
            <h1 className="admin-page-title">Food & Nutrition Database</h1>
            <p className="admin-page-sub">Manage food recommendations for Premium members</p>
          </div>
          <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>+ Add New Food</button>
        </div>

        {loading ? (
          <div className="loading-screen"><div className="spinner" /></div>
        ) : (
          <div className="food-grid">
            {foods.map((f) => (
              <div key={f.id} className="food-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div className="food-card-name">{f.name}</div>
                  <button className="btn btn-danger btn-sm" style={{ padding: '2px 8px', fontSize: '11px' }} onClick={() => handleDeleteFood(f.id, f.name)}>Delete</button>
                </div>
                <div className="food-card-desc">{f.description}</div>
                <div className="food-macros">
                  <div className="food-macro"><div className="food-macro-val">{f.calories_per_100g}</div><div className="food-macro-key">kcal</div></div>
                  <div className="food-macro"><div className="food-macro-val">{f.protein_g}g</div><div className="food-macro-key">Prot</div></div>
                  <div className="food-macro"><div className="food-macro-val">{f.carbs_g}g</div><div className="food-macro-key">Carb</div></div>
                  <div className="food-macro"><div className="food-macro-val">{f.fat_g}g</div><div className="food-macro-key">Fat</div></div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal for adding food */}
        {showAddModal && (
          <div className="modal-overlay">
            <div className="modal">
              <div className="modal-header">
                <h2>Add Food to Database</h2>
                <button className="modal-close" onClick={() => setShowAddModal(false)}>✕</button>
              </div>
              <form onSubmit={handleCreateFood}>
                <div className="form-group">
                  <label className="form-label">Food Name</label>
                  <input className="form-input" value={newFood.name} onChange={(e) => setNewFood({ ...newFood, name: e.target.value })} required />
                </div>
                <div className="form-grid">
                  <div className="form-group">
                    <label className="form-label">Category</label>
                    <select className="form-select" value={newFood.category} onChange={(e) => setNewFood({ ...newFood, category: e.target.value })}>
                      <option value="protein">Protein</option>
                      <option value="carbohydrate">Carbohydrate</option>
                      <option value="fat">Healthy Fat</option>
                      <option value="fiber">Fiber / Veggies</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Calories / 100g</label>
                    <input className="form-input" type="number" value={newFood.calories_per_100g} onChange={(e) => setNewFood({ ...newFood, calories_per_100g: e.target.value })} required />
                  </div>
                </div>
                <div className="form-grid">
                  <div className="form-group">
                    <label className="form-label">Protein (g)</label>
                    <input className="form-input" type="number" value={newFood.protein_g} onChange={(e) => setNewFood({ ...newFood, protein_g: e.target.value })} required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Carbs (g)</label>
                    <input className="form-input" type="number" value={newFood.carbs_g} onChange={(e) => setNewFood({ ...newFood, carbs_g: e.target.value })} required />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Description</label>
                  <input className="form-input" value={newFood.description} onChange={(e) => setNewFood({ ...newFood, description: e.target.value })} required />
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
                  <button type="button" className="btn btn-secondary" onClick={() => setShowAddModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Saving...' : 'Add Food'}</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
