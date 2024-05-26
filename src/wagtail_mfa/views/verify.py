from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from .mixins import RedirectURLMixin


@method_decorator(never_cache, name="dispatch")
class VerificationRequiredView(RedirectURLMixin, TemplateView):
    template_name = "wagtail_mfa/verification_required.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.get_redirect_url()
        return context
