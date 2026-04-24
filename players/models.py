from django.db import models

class PlayerModel(models.Model):
    player=models.CharField(default='', unique=True)
    email=models.EmailField(null=True, blank=True)
    phone=models.CharField(null=True, default='', blank=True)
    first_name=models.CharField(null=True, default='', blank=True)
    last_name=models.CharField(null=True,  default='', blank=True)
    password=models.CharField(null=True,  default='', blank=True)

    @classmethod
    def get_default_pk(cls):
        oneGame, created = cls.objects.get_or_create(
            player='default player', 
            defaults={
                'player':'this is not a player',
            },
        )
        return oneGame.pk        
    
    def __repr__(self):
        return self.player
    
class WinnersModel(models.Model):
    player=models.ForeignKey(PlayerModel,
                             null=True, 
                             related_name='winning_player',
                             on_delete=models.PROTECT)
    image = models.ImageField(default='winners_pics/default.jpg',
                                     upload_to='winners_pics')    
    display_text = models.CharField(max_length=100, null=True)