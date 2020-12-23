import os
import json
from six.moves.urllib import request
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from django.core.exceptions import ImproperlyConfigured


def setting(parameter, accept_empty=False):
    try:
        return os.environ[parameter]
    except KeyError:
        if not accept_empty:
            raise ImproperlyConfigured(f'Set the {parameter} parameter')

        return None

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = setting('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = setting('DEBUG', accept_empty=True) == "True"

ALLOWED_HOSTS = [setting('ALLOWED_HOST')]

FRONTEND_HOST = setting('FRONTEND_HOST', accept_empty=True)

CORS_ORIGIN_WHITELIST = []

if DEBUG:
    CORS_ORIGIN_WHITELIST.extend([
        'http://127.0.0.1:8080',
        'http://localhost:8080'
    ])

if FRONTEND_HOST:
    CORS_ORIGIN_WHITELIST.append(f'https://{FRONTEND_HOST}')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'recipes.apps.RecipesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'recipes_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'recipes_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': setting('APP_USER') if not DEBUG else 'postgres',
        'HOST': setting('DB_HOST'),
        'PASSWORD': setting('APP_USER_PASSWORD')if not DEBUG else setting('POSTGRES_PASSWORD'),
        'NAME': setting('APP_DB'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

## Set up Auth0 authentication
AUTHENTICATION = setting('AUTHENTICATION')

if AUTHENTICATION == 'Auth0':
    AUTH0_DOMAIN = setting('AUTH0_DOMAIN')
    INSTALLED_APPS.insert(INSTALLED_APPS.index('rest_framework') + 1, 'rest_framework_jwt')
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        )
    }

    API_IDENTIFIER = setting('API_IDENTIFIER', accept_empty=True)
    PUBLIC_KEY = None
    JWT_ISSUER = None

    jsonurl = request.urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read().decode('utf-8'))
    cert = f"-----BEGIN CERTIFICATE-----\n{jwks['keys'][0]['x5c'][0]}\n-----END CERTIFICATE-----"
    certificate = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
    PUBLIC_KEY = certificate.public_key()
    JWT_ISSUER = f'https://{AUTH0_DOMAIN}/'

    def jwt_get_username_from_payload_handler(payload): # pylint: disable=unused-argument
        return setting('AUTH0_USERNAME', accept_empty=True)

    JWT_AUTH = {
        'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
        'JWT_PUBLIC_KEY': PUBLIC_KEY,
        'JWT_ALGORITHM': 'RS256',
        'JWT_AUDIENCE': API_IDENTIFIER,
        'JWT_ISSUER': JWT_ISSUER,
        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    }
