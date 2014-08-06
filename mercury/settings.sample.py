"""
Django settings for mercury project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True or os.environ.get("DJANGO_DEBUG") # Change for production

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    ### Generic Apps
    'phsauth',
    'config',
    ### Mercury Apps
    'voting',
    'codecompetitions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'phsauth.middleware.RequireLoginMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'phsauth.ldap.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_DIRS = (
    'templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "config.context_processors.configuration",
    "mercury.context_processors.base",
    "mercury.context_processors.sidebar",
)

ROOT_URLCONF = 'mercury.urls'

WSGI_APPLICATION = 'mercury.wsgi.application'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    0: 'primary',
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static_resources/'
STATIC_ROOT = os.path.join(BASE_DIR,"managed_resources/staticfiles")
STATICFILES_DIRS = (
    "static",
)

MEDIA_URL = '/media_resources/'
MEDIA_ROOT = os.path.join(BASE_DIR,"managed_resources/mediafiles")

PRIVATE_ROOT = os.path.join(BASE_DIR,"privatefiles")

LDAP_SERVER = ""
LDAP_SEARCH_BASE = ""
LDAP_MASTER_USERNAME = ""
LDAP_MASTER_PASSWORD = ""

LDAP_GROUP_MAPPINGS = {
    "school": (),
    "type": ("students","faculty"),
}
