# Settings pattern adapted from
# https://overtag.dk/v2/blog/a-settings-pattern-for-reusable-django-apps/
from dataclasses import dataclass

from django.conf import settings as django_settings

settings_prefix = "WAGTAIL_MFA"


@dataclass(frozen=True)
class AppSettings:
    """Access this instance as ``wagtail_mfa.settings.app_settings``."""

    def __getattribute__(self, __name: str):
        # Check if a Django project settings should override the app default.
        # In order to avoid returning any random properties of the django settings, we inspect the prefix firstly.
        if __name.startswith(settings_prefix) and hasattr(django_settings, __name):
            return getattr(django_settings, __name)

        return super().__getattribute__(__name)


app_settings = AppSettings()
