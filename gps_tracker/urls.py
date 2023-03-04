from django.urls import path, include
from . import views

urlpatterns = [
    path('tracker/', views.get_gps_data),
    path('tracker/<int:pk>/', views.get_single_gps_data),
    path('map/', views.get_current_position),
]
