from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoryView.as_view()),
    path('create/', views.CreateStoryView.as_view()),
    path('test/', views.TestView.as_view()),
    path('stats/', views.StatisticsView.as_view())
]
