from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Ativo, Historico
from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.core.mail import send_mail


# classe para exibir a lista de ativos
class AtivoListView(LoginRequiredMixin, ListView):
    model = Ativo

    def preco():
        preco = Ativo.historico.order_by("data_hora").first()
        print(preco)
        return preco.preco


# classe para adicionar um ativo ao monitoramento
class AtivoCreateView(LoginRequiredMixin, CreateView):
    model = Ativo
    fields = ["codigo", "periodicidade", "valor_de_compra", "valor_de_venda"]
    success_url = reverse_lazy("meus ativos")

    def form_valid(self, form):
        if not self.request.user:
            print("usuario vazio")
        # Define o usuário logado como proprietário do ativo
        form.instance.usuario = self.request.user
        return super().form_valid(form)


# classe para editar as informações de um ativo
class AtivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Ativo
    fields = ["periodicidade", "valor_de_compra", "valor_de_venda"]
    success_url = reverse_lazy("meus ativos")


# classe para deletar um ativo
class AtivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Ativo


# classe para mostrar o historico de cotações de cada ativo
class HistoricoListView(LoginRequiredMixin, ListView):
    model = Historico
    template_name = "historico_list.html"
    context_object_name = "historico_list"
    paginate_by = 10

    # função responsavel por buscar o ativo correspondente a aquele historico
    def get_queryset(self):
        # Busca o ativo pelo id que será passado na URL
        ativo = get_object_or_404(Ativo, id=self.kwargs["ativo_id"])
        # Filtra os históricos relacionados ao ativo
        return Historico.objects.filter(ativo=ativo).order_by("-data_hora")

    # função para passar o ativo por context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa o ativo para o context, para poder exibir o código do ativo na página
        context["ativo"] = get_object_or_404(Ativo, id=self.kwargs["ativo_id"])
        return context
