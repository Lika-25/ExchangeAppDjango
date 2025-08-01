from .models import Item
from django.forms import ModelForm, TextInput, Textarea, Select, FileInput
from django import forms

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "category", "exchange_category", "image"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть опис'
            }),
            "category": Select(attrs={
                'class': 'form-control',
            }),
            "exchange_category": Select(attrs={
                'class': 'form-control',                
            }),
            "image": FileInput(attrs={
                'class': 'form-control',
            }),
        }

    image = forms.ImageField(widget=forms.ClearableFileInput, required=False, label='Фото')
