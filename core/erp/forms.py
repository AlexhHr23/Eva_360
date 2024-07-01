from django.forms import ModelForm
from django import forms

from .models import *


class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'names', 'dni', 'email', 'mobile', 'birthdate', 'address', 'image'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese su número de cédula'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
        }
        exclude = ['username', 'groups', 'password', 'date_joined', 'last_login', 'is_superuser', 'email_reset_token', 'is_active', 'is_staff', 'is_change_password', 'user_permissions']

    birthdate = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'birthdate',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#birthdate'
        }), label='Fecha de nacimiento')

    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un teléfono celular',
        'autocomplete': 'off'
    }), max_length=10, label='Teléfono celular')

    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese una dirección',
        'autocomplete': 'off'
    }), max_length=500, label='Dirección')


class TeacherForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'names', 'dni', 'email', 'profession', 'mobile', 'birthdate', 'address', 'image'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese su número de cédula'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
        }
        exclude = ['username', 'groups', 'password', 'date_joined', 'last_login', 'is_superuser', 'email_reset_token', 'is_active', 'is_staff', 'is_change_password', 'user_permissions']

    birthdate = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'birthdate',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#birthdate'
        }), label='Fecha de nacimiento')

    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un teléfono celular',
        'autocomplete': 'off'
    }), max_length=10, label='Teléfono celular')

    profession = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese una profesión',
        'autocomplete': 'off'
    }), max_length=50, label='Profesión')

    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese una dirección',
        'autocomplete': 'off'
    }), max_length=500, label='Dirección')


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['autofocus'] = True

    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ingrese una descripción'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class QuizForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for i in self.fields:
            input = self.fields[i]
            if type(input) is forms.CharField:
                input.widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = Quiz
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
