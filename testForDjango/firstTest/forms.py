from django import forms
from .models import reporter, profile, article
from django.contrib.auth.models import User

class addArticleForm(forms.ModelForm):
    class Meta:
        model = article
        widgets = {
            'articleMain': forms.Textarea(attrs={'placeholder':'enter text here ...'}),
            'articleContent': forms.TextInput(attrs={'placeholder':'subject ...'})
        }
        fields = ('articleMain','articleContent','publisher')

class deleteArticleForm(forms.Form):
    articleName = forms.CharField(max_length=100)

class editArticleForm(forms.ModelForm):
    class Meta:
        model = article
        widgets = {
            'articleMain': forms.Textarea(),
        }
        fields = ('articleContent','articleMain')

class userForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ("username","password","first_name","last_name","email")

class profileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ("biography","location","phonenumber","image")