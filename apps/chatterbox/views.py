import asyncio
import csv
import json

from django.shortcuts import render

from apps.chatterbox.service import ChatterboxClient, AsyncChatterboxClient

# Create your views here.
client = ChatterboxClient()
client.auth()


def chat_detail(request, ticket_id: str):
    data = client.get_chat(ticket_id)
    return render(request, 'chatterbox/detail.html', {'title': f'Тикет: {ticket_id}', 'data': data})
