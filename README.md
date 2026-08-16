# Praveen Gym Portal

> **Train Smart. Eat Better. Become Stronger.**

Praveen Gym Portal is a full-stack digital web application built for physical gym management. It enables member registration, gender-tailored 6-day workout plans, a manual cash-first Premium activation flow, and an exclusive Premium diet & nutrition portal.

---

## 🌟 Key Features

### 👤 Member Portal
* **Registration & Auth**: Register with Name, Email, Password, Gender, Age, Height, Weight, Phone, Fitness Goal, and Dietary Preference.
* **Weekly Workout Plan**: Gender-specific workout routines for Monday through Saturday.
* **Sunday Rest Day**: Automatically detects Sunday and presents recovery advice.
* **Today's Workout**: Auto-detects the current day of the week and presents the scheduled exercises with sets, reps, and image cards.

### ⭐ Premium Membership & Diet Portal
* **Cash-First Activation**: No online payment gateway. Members pay in cash at the physical gym. Admins verify payment and activate Premium manually.
* **Personalised Nutrition Calculator**: Calculates Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the Harris-Benedict formula.
* **Macro Targets**: Provides daily estimates for Calories, Protein (2g/kg), Carbohydrates, Healthy Fats, Fiber, and Water intake.
* **Food Database**: Categorised foods (Proteins, Carbs, Fats, Fiber) with vegetarian/vegan tag filtering.
* **Meal Suggestions**: Goal-oriented meal ideas for breakfast, lunch, dinner, and snacks.

### 🛡️ Admin Dashboard
* **Statistics Overview**: Real-time stats on total, standard, premium, active/disabled, and male/female member counts.
* **Member Management**: Search, filter by gender or membership status, enable/disable accounts, and activate/remove Premium.
* **Workout Management**: Modify male/female workout plans and exercises per day.
* **Food Management**: Add and delete items in the food database.

---

## 🛠️ Tech Stack

* **Frontend**: React 18, Vite, React Router v6, Axios, Vanilla CSS (Design Tokens & CSS Variables).
* **Backend**: Python, FastAPI, Motor (Async MongoDB), Pydantic v2, PyJWT, Passlib (bcrypt).
* **Database**: MongoDB Atlas M0 (Free Tier).
* **Hosting**: Vercel (Frontend), Render.com (Backend Web Service).
* **Email**: Resend.com Free Tier (or SMTP).

---

## 🚀 Local Setup & Development

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
MONGODB_URL=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=praveen_gym
JWT_SECRET=your_super_secret_jwt_key_at_least_32_characters
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxx
FRONTEND_URL=http://localhost:5173
```

Run the backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Database Seeding & Admin Creation

Run the administrative scripts against your MongoDB Atlas instance:

```bash
# Create initial Admin account
python scripts/create_admin.py

# Seed initial workout plans (Male/Female Mon-Sat) & food database
python scripts/seed_data.py
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## ☁️ Free-Tier Online Deployment Guide

### A. MongoDB Atlas Database (Free M0 Cluster)
1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create an **M0 Free Cluster**.
3. Under **Network Access**, add `0.0.0.0/0` (Allow access from anywhere for Render deployment).
4. Under **Database Access**, create a database user and copy the connection string.

### B. Backend Deployment (Render.com)
1. Sign up at [Render.com](https://render.com).
2. Click **New +** → **Web Service**.
3. Connect your GitHub repository containing the project.
4. Set **Root Directory** to `backend`.
5. Set **Build Command**: `pip install -r requirements.txt`
6. Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add Environment Variables:
   * `MONGODB_URL`: Your MongoDB Atlas URL
   * `DATABASE_NAME`: `praveen_gym`
   * `JWT_SECRET`: Random 32+ char secret string
   * `FRONTEND_URL`: Your Vercel frontend URL
   * `RESEND_API_KEY`: Resend API key (optional)
8. Deploy the Web Service and copy the live URL (e.g. `https://praveen-gym-backend.onrender.com`).

### C. Frontend Deployment (Vercel)
1. Sign up at [Vercel](https://vercel.com).
2. Click **Add New Project** and import your repository.
3. Set **Root Directory** to `frontend`.
4. Add Environment Variable:
   * `VITE_API_URL`: `https://praveen-gym-backend.onrender.com` (Your Render URL)
5. Click **Deploy**.

---

## 🔒 Security Practices
* Passwords hashed using `bcrypt`.
* JWT Bearer authentication on protected endpoints.
* Backend role-based authorization dependencies (`get_current_admin`, `get_current_premium_member`).
* Secrets stored strictly in environment variables.
* No public endpoints for admin registration.

---

## ⚖️ License & Disclaimer
Nutrition calculations are general estimates based on standard fitness formulas and do not substitute for professional medical advice.
