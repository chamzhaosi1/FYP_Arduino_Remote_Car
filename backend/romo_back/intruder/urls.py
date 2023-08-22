from django.urls import path
from . import views

urlpatterns = [
    path('upl_intr_img/', views.intr_img_upload),
    path('get_intr_img/', views.get_intr_img),
    path('upt_intr_img/', views.upt_intr_img),
    path('cvt_intr_auth_img/', views.covert_intr_to_auth),
    path('del_intr_img/<int:id>', views.del_intr_img),
]