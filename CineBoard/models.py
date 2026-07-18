from django.db import models
from django.contrib.auth.models import User

class CustomUser(User):
    icon = models.ImageField(upload_to='work/')
    GENDER = (
        ('F', 'F'),
        ('M', 'M')
    )
    gender = models.CharField(max_length=100, choices=GENDER, default='M')

    def __str__(self):
        return self.username


from django.db import models

class Movie(models.Model):
    GENRES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'),
    )
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    poster = models.ImageField(upload_to='media/', null=True, blank=True)
    genre = models.CharField(max_length=100, choices=GENRES, verbose_name='Genre')
    release_year = models.IntegerField()
    director = models.CharField(max_length=150)
    duration_minutes = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    country = models.CharField(max_length=100, verbose_name='Country')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    views = models.IntegerField(default=0, verbose_name='Views')

    def __str__(self):
        return self.title