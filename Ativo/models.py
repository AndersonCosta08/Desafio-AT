from django.db import models
from Usuario.models import Usuario
# Create your models here.

class Ativo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ativos')
    codigo = models.CharField(max_length=10, null=False, blank=False)
    nome = models.CharField(max_length=10, null=False, blank=False)
    periodicidade = models.DurationField(blank=False, null=False)
    valor_de_compra = models.FloatField(null=False)
    valor_de_venda = models.FloatField(null=False) 

    def __str__(self):
        return self.all()


class Historico(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE, related_name='historico')
    preco = models.FloatField(null=False)
    data_hora = models.DateTimeField(null=False, auto_now_add=True)
    

    def __str__(self):
        return self.all()
    
    def criar_historico(self):
        return
    
    def create_user(self, ativo, preco):
        historico = self.model(ativo=ativo, preco=preco)
        historico.save(using=self._db)
        return historico
    



