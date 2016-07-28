# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

from ata.settings_local import *  # noqa

ASSETS_DEBUG = DEBUG
BASE_DIR = dirname(dirname(abspath(__file__)))
LANGUAGE_CODE = 'en-us'
ROOT_URLCONF = 'ata.urls'
STATIC_ROOT = join(BASE_DIR, 'static')
STATIC_URL = '/static/'
TIME_ZONE = 'UTC'
WSGI_APPLICATION = 'ata.wsgi.application'

ASSETS_MODULES = [
    'docker_status.assets',
]

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django_assets',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_DIRS = [
    join(BASE_DIR, 'docker_status', 'static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
]

TEMPLATES = [
    {
        'APP_DIRS': True,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'docker_status', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
