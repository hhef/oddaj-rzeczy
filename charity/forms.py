from django import forms
from django.contrib.auth.models import User


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        help_texts = {
            "username": None
        }
        fields = ("username", "email", "first_name", "last_name")