# hosteldb20/apps.py

from django.apps import AppConfig

class Hosteldb20Config(AppConfig):
    name = 'hosteldb20'

    def ready(self):
        # Import and connect your signals here to ensure they are hooked up at startup
        import hosteldb20.signals
