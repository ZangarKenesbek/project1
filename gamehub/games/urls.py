from django.urls import path
from . import views
from .views import submit_review, register, login_view, logout_view, profile, about_view, edit_review

urlpatterns = [
    path('', views.index, name='home'),
    path('games/', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/review/', submit_review, name='submit_review'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path("about/", about_view, name="about"),
    path('review/edit/<int:pk>/', edit_review, name='edit_review'),

]
