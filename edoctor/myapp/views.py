from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import DocumentSerializer, RegisterSerializer
from .models import CustomUser, Document, DocumentBlock
from django.contrib import messages
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate



# Create your views here.
@api_view(['GET'])
def get_all_documents(request):
    documents = Document.objects.all()  # Получаем все документы из базы данных
    serializer = DocumentSerializer(documents, many=True)  # Сериализуем их в JSON
    return Response(serializer.data)


# Обработчик сохранения документа
@api_view(['POST'])
def create_document(request):
    data = request.data  # Получаем данные из запроса
    title = data.get("title")
    created_by = CustomUser.objects.get_or_create(username='test_user')[0]  # Используем CustomUser

    # Создание документа
    document = Document.objects.create(
        title=title,
        created_by=created_by,
        updated_by=created_by,
    )

    # Создание блоков для документа
    blocks = data.get("blocks", [])
    for block in blocks:
        DocumentBlock.objects.create(
            document=document,
            block_type=block.get('block_type'),
            content=block.get('content'),
            image=block.get('image', ''),
            video_url=block.get('video_url', ''),
            level=block.get('level', 1),
            font_size=block.get('font_size', '16px'),
            color=block.get('color', 'black'),
            alignment=block.get('alignment', 'left'),
            order=block.get('order', 0)
        )

    messages.success(request, "Документ успешно создан!")
    return redirect('get_all_documents')  # Перенаправляем на страницу со всеми документами


@api_view(['DELETE'])
def delete_document(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
        document.delete()
        return JsonResponse({'message': 'Document deleted successfully'}, status=200)
    except Document.DoesNotExist:
        return JsonResponse({'message': 'Document not found'}, status=404)


@api_view(['PUT'])
def update_document(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        raise NotFound('Document not found')

    # Обновление названия документа
    document.title = request.data.get('title', document.title)
    document.save()

    data = request.data
    blocks_data = data.get('blocks', [])
    blocks = []
    for block_data in blocks_data:
        block_data['document'] = document  # Привязка блока к документу
        block, created = DocumentBlock.objects.update_or_create(
            id=block_data.get('id'), defaults=block_data
        )
        blocks.append(block)

    document.blocks.set(blocks)
    document.save()
    
    return Response({"message": "Document updated successfully"}, status=200)


@api_view(['GET'])
def get_document(request, id):
    # Получаем документ по ID
    document = get_object_or_404(Document, id=id)
    serializer = DocumentSerializer(document)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Регистрирует нового пользователя.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пользователь успешно зарегистрирован'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    return Response({'message': 'Неверный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)