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
# da86-2401-4900-60e9-97b6-d553-248f-608b-f6ac.ngrok-free.app (this kepis use for ngrok service its helps to run the server locally for some specific time )

# DEBUG = True
# SESSION_COOKIE_SECURE = False  
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost','da86-2401-4900-60e9-97b6-d553-248f-608b-f6ac.ngrok-free.app']
# SECURE_SSL_REDIRECT = False


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

# this is not a mandatory for local prodution

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
  # Place media files in a directory outside of STATIC_ROOT


# password reset setting

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # Use your email service provider's SMTP server
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
# SITE_URL = 'http://127.0.0.1:8000'




# --------------------------------------------------------------
# for production process

DEBUG = os.environ.get('DEBUG', 'False') == 'True'


# ______________________________________________

# Load allowed hosts from environment variable



# this line use for both local and production

# ------------------------------------------------------
# for production process

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

ALLOWED_HOSTS = ['ooye.in', 'www.ooye.in', 'ooye-59a192f7481a.herokuapp.com']

# comment this line if we plan to run this in local terminal
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SITE_URL = "https://ooye.in"

# ----------------------------------------------------------------------

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
    'django_extensions',
    'cloudinary',  # add this
    'cloudinary_storage',  # add this
    'pwa',
    # 'django_csp',
    

]


import environ
import cloudinary


env = environ.Env()
environ.Env.read_env()


# Direct URL Configuration (CLOUDINARY_URL)

CLOUDINARY_URL = env('CLOUDINARY_URL')  # Load from .env file or environment variables

cloudinary.config(secure=env.bool('CLOUDINARY_SECURE', default=True))

# Separate Parameter Configuration (cloudinary.config(...))

# Cloudinary configuration
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
#     'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
#     'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
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


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ensure this is set


# for sicoal authanticatuon

MEDIA_URL = '' 
 # Ensure MEDIA_URL is distinct from STATIC_URL
STATIC_URL = '/static/'



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


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }



# ztjh fdxk rytu vnef
# Add logging


