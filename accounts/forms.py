from django import forms
from django.contrib.auth.models import User, auth
from .models import Profile

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo','bio')


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', )


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo','bio')


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type':"text", 'name':"first_name", 'class':"form-control input-sm", 'placeholder':"First Name"}))

    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "text", 'name': "last_name", 'class': "form-control input-sm", 'placeholder': "Last Name"}))

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type':"text", 'name':"username", 'class':"form-control input-sm", 'placeholder':"Username"}))

    email = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "email", 'name': "email",  'class': "form-control input-sm", 'placeholder': "Email Address"}))

    password1 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "password", 'name': "password1", 'class': "form-control input-sm", 'placeholder': "Password"}))

    password2 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "password", 'name': "password2", 'class': "form-control input-sm", 'placeholder': "Confirm Password"}))




    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')


        if username and email and password1 and password2:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username taken")
            if password1 != password2:
                raise forms.ValidationError("Passwords confirm failed. Try again!")



class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type':"text", 'name':"username", 'class':"form-control input-sm", 'placeholder':"Username"}))

    password = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "password", 'name': "password1", 'class': "form-control input-sm", 'placeholder': "Password"}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not auth.authenticate(username=username, password=password):
            raise forms.ValidationError("Enter a valid username and password.")


class EditForm(forms.Form):

    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "text", 'name': "first_name", 'class': "form-control input-sm",
                   'placeholder': "First Name"}))

    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "text", 'name': "last_name", 'class': "form-control input-sm", 'placeholder': "Last Name"}))

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "text", 'name': "username", 'class': "form-control input-sm", 'placeholder': "Username"}))

    email = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "email", 'name': "email", 'class': "form-control input-sm", 'placeholder': "Email Address"}))

    password1 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "password", 'name': "password1", 'class': "form-control input-sm", 'placeholder': "New Password"}))

    password2 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': "password", 'name': "password2", 'class': "form-control input-sm", 'placeholder': "Confirm Password"}))



    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if username and email and password1 and password2:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username taken")
            if password1 != password2:
                raise forms.ValidationError("Passwords confirm failed. Try again!")