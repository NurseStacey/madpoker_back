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

    def this_result(self):
        game_info = self.game.get_dictionary_for_results_view()

        return '{} - {} - {} - {}'.format(game_info['venue'],game_info['date'], self.position, self.points)