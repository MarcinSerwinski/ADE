from django.urls import path

from . import views

app_name = 'alarm_systems'

urlpatterns = [
path('', views.home, name='home')
]

