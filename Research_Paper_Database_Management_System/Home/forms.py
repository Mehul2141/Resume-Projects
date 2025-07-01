from django import forms
from Home.models import research_Model

class researchforms(forms.ModelForm):
    class Meta:
        model=research_Model
        fields="__all__"