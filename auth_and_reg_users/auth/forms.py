from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

class SigInUpform(LoginForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    def clean(self):
        super().clean()
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw1 != pw2:
            # raise forms.ValidationError('Пароли не совпадают')
            self.add_error('password', 'Пароли не совпадают')

