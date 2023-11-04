"""Application definition & config settings for dangerdine app."""

from django.apps import AppConfig


class DangerDineConfig(AppConfig):
    """Config class to hold application's definition & configuration settings."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dangerdine"
    verbose_name = "DangerDine"

    def ready(self) -> None:
        """
        Ensures the signal handlers within this app are loaded and waiting for signals.

        This ready function should be called whenever this config class is imported.
        """
        from dangerdine.models import signals
        signals.ready()
