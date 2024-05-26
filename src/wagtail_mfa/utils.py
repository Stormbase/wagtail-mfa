from django.urls import reverse
from django_otp_webauthn.utils import get_exempt_urls as webauthn_api_exempt_urls


def get_exempt_urls():
    urls = [
        reverse("wagtail_mfa_webauthn_create"),
    ]
    urls += webauthn_api_exempt_urls()
    return urls
