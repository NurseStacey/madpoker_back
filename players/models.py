from django.db import models

class PlayersModel(models.Model):
    player=models.CharField(default='')
    email=models.EmailField(null=True)
    phone=models.CharField(default='')
    
    @classmethod
    def get_default_pk(cls):
        oneGame, created = cls.objects.get_or_create(
            player='default player', 
            defaults={
                'player':'this is not a player',
            },
        )
        return oneGame.pk        