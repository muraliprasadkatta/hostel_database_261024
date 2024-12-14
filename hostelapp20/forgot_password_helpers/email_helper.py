from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    """
    Sends an OTP to the specified email.
    
    Args:
        email (str): The recipient's email address.
        otp (str): The one-time password to be sent.
    
    Returns:
        dict: A dictionary with the success status and a message or error.
    """
    try:
        # Email subject and message
        subject = "Your OTP for Password Reset"
        message = f"Your OTP is {otp}. It is valid for 10 minutes."
        
        # Sending email using Django's send_mail function
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email from settings
            [email],  # Recipient email list
        )

        # If email is sent successfully
        return {"success": True, "message": "OTP sent successfully!"}

    except Exception as e:
        # Log the exception for debugging
        print(f"Error while sending email: {e}")
        
        # Return error response
        return {"success": False, "error": str(e)}
