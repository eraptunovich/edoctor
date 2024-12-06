from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Категории пользователей
USER_TYPE_CHOICES = [
    ('healthcare', 'Healthcare Worker'),  # Сотрудник учреждения здравоохранения
    ('bsl', 'BSL Employee'),             # Сотрудник БСЛ
]

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=150, unique=True)  # Уникальный логин
    # Поля для сотрудников здравоохранения
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    organization_address = models.CharField(max_length=200, blank=True, null=True)
    organization_head_doctor = models.CharField(max_length=100, blank=True, null=True)
    organization_email = models.EmailField(blank=True, null=True)
    organization_phone = models.CharField(max_length=15, blank=True, null=True)

    # Поля для сотрудников БСЛ
    position = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='documents_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='documents_updated'
    )
    updated_at = models.DateTimeField(auto_now=True)
    

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
    
