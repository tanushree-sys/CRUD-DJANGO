from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model= Item
        fields= ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
        }
