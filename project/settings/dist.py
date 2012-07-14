# coding=utf8
#
#COPY THIS FILE TO "local.py"
#

ADMINS = (
    ('Kovalenko Pavel', 'pavel@bitrain.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default':{
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     '',
        'USER':     '',
        'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

DEBUG = True
TEMPLATE_DEBUG = True

DEFAILT_FROM = "root@localhost"
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
