from django import forms
from . import models
from CineBoard.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

GENDER = (
        ('F', 'F'),
        ('M', 'M')
    )

class CustomRegisterForm(UserCreationForm):
    photo = forms.ImageField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, initial='+996')
    gender = forms.ChoiceField(choices=GENDER, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password1',
            'password2',
            'photo',
            'first_name',
            'email',
            'phone_number',
            'gender',
        )
    def save(self, commit = True):
        user = super(CustomRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    
class MovieForm(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = ['title', 'description', 'poster', 'genre', 'release_year',
                'director', 'duration_minutes', 'rating', 'country']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['author_name', 'text']
        
    
class VipClientForm(forms.ModelForm):
    class Meta:
        model = models.VipClient
        fields = '__all__'
        exclude = ['select_movie']