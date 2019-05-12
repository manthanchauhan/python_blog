from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(User.objects.filter(email=email)) != 0:
            raise forms.ValidationError(f'This email is already registered')
        return email
