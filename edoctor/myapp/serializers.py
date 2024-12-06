from rest_framework import serializers
from .models import Document, DocumentBlock
from .models import CustomUser

class DocumentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentBlock
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    blocks = DocumentBlockSerializer(many=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'blocks','created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'user_type',
            'organization_name', 'organization_address', 'organization_head_doctor',
            'organization_email', 'organization_phone', 'position',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user