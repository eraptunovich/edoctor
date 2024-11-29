from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DocumentSerializer

# Create your views here.
from .models import Document

@api_view(['GET'])
def get_all_documents(request):
    documents = Document.objects.all()  # Получаем все документы из базы данных
    serializer = DocumentSerializer(documents, many=True)  # Сериализуем их в JSON
    return Response(serializer.data)

#def document_list(request):
    #documents = Document.objects.all()
    #return render(request, 'document_list.html', {'documents': documents})

#def api_data(request):
    data = {'message': 'Hello from Django!'}
    return JsonResponse(data)


