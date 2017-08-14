from django import forms

from .models import Lesson

class DateInput(forms.DateInput):
    input_type = 'date'

class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ['teacher']
        widgets = {'date': DateInput}