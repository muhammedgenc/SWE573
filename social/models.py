import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)    
    name = models.TextField(max_length=150, blank=True)
    description = models.TextField(max_length=500, blank=True)
    service_date = models.DateField(default=timezone.now, validators=[MinValueValidator(datetime.datetime.now().date())])
    service_time = models.TimeField(null=False, default=timezone.now)
    duration = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    location = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(5)])
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    is_taken = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='uploads/service_pictures', default='uploads/service_pictures/default.png', blank=True)
    category = models.TextField(max_length=150, blank=True)

class ServiceApplication(models.Model):
    application_date= models.DateTimeField(default=timezone.now)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_service = models.ForeignKey('Service', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    name = models.TextField(max_length=150)
    description = models.TextField(max_length=500)
    event_date = models.DateField(default=timezone.now, validators=[MinValueValidator(datetime.datetime.now().date())])
    event_time = models.TimeField(null=False, default=timezone.now)
    duration = models.IntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(5)])    
    location = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(default=10, validators=[MinValueValidator(1),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='uploads/event_pictures/', default='uploads/event_pictures/default.png', blank=True)
    category = models.TextField(max_length=20,blank=True)

class EventApplication(models.Model):
    application_date= models.DateTimeField(default=timezone.now)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_event = models.ForeignKey('Event', on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    credit_hours = models.IntegerField(default=5)
    reserved_credits = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()