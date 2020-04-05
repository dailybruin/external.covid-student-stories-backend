from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoryView.as_view()),
    path('create/', views.CreateStoryView.as_view())
]
