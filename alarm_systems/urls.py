from django.urls import path

from . import views
from .views import MainView

app_name = 'alarm_systems'

urlpatterns = [
    path('', views.home, name='home'),
    path('main_view/', MainView.as_view(), name='main_view'),
    path('main_view/add_customer/', views.add_customer_view, name='add_customer_view'),
    path('main_view/delete_customer/<int:customer_id>', views.delete_customer_view, name='delete_customer_view'),

]
