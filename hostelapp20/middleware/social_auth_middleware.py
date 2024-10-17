# middleware.py
from social_core.exceptions import AuthAlreadyAssociated, AuthCanceled
from django.shortcuts import redirect, render
from django.contrib import messages

class SocialAuthExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            messages.error(request, "This social account is already associated with another account.")
            return render(request, 'errors_handilings/social_auth_error.html')
        elif isinstance(exception, AuthCanceled):
            messages.error(request, "Authentication process was canceled.")
            return redirect('login_and_registration')  # Redirect to the login and registration page
        return None
