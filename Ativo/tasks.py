from celery import shared_task
from Ativo.models import Ativo, Historico
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.core.mail import send_mail
from decouple import config
import requests


@shared_task(bind=True)
def cotacoes(self):
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
        ) and (time(10, 00, 00) < timezone.now().time() < time(17, 00, 00)):
            # busca as informações do ativo
            preco = cotacao(ativo.codigo)
            if preco is not None:
                # Salva a nova cotação no banco de dados
                Historico.objects.create(
                    ativo=ativo, preco=preco, data_hora=timezone.now()
                )
                # verifica o pipe de venda
                if preco >= ativo.valor_de_venda:
                    # envia o email caso o preco aeja igual ou maior ao valor estipulado
                    send_mail(
                        f"Aviso para venda do ativo: {ativo.codigo}",
                        f"O ativo {ativo.codigo} está acima do valor definido para venda {ativo.valor_de_venda} , apresentando o valor {preco}",
                        config("Email"),
                        [ativo.usuario.email],
                        fail_silently=False,
                    )
                    print('email de venda enviado')
                # verifica o pipe de compra
                elif preco <= ativo.valor_de_compra:
                    # envia o email caso o preco aeja igual ou menor ao valor estipulado
                    send_mail(
                        f"Aviso para venda do ativo: {ativo.codigo}",
                        f"O ativo {ativo.codigo} está abaixo do valor definido para compra {ativo.valor_de_compra} , apresentando o valor {preco}",
                        config("Email"),
                        [ativo.usuario.email],
                        fail_silently=False,
                    )
                    print('email de compra enviado')
    return "tarefa concluida"


# função para requisição de cotações
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

    # extrai o valor do preço do ativo no json de responde
    data_tratado = data["data"][0]["quote"]["regularMarketPrice"]

    print(f"cotação de {codigo}: {data_tratado}, horario: {datetime.now()}")

    return data_tratado
