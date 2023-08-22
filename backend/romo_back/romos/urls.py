from django.urls import path
from . import views

urlpatterns = [
    path('romo_register/', views.register_romo),
    path('romo_detail/', views.get_romo_data),
    path('romo_user_detail/<mac_address>', views.get_romo_user_data),
    path('romo_delete/<mac_address>', views.delete_romo),
    path('romo_update/', views.update_romo)
    # path('romo_connect_status/<mac_address>', views.connect_status_romo),
]

 