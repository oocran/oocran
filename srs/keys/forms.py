from django import forms
from .models import Key


class KeyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Key
        fields = [
            "name",
            "public_key",
        ]