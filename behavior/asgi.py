import os
import django
from channels.routing import get_default_application  # noqa


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "behavior.settings")
django.setup()
channel_layer = get_default_application()
