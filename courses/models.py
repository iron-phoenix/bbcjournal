from django.db import models
from profiles.models import Profile, ProfileGroup
import string

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True, default='')
    homework = models.TextField(blank = True, default='')
    date = models.DateField(blank = False, null = False)

    course = models.ForeignKey(Course, null = True)
    teacher = models.ForeignKey(Profile, null = True)
    group = models.ForeignKey(ProfileGroup, null = True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class StudentLesson(models.Model):
    student = models.ForeignKey(Profile, blank = False, null = False)
    lesson = models.ForeignKey(Lesson, blank = False, null = False)

    mark = models.CharField(max_length = 1, blank = True, choices = ((x, x) for x in string.ascii_uppercase[:6]))
    precense = models.BooleanField(default = True)
    reason_for_presence = models.CharField(max_length = 255, default = '')