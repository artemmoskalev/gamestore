from django.db import models
from gamedata.models import Game
from django.contrib.auth.models import User

""" Used to create the information about some particular game for a given user """
class GameState(models.Model):
    state = models.TextField(default="")
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    
class GameScore(models.Model):
    score = models.FloatField(default=0)
    time = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)