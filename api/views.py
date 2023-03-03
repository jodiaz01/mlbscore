from datetime import datetime, timedelta

import statsapi
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from statsapi import *
from rest_framework.serializers import ModelSerializer
from api.models import Favorite

import logging


# logger = logging.getLogger('statsapi')
# logger.setLevel(logging.DEBUG)
# rootLogger = logging.getLogger()
# rootLogger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(name)s(%(thread)s) - %(message)s")
# ch.setFormatter(formatter)
# rootLogger.addHandler(ch)


@api_view(['GET'])
def mlb(request):
    lista = []

    datas = standings_data()
    for x in datas:
        if datas:
            lista.append(datas[x])
    resp = Response(data=lista, status=status.HTTP_200_OK)
    return resp


'''
# dataset=[standings(division='all')]661648
# data = mlbgame.game.box_score(111)
# pruebas(request)
# progresso(request , gameid=662043)
# part = statsapi.game_highlight_data(gamePk=663456)
# for x in part:
#     print(x['playbacks'])
# print(game_highlights(663456))
'''


@api_view(['GET'])
def scheduleView(request, idteam):
    lista = []
    mont_is = datetime.today().month

    dat = timedelta(days=-1)

    dateofDay = datetime.today() + dat

    fecInic = datetime.strftime(dateofDay, '%m/%d/%Y')

    fechFin = last_day_of_month(dateofDay.year, mont_is)

    resp = ''
    dataset = {}
    if idteam is None or idteam == '':
        idteam = 111
    posiblegame = statsapi.schedule(start_date=fecInic, end_date=fechFin, team=idteam)
    # print(posiblegame)
    idgame = None
    progress = ''
    homes = ''
    away = ''
    videoplay = ''
    x = 0
    for x in posiblegame:
        idgame = x['game_id']
        statuss = x['status']
        varte = progresso(request, gameid=idgame, status=statuss)
        # videoplay =videoGame(request, gameid=idgame, status=statuss)
        if varte:
            for n in varte:
                progress = n['inning']
                homes = n['home']
                away = n['away']
        else:
            progress = ''
            homes = ''
            away = ''
        videoplay = videoHighLight(request, gameid=idgame, status=statuss)
        dataset = {
            'game_id': x['game_id'],
            'hora': x['game_datetime'],
            'status': x['status'],
            'home': x['home_name'],
            'away': x['away_name'],
            'homepitcher': x['home_pitcher_note'],
            'awaypitcher': x['away_pitcher_note'],
            'phomepitcher': x['home_probable_pitcher'],
            'pawaypitcher': x['away_probable_pitcher'],
            'homescore': x['home_score'],
            'awayscore': x['away_score'],
            'homeid': x['home_id'],
            'awayid': x['away_id'],
            'iningprogreso': x['current_inning'],
            'statuining': x['inning_state'],
            'progress': progress,
            'pghome': homes,
            'pgaway': away,
            'video': videoplay[0],
            'title': videoplay[1]

        }
        lista.append(dataset)

    resp = Response(data={'horarios': lista}, status=status.HTTP_200_OK)
    return resp


def progresso(request, gameid, status):
    dictas = {}
    list = []
    if status != 'Scheduled':
        part = linescore(gamePk=gameid).splitlines()

        dictas = {
            'inning': part[0],
            'away': part[1],
            'home': part[2],
        }
        list.append(dictas)
    # part =  statsapi.game_highlight_data(gamePk=661236)

    return list


def videoHighLight(request, gameid, status):
    lista = []
    lista2 = []
    dicion = {}
    if status != 'Scheduled':
        try:
            apidata = statsapi.game_highlight_data(gamePk=gameid)

            if apidata:
                for x in apidata:
                    mapa = x['playbacks']
                    # print(x['id'])
                    lista2.append(x['id'])
                    for i in mapa:
                        filetipes = i['url']
                        if filetipes.endswith('.mp4') and not filetipes.endswith(
                                '_16000K.mp4'):  # solo 4k o no sea 16000k si quiero mas resolucion deja asta el punto
                            lista.append(i['url'])
        except Exception:
            return lista, lista2
    return lista, lista2


def home(request):
    contex = standings(division='all')
    apart = statsapi.latest_season()
    print(statsapi.last_game(135))
    return render(request, 'index.html', context={'mlb': contex, 'str': apart})


# print(season_data['seasonId'])
# most_recent_game_id = statsapi.last_game(teamId=117 )
# print(statsapi.boxscore(most_recent_game_id))
# print(statsapi.boxscore_data( most_recent_game_id))
# print(statsapi.game_scoring_plays(662000))


class FavoriteView(APIView):
    @staticmethod
    def get(request):
        fav = Favorite.objects.all()
        data = Serial_Favorite(fav, many=True).data
        return Response({'favorito': data})


@api_view(['GET'])
def getFavoriteTeams(request, idTeams):
    favorite = Favorite.objects.filter(seraial=idTeams)
    if favorite:
        maps = {'horarios': favorite[0].teamId}

    else:
        maps = {'horarios': 'No'}
    resp = Response(data=maps, status=status.HTTP_201_CREATED)
    return resp


@api_view(['POST'])
def SetFavorite(request):
    teaid = request.POST['teamid']
    name = request.POST['name']
    device = request.POST['device']
    favorite = Favorite.objects.filter(seraial=device, isFavorite=True)
    if favorite:
        Favorite.objects.filter(seraial=device).update(
            teamId=teaid,
            nameTeams=name,
            seraial=device,
            user='',
            isFavorite=True
        )
    else:
        Favorite.objects.get_or_create(
            teamId=teaid,
            nameTeams=name,
            seraial=device,
            user='',
            isFavorite=True
        )
    resp = Response(data={'message': 'Favorito Asignado..!', }, status=status.HTTP_201_CREATED)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp


'---------------------------------------------UTILES COMMUN--------------------------------------------------------'


def Mes_delano(x):
    m = ''

    if x == 1:
        m = 'Enero'
    elif x == 2:
        m = 'Febrero'
    elif x == 3:
        m = 'Marzo'
    elif x == 4:
        m = 'Abril'
    elif x == 5:
        m = 'Mayo'
    elif x == 6:
        m = 'Junio'
    elif x == 7:
        m = 'Julio'
    elif x == 8:
        m = 'Agosto'
    elif x == 9:
        m = 'Septiembre'
    elif x == 10:
        m = 'Octubre'
    elif x == 11:
        m = 'Noviembre'
    elif x == 12:
        m = 'Diciembre'
    return m


def last_day_of_month(year, month):
    """ Work out the last day of the month """
    last_days = [31, 30, 29, 28]
    # print('---------------------------------------------------------', month)
    for i in last_days:
        try:
            end = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return end.date()
    return None


""" Serializador """


class Serial_Favorite(ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


@api_view(['GET'])
def ScoreLastGame(request):
    mont_is = datetime.today().month
    lista = []
    dat = timedelta(days=-1)

    dateofDay = datetime.today() + dat

    fec_inc = datetime.strftime(dateofDay, '%m/%d/%Y')

    fec_fin = datetime.today()
    posiblegame = statsapi.schedule(start_date=fec_inc, end_date=fec_fin.strftime('%m/%d/%Y'))
    for x in posiblegame:
        datar = linescore(gamePk=x['game_id']).splitlines()

        mapa = {
            'score': datar,
            'status': x['status']
        }
        lista.append(mapa)
    resp = Response(data={'games': lista}, status=status.HTTP_200_OK)
    return resp


""" ---------------------------------------- Pruebas necesarias """


def pruebas(request):
    # valores=  statsapi.get('team', {'teamId': 143})# reeferencia teams

    # valores=statsapi.boxscore(661648,battingInfo=True,fieldingInfo=True,pitchingBox=True,gameInfo=True) retorna info del juego del dia anterior
    # valores=statsapi.boxscore(661236, battingInfo=False,fieldingInfo=False, pitchingBox=False) #lo mismo mas corto
    valores = statsapi.game_highlights(663456)  # lo mas detacado con video del juego anterior
    # valores=statsapi.game_scoring_plays(gamePk=661236) #las carreara anotada del juego anterior
    # valores = statsapi.linescore(661648, timecode=None) resultado del juego anterior
    # valores= statsapi.boxscore_data(661648,20220831) JSON DE CADA SUCESO DEL JUEGO
    # valores = statsapi.boxscore(661649, battingInfo=False,fieldingInfo=False,pitchingBox=False,gameInfo=False) resultado juego en curso
    # valores = statsapi.game_scoring_play_data(661236)
    # valores = linescore(663213)  # // resultado envivo anotaciones

    # valores = statsapi.game_highlight_data(661649)# juego actual
    # part = linescore(661236)
    # valores = part.splitlines()
    # valores = valores
    # part = valores = statsapi.game_highlight_data(gamePk=661923)
    # print(part[0]['playbacks'])
    # list = []
    # for x in part:
    #     print(x['playbacks'])
    #     list.append(x['playbacks'])

    print(valores.splitlines())
    return list
