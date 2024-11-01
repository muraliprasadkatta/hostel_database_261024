"""
Django settings for hosteldb20 project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# -----------------------------------------------------
# for local host

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# SESSION_COOKIE_SECURE = False  
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# ALLOWED_HOSTS = []


# # Database Configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT'),
#     }
# }


# ______________________________________________
# for production process

# DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# its should be ture in production 
# SESSION_COOKIE_SECURE = True  
# CSRF_COOKIE_SECURE = True  


# Load allowed hosts from environment variable
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# ALLOWED_HOSTS = ['ooye.in', 'www.ooye.in', 'ooye-59a192f7481a.herokuapp.com']


# this line use for both local and production

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


import dj_database_url
DEBUG = False
SESSION_COOKIE_SECURE = True  
CSRF_COOKIE_SECURE = True 

import os
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# comment this line if we plan to run this in local terminal
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # for auto commas and rupee symbol
    'hostelapp20',
    'django.contrib.sites',
    'social_django',  # add this
    'rest_framework',
    'django.contrib.sitemaps',
    'cloudinary',  # add this
    'cloudinary_storage',  # add this
]
import environ

env = environ.Env()
environ.Env.read_env()

CLOUDINARY_URL = env('CLOUDINARY_URL')  
# Load from .env file or environment variables

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}


# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'dkvy141bt',
#     'API_KEY': '874815941261685',
#     'API_SECRET': 'TYrM78ydt8WXmhVUWbYvdo3BNZQ',
# }


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hostelapp20.middleware.social_auth_middleware.SocialAuthExceptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line

]


#social app custom settings
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
  
]

# Google OAuth Credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# LOGIN_REDIRECT_URL = 'dashboard'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/dashboard/'  # URL to redirect after login
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login_and_registration/'  # URL to redirect after a failed login

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',  # Gather details from the social provider
    'social_core.pipeline.social_auth.social_uid',      # Extract the user ID from the social provider
    'social_core.pipeline.social_auth.auth_allowed',    # Check if authentication is allowed
    'social_core.pipeline.social_auth.social_user',     # Associates current social details with a user account
    'hostelapp20.pipeline.handle_user_email',           # Custom function to handle email checks
    'social_core.pipeline.user.get_username',           # Get a username for the new user
    'social_core.pipeline.user.create_user',            # Create a new user account if one does not exist
    'social_core.pipeline.social_auth.associate_user',  # Associate the social account with the user
    'social_core.pipeline.social_auth.load_extra_data', # Load extra data from the social provider
    'social_core.pipeline.user.user_details',           # Populate the user details
)

SOCIAL_AUTH_STRATEGY = 'hostelapp20.strategies.CustomSocialStrategy'  #for this 


# ------------------------------------------------------------------------

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'


ROOT_URLCONF = 'hosteldb20.urls'
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  #dd this 

            ],
        },
    },
]

WSGI_APPLICATION = 'hosteldb20.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# settings.py




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ensure this is set


# for sicoal authanticatuon

MEDIA_URL = '/media/'  # Ensure MEDIA_URL is distinct from STATIC_URL
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Place media files in a directory outside of STATIC_ROOT

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  ## for static folder

## if the 'auth.User', which has been swapped out  use custom user
AUTH_USER_MODEL = 'hostelapp20.CustomUser'  ## for abstract user

## Define the path to the static/media directory

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Email Configuration
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# ztjh fdxk rytu vnef
# Add logging



