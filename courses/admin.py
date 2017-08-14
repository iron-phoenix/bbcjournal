from django.contrib import admin
from .models import Course, Lesson, StudentLesson

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(StudentLesson)

# Register your models here.
