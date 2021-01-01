from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'geitpl_erp',
        'USER':     'geitpl',
        'PASSWORD': '123',
        'HOST':     '127.0.0.1',
        'PORT':     '5432',
    }
}


MEDIA_URL = 'http://erp.geitpl.com/media/'
