from django import forms
from .models import Library


class LibraryForm(forms.ModelForm):
    type = forms.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        super(LibraryForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'id': 'Ufile'})
        self.fields['type'] = forms.ChoiceField(required=False,
                                                widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                choices=[("file", "file"), ("script", "script")])  # ,("ansible", "ansible"),("puppet", "puppet")])

    class Meta:
        model = Library
        fields = [
            "name",
            "description",
            "script",
            "file",
            "type",
        ]
