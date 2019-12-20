from djongo import models
from django.forms import ModelForm

class  Game(models.Model):
    name = models.CharField(max_length=30)
    active = models.BooleanField()

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('name',)

