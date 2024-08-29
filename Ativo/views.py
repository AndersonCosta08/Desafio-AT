from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ativo, Historico
from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config
from django.core.mail import send_mail
import requests

from Ativo import models


def cotacao(codigo):

    # url de conexção da api
    url = config("RapidUrl")

    # Instrução de codigo para ativo
    querystring = {"symbol": f"{codigo}.SA"}

    # Instrução de codigo para ativo
    # querystring = {"symbol": "PETR4.SA"}

    # chave de acesso e hosta para api
    headers = {
        "x-rapidapi-key": config("RapidKey"),
        "x-rapidapi-host": config("RapidHost"),
    }

    # extraindo dados da api
    response = requests.get(url, headers=headers, params=querystring)

    # tratamento de dados para armazenamento
    data = response.json()

    data_tratado = data["data"][0]["quote"]["regularMarketPrice"]

    print(f"cotação: {data_tratado}, horario: {datetime.now()}")

    return data_tratado


# def teste(request):
#     ativo = Ativo.objects.all()
#     return render(request, "ativo/teste.html", {"ativos": ativo} )


class AtivoListView(LoginRequiredMixin, ListView):
    model = Ativo


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


def cotacoes(request):
    ativos = Ativo.objects.all()
    for ativo in ativos:
        # Verificar a última cotação salva para determinar se já passou o intervalo de tempo
        ultima_cotacao = (
            Historico.objects.filter(ativo=ativo).order_by("-data_hora").first()
        )
        if (
            ultima_cotacao is None
            or ultima_cotacao.data_hora
            <= timezone.now() - timedelta(minutes=ativo.periodicidade)
        ):
            preco = cotacao(ativo.codigo)
            if preco is not None:
                # Salva a nova cotação no banco de dados
                Historico.objects.create(ativo=ativo, preco=preco)
                if preco >= ativo.valor_de_venda:
                    send_mail(
                        f"Aviso para venda do ativo: {ativo.codigo}",
                        f"O ativo {ativo.codigo} está acima do valor definido para venda {ativo.valor_de_venda} , apresentando o valor {preco}",
                        config("Email"),
                        [ativo.usuario.email],
                        fail_silently=False,
                    )
                elif preco <= ativo.valor_de_compra:
                    send_mail(
                        f"Aviso para venda do ativo: {ativo.codigo}",
                        f"O ativo {ativo.codigo} está abaixo do valor definido para compra {ativo.valor_de_compra} , apresentando o valor {preco}",
                        config("Email"),
                        [ativo.usuario.email],
                        fail_silently=False,
                    )
    return render(request, "ativo/cotacao.html")
