from django.urls import path
from . import views

urlpatterns = [
    path('hostels/', views.api_list_hostels, name='api_list_hostels'),
    path('hostels/<int:property_id>/rooms/', views.api_list_rooms, name='api_list_rooms'),
]
    