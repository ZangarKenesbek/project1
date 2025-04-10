import re

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .forms import GameFilterForm
from .forms import UserRegisterForm


def index(request):
    return render(request, "base.html")

def game_list(request):
    form = GameFilterForm(request.GET)
    games = Game.objects.all()

    if form.is_valid():
        title_query = form.cleaned_data.get("title")
        genre_query = form.cleaned_data.get("genre")

        if title_query:
            games = games.filter(title__istartswith=title_query)

        if genre_query:
            games = games.filter(genre__icontains=genre_query)

    game_list = []
    for game in games:
        reviews = game.review_set.all()
        game_rating = average_rating([review.rating for review in reviews]) if reviews else None
        number_of_reviews = len(reviews)

        if form.is_valid() and form.cleaned_data.get("min_rating") and game_rating is not None:
            if game_rating < form.cleaned_data["min_rating"]:
                continue

        game_list.append({"game": game, "game_rating": game_rating, "number_of_reviews": number_of_reviews})

    context = {"form": form, "game_list": game_list}
    return render(request, "games/games_list.html", context)

def average_rating(ratings):
    return sum(ratings) / len(ratings) if ratings else None

from django.shortcuts import get_object_or_404, render, redirect
from .models import Game, Review
from .forms import ReviewForm
from .utils import average_rating

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    reviews = game.review_set.all()
    game_rating = average_rating([review.rating for review in reviews]) if reviews else None
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user if request.user.is_authenticated else None
            review.save()
            return redirect("game_detail", pk=game.pk)
    if request.user.is_authenticated:
        max_viewed_games_length = 10
        viewed_games = request.session.get("viewed_games", [])
        viewed_game = [game.id, game.title]

        if viewed_game in viewed_games:
            viewed_games.pop(viewed_games.index(viewed_game))

        viewed_games.insert(0, viewed_game)
        viewed_games = viewed_games[:max_viewed_games_length]
        request.session["viewed_games"] = viewed_games

    return render(
        request,
        "games/game_detail.html",
        {
            "game": game,
            "game_rating": game_rating,
            "reviews": reviews,
            "form": form,
        },
    )


def clean_title(self):
    title = self.cleaned_data.get("title")
    if title and len(title) > 100:
        raise ValidationError("Title must be 100 characters or less.")
    return title
def clean_genre(self):
    genre = self.cleaned_data.get("genre")
    if genre and re.search(r'\d', genre):
        raise ValidationError("Genre must not contain numbers.")
    return genre
@login_required
def submit_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            return redirect("game_detail", pk=game.id)
    else:
        form = ReviewForm()

    return render(request, "games/submit_review.html", {"form": form, "game": game})
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game_list')
    else:
        form = UserRegisterForm()
    return render(request, 'games/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('game_list')
    else:
        form = AuthenticationForm()
    return render(request, 'games/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('game_list')
@login_required
def profile(request):
    return render(request, 'profile.html')
def about_view(request):
    return render(request, 'games/about.html')
@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.user != review.user and not request.user.is_staff:
        return redirect('game_detail', pk=review.game.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('game_detail', pk=review.game.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'games/edit_review.html', {'form': form, 'review': review})