# registration_forms.py

# from django import forms
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError

# class RegistrationForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     mobile = forms.CharField(max_length=15)
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirmPassword = forms.CharField(widget=forms.PasswordInput)

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if '@something.com' in email:
#             raise forms.ValidationError("Please enter a valid email address.")
#         return email

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirmPassword")

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")

#         return cleaned_data
