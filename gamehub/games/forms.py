from django import forms
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Review


class GameFilterForm(forms.Form):
    title = forms.CharField(
        required=False,
        label="Title",
        widget=forms.TextInput(attrs={"placeholder": "Search by title", "class": "form-control"})
    )
    genre = forms.CharField(
        required=False,
        label="Genre",
        widget=forms.TextInput(attrs={"placeholder": "Search by genre", "class": "form-control"})
    )
    min_rating = forms.FloatField(
        required=False,
        label="Min Rating",
        widget=forms.NumberInput(attrs={"step": "0.1", "placeholder": "Min Rating", "class": "form-control"})
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and len(title) > 100:
            raise forms.ValidationError("Title must be 100 characters or less.")
        return title

    def clean_genre(self):
        genre = self.cleaned_data.get("genre")
        if genre and re.search(r'\d', genre):
            raise forms.ValidationError("Genre must not contain numbers.")
        return genre



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter your review"}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }