from django.urls import path


from .views import get_all_documents

urlpatterns = [
  
    path('api/documents/', get_all_documents, name='get_all_documents'),
]
