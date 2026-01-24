import logging
from datetime import timedelta
from pathlib import Path
import os
import pymysql

# Monkey patch for Django to work with PyMySQL
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1gm7eozzeu3ac8c6_rycbegs6x3*hxu%z_^bnthml(qrhr%50_'

DEBUG = True
PRODUCTION = True


# ========== ALLOWED HOSTS ==========
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '103.191.51.224',
    'api.nkscdu.com',
    'www.api.nkscdu.com',
    '.nkscdu.com',
]

# Application definition
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    'rest_framework_simplejwt',
    "drf_spectacular",
    "corsheaders",

    "django_cleanup.apps.CleanupConfig",
    "ckeditor",

    "journal",
    "media_stuff",
    "news",
    "staff",
    "publications",
    "user_management",
    "about",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nksc_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nksc_backend.wsgi.application'

# ========== DATABASE CONFIGURATION WITH IF/ELSE ==========
if PRODUCTION:
    # Production database (Docker container)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nksc_db',
            'USER': 'root',
            'PASSWORD': 'Nksc@2026',  # Your MySQL password
            'HOST': 'nksc-db',  # Docker container name
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
    }
    print("=" * 50)
    print("PRODUCTION MODE: Using Docker MySQL database")
    print(f"Database Host: {DATABASES['default']['HOST']}")
    print("=" * 50)
else:
    # Development database (local machine)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nksc_db',
            'USER': 'root',
            'PASSWORD': '',  # Your local MySQL password (empty for development)
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
    }
    print("=" * 50)
    print("DEVELOPMENT MODE: Using Local MySQL database")
    print(f"Database Host: {DATABASES['default']['HOST']}")
    print("=" * 50)

# Password validation
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

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Nazmul Karim Study-Center API University Of Dhaka",
    "DESCRIPTION": "NKSC Backend APIs-Zahed Hasan",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
    # Add this to fix 500 error
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r'/api/',
}

# Optional: Suppress warnings
logging.getLogger('drf_spectacular').setLevel(logging.ERROR)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# ========== CSRF AND CORS SETTINGS ==========
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:4300",
    "http://localhost:3000",
    "http://103.191.51.224",
    "https://103.191.51.224",
    "http://api.nkscdu.com",
    "https://api.nkscdu.com",
    "http://www.api.nkscdu.com",
    "https://www.api.nkscdu.com",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:4300",
    "http://localhost:3000",
    "http://103.191.51.224",
    "https://103.191.51.224",
    "http://api.nkscdu.com",
    "https://api.nkscdu.com",
    "http://www.api.nkscdu.com",
    "https://www.api.nkscdu.com",
]

# ========== IMPORTANT: NO SSL SETTINGS ==========
# Let aaPanel/nginx handle SSL, NOT Django

# These should be False since nginx handles SSL
CSRF_COOKIE_SECURE = False  # Set to False, nginx handles SSL
SESSION_COOKIE_SECURE = False  # Set to False, nginx handles SSL

CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'syscomatic.technologies@gmail.com'
EMAIL_HOST_PASSWORD = 'nckp gdyt pppw axch'

FRONTEND_LOGIN_URL = 'http://localhost:4200/'

# CKEditor Configuration
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'extraPlugins': ','.join([
            'codesnippet',
            'widget',
            'dialog',
        ]),
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks'],
            ['CodeSnippet', 'Source'],
        ],
        'codeSnippet_theme': 'monokai',
    },
    'minimal': {
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 150,
        'width': '100%',
    }
}

# CKEditor upload path
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True

# Debug output
print("=" * 50)
print(f"DEBUG: {DEBUG}")
print(f"PRODUCTION: {PRODUCTION}")
print(f"Allowed Hosts: {ALLOWED_HOSTS}")
print("=" * 50)
