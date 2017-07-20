from django import forms
from .models import Script


class ScriptForm(forms.ModelForm):
    type = forms.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'id': 'Ufile'})
        self.fields['type'] = forms.ChoiceField(required=False,
                                                widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                choices=[("Script", "Script"),
                                                         ("Direct Input", "Direct Input"),
                                                         ("File", "File"),
                                                         ("Ansible", "Ansible"),])
                                                         #("Puppet", "Puppet"),
                                                         #("Chef", "Chef")])

    class Meta:
        model = Script
        fields = [
            "name",
            "description",
            "script",
            "file",
            "type",
        ]
