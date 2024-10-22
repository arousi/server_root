from django import forms
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = AppUser
        fields = ['email', 'password']

class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['nickname', 'sector', 'region', 'user', 'total_score']

class PromptForm(forms.ModelForm):
    class Meta:
        model = PromptModel
        fields = ['gemini_response', 'user', 'prompt_text', 'response', 'yes_count', 'no_count', 'score']
        widgets = {
            'gemini_response': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter Gemini response'}),
            'prompt_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your prompt'}),
            'response': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter response'}),
            'yes_count': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Yes count'}),
            'no_count': forms.NumberInput(attrs={'min': 0, 'placeholder': 'No count'}),
            'score': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Score'}),
        }