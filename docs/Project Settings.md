#VMS Project Settings

The following are the current project settings located in **vms/settings.py**. If your development setup differs from the one specified in the tutorial, you may have to change some of the settings in this file.

## Update DBMS Settings

You may need to update the following DBMS settings, in particular the `NAME`, `USER` and `PASSWORD` fields.

## Update `STATIC_URL` field

Ensure that `STATIC_URL` is set to the directory where static files (CSS, Javascript) are located.

## Update `MEDIA_ROOT`

Ensure that `MEDIA_ROOT` is set to the directory where uploaded files are to be stored.

## Source Code for settings.py

```
"""
Django settings for vms project.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rs473)3n^fe0^t-^s$n)_%pl=75f_na7z5ee@(^xc-vn^bzr%a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# Make sure all apps are specified here
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'administrator',
    'authentication',
    'event',
    'home',
    'job',
    'organization',
    'registration',
    'shift',
    'vms',
    'volunteer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vms.urls'

WSGI_APPLICATION = 'vms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Change these database settings if your database engine, database name, username or password changes
DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',    #your database engine
        'NAME' : 'vms',             #the name of your database
        'USER' : 'vmsadmin',          #your DBMS username
        'PASSWORD' : '0xdeadbeef',  #your DBMS password
        'HOST' : 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Specifies the directory where static files (CSS, JavasScript) are stored
STATIC_URL = '/static/'

# All uploaded files (such as resumes) are stored in the /srv directory
# /srv directory contains site-specific data which is served by the system
MEDIA_ROOT = '/srv/'

# Uploaded files have read and write permissions to the owner only
FILE_UPLOAD_PERMISSIONS = 0600

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0600

# If user fails to authenticate, then they are redirected to the view specified in the reverse_lazy call
LOGIN_URL = reverse_lazy('auth:user_login')
```
