"""
URL configuration for postcrossing_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



import main.views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # main page
    path('', main_views.main, name='main'),
    
    # page about
    path('about/', main_views.about_postcrossing, name='about_postcrossing'),
    
    # view all added postcards
    path('postcards/', main_views.postcards, name='postcards'),
    
    # see the postcard
    path('postcards/<int:id>/', main_views.get_postcard, name="get_postcard"),
    
    # add comment
    path('add_comment/<int:id>/', main_views.add_comment, name='add_comment'),

    # add postcard
    path('add/', main_views.add_postcard, name='add_postcard'),
    
    # registration
    path('registration/', main_views.registration, name='registration'),

    # see your own profile
    path('user_profile/<int:id>/', main_views.user_profile, name='user_profile'),
    
    # add information to your own profile
    path('user_profile/add_profile_info/<int:id>/', main_views.add_profile_info, name='user_profile_info'),
    
    # send postcard to random user
    path('send_to_random_user/', main_views.generate_random_user, name='generate_random_user'), 
    
    # view another user's profile
    path('get_userprofile/<int:id>/', main_views.get_userprofile,name ='get_userprofile')
]


urlpatterns += [path('accounts/', include('django.contrib.auth.urls')),]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
