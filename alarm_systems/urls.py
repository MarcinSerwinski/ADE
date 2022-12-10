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
    path('main_view/details_customer/<int:customer_id>', views.details_customer,
         name='details_customer'),
    path('main_view/add_location/<int:customer_id>', views.add_location,
         name='add_location_customer'),
    path('main_view/details_customer/location_details/<int:location_id>', views.location_details,
         name='location_details'),
    path('main_view/add_system/<int:location_id>', views.add_system_for_location,
         name='add_system_for_location'),
    path('main_view/details_system/<int:system_id>', views.details_system,
         name='details_system'),
    path('main_view/add_registrator/<int:system_id>', views.add_registrator,
         name='add_registrator'),
    path('main_view/add_registrator/add_camera/<int:system_id>', views.add_camera,
         name='add_camera'),
    path('main_view/add_central/<int:system_id>', views.add_central,
         name='add_central'),
    path('main_view/add_central/add_motionsensor/<int:system_id>', views.add_motionsensor,
         name='add_motionsensor'),
    path('main_view/add_registrator/empty_system/<int:system_id>', views.empty_system,
          name='empty_system'),
]
