from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import REDIRECT_FIELD_NAME
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import DeleteView, FormView, TemplateView, UpdateView
from django_otp_webauthn.utils import get_credential_model

from wagtail_mfa.forms import WebAuthnCredentialForm, WebAuthnCredentialRenameForm

WebAuthnCredential = get_credential_model()

__all__ = [
    "RegisteredDevicesListView",
    "CreateWebAuthnDeviceView",
    "EditWebAuthnDeviceView",
    "DeleteWebAuthnDeviceView",
]


class RedirectURLMixin:
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url_allowed_hosts = set()

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(self.redirect_field_name, self.request.GET.get(self.redirect_field_name))
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["redirect_next"] = self.get_redirect_url()
        return context


@method_decorator(never_cache, name="dispatch")
class RegisteredDevicesListView(LoginRequiredMixin, TemplateView):
    template_name = "wagtail_mfa/registered_devices_list.html"

    def get_webauthn_devices(self):
        user = self.request.user
        return (
            WebAuthnCredential.objects.filter(user=user, confirmed=True)
            .order_by("-last_used_at")
            .only("name", "last_used_at", "created_at", "backup_state", "id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["webauthn_devices"] = self.get_webauthn_devices()
        return context


@method_decorator(never_cache, name="dispatch")
class VerificationRequiredView(RedirectURLMixin, TemplateView):
    template_name = "wagtail_mfa/verification_required.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.get_redirect_url()
        return context


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
