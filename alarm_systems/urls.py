from django.urls import path

from . import views
from .views import MainView

app_name = 'alarm_systems'

urlpatterns = [
    path('', views.home, name='home'),
    path('main_view/', MainView.as_view(), name='main_view'),

]
