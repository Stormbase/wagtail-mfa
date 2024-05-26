from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django_otp_webauthn.utils import get_credential_model
from precis_i18n import get_profile

nickname_profile = get_profile("NicknameCasePreserved")

WebAuthnCredential = get_credential_model()


class WebAuthnCredentialForm(ModelForm):
    device = forms.ModelChoiceField(queryset=WebAuthnCredential.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = WebAuthnCredential
        fields = []


class WebAuthnCredentialRenameForm(ModelForm):
    name = forms.CharField(
        label=_("Nickname"),
        max_length=255,
        help_text=_("Give this Passkey a memorable name. This will help you identify it later."),
    )

    class Meta:
        model = WebAuthnCredential
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            name = nickname_profile.enforce(name)
        except UnicodeEncodeError:
            raise forms.ValidationError(_("Name contains invalid characters."))
        return name
