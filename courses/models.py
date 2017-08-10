from django.db import models
from profiles.models import Profile

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

    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Profile)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
