from django import forms
from django.contrib.auth import authenticate

class LogForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Extract the `request` argument
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(request=self.request, email=email, password=password)
        if not user:
            raise forms.ValidationError("Invalid email or password")

        cleaned_data['user'] = user  # Save the user object for later use
        return cleaned_data
