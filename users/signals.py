import django.dispatch
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def create_user_profile(sender, instance, created, **kwargs):
    print('user created with id '+str(instance.id)+' and email '+instance.email)


def create_user_job(sender, instance, created, **kwargs):
    print('user job created with id '+str(instance.id))