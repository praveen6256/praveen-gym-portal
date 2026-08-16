import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import client from '../api/client';

export default function Diet() {
  const { user } = useAuth();
  const [nutrition, setNutrition] = useState(null);
  const [foods, setFoods] = useState([]);
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [foodCategory, setFoodCategory] = useState('');
  const [dietaryTag, setDietaryTag] = useState('');

  const [bodyForm, setBodyForm] = useState({
    weight: user?.weight || 70,
    height: user?.height || 170,
    age: user?.age || 25,
    gender: user?.gender || 'male',
    activity_level: user?.activity_level || 'moderate',
    fitness_goal: user?.fitness_goal || 'maintain',
    dietary_preference: user?.dietary_preference || 'non_vegetarian',
  });

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      // 1. Calculate macros based on user profile
      const nutRes = await client.post('/nutrition/calculate', bodyForm);
      setNutrition(nutRes.data);

      // 2. Fetch food database
      const foodRes = await client.get('/nutrition/foods');
      setFoods(foodRes.data);

      // 3. Fetch meal suggestions
      const mealRes = await client.get('/nutrition/meal-suggestions', {
        params: {
          dietary_preference: bodyForm.dietary_preference,
          fitness_goal: bodyForm.fitness_goal,
        },
      });
      setMeals(mealRes.data.meals || []);
    } catch (err) {
      console.error("Failed to load nutrition data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRecalculate = async (e) => {
    e.preventDefault();
    setCalculating(true);
    try {
      const res = await client.post('/nutrition/calculate', {
        ...bodyForm,
        weight: parseFloat(bodyForm.weight),
        height: parseFloat(bodyForm.height),
        age: parseInt(bodyForm.age),
      });
      setNutrition(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setCalculating(false);
    }
  };

  const filterFoods = async () => {
    try {
      const params = {};
      if (foodCategory) params.category = foodCategory;
      if (dietaryTag) params.dietary_tag = dietaryTag;
      const res = await client.get('/nutrition/foods', { params });
      setFoods(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    filterFoods();
  }, [foodCategory, dietaryTag]);

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Calculating personalised nutrition...</p></div>;
  }

  const m = nutrition?.macros;

  return (
    <div className="page">
      <div className="container" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
        <div style={{ marginBottom: '32px' }}>
          <div className="badge badge-premium" style={{ marginBottom: '8px' }}>⭐ Premium Exclusive</div>
          <h1 style={{ fontSize: '32px', fontWeight: 800 }}>Diet & Nutrition Portal</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: '4px' }}>
            Personalised caloric & macro targets calculated for <strong>{user?.name}</strong>.
          </p>
        </div>

        {/* Nutrition Estimates Grid */}
        {m && (
          <div style={{ marginBottom: '48px' }}>
            <h2 style={{ fontSize: '20px', fontWeight: 800, marginBottom: '16px' }}>Your Recommended Daily Intake</h2>
            <div className="macro-grid">
              <div className="macro-card macro-calories">
                <div className="macro-icon">🔥</div>
                <div className="macro-value">{m.calories}</div>
                <div className="macro-unit">kcal / day</div>
                <div className="macro-label">Energy Target</div>
              </div>
              <div className="macro-card macro-protein">
                <div className="macro-icon">🥩</div>
                <div className="macro-value">{m.protein_g}</div>
                <div className="macro-unit">grams</div>
                <div className="macro-label">Protein Target</div>
              </div>
              <div className="macro-card macro-carbs">
                <div className="macro-icon">🌾</div>
                <div className="macro-value">{m.carbs_g}</div>
                <div className="macro-unit">grams</div>
                <div className="macro-label">Carbohydrates</div>
              </div>
              <div className="macro-card macro-fat">
                <div className="macro-icon">🥑</div>
                <div className="macro-value">{m.fat_g}</div>
                <div className="macro-unit">grams</div>
                <div className="macro-label">Healthy Fats</div>
              </div>
              <div className="macro-card macro-fiber">
                <div className="macro-icon">🥦</div>
                <div className="macro-value">{m.fiber_g}</div>
                <div className="macro-unit">grams</div>
                <div className="macro-label">Dietary Fiber</div>
              </div>
              <div className="macro-card macro-water">
                <div className="macro-icon">💧</div>
                <div className="macro-value">{m.water_liters}</div>
                <div className="macro-unit">Liters</div>
                <div className="macro-label">Water Hydration</div>
              </div>
            </div>
            
            <div style={{ display: 'flex', gap: '16px', marginTop: '16px', fontSize: '13px', color: 'var(--text-muted)' }}>
              <span>BMR (Basal Metabolic Rate): <strong>{m.bmr} kcal</strong></span>
              <span>•</span>
              <span>TDEE (Total Expenditure): <strong>{m.tdee} kcal</strong></span>
            </div>
          </div>
        )}

        {/* Quick Body Details Recalculator */}
        <div className="card" style={{ marginBottom: '48px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '16px' }}>Adjust Body Data & Recalculate</h3>
          <form onSubmit={handleRecalculate}>
            <div className="form-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))' }}>
              <div className="form-group">
                <label className="form-label">Weight (kg)</label>
                <input className="form-input" type="number" value={bodyForm.weight} onChange={(e) => setBodyForm({ ...bodyForm, weight: e.target.value })} required />
              </div>
              <div className="form-group">
                <label className="form-label">Height (cm)</label>
                <input className="form-input" type="number" value={bodyForm.height} onChange={(e) => setBodyForm({ ...bodyForm, height: e.target.value })} required />
              </div>
              <div className="form-group">
                <label className="form-label">Age</label>
                <input className="form-input" type="number" value={bodyForm.age} onChange={(e) => setBodyForm({ ...bodyForm, age: e.target.value })} required />
              </div>
              <div className="form-group">
                <label className="form-label">Activity Level</label>
                <select className="form-select" value={bodyForm.activity_level} onChange={(e) => setBodyForm({ ...bodyForm, activity_level: e.target.value })}>
                  <option value="sedentary">Sedentary</option>
                  <option value="light">Light</option>
                  <option value="moderate">Moderate</option>
                  <option value="active">Active</option>
                  <option value="very_active">Very Active</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Fitness Goal</label>
                <select className="form-select" value={bodyForm.fitness_goal} onChange={(e) => setBodyForm({ ...bodyForm, fitness_goal: e.target.value })}>
                  <option value="weight_loss">Weight Loss</option>
                  <option value="muscle_gain">Muscle Gain</option>
                  <option value="maintain">Maintain</option>
                  <option value="endurance">Endurance</option>
                </select>
              </div>
            </div>
            <button type="submit" className="btn btn-primary btn-sm" disabled={calculating}>
              {calculating ? 'Calculating...' : 'Recalculate Targets'}
            </button>
          </form>
        </div>

        {/* Meal Suggestions */}
        <div style={{ marginBottom: '48px' }}>
          <h2 style={{ fontSize: '22px', fontWeight: 800, marginBottom: '20px' }}>Suggested Meal Ideas</h2>
          {meals.map((mGroup) => (
            <div key={mGroup.meal_time} className="meal-section">
              <div className="meal-section-title">{mGroup.meal_time.toUpperCase()}</div>
              <div className="meal-options">
                {mGroup.options.map((opt, idx) => (
                  <div key={idx} className="meal-card">
                    <div className="meal-card-name">{opt.name}</div>
                    <div className="meal-card-desc">{opt.description}</div>
                    <div className="meal-card-macros">{opt.macros}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Recommended Foods Database */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '20px' }}>
            <h2 style={{ fontSize: '22px', fontWeight: 800 }}>Food Database & Recommendations</h2>
            <div style={{ display: 'flex', gap: '12px' }}>
              <select className="form-select" style={{ width: 'auto' }} value={foodCategory} onChange={(e) => setFoodCategory(e.target.value)}>
                <option value="">All Categories</option>
                <option value="protein">Proteins</option>
                <option value="carbohydrate">Carbohydrates</option>
                <option value="fat">Healthy Fats</option>
                <option value="fiber">Fiber / Veggies</option>
              </select>
              <select className="form-select" style={{ width: 'auto' }} value={dietaryTag} onChange={(e) => setDietaryTag(e.target.value)}>
                <option value="">All Diets</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
              </select>
            </div>
          </div>

          <div className="food-grid">
            {foods.map((f) => (
              <div key={f.id} className="food-card">
                <div className="food-card-name">{f.name}</div>
                <div className="food-card-desc">{f.description}</div>
                <div className="food-macros">
                  <div className="food-macro"><div className="food-macro-val">{f.calories_per_100g}</div><div className="food-macro-key">kcal</div></div>
                  <div className="food-macro"><div className="food-macro-val">{f.protein_g}g</div><div className="food-macro-key">Prot</div></div>
                  <div className="food-macro"><div className="food-macro-val">{f.carbs_g}g</div><div className="food-macro-key">Carb</div></div>
                  <div className="food-macro"><div className="food-macro-val">{f.fat_g}g</div><div className="food-macro-key">Fat</div></div>
                </div>
                {f.dietary_tags && f.dietary_tags.length > 0 && (
                  <div className="food-tags">
                    {f.dietary_tags.map((t) => <span key={t} className="food-tag">{t}</span>)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="disclaimer">
          ⚠️ <strong>Medical Disclaimer:</strong> {nutrition?.disclaimer || "All nutrition information provided on this platform is for general educational and fitness estimation purposes only. It is not intended as medical advice or personalized clinical prescription. Consult a qualified medical practitioner or nutritionist prior to starting any rigorous diet program."}
        </div>
      </div>
    </div>
  );
}
