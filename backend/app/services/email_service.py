import httpx
from app.config import get_settings

settings = get_settings()


def _get_html_base(title: str, body_content: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f0f; color: #e0e0e0; margin: 0; padding: 0; }}
    .container {{ max-width: 600px; margin: 40px auto; background: #1a1a1a; border-radius: 16px; overflow: hidden; border: 1px solid #2a2a2a; }}
    .header {{ background: linear-gradient(135deg, #ff6b35, #f7c59f); padding: 40px 32px; text-align: center; }}
    .header h1 {{ margin: 0; color: #0f0f0f; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }}
    .header p {{ margin: 8px 0 0; color: #0f0f0f; opacity: 0.7; font-size: 14px; }}
    .body {{ padding: 40px 32px; }}
    .body h2 {{ color: #ff6b35; margin-top: 0; }}
    .body p {{ color: #b0b0b0; line-height: 1.7; }}
    .highlight {{ background: #252525; border-left: 4px solid #ff6b35; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 20px 0; }}
    .highlight p {{ margin: 0; color: #e0e0e0; }}
    .btn {{ display: inline-block; background: linear-gradient(135deg, #ff6b35, #ff8c42); color: #fff !important; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 700; font-size: 15px; margin: 20px 0; }}
    .features {{ background: #252525; border-radius: 12px; padding: 20px; margin: 20px 0; }}
    .features ul {{ margin: 8px 0; padding-left: 20px; color: #b0b0b0; }}
    .features li {{ padding: 4px 0; }}
    .footer {{ padding: 24px 32px; text-align: center; border-top: 1px solid #2a2a2a; }}
    .footer p {{ color: #555; font-size: 12px; margin: 0; }}
    .badge {{ display: inline-block; background: #ff6b35; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
    .premium-badge {{ background: linear-gradient(135deg, #FFD700, #FFA500); color: #0f0f0f; }}
  </style>
</head>
<body>
  <div class="container">
    {body_content}
    <div class="footer">
      <p>© 2024 Praveen Gym Portal &nbsp;|&nbsp; Train Smart. Eat Better. Become Stronger.</p>
      <p style="margin-top:8px;">This is an automated message. Please do not reply to this email.</p>
    </div>
  </div>
</body>
</html>"""


async def send_registration_email(name: str, email: str, membership_type: str = "standard"):
    subject = "Welcome to Praveen Gym Portal! 🏋️"
    body_content = f"""
    <div class="header">
      <h1>🏋️ Praveen Gym Portal</h1>
      <p>Train Smart. Eat Better. Become Stronger.</p>
    </div>
    <div class="body">
      <h2>Welcome, {name}! 🎉</h2>
      <p>Your registration is successful. You are now a member of <strong>Praveen Gym Portal</strong>.</p>
      <div class="highlight">
        <p>📧 <strong>Email:</strong> {email}</p>
        <p>🏅 <strong>Membership:</strong> <span class="badge">{membership_type.upper()}</span></p>
      </div>
      <p>With your Standard membership you can access:</p>
      <div class="features">
        <ul>
          <li>📅 Weekly workout plan (Mon–Sat)</li>
          <li>💪 Today's personalised workout</li>
          <li>👤 Your profile and membership info</li>
          <li>😴 Sunday rest day tracking</li>
        </ul>
      </div>
      <p><strong>Want to unlock Premium features?</strong></p>
      <p>Visit the gym, pay at the counter in cash, and our Admin will activate your Premium membership — giving you access to full diet guidance, nutrition calculations, and meal suggestions tailored to your goals.</p>
      <a href="{settings.FRONTEND_URL}/login" class="btn">Login to Portal →</a>
    </div>
    """
    html_content = _get_html_base(subject, body_content)
    await _send_email(to_email=email, subject=subject, html_content=html_content)


async def send_premium_activation_email(name: str, email: str, activated_by: str):
    subject = "🌟 Your Premium Membership is Active! — Praveen Gym Portal"
    body_content = f"""
    <div class="header">
      <h1>🏋️ Praveen Gym Portal</h1>
      <p>Train Smart. Eat Better. Become Stronger.</p>
    </div>
    <div class="body">
      <h2>Congratulations, {name}! ⭐</h2>
      <p>Your <span class="badge premium-badge">PREMIUM</span> membership has been activated by our team.</p>
      <div class="highlight">
        <p>✅ <strong>Status:</strong> Premium Active</p>
        <p>👤 <strong>Activated by:</strong> {activated_by}</p>
      </div>
      <p>You now have access to all Premium features:</p>
      <div class="features">
        <ul>
          <li>🥗 Personalised diet guidance</li>
          <li>🧮 Nutrition calculator (Calories, Protein, Carbs, Fat, Fiber)</li>
          <li>💧 Daily water intake guidance</li>
          <li>🍱 Meal suggestions based on your goals</li>
          <li>🥦 Food recommendations by category</li>
          <li>📊 Macro tracking estimates</li>
        </ul>
      </div>
      <p>Login now and explore your Premium Diet section!</p>
      <a href="{settings.FRONTEND_URL}/diet" class="btn">Open Diet Section →</a>
      <p style="font-size:12px; color:#555; margin-top:24px;">
        ⚠️ All nutrition information is general guidance only and not medical advice.
        Consult a qualified nutritionist for personalised recommendations.
      </p>
    </div>
    """
    html_content = _get_html_base(subject, body_content)
    await _send_email(to_email=email, subject=subject, html_content=html_content)


async def _send_email(to_email: str, subject: str, html_content: str):
    if not settings.RESEND_API_KEY or settings.RESEND_API_KEY == "":
        print(f"[EMAIL SKIPPED - No API key] To: {to_email}, Subject: {subject}")
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": f"Praveen Gym Portal <{settings.FROM_EMAIL}>",
                    "to": [to_email],
                    "subject": subject,
                    "html": html_content,
                },
                timeout=10,
            )
            if response.status_code in (200, 201):
                print(f"✅ Email sent to {to_email}")
            else:
                print(f"❌ Email failed: {response.status_code} — {response.text}")
    except Exception as e:
        print(f"❌ Email error: {e}")
