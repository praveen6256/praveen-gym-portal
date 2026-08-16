import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute';

import Landing from './pages/Landing';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Workouts from './pages/Workouts';
import TodayWorkout from './pages/TodayWorkout';
import Profile from './pages/Profile';
import Membership from './pages/Membership';
import Diet from './pages/Diet';

import AdminDashboard from './pages/admin/AdminDashboard';
import AdminMembers from './pages/admin/AdminMembers';
import AdminWorkouts from './pages/admin/AdminWorkouts';
import AdminFoods from './pages/admin/AdminFoods';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />

          {/* Member Protected Routes */}
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/workouts" element={<ProtectedRoute><Workouts /></ProtectedRoute>} />
          <Route path="/workouts/today" element={<ProtectedRoute><TodayWorkout /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/membership" element={<ProtectedRoute><Membership /></ProtectedRoute>} />

          {/* Premium Protected Routes */}
          <Route path="/diet" element={<ProtectedRoute requirePremium={true}><Diet /></ProtectedRoute>} />

          {/* Admin Protected Routes */}
          <Route path="/admin" element={<ProtectedRoute requireAdmin={true}><AdminDashboard /></ProtectedRoute>} />
          <Route path="/admin/members" element={<ProtectedRoute requireAdmin={true}><AdminMembers /></ProtectedRoute>} />
          <Route path="/admin/workouts" element={<ProtectedRoute requireAdmin={true}><AdminWorkouts /></ProtectedRoute>} />
          <Route path="/admin/foods" element={<ProtectedRoute requireAdmin={true}><AdminFoods /></ProtectedRoute>} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </AuthProvider>
  );
}
