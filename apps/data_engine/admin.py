from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from apps.data_engine.models import Directory


# Register your models here.
@admin.register(Directory)
class DirectoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('name',)}
