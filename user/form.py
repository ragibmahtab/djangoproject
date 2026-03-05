from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django import forms
import re
from task.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

User = get_user_model()






class customregistrationform(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']

    
    def clean_email(self):
        emaill = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=emaill).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return emaill
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise forms.ValidationError("Phone number must be a valid format (9-15 digits)")
            if User.objects.filter(phone_number=phone).exists():
                raise forms.ValidationError("This phone number is already registered")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password):
            errors.append(
                'Password must include at least one special character.')

        
            
        if errors:
            raise forms.ValidationError(errors)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password does not match")
        return cleaned_data


class UserProfileForm(StyledFormMixin, forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'block w-full text-gray-500'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if user:
            raise forms.ValidationError("This email is already registered")
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise forms.ValidationError("Phone number must be a valid format")
            user = User.objects.filter(phone_number=phone).exclude(pk=self.instance.pk).exists()
            if user:
                raise forms.ValidationError("This phone number is already registered")
        return phone


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with styled widgets"""
    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Old Password',
        'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
    }))
    
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New Password',
        'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
    }))
    
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm New Password',
        'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
    }))
    
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form"""
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
    }))


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form for password reset"""
    
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New Password',
        'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
    }))
    
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm New Password',
        'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'
    }))
