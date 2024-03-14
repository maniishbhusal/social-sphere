from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ai/', views.artificialIntelligenceView, name='ai'),
]
