from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django_otp_webauthn.utils import get_credential_model

WebAuthnCredential = get_credential_model()

__all__ = [
    "RegisteredDevicesListView",
]


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
