from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class BaseModel(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True)

    # 📍 LOCALIZAÇÃO (MAPA)
    latitude = models.FloatField()
    longitude = models.FloatField()

    imagem = models.ImageField(upload_to='uploads/')

    aprovado = models.BooleanField(default=False)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PontoTuristico(BaseModel):
    pass


class Hotel(BaseModel):
    pass


class Restaurante(BaseModel):
    pass


class Evento(BaseModel):
    data_evento = models.DateField()