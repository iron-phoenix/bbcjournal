from django import forms

from .models import Lesson, StudentLesson

class DateInput(forms.DateInput):
    input_type = 'date'

class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'course', 'group', 'type', 'description', 'date']
        widgets = {'date': DateInput}

class StudentLessonEditForm(forms.Form):
    is_presence = forms.BooleanField(initial = True)
    mark = forms.ChoiceField(choices = StudentLesson.mark_types)
    reason_for_abcense = forms.CharField(widget = forms.TextInput)