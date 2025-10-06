from django.urls import path
import apps.shift.views as views

urlpatterns = [
    path('<str:shift_id>/', views.shift_detail, name='shift_detail'),
]
