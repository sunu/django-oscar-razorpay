import os

from django.utils.translation import ugettext_lazy as _

from oscar.defaults import *
from oscar import OSCAR_MAIN_TEMPLATE_DIR, get_core_apps

import keys

# Django settings for oscar project.
PROJECT_DIR = os.path.dirname(__file__)
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x
)

DEBUG = True
SQL_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': location('db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
ATOMIC_REQUESTS = True

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-gb'

gettext_noop = lambda s: s
LANGUAGES = (
    ('en-gb', gettext_noop('British English')),
    ('zh-cn', gettext_noop('Simplified Chinese')),
    ('nl', gettext_noop('Dutch')),
    ('it', gettext_noop('Italian')),
    ('pl', gettext_noop('Polish')),
    ('ru', gettext_noop('Russian')),
    ('sk', gettext_noop('Slovak')),
    ('pt-br', gettext_noop('Brazilian Portuguese')),
    ('fr', gettext_noop('French')),
    ('de', gettext_noop('German')),
    ('ko', gettext_noop('Korean')),
    ('uk', gettext_noop('Ukrainian')),
    ('es', gettext_noop('Spanish')),
    ('da', gettext_noop('Danish')),
    ('ar', gettext_noop('Arabic')),
    ('ca', gettext_noop('Catalan')),
    ('cs', gettext_noop('Czech')),
    ('el', gettext_noop('Greek')),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True


MEDIA_ROOT = location("public/media")
MEDIA_URL = '/media/'


STATIC_URL = '/static/'
STATIC_ROOT = location('public')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$)a7n&o80u!6y5t-+jrd3)3!%vh&shg$wqpjpxc!ar&p#!)n1a'

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
            os.path.join(OSCAR_MAIN_TEMPLATE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
            'debug': DEBUG
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'oscar.checkout': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'razorpay': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    # Apps from oscar
    'rzpay',
    'compressor',
    'widget_tweaks',
]

INSTALLED_APPS = INSTALLED_APPS + get_core_apps([
    'apps.shipping'])

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.Emailbackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/accounts/'
APPEND_SLASH = True

# Oscar settings
OSCAR_ALLOW_ANON_CHECKOUT = True

OSCAR_SHOP_TAGLINE = 'Razorpay'

# Add Razorpay dashboard stuff to settings
OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('Razorpay'),
        'icon': 'icon-globe',
        'children': [
            {
                'label': _('Razorpay transactions'),
                'url_name': 'razorpay-list',
            },
        ]
    })

OSCAR_DEFAULT_CURRENCY = "INR"

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

RAZORPAY_API_KEY = keys.RAZORPAY_API_KEY
RAZORPAY_API_SECRET = keys.RAZORPAY_API_SECRET
RAZORPAY_CURRENCY = "INR"

# Put your own sandbox settings into an integration.py modulde (that is ignored
# by git).
try:
    from integration import *  # noqa
except ImportError:
    pass
