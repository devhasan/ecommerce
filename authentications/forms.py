from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):  #for signup
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password1', 'placeholder': 'Password', 'required': True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password2', 'placeholder': 'Confirm Password', 'required': True}))
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id':'first_name', 'placeholder': 'First Name', 'required': True, 'autofocus': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id':'last_name', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id':'email', 'placeholder': 'Email', 'required': True}),
        }    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken')
        return email
    
# class CustomAuthenticationForm(AuthenticationForm):  #for login
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password', 'placeholder': 'Password', 'required': True}))
     
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password']        
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'id':'email', 'placeholder': 'Email', 'required': True}),
#         }        
            

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True)

class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ('new_password1', 'new_password2')

# class CustomUserChangeForm(UserChangeForm):
#     # Remove the password field from the form
#     password = None

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'first_name', 'last_name')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Customize the form fields if needed
#         self.fields['username'].widget.attrs.update({'class': 'form-control'})
#         self.fields['email'].widget.attrs.update({'class': 'form-control'})
#         self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
#         self.fields['last_name'].widget.attrs.update({'class': 'form-control'})