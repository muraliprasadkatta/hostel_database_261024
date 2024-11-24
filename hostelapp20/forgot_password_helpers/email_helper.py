from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

# Create a logger
logger = logging.getLogger(__name__)

def send_reset_email(email, token):
    subject = "Reset Your Password"
    # reset_link = f"{settings.SITE_URL}/change-password/{token}/"
    reset_link = f"{settings.SITE_URL}/forget-password/{token}/"

    text_content = (
        f"Hi,\n\n"
        f"You requested to reset your password. Click the link below to reset it:\n\n"
        f"{reset_link}\n\n"
        f"If you did not make this request, you can ignore this email."
    )
    html_content = f"""
    <p>Hi,</p>
    <p>You requested to reset your password. Click the link below to reset it:</p>
    <a href="{reset_link}" style="background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-size: 16px;">Reset Password</a>
    <p>If you did not make this request, you can ignore this email.</p>
    """
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f"Password reset email sent to {email} successfully.")
        return {"success": True, "message": "Email sent successfully."}
    except Exception as e:
        logger.error(f"Error sending email to {email}. Token: {token}, Reset link: {reset_link}. Error: {e}")
        return {"success": False, "message": f"Error: {e}"}
