from django.db import models
from django.contrib.auth.models import User
from random import randint
from django.templatetags.static import static

class Game(models.Model):
   
    CATEGORIES = (
        ('action', 'action'),
        ('adventure', 'adventure'),
        ('puzzle', 'puzzle'),
        ('strategy', 'strategy'),
        ('sport', 'sport'),
        ('misc', 'misc'),
    )
    
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    url = models.URLField(max_length=250, blank=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='misc')
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.99)

    imageUrl = models.URLField(max_length=250, blank=True)
    maker = models.ForeignKey(User, null=True, related_name="madeGames")
    
    """ instance method returns the string representing URL of the game cover picture """
    def generate_game_cover_pic(self):
        if self.imageUrl == "":
            return static("img/game_noname_" + str(randint(1, 6)) + ".png")
        else:
            return self.imageUrl
    
    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ["name"]	
        
        permissions = (
            ('can_play', 'Can Play'),
            ('can_publish', 'Can Publish'),
        )


""" Class used to track the payments of players """
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    time = models.DateTimeField(auto_now=True)
    payer = models.ForeignKey(User)
    game = models.ForeignKey(Game, related_name="transactions")
    
    def __str__(self):
        return 'From: %s -> to: %s     amount: %s' % (self.payer.username, self.game.name, self.amount)
    