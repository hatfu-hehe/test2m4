from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.AuthLoginView.as_view(), name='login'),
    path('logout/', views.AuthLogoutView.as_view(), name='logout'),
    path('users_list/', views.UsersListView.as_view(), name='work_list'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/add/', views.CreateMovieView.as_view(), name='movie_add'),
    path('movies/<int:id>/edit/', views.UpdateMovieView.as_view(), name='movie_edit'),
    path('movies/<int:id>/delete/', views.DeleteMovieView.as_view(), name='movie_delete'),
    path('search/', views.SearchMovieView.as_view(), name='search'),
]
