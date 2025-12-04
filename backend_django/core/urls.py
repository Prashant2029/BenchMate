from django.urls import path
from .views import UploadView, GenerateQuizView, GenerateFlashcardsView, SubmitQuizView, ChatView, NoteView, DocumentDeleteView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload_pdf'),
    path('generate/quiz/', GenerateQuizView.as_view(), name='generate_quiz'),
    path('generate/flashcards/', GenerateFlashcardsView.as_view(), name='generate_flashcards'),
    path('submit/quiz/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('chat/', ChatView.as_view(), name='chat_pdf'),
    path('notes/', NoteView.as_view(), name='notes'),
    path('documents/<int:pk>/', DocumentDeleteView.as_view(), name='delete_document'),
]
