from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='documents_created', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='documents_updated', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class DocumentBlock(models.Model):
    TITLE = 'title'
    TEXT = 'text'
    LIST = 'list'
    IMAGE = 'image'
    VIDEO = 'video'

    BLOCK_TYPES = [
        (TITLE, 'Title'),
        (TEXT, 'Text'),
        (LIST, 'List'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    
    document = models.ForeignKey(Document, related_name='blocks', on_delete=models.CASCADE)
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES)
    content = models.TextField(blank=True, null=True)  # Содержимое для текста и списка
    image = models.ImageField(upload_to='document_images/', blank=True, null=True)  # Изображение
    video_url = models.URLField(blank=True, null=True)  # Ссылка на видео
    level = models.PositiveIntegerField(blank=True, null=True)  # Уровень заголовка (для Title)
    font_size = models.CharField(max_length=20, blank=True, null=True)  # Размер шрифта
    color = models.CharField(max_length=20, blank=True, null=True)  # Цвет текста или заголовка
    alignment = models.CharField(max_length=10, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], blank=True, null=True)  # Выравнивание
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.block_type} block for {self.document.title}'