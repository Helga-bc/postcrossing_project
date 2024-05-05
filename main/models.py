from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, editable=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_profile')
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=100, blank=True)
    mail_index = models.CharField(max_length=10, blank=True)
    experience = models.IntegerField(default=0)



class Postcard(models.Model):
    owner = models.ForeignKey("UserProfile", on_delete=models.DO_NOTHING)
    country = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='uploads', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.IntegerField(blank=True, null=True)
    
    
    
class Comment(models.Model):
    content = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments')
    postcard = models.ForeignKey(Postcard, on_delete=models.CASCADE, related_name='comments')
    date_created = models.DateTimeField(auto_now_add=True)
