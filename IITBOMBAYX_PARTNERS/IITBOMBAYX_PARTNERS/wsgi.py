"""
WSGI config for IITBOMBAYX_PARTNERS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application
project_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IITBOMBAYX_PARTNERS.settings")

application = get_wsgi_application()
