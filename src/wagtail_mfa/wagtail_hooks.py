from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks

from wagtail_mfa import views


@hooks.register("register_admin_urls")
def urlpatterns():
    return [
        path("wagtail_mfa/devices/", views.RegisteredDevicesListView.as_view(), name="wagtail_mfa_registered_devices"),
        path(
            "wagtail_mfa/devices/webauthn/create/",
            views.CreateWebAuthnDeviceView.as_view(),
            name="wagtail_mfa_webauthn_create",
        ),
        path(
            "wagtail_mfa/devices/webauthn/<pk>/",
            views.EditWebAuthnDeviceView.as_view(),
            name="wagtail_mfa_webauthn_edit",
        ),
        path(
            "wagtail_mfa/devices/webauthn/<pk>/delete/",
            views.DeleteWebAuthnDeviceView.as_view(),
            name="wagtail_mfa_webauthn_delete",
        ),
    ]


@hooks.register("register_account_menu_item")
def register_manage_devices_button_account_menu(request):
    return {
        "url": reverse("wagtail_mfa_registered_devices"),
        "label": _("Manage authentication settings"),
        "help_text": _("Manage your multi-factor authentication settings."),
    }


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtail_mfa/icons/passkey.svg",
    ]
