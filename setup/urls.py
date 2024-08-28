"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from Usuario.views import LoginView, RegistroView

from Ativo.views import AtivoListView, AtivoCreateView ,cotacao

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cotacao/", cotacao, name="cotacao"),
    path("ativos/", AtivoListView.as_view(), name= "meus ativos"),
    path("cadastro/ativo",AtivoCreateView.as_view(), name= "cadastrar ativo"),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/usuario', RegistroView.as_view(), name='registro'),
    
]
