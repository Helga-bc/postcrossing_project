from django import forms
from .models import UserProfile, Postcard
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    username = forms.CharField(required=True, label='Имя пользователя')
    first_name = forms.CharField(required=True, label='Ваше имя')
    email = forms.EmailField(required=True, label='Введите емайл')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают!')
        return cd['password2']
    
    


class AddUserProfileInfoForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            fields = ('name', 'country', 'city', 'street', 'mail_index')
            
        name = forms.CharField(min_length=3, required=True, label= "Имя")
        country = forms.CharField(required=True, label= 'Страна')
        city = forms.CharField(required=True, label= 'Город')
        street = forms.CharField(required=True, label= 'Улица')
        mail_index = forms.CharField(required=True, label= 'Почтовый индекс')
        
        


class AddPostcardForm(forms.ModelForm):
    class Meta:
        model = Postcard
        fields = ('country', 'description', 'image', 'sender_id')
        labels = {'country':"Страна", 'description':"Описание", 'sender_id':'ID отправителя', 'image':'Добавить изображение'}
        
        country = forms.CharField(required=True,label= 'Страна')
        description = forms.CharField(max_length=100)
        sender_id = forms.IntegerField(required=False)     
        
        
    def clean_sender_id(self):
        raw_data = self.cleaned_data['sender_id']
        users = UserProfile.objects.all()   
        users_id_list = [user.user_id for user in users]
        users_id_list.append(None)

        
        if raw_data not in users_id_list:
            raise ValidationError("Неправильный ID отправителя. Пользователя с таким ID не существует! Измените или оставьте пустым.")
        else:
            cleaned_data = raw_data
        return cleaned_data
        
      
        