from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'flickerp',
        'USER':     'yogesh',
        'PASSWORD': '123',
        'HOST':     '127.0.0.1',
        'PORT':     '5432',
    }
}
MEDIA_URL = '/media/'


WEBSITE_NAME="Golden Eagle It technologies Pvt Ltd"

WEBSITE_SORT_NAME="GEITPL"


ADMIN_EMAIL = "django.work@gmail.com"

SLACK_BOT_TOKEN = "xoxb-63098719655-1608958077714-53yiPBV6SpjkjmJDuyIgTNTj"