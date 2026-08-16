import React from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function Membership() {
  const { user } = useAuth();
  const isPremium = user?.membership_type === 'premium';

  return (
    <div className="page">
      <div className="container-md" style={{ paddingTop: '40px', paddingBottom: '60px' }}>
        <div className="card" style={{ marginBottom: '32px' }}>
          <div className="card-header">
            <h1 className="card-title" style={{ fontSize: '24px' }}>My Membership Status</h1>
            <span className={`badge ${isPremium ? 'badge-premium' : 'badge-standard'}`}>
              {isPremium ? '⭐ Premium Active' : 'Standard Member'}
            </span>
          </div>

          {isPremium ? (
            <div className="alert alert-success">
              🎉 Your <strong>Premium Membership</strong> is active! You have full access to personalised diet plans, food recommendations, and macro calculators.
            </div>
          ) : (
            <div className="alert alert-info">
              ℹ️ You currently have a <strong>Standard Membership</strong>. Upgrade to Premium to unlock personalised nutrition guidance!
            </div>
          )}

          <div className="profile-grid" style={{ marginTop: '20px' }}>
            <div className="profile-field">
              <div className="profile-field-label">Member ID</div>
              <div className="profile-field-value">{user?.id}</div>
            </div>
            <div className="profile-field">
              <div className="profile-field-label">Membership Type</div>
              <div className="profile-field-value" style={{ textTransform: 'capitalize' }}>{user?.membership_type}</div>
            </div>
            <div className="profile-field">
              <div className="profile-field-label">Member Since</div>
              <div className="profile-field-value">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </div>
            </div>
            <div className="profile-field">
              <div className="profile-field-label">Premium Activated Date</div>
              <div className="profile-field-value">
                {user?.premium_activated_at ? new Date(user.premium_activated_at).toLocaleDateString() : 'Not Activated'}
              </div>
            </div>
          </div>
        </div>

        {/* Cash Activation Info Box */}
        {!isPremium && (
          <div className="premium-upsell" style={{ textAlignment: 'left' }}>
            <h2 style={{ fontSize: '22px', fontWeight: 800, marginBottom: '12px' }}>How to Upgrade to Premium</h2>
            <p style={{ color: 'var(--text-muted)', marginBottom: '20px' }}>
              We do not accept online payments. Please follow these simple steps to activate Premium:
            </p>
            <ol style={{ textAlign: 'left', margin: '0 auto 24px', maxWidth: '500px', lineHeight: 1.8, color: 'var(--text-muted)' }}>
              <li>Visit <strong>Praveen Gym</strong> physically in person.</li>
              <li>Pay your Premium membership fee in cash at the main counter.</li>
              <li>The Gym Admin will activate your account on their dashboard.</li>
              <li>You will receive a confirmation email and immediate access to Diet features!</li>
            </ol>
          </div>
        )}
      </div>
    </div>
  );
}
