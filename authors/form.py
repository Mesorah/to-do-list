from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=16,
    )

    first_name = forms.CharField(
        label='First name'
    )

    last_name = forms.CharField(
        label='Last name'
    )

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )

    repeat_password = forms.CharField(
        label='Repeat you password',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'repeat_password',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Esse username já existe')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Esse email já existe')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            self.add_error('password', 'As senhas não são iguais')

        if password:
            if len(password) < 8:
                self.add_error('password', 'Password must be at least 8 characters long.') # noqa E501

            has_upper = any(word.isupper() for word in password)
            has_lower = any(word.islower() for word in password)
            has_digit = any(word.isdigit() for word in password)
            has_special = any(word in "!@#$%^&*()-_+=<>?/[]{}|;:," for word in password) # noqa E501

            if not has_upper:
                self.add_error('password', 'Password must contain at least one uppercase letter.') # noqa E501

            if not has_lower:
                self.add_error('password', 'Password must contain at least one lowercase letter.') # noqa E501

            if not has_digit:
                self.add_error('password', 'Password must contain at least one digit.') # noqa E501

            if not has_special:
                self.add_error('password', 'Password must contain at least one special character.') # noqa E501

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username'
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )
