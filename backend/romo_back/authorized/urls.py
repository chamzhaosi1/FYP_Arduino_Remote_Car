from django.urls import path
from . import views

urlpatterns = [
    path('upl_auth_img/', views.auth_img_upload),
    path('get_auth_img/', views.get_auth_img),
    path('del_auth_img/<int:id>', views.del_auth_img),
]