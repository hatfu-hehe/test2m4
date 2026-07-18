from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from . import models, forms
from django.db.models import F
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView


class RegisterView(generic.CreateView):
    template_name = 'users/register.html'
    model = models.CustomUser
    context_object_name = 'form'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class AuthLoginView(generic.LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/users_list/'


class AuthLogoutView(generic.LogoutView):
    next_page = reverse_lazy('login')


class UsersListView(generic.ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'usr_lst'
    ordering = ['-id']
    
    
class MovieListView(generic.ListView):
    template_name = 'movies/movie_list.html'
    model = models.Movie
    context_object_name = 'movies'
    ordering = ['-created_at']

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MovieDetailView(generic.DetailView):
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'id'
    model = models.Movie

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        request = self.request
        viewed_movies = request.session.get('viewed_movies', [])
        if obj.pk not in viewed_movies:
            self.model.objects.filter(pk=obj.pk).update(views=F('views') + 1)
            viewed_movies.append(obj.pk)
            request.session['viewed_movies'] = viewed_movies
            obj.refresh_from_db()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm()
        return context
    
    
class CreateMovieView(generic.CreateView):
    template_name = 'crud/create.html'
    form_class = forms.MovieForm
    model = models.Movie
    success_url = '/movies/'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(CreateMovieView, self).form_valid(form=form)


class MovieCRUDListView(generic.ListView):
    template_name = 'crud/read.html'
    model = models.Movie
    paginate_by = 2
    ordering = ['-id']

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = context['page_obj']
        return context
    
    
class UpdateMovieView(generic.UpdateView):
    template_name = 'crud/update.html'
    form_class = forms.MovieForm
    success_url = '/movies/'
    model = models.Movie

    def get_object(self, **kwargs):
        movie_id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=movie_id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(UpdateMovieView, self).form_valid(form=form)


class DeleteMovieView(generic.DeleteView):
    template_name = 'crud/conf_del.html'
    success_url = '/movies/'
    context_object_name = 'movie_id'
    model = models.Movie

    def get_object(self, **kwargs):
        movie_id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=movie_id)
    

class SearchMovieView(generic.ListView):
    template_name = 'crud/read.html'
    context_object_name = 'movies'
    model = models.Movie

    def get_queryset(self):
        return self.model.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = self.request.GET.get('s')
        return context
    
    
class MoviesByGenreView(generic.ListView):
    template_name = 'crud/read.html'
    context_object_name = 'movies'

    def get_queryset(self):
        genre_id = self.kwargs.get('genre_id')
        return models.Movie.objects.filter(genre__id=genre_id)
    
    
class AddCommentView(generic.CreateView):
    form_class = forms.CommentForm
    template_name = 'crud/create.html'

    def form_valid(self, form):
        movie_id = self.kwargs.get('movie_id')
        movie = get_object_or_404(models.Movie, id=movie_id)
        comment = form.save(commit=False)
        comment.movie = movie
        comment.save()
        return redirect('movie_detail', id=movie_id)
    
    
class AddVipClientView(generic.CreateView):
    form_class = forms.VipClientForm
    template_name = 'crud/create.html'

    def form_valid(self, form):
        movie_id = self.kwargs.get('movie_id')
        movie = get_object_or_404(models.Movie, id=movie_id)
        vip_client = form.save(commit=False)
        vip_client.select_movie = movie
        vip_client.save()
        return redirect('movie_detail', id=movie_id)
    

