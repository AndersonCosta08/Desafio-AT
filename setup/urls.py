from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from Usuario.views import LoginView, RegistroView

from Ativo.views import AtivoListView, AtivoCreateView, cotacoes

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cotacao/", cotacoes, name="cotacao"),
    path("ativos/", AtivoListView.as_view(), name="meus ativos"),
    path("cadastro/ativo", AtivoCreateView.as_view(), name="cadastrar ativo"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/usuario", RegistroView.as_view(), name="cadastro"),
]
