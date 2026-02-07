from django.db import models
from players.models import PlayerModel
from games.models import PlayedGameModel
from django.utils import timezone

class GameResultModel(models.Model):
    player=models.ForeignKey(PlayerModel,  default=PlayerModel.get_default_pk, on_delete=models.PROTECT)
    position=models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    registration_date_time=models.DateTimeField(default=timezone.now)
    game=models.ForeignKey(PlayedGameModel, null=True, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'player'], name='unique_registration')
        ]