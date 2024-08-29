from Ativo.views import cotacao
from celery import shared_task
from Ativo.models import Ativo, Historico
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from decouple import config
from setup.celery_app import app


@app.task()
def cotacoes():
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
