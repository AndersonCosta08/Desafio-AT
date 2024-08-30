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
    path("", LoginView.as_view(), name="login"), #url para login
    path("logout/", CustomLogoutView.as_view(), name="logout"), #url para logout
    path("cadastro/usuario", RegistroView.as_view(), name="cadastro"), #url para cadastro de usuario
    path("ativos/", AtivoListView.as_view(), name="meus ativos"), #url para pagina principal, onde os ativos cadastrados são exibidos
    path("cadastro/ativo", AtivoCreateView.as_view(), name="cadastrar ativo"), #url para cadastro de ativo
    path("ativos/<int:ativo_id>/", HistoricoListView.as_view(), name="historico"), #url para visualização do historico de cotações
    path("editar/<int:pk>/", AtivoUpdateView.as_view(), name="editar"), #url para edição de um ativo
    path("excluir/<int:pk>/", AtivoDeleteView.as_view(), name="excluir"), #utl para excluir um ativo
    
]
