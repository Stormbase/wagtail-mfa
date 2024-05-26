from django.contrib.auth.views import REDIRECT_FIELD_NAME
from django.utils.http import url_has_allowed_host_and_scheme

__all__ = [
    "RedirectURLMixin",
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
