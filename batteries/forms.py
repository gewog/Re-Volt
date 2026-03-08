from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BatterySubmission
from .cities import ALLOWED_CITIES, RUSSIAN_CITIES, CITY_ABSENT


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
        }


def validate_city(value):
    if not value or not value.strip():
        return  # пустое обработаем в clean_city
    if value.strip() not in ALLOWED_CITIES:
        raise forms.ValidationError('Выберите город из списка или «Город отсутствует».')


class BatterySubmissionForm(forms.ModelForm):
    city = forms.CharField(
        max_length=100,
        label='Город сдачи',
        required=False,
        validators=[validate_city],
        widget=forms.TextInput(attrs={
            'placeholder': 'Начните вводить название города...',
            'class': 'form-control',
            'autocomplete': 'off',
            'id': 'id_city_autocomplete',
        }),
    )

    def clean_city(self):
        value = (self.cleaned_data.get('city') or '').strip()
        return value if value in ALLOWED_CITIES else CITY_ABSENT

    class Meta:
        model = BatterySubmission
        fields = ('count', 'city')
        labels = {'count': 'Количество батареек'}
        widgets = {
            'count': forms.NumberInput(attrs={
                'min': 1,
                'placeholder': 'Введите число',
                'class': 'form-control',
            }),
        }
