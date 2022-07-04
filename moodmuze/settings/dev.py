from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jpebtc3!66&4njhc+$u3f0(*))wt44*hkf*l=wcy1z!4=c6pw&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dbname',
#         'HOST': 'localhost',
#         'USER': 'root',
#         'PASSWORD': 'MyPassword'
#     }
# }