from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    type_choises = (
        ('A', 'Administrator'),
        ('T', 'Teacher'),
        ('S', 'Student')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=type_choises, default="T")
    full_name = models.CharField(max_length=255, blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)

def post_save_user_receiver(sender, instance, created, **kwargs):
    if created:
       profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)