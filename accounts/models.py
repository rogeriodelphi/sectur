from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TIPO_USUARIO = (
        ('COMERCIANTE', 'Comerciante'),
        ('SECRETARIA', 'Secretária'),
    )

    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)