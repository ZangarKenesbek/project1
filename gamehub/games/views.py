from django.core.exceptions import ValidationError
from .utils import average_rating
from .forms import GameFilterForm
import re
from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from .forms import ReviewForm

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

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    reviews = game.review_set.all()
    game_rating = average_rating([review.rating for review in reviews]) if reviews else None
    return render(request, "games/game_detail.html", {"game": game, "game_rating": game_rating, "reviews": reviews})
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
def submit_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.save()
            return redirect("game_detail", pk=game.id)
    else:
        form = ReviewForm(initial={'game': game})

    return render(request, "games/submit_review.html", {"form": form, "game": game})