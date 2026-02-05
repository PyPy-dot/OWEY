from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse


# Create your models here.
class Directory(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name='URL директории')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='Директория'
    )

    class MPPTMeta:
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = 'Директория'
        verbose_name_plural = 'Директории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('directory', kwargs={'slug': self.slug})


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    dataset_id = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
