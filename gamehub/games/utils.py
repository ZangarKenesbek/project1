def average_rating(ratings):
    return round(sum(ratings) / len(ratings), 1) if ratings else None
