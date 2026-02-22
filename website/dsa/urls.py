from django.urls import path
from .views import HomeView, VoteView

urlpatterns = [
    path('',  HomeView.as_view(), name='home'),
    path('vote/',  VoteView.as_view(), name='vote'),
]
