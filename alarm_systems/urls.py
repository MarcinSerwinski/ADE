from django.urls import path

from . import views
from .views import MainView

app_name = 'alarm_systems'

urlpatterns = [
    path('', views.home, name='home'),
    path('main_view/', MainView.as_view(), name='main_view'),
    path('main_view/add_customer/', views.add_customer_view, name='add_customer'),
    path('main_view/delete_customer/<int:customer_id>', views.delete_customer_view, name='delete_customer'),
    path('main_view/edit_customer/<int:customer_id>', views.edit_customer_all_view, name='edit_customer_all_view'),
    path('main_view/edit_customer_first_name/<int:customer_id>', views.edit_customer_first_name,
         name='edit_customer_first_name'),
    path('main_view/edit_customer_last_name/<int:customer_id>', views.edit_customer_last_name,
         name='edit_customer_last_name'),
    path('main_view/edit_customer_address/<int:customer_id>', views.edit_customer_address,
         name='edit_customer_address'),
    path('main_view/edit_customer_email/<int:customer_id>', views.edit_customer_email,
         name='edit_customer_email'),
    path('main_view/edit_customer_phone_number/<int:customer_id>', views.edit_customer_phone_number,
         name='edit_customer_phone_number'),
    path('main_view/edit_customer_description/<int:customer_id>', views.edit_customer_description,
         name='edit_customer_description'),
]
