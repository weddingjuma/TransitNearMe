import os

# Local time zone for this installation.
# Choices at: http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LANGUAGES = (('en', 'English'),)

# Internationalization / localization.
USE_I18N = False
USE_L10N = True

# Useful variables.
path = lambda root,*a: os.path.join(root, *a)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_MODULE = os.path.split(PROJECT_ROOT)[1]
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Make sure to use a trailing slash.
MEDIA_URL = ''

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = PROJECT_MODULE + '.urls'

TEMPLATE_DIRS = (
	path(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'pipeline',
    'gtfs',
    'api',
    'client',
    'transitapis'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
	'formatters': {
		'simple': {
			'format': '%(levelname)s %(asctime)s %(message)s'
		},
	},
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
		'api': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'formatter': 'simple',
			'filename': path(SITE_ROOT, os.path.join('log', 'api.log'))
		},
        'predictions': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': path(SITE_ROOT, os.path.join('log', 'predictions.log'))
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
		'api': {
			'handlers': ['api'],
			'level': 'INFO',
			'propagate': True,
		},
	    'predictions': {
            'handlers': ['predictions'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# JS/CSS compression.
PIPELINE_YUI_BINARY = path(SITE_ROOT, 'bin/yuicompressor')
PIPELINE_CSS = {
    'tnm': {
        'source_filenames': (
            'leaflet.css',
            'tnm.css',
        ),
        'output_filename': 'tnm-?.css',
    },
}

PIPELINE_JS = {
    'tnm': {
        'source_filenames': (
            'leaflet.js',
            'transit.js',
            'tnm.js',
        ),
        'output_filename': 'tnm-?.js',
    },
}

# Import local settings. This is required.
from local_settings import *
