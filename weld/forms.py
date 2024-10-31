# forms.py
from django import forms
from .models import Weld_info

class WeldInfoForm(forms.ModelForm):
    class Meta:
        model = Weld_info
        fields = ['model_name', 'program', 'power', 'freq', 'length']  # 입력받을 필드 지정
