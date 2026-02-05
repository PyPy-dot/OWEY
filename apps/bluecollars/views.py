import asyncio
import csv
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.conf import settings


# Create your views here.
client = settings.API_SESSIONS['sync']['bluecollars'].auth()


def shift_detail(request, shift_id):
    data = client.get_shift(shift_id)
    return render(request, 'shift/detail.html', {'title': f'Смена: {shift_id}', 'data': data})

