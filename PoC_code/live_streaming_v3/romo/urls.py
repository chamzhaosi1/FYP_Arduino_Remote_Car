from django.urls import path
from . import views

urlpatterns = [
    path('romo_register/', views.register_romo),
    path('romo/', views.get_romo_data),
]