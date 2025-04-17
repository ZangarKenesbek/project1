from django.contrib import admin

from .models import Game, Review
# Register your models here.
admin.site.site_header = ("GameHub Admin")
admin.site.register(Game)
admin.site.register(Review)
