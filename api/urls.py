from django.urls import path

from api.views import home, mlb, scheduleView, FavoriteView, getFavoriteTeams, SetFavorite, progresso, ScoreLastGame

urlpatterns = [
    path('api/home/', home, name='home'),
    path('api/mlb/', mlb, name='mlb'),  # para el standing
    path('api/proximo/<int:idteam>', scheduleView, name='proximo'),  # obtener juego proximo
    # path('api/progress/<int:gameid>', progresso, name='progress'), #progerso del juego
    path('api/favorite/', FavoriteView.as_view(), name='favorite'),  # ver favorito
    path('api/getfavorite/<str:idTeams>', getFavoriteTeams, name='getfavorite'),  # filtrar favorito
    path('creupFavorito', SetFavorite, name='creupFavorito'),  # crear o cambiar de favorito
    path('api/score', ScoreLastGame, name='score'),  # crear o cambiar de favorito

]
