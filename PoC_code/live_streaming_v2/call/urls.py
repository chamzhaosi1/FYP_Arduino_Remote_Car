from django.urls import path
from . import views
from . import opencv

urlpatterns = [
    path('', views.index, name='index'),
    path('system/', opencv.offer)
]