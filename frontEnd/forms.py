"""This forms handles Register/SignUp functionality of JewelBox..."""

from django import forms
from django.contrib.auth import get_user_model  # Import this instead of User
from django.db import IntegrityError

CustomUser = get_user_model()  # Get the custom user model dynamically


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10', 'pattern': '^\d{10}$', 'title': 'Phone number must be exactly 10 digits'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Email is already in use.")
        except IntegrityError as e:
            raise forms.ValidationError(f"An error occurred while checking the email: {e}")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')  # Corrected the field name
        if phone_number:  # Check if phone_number is not None or empty
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_number  # Return the cleaned phone number, even if it's empty

    def save(self, commit=True):
        try:
            user = self.instance
            user.username = user.email  # Set username as email

            user.set_password(self.cleaned_data["password"])  # Securely hash password

            if commit:
                user.save()
            return user

        except IntegrityError as e:
            raise forms.ValidationError(f"An error occurred while saving the user: {e}")