from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CreateUserForm(forms.ModelForm):
    full_name = forms.CharField()
    birth_date = forms.DateField()
    class Meta:
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit = False)
        user.set_password("123456789") #TODO generate password
        user.is_active = True

        if commit:
            user.save()
            user.profile.birth_date = self.cleaned_data["birth_date"]
            user.profile.full_name = self.cleaned_data["full_name"]
        return user