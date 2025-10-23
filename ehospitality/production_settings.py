from .settings import *

# SECURITY WARNING: Update this with a real secret key in production
SECRET_KEY = '%+o^zq0n&c0($0p5(we71lq+7x!y0rxqjalm5lsi1=7e@%srfk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
ALLOWED_HOSTS = ['Ramasnampoothiry.pythonanywhere.com']

# Database - Use MySQL on PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Ramasnampoothiry$ehospitality',
        'USER': 'Ramasnampoothiry',
        'PASSWORD': 'MySecure@Pass2024',
        'HOST': 'Ramasnampoothiry.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files
STATIC_ROOT = '/home/Ramasnampoothiry/ehospitality_project/staticfiles'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/home/Ramasnampoothiry/ehospitality_project/media'
MEDIA_URL = '/media/'