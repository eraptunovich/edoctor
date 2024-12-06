from django.urls import path


from .views import get_all_documents
from .views import create_document
from .views import delete_document
from .views import update_document
from .views import get_document
from .views import register_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
  
    path('api/documents/', get_all_documents, name='get_all_documents'),
    path('api/create_document/', create_document, name='create_document'),
    path('api/documents/delete/<int:document_id>/', delete_document, name='delete_document'),
    path('api/documents/update/<int:document_id>/', update_document, name='update_document'),  # Для обновления
    path('api/documents/<int:id>/', get_document, name='get_document'),
    path('api/register/', register_user, name='register_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
