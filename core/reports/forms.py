from django import forms

from core.erp.models import Quiz


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')

    quiz = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Quiz.objects.all(), label='Encuesta')
