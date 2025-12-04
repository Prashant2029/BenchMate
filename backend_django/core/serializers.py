from rest_framework import serializers
from .models import Document, ChatMessage, Note

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file', 'uploaded_at', 'extracted_text')

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('role', 'content', 'created_at')

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('content', 'updated_at')
        read_only_fields = ('extracted_text', 'created_at')
