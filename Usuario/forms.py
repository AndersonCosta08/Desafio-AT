from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from .models import Usuario


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")
        if email and senha:
            user = authenticate(username=email, password=senha)
            if not user:
                raise forms.ValidationError(
                    "Login inválido. Verifique o email e a senha."
                )
        return super().clean()


class RegistroForm(forms.ModelForm):
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(
        label="Confirme a senha", widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = ["nome", "email", "senha"]

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get("senha")
        confirmar_senha = self.cleaned_data.get("confirmar_senha")
        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        return confirmar_senha

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data["senha"])  # Hash a senha
        if commit:
            user.save()
        return user
