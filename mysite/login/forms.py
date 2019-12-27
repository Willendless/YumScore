from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}
    ))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}
    ))
    password1 = forms.CharField(label='密码', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))
    password2 = forms.CharField(label="密码确认", max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}
    ))
    name = forms.CharField(label="姓名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}
    ))

    # Use clean method to define custom validation rules

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配， 请再次输入")

        return password2


class ProfileForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control','autofocus': ''}
    ))
    password1 = forms.CharField(label='密码', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    password2 = forms.CharField(label="密码确认", max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    name = forms.CharField(label="姓名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    # Use clean method to define custom validation rules

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配， 请再次输入")

        return password2

