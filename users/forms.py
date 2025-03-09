from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True, label="Nome completo")
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    ) 