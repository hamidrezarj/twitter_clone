from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not "gmail.com" in email:
            raise forms.ValidationError("Email must be gmail.")
        return email


class EditForm(forms.Form):
    profile_img = forms.ImageField(required=False)
    username = forms.CharField(required=False)

    def clean_username(self):
        new_username = self.cleaned_data['username']
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError("Username is already taken!")
        return new_username
