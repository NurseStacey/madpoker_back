from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from login_api.models import UserModel
from .serializers import *
from rest_framework import status
from players.serializers import PlayersSerializer
from gameresults.models import GameResultModel
from players.models import PlayerModel
from django.db.models import ProtectedError
from django.http import JsonResponse
import datetime
import itertools

      
class GameModelAPI(APIView):
    #used for getting all games and creating/altering a game
    def get(self, request, *args, **kwargs):

        try:
            Games = GameModel.objects.all()
            serializer = GamesSerializer(Games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request,*args, **kwargs):
        #print('here')
        try:
            serializer = GamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # thisRecord=SectionThrough(
        #     #section=SectionModel.objects.get(name='Texas Holdem'),
        #     game=GameModel.objects.get(id=serializer.data['id']),
        #     description=request.data['description']
        # )

        # thisRecord.save()
        # try:
        #     thisDirector = UserModel.objects.get(id=request.data['director'])
        #     thisRecord.director=thisDirector
        #     thisRecord.save()
        # except:
        #     pass
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OneGameModelAPI(APIView):
    #used when we need to get one game or alter a game.
    def get(self, request, id, *args, **kwargs):

        try:
            Games = GameModel.objects.get(id=id)
            serializer = GamesSerializer(Games)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({'status':'Problem'}, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request,*args, **kwargs):

    #     try:
    #         serializer = GamesSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()

    #             TexasHoldemSection=SectionModel.objects.get(name='Texas Holdem')
    #             try:
    #                 thisSectionThrough=SectionThrough.objects.filter(game=request.data['id']).get(section=TexasHoldemSection)
    #                 thisSectionThrough.description=request.data['description']
    #                 thisSectionThrough.save()
    #                 print('section  updated')
    #             except:
    #                 pass

    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except:
            
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     #
    #     #print(serializer.errors)
    #     return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,id,*args, **kwargs):

        try:
            thisRecord = GameModel.objects.get(id=id)
            thisRecord.delete()
        except ProtectedError:
            pass
            if PlayedGameModel.objects.filter(which_game=thisRecord).filter(finalized=True).count()>0:
                return Response({}, status=status.HTTP_403_FORBIDDEN)
            else:
                PlayedGameModel.objects.filter(which_game=thisRecord).delete()
                thisRecord.delete()

            # print('protected error')
            # for oneSection in SectionThrough.objects.filter(game=thisRecord):
            #     if oneSection.need_to_protect():
            #         return Response({'status':'protected'}, status=status.HTTP_403_FORBIDDEN)  
            
            # try:
            #     for oneSection in SectionThrough.objects.filter(game=thisRecord):
            #         for oneplayedgame in PlayedGameModel.objects.filter(which_game=oneSection):
            #             oneplayedgame.delete()
            #         oneSection.delete()
            
            #     thisRecord.delete() 
            # except Exception as e:
            #     print('other protected error')
            #     print(e)
            #     return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        print("patch")
        try:
            thisRecord = GameModel.objects.get(id=id)
            serializer = GamesSerializer(thisRecord, data=request.data, partial=True)
            #print(request.data)
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({'status':'trouble with updating game'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     SectionToUpdate=None
        #     AllSectionThrough=SectionThrough.objects.filter(game=thisRecord)
            
        #     if AllSectionThrough.count()==1:
        #         SectionToUpdate=AllSectionThrough[0]
                
        #     elif AllSectionThrough.filter(section=SectionModel.objects.get(name='Texas Holdem')).count()==1:
        #         print('three')
        #         SectionToUpdate=AllSectionThrough.get(section=SectionModel.objects.get(name='Texas Holdem'))
        #     else:
        #         return Response({'status':'no section updated'}, status=status.HTTP_200_OK)
            
        #     SectionToUpdate.director=UserModel.objects.get(id=request.data['director'])
        #     print(request.data)
        #     SectionToUpdate.description=request.data['description']
        #     print('one')
        #     SectionToUpdate.save()
        #     print('two')
        # except:
        #     return Response({'status':'trouble with section'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   


def InfoForLocations(request, *args, **kwargs):

    return_values = {
        "Sunday":[],
        "Monday":[],
        "Tuesday":[],
        "Wednesday":[],
        "Thursday":[],
        "Friday":[],
        "Saturday":[],
    }

    try:
        for one_game in GameModel.objects.filter(active=True).order_by('venue__venue_name','time'):

            this_dictionary=one_game.GetNextPlayedGameInfo()
            return_values[one_game.week_day].append(this_dictionary)
            # for one_section in SectionThrough.objects.filter(active=True).filter(game=one_game):
            #     this_dictionary['sections'].append(one_section.GetNextPlayedGameInfo())
            #     # this_dictionary['sections'].append({
            #     #     'description':one_section.description,
            #     #     'id':one_section.id,
            #     #     'event':one_section.section.name,
            #     #     'played_game_id':one_section.GetNextPlayedGameID()
            #     # })
            # return_values[one_game.week_day].append(this_dictionary)
    except Exception as e:
        print(e)
        return JsonResponse({
            'data':[],
            'status':'Problem'})
    
    return JsonResponse({
        'data':return_values,
        'status':'No Problem'})

class GameTypeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            GameTypes = GameTypeModel.objects.all()
            serializer = GamesTypesSerializer(GameTypes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request,*args, **kwargs):
        try:
            serializer = GamesTypesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request,id,*args, **kwargs):

        def override_protction():            
            thesePlayedGames.delete()
            theseGames.delete()
            try:
                thisRecord.delete()
                return Response({}, status=status.HTTP_200_OK)
            except:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
                    
        try:
            thisRecord = GameTypeModel.objects.get(id=id)
            thisRecord.delete()

        except ProtectedError:
            theseGames=GameModel.objects.filter(venue=thisRecord)
            thesePlayedGames = PlayedGameModel.objects.filter(which_game__in=theseGames).filter(date__lt=date.today())
            if thesePlayedGames.count()==0:
                thesePlayedGames = PlayedGameModel.objects.filter(which_game__in=theseGames)
                override_protction()
            else:
                thesePlayedGames = PlayedGameModel.objects.filter(which_game__in=theseGames)
                players = [x  for thisGame in thesePlayedGames for x in thisGame.player_results.all()]
                if len(players)==0:
                    override_protction()

            return Response({}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)
    
    def patch(self, request,id,*args, **kwargs):
        try:
            thisRecord = GameTypeModel.objects.get(id=id)
            serializer = GamesTypesSerializer(thisRecord, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_200_OK)   
    
class GamesForRostersView(APIView):
    def get(self, request,*args, **kwargs):
        all_game_data=[]

        for oneGame in GameModel.objects.exclude(description='default game'):
            all_game_data.append(oneGame.RosterDictionary())
        
        #all_venues = list(set([x['venue'] for x in all_game_data]))
        pass

        return Response({
            'all_game_data':all_game_data,
            'directors':set([x['director'] for x in all_game_data]),
            'venues':set([x['venue'] for x in all_game_data]),
            'all_dates':[x for y in all_game_data for x in y['dates']]
        }, status=status.HTTP_200_OK)   

class GameInfoForReview(APIView):
    def get(self, request, *args, **kwargs):
        return_value=[]

        try:
            for oneGame in GameModel.objects.all():
                return_value.append({
                    'title':oneGame.GetText(),
                    'dates':[x.get_date_with_ID() for x in self.played_games.all()]
                })
        except Exception as e:
            print(e)
            return Response({'status':'problem getting game info'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'all_data':return_value
        })
    
class PlayedGamesEvents(APIView):
    def get(self, request,  id, *args, **kwargs):

        try:
            thisGame = PlayedGameModel.objects.get(id=id)
            #serializer= PlayedGamesSerializer(thisGame, many=True)
            #print(serializer.data)
            return Response({'data':thisGame.get_players()},status=status.HTTP_200_OK)
        except Exception as e:

            print(e)
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,id,*args,**kwargs):
        try:
            thisGame = PlayedGameModel.objects.get(id=id)
            thisGame.finalized=request.data['finalized']
            thisGame.save()
            
            return Response({'status':'finalized'},status=status.HTTP_200_OK)
        except:
            return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

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

                index_for_iterator =(date(2026,9,1)-this_date).days
                while not isPrime(index_for_iterator):
                    index_for_iterator+=1
                    
                this_order=[]
                for index in range(19):
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

    #print('here')
    return JsonResponse({})

# class GetThisPlayerResults(APIView):
#     def get(self, request, id, *args, **kwargs):

#         if id==-1:
#             return Response({}, status=status.HTTP_100_CONTINUE)
        
#         print(request.data)
#         try:
#             allGames=PlayedGameModel.objects.filter(finalized=True)
              

#             # if request.data['venueID']!=-1:
#             #     thisVenue=VenueModel.objects.get(id=request.data['venueID'])
#             #     allGames=allGames.filter(which_game__in=
#             #                              SectionModel.objects.filter(game__in=
#             #                                                          GameModel.objects.filter(venue=thisVenue)))

#             # if request.data['seasonID']!=-1:
#             #     this_season=SeasonModel.objects.get(id=request.data['seasonID'])
#             #     start_date=this_season.start_date
#             #     end_date=this_season.end_date
#             #     allGames=allGames.filter(date__gte=start_date).filter(date__le=end_date)

#             return_values=[]
#             the_seasons=[]
#             the_venues=[]
#             thisPlayer=PlayerModel.objects.get(id=id)
#             for oneGame in GameResultModel.objects.filter(game__in=allGames).filter(player=thisPlayer):
#                 return_values.append({
#                     'result_test':oneGame.this_result(),
#                     'venue':oneGame.game.get_venue_name(),
#                     'season':oneGame.game.get_season()
#                     })
#                 the_seasons.append(oneGame.game.get_season())
#                 the_venues.append(oneGame.game.get_venue_name())

#             return Response({
#                 'all_results':return_values,
#                 'the_venues':set(the_venues),
#                 'the_seasons':set(the_seasons)
#                 }, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             print(e)

#             return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)
        
# class GetAllGamesInfoGameView(APIView):
#     def get(self, request, *args, **kwargs):

#         return_value={
#             'game_dictionaries':[],
#             'all_dates':[],
#             'all_seasons':[],
#             'sections':[],
#             'venues':[]
#         }
#         try:
#             for one_played_game in PlayedGameModel.objects.filter(finalized=True):
#                 return_value['game_dictionaries'].append(one_played_game.get_dictionary_for_results_view())

#             if return_value['game_dictionaries']==[]:
#                 return Response({'status':'no finalized games'}, status=status.HTTP_200_OK)

#             return_value['venues']=list(set([x['venue'] for x in return_value['game_dictionaries']])).sort()

#             return_value['all_dates']=list(set([x['date'] for x in return_value['game_dictionaries']])).sort().reversed()
#             return_value['all_seasons']=list(set([x['season'] for x in return_value['game_dictionaries']])).sort()
#             return_value['sections']=list(set([x['section'] for x in return_value['game_dictionaries']])).sort()

#             return Response(return_value, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)

#             return Response({'status':'problem'}, status=status.HTTP_400_BAD_REQUEST)

 

# # class NewPlayerRegistrationAPI(APIView):
# # #used for registering a new player and signing up for game
# #     def post(self, request,*args, **kwargs):
        
# #         try:
# #             newPlayerSerializer = PlayersSerializer(data=request.data['new_player'])
# #             if newPlayerSerializer.is_valid():
# #                 newPlayerSerializer.save()    
            
# #             return RegisterForGame(newPlayerSerializer.data['id'],request.data['which_game'])

# #         except Exception as e:
# #             if 'player' in newPlayerSerializer.errors:
# #                 if 'unique' in [x.code for x in newPlayerSerializer.errors['player']]:
# #                     return Response({'status':'duplicit username'}, status=status.HTTP_409_CONFLICT)

# #             return Response({'status':'problem'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
      
    
# class AllSectionsAPI(APIView):
#     def get(self, request, *args, **kwargs):

#         try:
#             Sections = SectionThrough.objects.filter(active=True)
#             serializer = SectionThroughSerializer(Sections, many=True)
#         except Exception as e:
#             print(e)
#             return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data, status=status.HTTP_200_OK)
        
# class GamesByDirectorAPI(APIView):
#     #used if we need the games assigned to one director
#     def get(self, request, id,  *args, **kwargs):

#         if id<0:
#             return Response({'status':'error'}, status=status.HTTP_200_OK)
#         try:
#             Sections = SectionThrough.objects.filter(director=UserModel.objects.get(id=id)).filter(active=True)
#             serializer = SectionThroughSerializer(Sections, many=True)
#         except Exception as e:
#             print(e)
#             return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
  

# class OneGameModelAPI(APIView):
#     #used when we need to get one game or alter a game.
#     def get(self, request, id, *args, **kwargs):

#         try:
#             Games = GameModel.objects.get(id=id)
#             serializer = GamesSerializer(Games)
#             return Response(serializer.data, status=status.HTTP_200_OK)


#         except Exception as e:
#             print(e)
#             return Response({'status':'Problem'}, status=status.HTTP_400_BAD_REQUEST)
    
#     def post(self, request,*args, **kwargs):

#         try:
#             serializer = GamesSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()

#                 TexasHoldemSection=SectionModel.objects.get(name='Texas Holdem')
#                 try:
#                     thisSectionThrough=SectionThrough.objects.filter(game=request.data['id']).get(section=TexasHoldemSection)
#                     thisSectionThrough.description=request.data['description']
#                     thisSectionThrough.save()
#                     print('section  updated')
#                 except:
#                     pass

#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except:
            
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         #
#         #print(serializer.errors)
#         return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request,id,*args, **kwargs):

#         try:
#             thisRecord = GameModel.objects.get(id=id)
#             thisRecord.delete()
#         except ProtectedError:
#             print('protected error')
#             for oneSection in SectionThrough.objects.filter(game=thisRecord):
#                 if oneSection.need_to_protect():
#                     return Response({'status':'protected'}, status=status.HTTP_403_FORBIDDEN)  
            
#             try:
#                 for oneSection in SectionThrough.objects.filter(game=thisRecord):
#                     for oneplayedgame in PlayedGameModel.objects.filter(which_game=oneSection):
#                         oneplayedgame.delete()
#                     oneSection.delete()
            
#                 thisRecord.delete() 
#             except Exception as e:
#                 print('other protected error')
#                 print(e)
#                 return Response({}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:

#             return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({}, status=status.HTTP_200_OK)
    
#     def patch(self, request,id,*args, **kwargs):
#         print("patch")
#         try:
#             thisRecord = GameModel.objects.get(id=id)
#             serializer = GamesSerializer(thisRecord, data=request.data, partial=True)
#             #print(request.data)
#             if serializer.is_valid():
#                 serializer.save()
#         except:
#             return Response({'status':'trouble with updating game'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             SectionToUpdate=None
#             AllSectionThrough=SectionThrough.objects.filter(game=thisRecord)
            
#             if AllSectionThrough.count()==1:
#                 SectionToUpdate=AllSectionThrough[0]
                
#             elif AllSectionThrough.filter(section=SectionModel.objects.get(name='Texas Holdem')).count()==1:
#                 print('three')
#                 SectionToUpdate=AllSectionThrough.get(section=SectionModel.objects.get(name='Texas Holdem'))
#             else:
#                 return Response({'status':'no section updated'}, status=status.HTTP_200_OK)
            
#             SectionToUpdate.director=UserModel.objects.get(id=request.data['director'])
#             print(request.data)
#             SectionToUpdate.description=request.data['description']
#             print('one')
#             SectionToUpdate.save()
#             print('two')
#         except:
#             return Response({'status':'trouble with section'}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({}, status=status.HTTP_200_OK)   

        

# class SectionsAPI(APIView):
    
#     def get(self, request, *args, **kwargs):

#         TextItems = SectionModel.objects.all().order_by('name')
#         serializer = SectionSerializer(TextItems, many=True)
#         return Response(serializer.data)
    
#     def post(self, request,*args, **kwargs):
#         #print(request.data)
#         try:
#             serializer = SectionSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             try:
#                 if 'unique' in [x.code for x in SectionSerializer.errors['name']]:
#                     return Response({'status':'duplicit event name'}, status=status.HTTP_409_CONFLICT)
#             except:
#                 pass
        
#             return Response({'status':'problem'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request,id,*args, **kwargs):
        
#         try:
#             thisRecord = SectionModel.objects.get(id=id)
#             thisRecord.delete()
#         except ProtectedError:
#             return Response({}, status=status.HTTP_403_FORBIDDEN)
#         except Exception as e:
#             return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({}, status=status.HTTP_200_OK)
    
#     def patch(self, request,id,*args, **kwargs):

#         try:
#             thisRecord = SectionModel.objects.get(id=id)
#             serializer = SectionSerializer(thisRecord, data=request.data, partial=True)
            
#             if serializer.is_valid():
#                 serializer.save()
#         except:
#             return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({}, status=status.HTTP_200_OK)   
            

# class SectionsThroughAPI(APIView):
    
#     def get(self, request, *args, **kwargs):

#         try:
#             AllItems = SectionThrough.objects.all()

#             serializer = SectionThroughSerializerSimple(AllItems, many=True)

#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)
        
#     def post(self, request, *args, **kwargs):

#         print(request.data)
#         try:
#             serializer = SectionThroughSerializerSimple(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)            
#         except Exception as e:
#             print(serializer.errors)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request,id,*args, **kwargs):
#         try:
            
#             thisRecord = SectionThrough.objects.get(id=id)

#             serializer = SectionThroughSerializerSimple(thisRecord, data=request.data, partial=True)

#             if serializer.is_valid():
#                 serializer.save()
             
#                 if thisRecord.section.name=='Texas Holdem':
#                     thisGame=thisRecord.game
#                     print(thisGame.venue.venue_name)
#                     #print(request.data('description'))
#                     thisGame.description=request.data['description']
#                     thisGame.save()
#         except:
#             return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response({}, status=status.HTTP_200_OK)      
        