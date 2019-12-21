from enum import Enum
from django import forms
from django.db import models
from django_google_maps import fields as map_fields
from django_enum_choices.fields import EnumChoiceField
#from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Permission, User
#from django.forms import ModelForm
from geoposition.fields import GeopositionField

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Status(Enum):
    F = 'Finalized'
    P = 'In Progresss'

class Game(models.Model):
    name = models.CharField(max_length=100)
    player = models.ManyToManyField(User)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='creator_game')
    registration_on = models.DateTimeField
    address_center = models.CharField(max_length = 100)
    position = GeopositionField()
    radius = models.IntegerField()
    status = EnumChoiceField(Status)
    def __str__(self):
        return self.name

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name','address_center','position','radius')


class Treasure(models.Model):
    name = models.CharField(max_length=100)
    clue = models.TextField()
    solution = models.TextField()
    address = models.CharField(max_length = 100)
    position = GeopositionField()
    treasure_img = models.ImageField(upload_to='treasure/%Y/%m/%d')

    def __str__(self):
        return self.name

class TreasureForm(forms.ModelForm):
    class Meta:
        model = Treasure
        fields = ('name','clue','solution','address','position','treasure_img')
        #widgets = {'position': forms.HiddenInput()}
        widgets = {
            'clue': forms.Textarea(attrs={'rows': 2}),
            'solution': forms.Textarea(attrs={'rows': 2}),
        }

class Player_Treasure_Found(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    treasure_id = models.ForeignKey(Treasure, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    prove_img = models.ImageField(upload_to=user_directory_path)
    prove_date = models.DateTimeField()
