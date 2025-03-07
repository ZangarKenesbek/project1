from django import forms
import re
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
        fields = ['game', 'rating', 'comment']
        widgets = {
            'game': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your review'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating
