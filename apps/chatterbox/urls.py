from django.urls import path
from apps.chatterbox import views
from apps.chatterbox.service import ChatterboxClient, AsyncChatterboxClient


urlpatterns = [
    path('<str:ticket_id>/', views.chat_detail, name='chat_detail'),
    # path('', ..., name='chats_list')
]