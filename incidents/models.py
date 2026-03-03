from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    titol = models.CharField(max_length=200)
    descripcio = models.TextField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titol