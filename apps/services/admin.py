from django.contrib import admin
from apps.services.models import Cookie


@admin.register(Cookie)
class ModelNameAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['created_at', 'updated_at', 'name', 'value']
