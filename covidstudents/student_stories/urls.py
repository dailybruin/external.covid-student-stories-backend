from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoryView.as_view()),
    path('create/', views.CreateStoryView.as_view()),
    path('test/', views.TestView.as_view()),
    path('stats/', views.StatisticsView.as_view()),
    path('react/', views.ReactView.as_view()),
    path('vetting-table/', views.admin_table_page, name="vetting-table"),
    path('vetting-table/approve/<int:id>', views.approve),
    path('vetting-table/reject/<int:id>', views.reject)
]
