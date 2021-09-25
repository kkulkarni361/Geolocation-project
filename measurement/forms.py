from django import forms
from .models import Measurement


class MeasurementModelForm(forms.ModelForm):
    class meta:
        model = Measurement
        field = ('destination',)
