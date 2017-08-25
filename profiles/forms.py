from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import cyrtranslit
from django.template.defaultfilters import date
from django.utils import formats
from random import randrange

from .models import Profile

User = get_user_model()

type_choises = type_choises = (
        ('T', 'Учитель'),
        ('S', 'Студент')
    )

class DateInput(forms.DateInput):
    input_type = 'date'

    def _format_value(self, value):
        return value

class CreateUserForm(forms.ModelForm):
    full_name = forms.CharField(label="ФИО")
    birth_date = forms.DateField(label="Дата рождения", widget=DateInput)
    user_type = forms.ChoiceField(label="Тип пользователя", choices=type_choises)

    class Meta:
        model = User
        fields = []

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        fio = full_name.split()
        if len(fio) < 2:
            raise ValidationError('Неверный формат ФИО')
        return full_name

    def save(self, commit = True):
        user = super(CreateUserForm, self).save(commit = False)
        user.set_password("password")
        user.is_active = True

        full_name = self.cleaned_data.get('full_name')
        full_name_en = cyrtranslit.to_latin(full_name, 'ru')
        full_name_clean = full_name_en.replace('#', '')
        full_name_clean = full_name_clean.replace("'", "")

        fio = full_name_clean.split()
        if len(fio) == 2:
            username = fio[1][0].lower() + fio[0].lower()
        else:
            username = fio[1][0].lower() + fio[2][0].lower() + fio[0].lower()
        same_name_users = User.objects.filter(username__iexact=username)
        if same_name_users:
            username += str(randrange(100))
        user.username = username

        if commit:
            user.save()
            user.profile.birth_date = self.cleaned_data.get("birth_date")
            user.profile.full_name = self.cleaned_data.get("full_name")
            user.profile.user_type = self.cleaned_data.get("user_type")
            user.profile.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', validators=[RegexValidator(
                        regex = '^[a-zA-Z0-9.@+-]*$',
                        message = 'Имя пользователя может содержать латинские буквы, цифры и следующие символы: ". @ + -" ',
                        code='invalid_username'
                    )])
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # the_user = authenticate(username=username, password=password)
        # if not the_user:
        #     raise forms.ValidationError("Invalid credentials")
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            raise forms.ValidationError("Invalid credentials")
        else:
            if not user_obj.check_password(password):
                # log auth tries
                raise forms.ValidationError("Invalid credentials")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UpdateStudentForm(forms.ModelForm):
    user_type = forms.ChoiceField(label="Тип пользователя", choices=type_choises)

    class Meta:
        model = Profile
        fields = ['full_name',
                  'birth_date',
                  'user_type',
                  'group']
        widgets = {'birth_date': DateInput}
        labels = {
            'full_name': 'ФИО',
            'birth_date': 'Дата рождения',
            'user_type': 'Тип пользователя',
            'group': 'Группа'
        }


class UpdateTeacherForm(forms.ModelForm):
    user_type = forms.ChoiceField(label="Тип пользователя", choices=type_choises)

    class Meta:
        model = Profile
        fields = ['full_name',
                  'birth_date',
                  'user_type']
        widgets = {'birth_date': DateInput}
        labels = {
            'full_name': 'ФИО',
            'birth_date': 'Дата рождения',
            'user_type': 'Тип пользователя'
        }