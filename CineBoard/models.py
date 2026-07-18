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



class Genre(models.Model):
    GENRES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'),
    )
    name_genre = models.CharField(max_length=100, choices=GENRES)

    def __str__(self):
        return self.name_genre


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='movies/', verbose_name='Фото', null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='Жанр')
    release_year = models.IntegerField(verbose_name='Год выпуска')
    director = models.CharField(max_length=150, verbose_name='Режиссёр')
    duration_minutes = models.IntegerField(verbose_name='Длительность (мин)')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name='Рейтинг')
    country = models.CharField(max_length=100, verbose_name='Страна')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.title}: {", ".join(i.name_genre for i in self.genre.all())}'
    
    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, default='Гость')
    text = models.TextField(verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.movie} - {self.author_name}'


class VipClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    select_movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.select_movie.title}'