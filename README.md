# Wagtail MFA

Wagtail MFA is a multi-factor authentication package for Wagtail. It adds an extra layer of security to your Wagtail admin interface.

Supported factors:

- Passkeys (WebAuthn credentials)
- TOTP (Time-based One-Time Password)

Under the hood, Wagtail MFA uses [django-otp](https://github.com/django-otp/django-otp/) and [django-otp-webauthn](https://github.com/Stormbase/django-otp-webauthn) to provide the TOPT and Passkey/WebAuthn functionality respectively. All this package does is provide a Wagtail-specific UI to let users manage their MFA settings and a page for MFA verification.

## Requirements

- Python >= 3.9
- Django >= 4.2
- Wagtail >= 5.2

## Installation

Install the package using pip:

```console
pip install wagtail-2fa
```

Add all required apps to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    ...
    "wagtail_mfa",
    "django_otp",
    "django_otp_webauthn,
    ...
]
```

## Acknowledgements
