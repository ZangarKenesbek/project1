from django.urls import path
from . import views
from .views import submit_review

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/review/', submit_review, name='submit_review'),
]
