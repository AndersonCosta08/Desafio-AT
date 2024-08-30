from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from Usuario.views import LoginView, RegistroView, CustomLogoutView

from Ativo.views import (
    AtivoListView,
    AtivoCreateView,
    HistoricoListView,
    AtivoUpdateView,
    AtivoDeleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ativos/", AtivoListView.as_view(), name="meus ativos"),
    path("cadastro/ativo", AtivoCreateView.as_view(), name="cadastrar ativo"),
    path("", LoginView.as_view(), name="login"),
    path("cadastro/usuario", RegistroView.as_view(), name="cadastro"),
    path("ativos/<int:ativo_id>/", HistoricoListView.as_view(), name="historico"),
    path("editar/<int:pk>/", AtivoUpdateView.as_view(), name="editar"),
    path("excluir/<int:pk>/", AtivoDeleteView.as_view(), name="excluir"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
