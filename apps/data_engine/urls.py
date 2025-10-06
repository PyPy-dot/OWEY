from django.urls import path
from apps.data_engine import views


urlpatterns = [
    path('<slug:slug>/', views.cascade_folders, name='directory'),
]
