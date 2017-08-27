SECRET_KEY = "hi"

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": dict(ENGINE='django.db.backends.sqlite3', NAME=':memory:')
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'tests.app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
)
