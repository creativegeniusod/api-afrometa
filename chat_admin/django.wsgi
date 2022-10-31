import os
import sys

path='/var/www/html/admin_dashboard/chat_admin'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'chat_admin.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
