from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import DeleteView, FormView, UpdateView
from django_otp_webauthn.utils import get_credential_model

from wagtail_mfa.forms import WebAuthnCredentialForm, WebAuthnCredentialRenameForm

WebAuthnCredential = get_credential_model()

__all__ = [
    "CreateWebAuthnDeviceView",
    "EditWebAuthnDeviceView",
    "DeleteWebAuthnDeviceView",
]


@method_decorator(never_cache, name="dispatch")
class CreateWebAuthnDeviceView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "wagtail_mfa/webauthn/create.html"
    form_class = WebAuthnCredentialForm

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return _("Your passkey was created successfully! Now, please give it a name.")

    def get_success_url(self) -> str:
        return reverse("wagtail_mfa_webauthn_edit", args=[self.device.pk])

    def form_valid(self, form):
        self.device = form.cleaned_data.get("device")
        return super().form_valid(form)


@method_decorator(never_cache, name="dispatch")
class EditWebAuthnDeviceView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "wagtail_mfa/webauthn/edit.html"
    form_class = WebAuthnCredentialRenameForm

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return _("Passkey saved successfully.")

    def get_success_url(self) -> str:
        return reverse("wagtail_mfa_registered_devices")

    def get_queryset(self):
        return WebAuthnCredential.objects.filter(user=self.request.user)


@method_decorator(never_cache, name="dispatch")
class DeleteWebAuthnDeviceView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "wagtail_mfa/webauthn/delete.html"

    # This is a dummy form class, as we don't need a form for this view
    form_class = forms.Form

    def get_queryset(self):
        return WebAuthnCredential.objects.filter(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("wagtail_mfa_registered_devices")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return _("Passkey “%(device_name)s“ deleted successfully") % {"device_name": self.object.name}
