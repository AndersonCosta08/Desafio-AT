# Desafio-AT

Este projeto consiste em um sistema web para auxiliar investidores em através do monitoramento de ativos e
seu tunel de preço. Para isso, o sistema consulta e armazena as cotações dos respectivos ativos periodicamente e envia um email para o usuario  
quando há possibilidade de negociação

### Tecnologias Utilizadas

- [Python](https://docs.python.org/pt-br/3/)
- [Django](https://docs.djangoproject.com/pt-br/5.1/)
- [Bootstarp](https://getbootstrap.com.br/docs/4.1/getting-started/introduction/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Docker](https://docs.docker.com/reference/)

## Dependências Necessárias

Para execução de tarefas assincornas (monitoramento e envio de email), utilizou-se o Celery como fila de tarefas, tecnologia que necessita de um gerenciador de filas. Dessa forma, utilizou-se uma imagem de um broker Redis no Docker para executar os testes.

```
docker run -d -p 6379:6379 redis
```
Todas as bibliotecas e frmaeworks utilizadas no projeto encontram-se no arquivo requirements.txt, para intala-las basta o seguinte comando:

```
pip install -r requirements.txt
```

## Como rodar o projeto 

Para rodar o projeto localmente basta executar os seguinte comandos em tres terminais diferentes:

Para rodar o servidor django:

```
python manage.py runserver 
```

Para rodar do Celery:
```
celery -A setup worker --loglevel=info
```

Para envio programado da task de monitoramento:
```
celery -A setup beat --loglevel=info
```

Lembrese de iniciar também o seu broker.


## Rotas para acesso da aplicação

- Login - http://127.0.0.1:8000/

- Cadastro de usuario - http://127.0.0.1:8000/cadastro/usuario  

- Logout - http://127.0.0.1:8000/logout

- Pagina inicial - http://127.0.0.1:8000/ativos

- Cadastro de ativo - http://127.0.0.1:8000/cadastro/ativos

- Histórico de um ativo - http://127.0.0.1:8000/ativos/:id 

- Editar um ativo - http://127.0.0.1:8000/editar/:id

- Excluir um ativo - http://127.0.0.1:8000/excluir/:id


