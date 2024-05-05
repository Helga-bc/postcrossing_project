from django.contrib import admin
from .models import UserProfile, Postcard, Comment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Postcard)
admin.site.register(Comment)

