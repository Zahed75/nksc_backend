# import logging
# from datetime import timedelta
# from pathlib import Path
# import os
# import pymysql

# # Monkey patch for Django to work with PyMySQL
# pymysql.version_info = (2, 2, 1, "final", 0)
# pymysql.install_as_MySQLdb()


# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# MEDIA_DIR = os.path.join(BASE_DIR, 'media')
# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-1gm7eozzeu3ac8c6_rycbegs6x3*hxu%z_^bnthml(qrhr%50_'

# DEBUG = True
# PRODUCTION = False

# ALLOWED_HOSTS = []

# # Application definition
# INSTALLED_APPS = [

#     # Django core
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third-party
#     "rest_framework",
#     'rest_framework_simplejwt',
#     "drf_spectacular",
#     "corsheaders",

#     "django_cleanup.apps.CleanupConfig",
#     "ckeditor",

#     "journal",
#     "media_stuff",
#     "news",
#     "staff",
#     "publications",
#     "user_management",
#     "about",
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'nksc_backend.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [TEMPLATES_DIR],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'nksc_backend.wsgi.application'

# # Database
# # Database configuration
# if PRODUCTION:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'nksc_db',
#             'USER': 'root',
#             'PASSWORD': '',
#             'HOST': 'localhost',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#                 'charset': 'utf8mb4',
#             }
#         }
#     }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# REST_FRAMEWORK = {
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework.authentication.SessionAuthentication",
#         "rest_framework.authentication.BasicAuthentication",
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.AllowAny",
#     ),
# }

# SPECTACULAR_SETTINGS = {
#     "TITLE": "Nazmul Karim Study-Center API University Of Dhaka ",
#     "DESCRIPTION": "NKSC Backend APIs-Zahed Hasan",
#     "VERSION": "1.0.0",
#     "SERVE_INCLUDE_SCHEMA": True,
# }


# # Optional: Suppress warnings

# logging.getLogger('drf_spectacular').setLevel(logging.ERROR)

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': False,
#     'UPDATE_LAST_LOGIN': False,
#     'ALGORITHM': 'HS256',
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#     'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
#     'JTI_CLAIM': 'jti',
#     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
#     'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
#     'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
#     'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
#     'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
#     'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
#     'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
# }

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA_URL = '/media/'
# MEDIA_ROOT = MEDIA_DIR
# # CSRF and CORS settings
# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:4200",
#     "http://localhost:4300",
#     "http://localhost:3000",
#     'https://postcodes.io/',

# ]

# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:4200",
#     "http://localhost:4300",
#     "http://localhost:3000",

# ]

# # For development, keep these False
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False

# # CSRF settings for DRF - ADD THESE
# CSRF_USE_SESSIONS = False
# CSRF_COOKIE_HTTPONLY = False

# # Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'syscomatic.technologies@gmail.com'
# EMAIL_HOST_PASSWORD = 'nckp gdyt pppw axch'

# FRONTEND_LOGIN_URL = 'http://localhost:4200/'


# # CKEditor Configuration
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',
#         'height': 400,
#         'width': '100%',
#         'extraPlugins': ','.join([
#             'codesnippet',
#             'widget',
#             'dialog',
#         ]),
#         'toolbar_Custom': [
#             ['Bold', 'Italic', 'Underline', 'Strike'],
#             ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
#             ['Link', 'Unlink', 'Anchor'],
#             ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
#             ['Styles', 'Format', 'Font', 'FontSize'],
#             ['TextColor', 'BGColor'],
#             ['Maximize', 'ShowBlocks'],
#             ['CodeSnippet', 'Source'],
#         ],
#         'codeSnippet_theme': 'monokai',
#     },
#     'minimal': {
#         'toolbar': [
#             ['Bold', 'Italic', 'Underline', 'Strike'],
#             ['NumberedList', 'BulletedList'],
#             ['Link', 'Unlink'],
#             ['RemoveFormat', 'Source']
#         ],
#         'height': 150,
#         'width': '100%',
#     }
# }

# # CKEditor upload path
# CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_IMAGE_BACKEND = "pillow"
# CKEDITOR_ALLOW_NONIMAGE_FILES = False
# CKEDITOR_RESTRICT_BY_USER = True


import logging
from datetime import timedelta
from pathlib import Path
import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Monkey patch for Django to work with PyMySQL
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Create required directories
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'staticfiles'), exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
# Get from .env, fallback to development key
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'django-insecure-1gm7eozzeu3ac8c6_rycbegs6x3*hxu%z_^bnthml(qrhr%50_')

# Get DEBUG and PRODUCTION from .env
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'

# ALLOWED_HOSTS from .env
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

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
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware
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

# Database configuration - FIXED VERSION
if PRODUCTION:
    # Production database (uses DATABASE_* variables)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nksc_db',
            'USER': 'root',           # Using root user
            'PASSWORD': 'Nksc@2026',  # Your password
            'HOST': 'nksc-mysql',     # MySQL container name
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        }
    }
else:
    # Development database (uses DEV_DB_* variables)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DEV_DB_NAME', 'nksc_db'),
            'USER': os.getenv('DEV_DB_USER', 'root'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD', 'Nksc@2026'),
            # Fixed: default to nksc-mysql
            'HOST': os.getenv('DEV_DB_HOST', 'nksc-mysql'),
            'PORT': os.getenv('DEV_DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
    }
    print(
        f"DEVELOPMENT MODE: Using database host: {os.getenv('DEV_DB_HOST', 'nksc-mysql')}")

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
    "TITLE": "Nazmul Karim Study-Center API University Of Dhaka ",
    "DESCRIPTION": "NKSC Backend APIs-Zahed Hasan",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
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
    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
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

# CSRF and CORS settings from .env
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS', 'http://localhost:4200,http://localhost:4300,http://localhost:3000').split(',')
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS', 'http://localhost:4200,http://localhost:4300,http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# Security settings based on PRODUCTION flag
if PRODUCTION:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

# CSRF settings for DRF
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# Email settings from .env
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv(
    'EMAIL_HOST_USER', 'syscomatic.technologies@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'nckp gdyt pppw axch')

FRONTEND_LOGIN_URL = os.getenv('FRONTEND_LOGIN_URL', 'http://localhost:4200/')

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
            ['NumberedList', 'BulletedList', '-',
                'Outdent', 'Indent', '-', 'Blockquote'],
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

# Simplified logging to avoid file errors
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
