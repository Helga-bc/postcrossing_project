from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User

import datetime
import random
from .models import UserProfile, Postcard, Comment
from .forms import AddPostcardForm, UserRegistrationForm, AddUserProfileInfoForm



def main(request):
  
    last_added = Postcard.objects.filter().order_by('-created_at')[:7]
    count_users = UserProfile.objects.all().count()
    users_country = UserProfile.objects.exclude(country='').filter().order_by('country').distinct().count()
    count_postcards = Postcard.objects.all().count()
    count_countries = Postcard.objects.filter().order_by('country').distinct().count()
    
    return render(request, 'main.html', {'last_added':last_added,
                                         'count_users':count_users, 
                                         'count_postcards':count_postcards,
                                          'count_countries':count_countries, 
                                          'users_country':users_country})



def about_postcrossing(request):
    return render(request, 'about_postcrossing.html')
    

def postcards(request):
    postcards = Postcard.objects.all()
    return render(request, 'postcards.html', {"postcards":postcards})


def get_postcard(request, id):
    try:
        postcard = Postcard.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("- такой открытки пока не сущестует - ")

    return render(request, 'get_postcard.html', {'postcard':postcard})



def add_postcard(request):
    if request.method == "POST":
        form = AddPostcardForm(request.POST, request.FILES)

        if form.is_valid():
            new_postcard = form.save(commit=False)
            new_postcard.owner = UserProfile.objects.get(email=request.user.email)
            new_postcard.country = form.cleaned_data['country']
            new_postcard.description = form.cleaned_data['description']
            new_postcard.image = form.cleaned_data['image']
            new_postcard.created_at = datetime.datetime.now()
            
            if form.cleaned_data['sender_id']:
                try:
                    sender = UserProfile.objects.get(user_id=new_postcard.sender_id)
                    sender.experience += 100
                    sender.save()
                except UserProfile.DoesNotExist:
                    pass
            else: pass
                                        
            form.save_m2m()
            new_postcard = form.save()
            return redirect('get_postcard', new_postcard.id)
        else:
            return render(request, 'add_postcard.html', {'form':form})        
    else:
        form = AddPostcardForm()
        return render(request, 'add_postcard.html', {'form':form})
    
    
    
def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()          
            user_profile = UserProfile.objects.create(email=new_user.email, user= new_user)            
            return render(request, 'register_done.html', {'new_user': new_user})
        return render(request, 'register.html', {'user_form': user_form})        
    else:
        user_form = UserRegistrationForm()
        return render(request, 'register.html', {'user_form': user_form})
        


def user_profile(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        user_profile = UserProfile.objects.get(user=user)
        user_postcards = Postcard.objects.filter(owner_id=id)
        return render(request, 'user_profile.html', {"user":user, 'user_profile':user_profile, 'user_postcards':user_postcards})
    else:
        return redirect(request, 'main.html')
    


def add_profile_info(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        user_info_form = AddUserProfileInfoForm(request.POST)
        if user_info_form.is_valid():
            
            user_profile = user_info_form.save(commit=False)
            user_profile.user_id = user.id
            user_profile.email = user.email
            user_profile.name = user_info_form.cleaned_data['name']
            user_profile.country = user_info_form.cleaned_data['country']
            user_profile.city = user_info_form.cleaned_data['city']
            user_profile.street = user_info_form.cleaned_data['street']
            user_profile.mail_index = user_info_form.cleaned_data['mail_index']
            user_profile.experience = UserProfile.objects.get(user_id=id).experience
            user_info_form.save_m2m()
            user_profile = user_info_form.save()           
            return render(request, 'user_profile.html', {'user_profile':user_profile})
    else:
        user_info_form = AddUserProfileInfoForm()
        return render(request, 'add_profile_info.html', {'user_info_form': user_info_form})
        


def generate_random_user(request):
    users_with_mail_index = []
    all_users = UserProfile.objects.all()
    
    for user in all_users:
        if user.mail_index != '':
            users_with_mail_index.append(user.user_id)
  
    random.shuffle(users_with_mail_index)
    id = random.choice(users_with_mail_index)
    winner_user = UserProfile.objects.get(user_id=id)
    return render(request, 'send_to_random_user.html', {'winner_user':winner_user})
    
    
    
def add_comment(request, id):
    try:
        postcard = Postcard.objects.get(id=id)
        Comment.objects.create(content=request.POST['content'],
                               user_id=request.user.id,
                               postcard_id=id,
                               date_created= datetime.datetime.now())
        
        return redirect("get_postcard", id=id)
    except Postcard.DoesNotExist:
        return HttpResponseNotFound(f"<h3> Открытки с id {id} нет, вы не можете добавить комментарий! </h3>")
    
    
    
    
def get_userprofile(request, id):
    get_user_profile = UserProfile.objects.get(user_id=id)
    user_postcards = Postcard.objects.filter(owner_id=id)
    return render(request, 'get_userprofile.html', {'get_user_profile':get_user_profile, 'user_postcards':user_postcards})

    



