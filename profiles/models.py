from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class ProfileGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name = 'Имя группы')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Profile(models.Model):
    type_choises = (
        ('A', 'Администратор'),
        ('T', 'Учитель'),
        ('S', 'Студент')
    )

    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=1, choices=type_choises, default="T")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    group = models.ForeignKey(ProfileGroup, blank=True, null=True, on_delete=models.SET_NULL)
    deactivation_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
       profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)