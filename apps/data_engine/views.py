from django.shortcuts import render
from apps.data_engine.models import Directory


# Create your views here.

def cascade_folders(request, slug):
    current_dir = Directory.objects.get(slug=slug)
    environment = Directory.objects.filter(parent=current_dir.pk)
    full_path = list(current_dir.get_ancestors()) + [current_dir]
    return render(request, 'base.html', {
        'title': f'Каталог {current_dir.name}',
        'environment': environment,
        'current_dir': current_dir,
        'full_path': full_path
    })
