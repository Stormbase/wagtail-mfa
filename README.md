# Wagtail MFA

Wagtail MFA is a multi-factor authentication package for Wagtail. It adds an extra layer of security to your Wagtail admin interface.

Under the hood, Wagtail MFA uses [django-otp](https://github.com/django-otp/django-otp/) and [django-otp-webauthn](https://github.com/Stormbase/django-otp-webauthn) to provide the Passkey login functionality. All this package does is provide a Wagtail-specific UI to let users manage their MFA settings and a page for MFA verification.

> [!IMPORTANT]  
> This package is alpha and not yet feature-complete. It hasn't been thoroughly tested and documented yet. If you are interested in using this package, please star this repository to show your interest. Eventually, I intend to

## Screenshots

<table>
    <tbody>
        <th>Safari autofill prompt for saved Passkey</th>
        <th>Login with fingerprint</th>
        <th>Registered Passkeys</th>
        <tr>
            <td>
                <a href="https://github.com/Stormbase/wagtail-mfa/blob/main/docs/images/wagtail-login-autofill-prompt.png" target="_blank">
                    <img src="https://github.com/Stormbase/wagtail-mfa/blob/main/docs/images/wagtail-login-autofill-prompt.png" alt="Wagtail login page showing a browser prompt to login to this site using saved Passkey">
                </a>
            </td>
            <td>
                <a href="https://github.com/Stormbase/wagtail-mfa/blob/main/docs/images/wagtail-login-touchid-prompt.png" target="_blank">
                    <img src="https://github.com/Stormbase/wagtail-mfa/blob/main/docs/images/wagtail-login-touchid-prompt.png" alt="Wagtail login page showing a browser prompt asking for a fingerprint scan">
                </a>
            </td>
            <td>
                <a href="https://github.com/Stormbase/wagtail-mfa/blob/main/docs/images/wagtail-user-passkeys-listing.png" target="_blank">
                    <img src="https://github.com/Stormbase/wagtail-mfa/blob/main/docs/images/wagtail-user-passkeys-listing.png" alt="Wagtail account settings page showing a list of registered Passkeys">
                </a>
            </td>
        </tr>
    </tbody>
</table>

## Features

Supported authentication methods:

- Passkeys (passwordless login supported)

**Coming soon:**

- Time-based one-time passwords (TOTP)
- Recovery codes

## Supported browsers

Passkeys are still a relatively new technology, and not all browsers support them reliably. The following browsers have been tested and are known to work with Passkeys:

- Chrome 125 on macOS 14
- Firefox 126 on macOS 14 (with known issues, see [Known limitations](#known-limitations)
- Safari 17 on macOS 14

[^1]: There is a known issue with logging in without a password, see [Known limitations](#known-limitations) for more information.

## Requirements

- Python >= 3.9
- Django >= 4.2
- Wagtail >= 5.2

## Installation

Install the package using pip:

```console
pip install wagtail-mfa
```

Add all required apps to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    ...
    # Wagtail MFA must appear before wagtail because it overrides the default Wagtail login template
    "wagtail_mfa",
    ...
    # django-otp and django-otp-webauthn are required
    "django_otp",
    "django_otp_webauthn",
    ...
]
```

For Passkeys to work properly, you need to set some additional `django_otp_webauthn` settings.

Adapt and add the following code snippet to your `settings.py`:

```python
# settings.py
OTP_WEBAUTHN_RP_ID = "your-domain.com"
OTP_WEBAUTHN_RP_NAME = WAGTAIL_SITE_NAME
OTP_WEBAUTHN_ALLOWED_ORIGINS = ["https://your-domain.com", "https://subdomain.your-domain.com"]
```

## Configuration

### `OTP_WEBAUTHN_RP_ID`

_example: `your-domain.com`_

This setting is the primary domain of your site. Passkeys are bound to this domain. This cannot be a 'public suffix' domain like `your-app.compute.amazonaws.com` or `your-app.herokuapp.com`. It must be a domain you own. Browsers will refuse to create Passkeys for public suffix domains. For a complete list of public suffix domains, see [publicsuffix.org](https://publicsuffix.org/list/public_suffix_list.dat).

### `OTP_WEBAUTHN_RP_NAME`

_example: `My Cool Wagtail Site`_

Some browsers show this name when registering a Passkey. This can be the name of your site or your company.

### `OTP_WEBAUTHN_ALLOWED_ORIGINS`

_example: `["https://your-domain.com", "https://subdomain.your-domain.com"]`_

This setting is similar to Django's [`CSRF_TRUSTED_ORIGINS`](https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS) setting and is used to verify Passkey registration/authentication requests. It must be a `https://` (sub)domain of the `OTP_WEBAUTHN_RP_ID`. Do not include a trailing slash.

## Known issues

- **Issues on Firefox**. When using Firefox to register and store a Passkey on an Android device, the Passkey will not be available to use for passwordless login. This is because Firefox does not create a `discoverable credential`. This appears to be a limitation of Firefox. This issue was observed on Firefox 126 on macOS 14.
- **Multi-site has limited support.** WebAuthn does not currently support using Passkeys across different domains. If you create a Passkey for `your-site.com`, you cannot use it to authenticate on `another-site.com`. Subdomains like `subdomain.your-site.com` are supported however.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for information on how to develop and contribute to this project.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.
