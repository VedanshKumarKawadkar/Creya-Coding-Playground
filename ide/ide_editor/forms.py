from django import forms
from django_ace import AceWidget
from ide_editor.models import CodeData

class IdeForm(forms.ModelForm):
    class Meta:
        model = CodeData 

        widgets = {
            "text": AceWidget(mode='python', theme='twilight'),
        }
        exclude = ()