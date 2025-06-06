from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError('Phone must contain digits only')
        if len(phone) != 10:
            raise forms.ValidationError('Phone must be 10 digits')
        return phone

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
