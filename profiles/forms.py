from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator

from .models import Profile

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(forms.ModelForm):
    full_name = forms.CharField(label="ФИО")
    birth_date = forms.DateField(label="Дата рождения", widget=DateInput)
    user_type = forms.ChoiceField(label="Тип пользователя", choices=Profile.type_choises)

    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': 'Имя пользователя'
        }

    def save(self, commit = True):
        user = super(CreateUserForm, self).save(commit = False)
        user.set_password("123456789") #TODO generate password
        user.is_active = True

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
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

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