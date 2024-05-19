from .formatters import CustomJsonFormatter
import os
from os.path import join
from pathlib import Path
import environ
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_CHANGE_PASSWORD = True
# ACCOUNT_RATE_LIMITS = 1
ACCOUNT_AUTHENTICATION_TIMEOUT = 100

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.postgres',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.socialaccount.providers.openid",
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.steam',


    'basket',
    'products',
    'users',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_FORMS = {
    'change_password': 'users.forms.CustomChangePasswordForm',
    'set_password': 'users.forms.CustomSetPasswordForm',
}

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.associate_by_email',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "allauth.account.middleware.AccountMiddleware",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{'
        },
        'json_formatter': {
            '()': CustomJsonFormatter,
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'information.log',
            'formatter': 'json_formatter',
        },
    },

    'loggers': {
        'main': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

ROOT_URLCONF = 'ProductStore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProductStore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': 5432,
    },
    'TEST': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('TEST_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': 5432,
    }
}

# если запущены тесты, то меняем базу данных на тестовую
if 'test' in sys.argv:
    DATABASES['default'] = DATABASES['TEST']


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


#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LANGUAGE_CODE = 'ru'

AUTH_USER_MODEL = 'users.CustomUser'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'products:main_page'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA__ROOT = join(BASE_DIR, '')

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, "static"),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
