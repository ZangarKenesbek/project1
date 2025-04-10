from django.contrib.auth.models import User
from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)


    def __str__(self):
        return self.title

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"Review by {user_name} for {self.game.title}"

