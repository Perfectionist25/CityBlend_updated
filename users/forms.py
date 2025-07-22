from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from kafe.bulma_mixin import BulmaMixin


class SignUpForm(BulmaMixin, UserCreationForm):
    username = forms.CharField(label='Create username')
    email = forms.EmailField(label='Write email')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Create password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Эта электронная почта уже используется.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя пользователя уже занято.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают.")
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class SignInForm(BulmaMixin, AuthenticationForm):
    username = forms.CharField(label='Введите имя')
    password = forms.CharField(widget=forms.PasswordInput(), label='Введите пароль')

    class Meta:
        model = User
        fields = ('username', 'password')

class EditProfileForm(BulmaMixin, forms.ModelForm):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email address')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ResetPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Old password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Create new password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat new password'
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError(
                "Passwords do not match."
            )
        return cleaned_data

    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        if commit:
            user.save()
            if request:
                messages.success(request, 'Your password has been successfully changed.')
        return user


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']