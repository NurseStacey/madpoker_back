###the code in this file is for testing purposes only

from gameresults.models import GameResultModel
from players.models import PlayerModel
from games.models import PlayedGameModel,GameModel
import datetime
from django.http import JsonResponse

players_for_testing=[
    'DAVID GEARHART',
    'KIM WOOLAM',
    'CHRISTOPHE POULIN',
    'JEANETTE MEIN',
    'JEFF MOORE',
    'SHAD POLLARI',
    'JAYE TYLER',
    'CHARLIE TURNER',
    'RANDY SMITH',
    'LA CUCARACHA',
    'MATT STEIN',
    'MICHAEL ANDERSON-NATHE',
    'DEBBIE WEST',
    'TRAVIS SPENCER',
    'FRANK HUI',
    'RON BOYLES',
    'RUDY MAMARADLO',
    'CATHY CULVER',
    'SCOTT MEIN',
    'DAVID ANDEREGG'
]

import math
def isPrime(this_number):

    for index in range(math.sqrt(this_number)):
        if this_number%index==0:
            return False
        
    return True
def CreateTestingData(request, *args, **kwargs):
    
    PlayedGameModel.objects.all().delete()
    PlayerModel.objects.all().delete()
    GameResultModel.objects.all().delete()

    password='password'
    phone='503-555-1212'

#first make the players
    for index,one_name in enumerate(players_for_testing):
        partitioned_name=one_name.partition(' ')
        first_name=partitioned_name[0]
        last_name=partitioned_name[2]
        player=last_name+first_name[0]
        email=player+'@gmail.com'
        PlayerModel.objects.create(
            id=index+100,
            password=password,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            player=player,
            email=email
        )

    initial_date = datetime.date(2025,7,1)

    for days_offset in range(7):
        this_date=initial_date + datetime.timedelta(days=days_offset)
        these_games=GameModel.objects.filter(week_day__iexact=this_date.strftime('%A'))
        one_week=datetime.timedelta(days=7)
        end_date=datetime.date(2026,3,30)
        while this_date<end_date:

            for one_game in these_games:
                this_played_game=PlayedGameModel.objects.get_or_create(
                    which_game=one_game,
                    date=this_date
                )

                index_for_iterator =(datetime.date(2026,9,1)-this_date).days
                while not isPrime(index_for_iterator):
                    index_for_iterator+=1
                    
                this_order=[]
                for index in range(19):
                    if not index_for_iterator%19 in this_order:  ###this should not happen if I remember prime cycles correctly
                        this_order.append(index_for_iterator%19)
                    index_for_iterator+=index_for_iterator

                for position,one_index in enumerate(this_order):
                    this_player=PlayerModel.objects.get(id=one_index+100)
                    points=19-position
                    if position<10:
                        points*=2
                    GameResultModel.objects.create(
                        player=this_player,
                        position=position,
                        points=points,
                        game=this_played_game
                    )

            this_date=this_date+one_week

    return JsonResponse({})