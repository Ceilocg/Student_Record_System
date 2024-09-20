from django import forms
from django.contrib.auth.models import User
from .models import ExcelFile
from .models import CertificateRequest
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm



class CertificateRequestForm(forms.ModelForm):
    class Meta:
        model = CertificateRequest
        fields = ['name', 'email', 'lrn', 'certificate_type', 'request_purpose']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'lrn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your LRN number'}),
            'certificate_type': forms.Select(attrs={'class': 'form-control'}),
            'request_purpose': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'State the purpose of the request', 'rows': 3}),
        }

class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file', 'name']

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=(
            "Your password must contain at least 8 characters, "
            "cannot be entirely numeric, and cannot be a common password."
        ),
        error_messages={
            'required': 'Please enter a password.',
            'invalid': 'Invalid password format.',
            'min_length': 'Password must be at least 8 characters.',
        },
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Re-enter the password for verification.",
        error_messages={
            'required': 'Please confirm your password.',
            'invalid': 'Passwords do not match.',
        },
    )

    auth_enabled = forms.ChoiceField(
        choices=[(True, 'Enabled'), (False, 'Disabled')],
        widget=forms.RadioSelect,
        label="Password-based authentication:",
        help_text=(
            "Whether the user will be able to authenticate using a password or not. "
            "If disabled, they may still be able to authenticate using other methods like SSO or LDAP."
        ),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'auth_enabled']
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.',
            'email': 'Required. Enter a valid email address.',
        }
        error_messages = {
            'username': {
                'required': 'Please enter a username.',
                'invalid': 'Invalid characters in the username.',
                'max_length': 'Username must be 150 characters or fewer.',
            },
            'email': {
                'required': 'Please enter an email address.',
                'invalid': 'Enter a valid email address.',
            },
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserCreationForm(UserCreationForm):
    # Add additional fields if needed
    auth_enabled = forms.BooleanField(required=False, label='Enable Two-Factor Authentication')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'auth_enabled']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class CustomUserChangeForm(UserChangeForm):
    # This form allows updating user data
    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateUserForm(forms.ModelForm):
    # Form for updating user details
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='New Password', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm New Password', required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data
    
