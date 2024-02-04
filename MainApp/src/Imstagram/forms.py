from django import forms
from .models import Image

class AddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['small_description', 'full_description', 'image', 'is_favorite']
        labels = {
            'small_description': 'Small Description',
            'full_description': 'Full Description',
            'image': 'Upload Image',
            'is_favorite': 'Is Favorite',
        }
        widgets = {
            'small_description': forms.TextInput(attrs={'class': 'form-control'}),
            'full_description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }