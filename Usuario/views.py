from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import logout
from .models import Usuario
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import LoginForm
from .forms import RegistroForm


# view para cadastrar usuario
class RegistroView(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = "Usuario/cadastro.html"
    success_url = reverse_lazy(
        "login"
    )  # Redireciona para a página de login após o cadastro


# view para login de usuario
class LoginView(View):
    form_class = LoginForm
    template_name = "Usuario/login.html"

    # função para passar o formulario alterado
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # função para validar o login
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            senha = form.cleaned_data.get("senha")
            user = authenticate(username=email, password=senha)
            if user is not None:
                login(request, user)
                return redirect(
                    reverse_lazy("meus ativos")
                )  # redireciona para meus ativos apos logar
        return render(request, self.template_name, {"form": form})


class CustomLogoutView(View):

    def get(self, request):
        # Lógica de logout
        logout(request)
        # Redireciona para a página 'home' após o logout
        return redirect(reverse_lazy("login"))
