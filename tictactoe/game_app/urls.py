from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/<int:player_id>/', views.play, name='play'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/<int:player_id>/', views.leaderboard, name='leaderboard'),
]
