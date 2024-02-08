from django import forms
from django.forms.widgets import HiddenInput

class AuthorisationForm(forms.Form):
    login = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'your login here...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))