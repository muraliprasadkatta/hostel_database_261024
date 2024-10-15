
# it is the main role of to access the google auth


import logging
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

logger = logging.getLogger(__name__)

def generate_username_from_email(email):
    return email.split('@')[0]

def handle_user_email(strategy, details, backend, user=None, *args, **kwargs):
    UserModel = get_user_model()
    email = details.get('email')
    request = strategy.request  # This needs to be defined before its first use

    if not user:
        existing_user = UserModel.objects.filter(email=email).first()
        if existing_user:
            logger.info(f"{email} is an existing user. Redirecting to login.")
            messages.error(request, 'This email is already registered. Please log in.')
            return redirect('login_and_registration')
        else:
            username = generate_username_from_email(email)
            new_user = UserModel.objects.create(username=username, email=email)
            new_user.set_unusable_password()
            new_user.save()
            logger.info(f"{email} is a new user. Account has been created.")
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Welcome! Your account has been created.')
            return {'user': new_user, 'is_new': True}
    else:
        # Assuming this else block is meant to handle cases where `user` is not None
        logger.info(f"User {email} logged in through session.")
        return {'user': user, 'is_new': False}

def validate_state(backend, details, response, *args, **kwargs):
    state = backend.strategy.session.get('state')
    if not state:
        logger.error("State missing in session")
    else:
        logger.info(f"State from session: {state}")
    return backend.validate_state()
