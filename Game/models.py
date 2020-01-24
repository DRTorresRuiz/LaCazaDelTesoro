from enum import Enum, IntEnum
from django import forms
from django.db import models
from django_google_maps import fields as map_fields
from django_enum_choices.fields import EnumChoiceField
#from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Permission, User
from geoposition.fields import GeopositionField
from django.urls import reverse_lazy
from django.utils.timezone import now

def user_directory_path(instance, filename):
    return 'games/{game}/treasure_{treasure}/user_{userid}/{filename}'.format(
        game=instance.game.id,treasure=instance.treasure.id,userid=instance.player.id, filename=filename)

class Status(IntEnum):
    Finalized = 1
    InProgress = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Game(models.Model):
    name = models.CharField(max_length=100)
    player = models.ManyToManyField(User)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='creator_game')
    registration_on = models.DateTimeField
    north_east_bound = GeopositionField(null=True)
    south_west_bound = GeopositionField(null=True)
    status = models.IntegerField(choices=Status.choices(), default=Status.InProgress)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner_game', null=True)

    def __str__(self):
        return self.name
    
    def get_details_url(self):
        return reverse_lazy('details', kwargs={'game_id': self.id})
    
    def get_join_url(self):
        return reverse_lazy('join', kwargs={'game_id': self.id})

    def get_leave_url(self):
        return reverse_lazy('leave', kwargs={'game_id': self.id})
   
    def get_chat_url(self):
        return reverse_lazy('chat', kwargs={'game_id': self.id})

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name','north_east_bound','south_west_bound')


class Treasure(models.Model):
    name = models.CharField(max_length=100)
    clue = models.TextField()
    solution = models.TextField()
    address = models.CharField(max_length = 100)
    position = GeopositionField()
    treasure_img = models.ImageField(upload_to='treasure/%Y/%m/%d', blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')

    def __str__(self):
        return self.name

    def get_found_url(self):
        return reverse_lazy('found', kwargs={'treasure_id': self.id})
    
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
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    treasure = models.ForeignKey(Treasure, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player')
    position = GeopositionField()
    prove_img = models.ImageField(upload_to=user_directory_path,blank=True, null=True)
    prove_date = models.DateTimeField(default=now, editable=False)

class Player_Treasure_Found_Form(forms.ModelForm):
    class Meta:
        model = Player_Treasure_Found
        fields = ('prove_img','position',)
