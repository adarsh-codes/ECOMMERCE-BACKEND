import smtplib
from app.core.config import settings


def send_reset_email(to_email, token):
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_FROM, settings.SMTP_PASSWORD)
        message = f"Subject: Reset Your Password\n\nClick to reset: http://localhost:8000/reset?token={token}"
        server.sendmail(settings.EMAIL_FROM, to_email, message)
