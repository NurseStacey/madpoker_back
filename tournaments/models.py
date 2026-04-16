from django.db import models
from players.models import PlayerModel
from venues.models import VenueModel
from django.utils import timezone
from games.models import GameTypeModel
from datetime import time


class WinnersModel(models.Model):
    player=models.ForeignKey(PlayerModel, null=True, on_delete=models.PROTECT)
    place = models.IntegerField(default=0)
    prize = models.FloatField(default=0)

    def __repr__(self):
        return '{} - ${}'.format(self.player.player, self.prize)
    
class TournamentModel(models.Model):
    name=models.CharField(max_length=100, default='No Tournament Name', unique=True)
    total_prize_pool = models.FloatField(default=0)
    winners = models.ManyToManyField(WinnersModel)
    location = models.ForeignKey(VenueModel, null=True, on_delete=models.PROTECT)
    time = models.TimeField(default=time(10,0))
    date = models.DateField(default=timezone.now())
    override_message = models.TextField(default='', null=True, blank=True)
    game_type = models.ForeignKey(GameTypeModel,  on_delete=models.SET_DEFAULT, default=GameTypeModel.get_default_pk)
    finalized = models.BooleanField(default=False)

    def __repr__(self):
        return self.name

class TournamentPlayersModel(models.Model):
    player=models.ForeignKey(PlayerModel, null=True, on_delete=models.PROTECT)
    position=models.IntegerField(default=0)
    registration_date_time=models.DateTimeField(default=timezone.now)
    tournament=models.ForeignKey(TournamentModel, null=True, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tournament', 'player'], name='tournament_unique_registration')
        ]    