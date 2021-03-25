"""
WSGI config for qyapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv

import sys
path = '/var/www/qyapp'
if path not in sys.path:
    sys.path.append(path)

path = '/home/webuser/miniconda3/envs/qyapp/bin'
if path not in sys.path:
    sys.path.insert(0, path)


load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qyapp.settings')

application = get_wsgi_application()
