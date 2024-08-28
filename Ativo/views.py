from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ativo, Historico
from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime
from decouple import config
import requests

from Ativo import models


def cotacao(request):

    # url de conexção da api
    url = config("RapidUrl")

    # querystring = {"symbol": f"{codigo}.SA"}

    # Instrução de codigo para ativo
    querystring = {"symbol": "PETR4.SA"}

    # chave de acesso e hosta para api
    headers = {
        "x-rapidapi-key": config("RapidKey"),
        "x-rapidapi-host": config("RapidHost"),
    }

    # extraindo dados da api
    response = requests.get(url, headers=headers, params=querystring)

    # tratamento de dados para armazenamento
    data = response.json()

    data_tratado = data["data"][0]["quote"]

    data_quotes = data_tratado["regularMarketPrice"]

    print(f"cotação: {data_quotes}, horario: {datetime.now()}")

    return render(request, "ativo/cotacao.html", {"data": data})


# def teste(request):
#     ativo = Ativo.objects.all()
#     return render(request, "ativo/teste.html", {"ativos": ativo} )


class AtivoListView(LoginRequiredMixin, ListView):
    model = Ativo


class AtivoCreateView(LoginRequiredMixin, CreateView):
    model = Ativo
    fields = ["codigo", "periodicidade", "valor_de_compra", "valor_de_venda"]
    success_url = reverse_lazy("Meus Ativos")

    def form_valid(self, form):
        print(self.request.user)
        # Define o usuário logado como proprietário do ativo
        form.instance.usuario = self.request.user
        return super().form_valid(form)
