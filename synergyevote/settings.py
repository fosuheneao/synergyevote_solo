"""
Django settings for synergyevote project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gou!a@bp-&_!_ua)4&_b9u86q3pes&2!q2f52-64p4!%+y5w)p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    #'django_tenants', # Django-Tenants must be the first app
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    #'api',  # Make sure this is included
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',  # Swagger Documentation
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'govote.apps.GovoteConfig',
    #'gotenant.apps.GotenantConfig',
]

#DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)

MIDDLEWARE = [
    #'django_tenants.middleware.TenantMainMiddleware',  # Must be first!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'synergyevote.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [BASE_DIR, 'templates'],
        "DIRS": [os.path.join(BASE_DIR, "govote/templates")],  # Custom templates directory
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

TEMPLATES[0]["DIRS"] = [os.path.join(BASE_DIR, "govote/templates")]
STATICFILES_DIRS = [os.path.join(BASE_DIR, "govote/static")]

WSGI_APPLICATION = 'synergyevote.wsgi.application'
DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)
# #DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Still using MySQL
        'NAME': 'db_aogovote_cop25',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        "OPTIONS": {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            'charset': 'utf8mb4',
            "autocommit": True,
        }
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django_tenants.postgresql_backend',  # Required for django-tenants
#         'NAME': 'db_aogovote',
#         'USER': 'postgres',
#         'PASSWORD': 'sajetAdmin',
#         'HOST': 'localhost',  # Or your database host
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Add this to specify where collected static files will be placed
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Ensure BASE_DIR is set in your settings

# Optionally, if you have custom static files (CSS, JS, images), ensure this is set
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',  # This should be the path where your custom static files are stored
# ]
# Ensure STATICFILES_DIRS is also defined:
STATICFILES_DIRS = [os.path.join(BASE_DIR, "govote/static")]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'