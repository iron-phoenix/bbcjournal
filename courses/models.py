from django.db import models
from profiles.models import Profile, ProfileGroup
from django.core.validators import MaxValueValidator

import string

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    type_choises = (('U', 'Обычный урок'),
                    ('T', 'Тестирование'),
                    ('E', 'Пробный'))
    name = models.CharField(max_length = 255, verbose_name = 'Название урока')
    description = models.TextField(blank = True, default='', verbose_name = 'Описание урока')
    homework = models.TextField(blank = True, default='', verbose_name = 'Домашнее задание')
    date = models.DateField(blank = False, null = False, verbose_name = 'Дата урока')
    type = models.CharField(max_length = 1, choices = type_choises, default = 'U', verbose_name = 'Тип')

    course = models.ForeignKey(Course, null = True, verbose_name = 'Курс')
    teacher = models.ForeignKey(Profile, null = True, verbose_name = 'Учитель')
    group = models.ForeignKey(ProfileGroup, null = True, verbose_name = 'Группа')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class StudentLesson(models.Model):
    mark_types = (('A', 'A'),
                  ('B', 'B'),
                  ('C', 'C'),
                  ('D', 'D'),
                  ('E', 'E'),
                  ('F', 'F'),
                  ('', ''))
    student = models.ForeignKey(Profile, blank = False, null = False)
    lesson = models.ForeignKey(Lesson, blank = False, null = False)

    mark = models.CharField(max_length = 1, choices = mark_types, default = '')
    mark_testing = models.PositiveIntegerField(validators = [MaxValueValidator(100)], blank = True, null = True)
    precense = models.BooleanField(default = True)
    reason_for_precense = models.CharField(max_length = 255, blank = True, default = '')

    def __str__(self):
        return self.student.full_name + ' ' + self.lesson.name

    def __unicode__(self):
        return self.student.full_name + ' ' + self.lesson.name