import asyncio

from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView

from apps.services.models import Token
from apps.shift.service import BlueCollarsAdminClient, AsyncBlueCollarsAdminClient
import csv

# Create your views here.
client = BlueCollarsAdminClient()
client.auth()


# async def main():
#     async with AsyncBlueCollarsAdminClient() as async_client:
#         data = await async_client.get_shift('e916de80-65fa-4e66-a3a9-504385a022fd')
#     print(data)
#
# asyncio.run(main())


def shift_detail(request, shift_id):
    try:
        data = client.get_shift(shift_id)
        return render(request, 'shift/detail.html', {'title': f'Смена: {shift_id}', 'data': data})
    except Token.TokenInvalidError:
        return HttpResponseRedirect('/')
