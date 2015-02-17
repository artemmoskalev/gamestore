"""
Django settings for gamestore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from authentication.config import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

HEROKU_MODE = False

if 'DYNO' in os.environ:
    HEROKU_MODE = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f$)8e+gt1ox+nfu=&ca_w^2!9mwt$k#pf#wiyxk)u(nnxlj!i5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not HEROKU_MODE

TEMPLATE_DEBUG = not HEROKU_MODE

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gamedata',
    'authentication',
    'developer',
    'player',
    'restapi',
    'social.apps.django_app.default', # For sosial login
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#For sosial login
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)
#For sosial login
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
#For adding sosial account to right user group
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'authentication.pipeline.save_sosial_account_as_player', #This is the custom one
)


ROOT_URLCONF = 'gamestore.urls'

WSGI_APPLICATION = 'gamestore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url

DATABASES = {}

if HEROKU_MODE:
    DATABASES['default'] =  dj_database_url.config()
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# lloks for the static files in the applications during development 
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

#if HEROKU_MODE:
#    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
    

# constants

SECRET_KEY = '16211d879ed0b895303bc8f0047c4166'
SELLER_ID = 'artemesko'

SUCCESS_URL = "http://localhost:8000/payment/success"
CANCEL_URL = "http://localhost:8000/payment/cancel"
ERROR_URL = "http://localhost:8000/payment/error"

# email settings

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'wsdgamingc3210@gmail.com'
EMAIL_HOST_PASSWORD = 'gamestore'
EMAIL_USE_TLS = True

