from django.db import models
from Usuario.models import Usuario

# Create your models here.


# classe Ativo
class Ativo(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="ativos"
    )
    codigo = models.CharField(max_length=10, null=False, blank=False)
    periodicidade = models.IntegerField(blank=False)
    valor_de_compra = models.FloatField(null=False)
    valor_de_venda = models.FloatField(null=False)


# classe Historico
class Historico(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE, related_name="historico")
    preco = models.FloatField(null=False)
    data_hora = models.DateTimeField(
        null=False,
    )
