from rest_framework import views, status, parsers, permissions
from rest_framework.response import Response
from .models import Document, ChatMessage, Note
from .serializers import DocumentSerializer, ChatMessageSerializer, NoteSerializer
from gamification.services import award_xp
from gamification.models import QuizResult
from pypdf import PdfReader
import io
import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

class UploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not file_obj.name.endswith('.pdf'):
            return Response({"error": "Only PDF files are allowed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read PDF
            pdf_reader = PdfReader(file_obj)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # Save Document
            document = Document.objects.create(
                user=request.user,
                file=file_obj,
                extracted_text=text
            )
            
            serializer = DocumentSerializer(document)
            return Response({
                "pdf_id": document.id,
                "filename": file_obj.name,
                "pages": len(pdf_reader.pages),
                "text_length": len(text),
                **serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateQuizView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pdf_id = request.data.get('pdf_id')
        num_questions = request.data.get('num_questions', 5)
        topic = request.data.get('topic', '')
        
        try:
            document = Document.objects.get(id=pdf_id, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
        
        text = document.extracted_text
        
        topic_instruction = f"Focus specifically on the topic: '{topic}'." if topic else "Cover key concepts from the text."
        
        prompt = f"""You are an expert tutor creating a quiz from a course book.
{topic_instruction}
Generate {num_questions} multiple-choice quiz questions.
Start from the beginning of the relevant section.
Ignore any pricing, publishing info, or preface material.
Each question should have 4 options (A, B, C, D) with only one correct answer.
Do NOT mark the correct answer in the option text (e.g., do not write "Option A (Correct)").
Return the response in JSON format with the following structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      }},
      "correct_answer": "A"
    }}
  ]
}}

Text:
{text[:30000]}"""

        try:
            response = model.generate_content(prompt)
            result_text = response.text
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            return Response({"quiz": result_text})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateFlashcardsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pdf_id = request.data.get('pdf_id')
        num_cards = request.data.get('num_cards', 10)
        
        try:
            document = Document.objects.get(id=pdf_id, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
        
        text = document.extracted_text
        prompt = f"""You are an expert tutor creating flashcards from a course book.
Generate {num_cards} flashcards for studying.
Focus on key definitions, concepts, and important facts.
Ignore any pricing, publishing info, or preface material.
Each flashcard should have a front (question or concept) and back (answer or explanation).
Return the response in JSON format with the following structure:
{{
  "flashcards": [
    {{
      "front": "Question or concept",
      "back": "Answer or explanation"
    }}
  ]
}}

Text:
{text[:30000]}"""

        try:
            response = model.generate_content(prompt)
            result_text = response.text
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            return Response({"flashcards": result_text})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pdf_id = request.query_params.get('pdf_id')
        if not pdf_id:
            return Response({"error": "pdf_id required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            document = Document.objects.get(id=pdf_id, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
            
        messages = document.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        pdf_id = request.data.get('pdf_id')
        message = request.data.get('message')
        # history is now fetched from DB, but we can still accept it if needed for context window optimization
        
        try:
            document = Document.objects.get(id=pdf_id, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Save user message
        ChatMessage.objects.create(document=document, role='user', content=message)
        
        text = document.extracted_text
        
        # Construct prompt with context and history from DB
        context_prompt = f"""You are a helpful AI tutor assisting a student with a document.
Use the following document text to answer the student's question.
If the answer is not in the text, say so politely.
Keep answers concise and relevant.

Document Text (excerpt):
{text[:30000]}...

Chat History:
"""
        # Fetch last 10 messages for context
        recent_messages = document.messages.order_by('-created_at')[:10:-1] 
        # Note: slicing with negative step might not work on queryset directly depending on DB, 
        # safer to slice normally then reverse in python or use order_by
        recent_messages = document.messages.order_by('-created_at')[:10]
        recent_messages = reversed(recent_messages)

        for msg in recent_messages:
            role = "Student" if msg.role == 'user' else "Tutor"
            context_prompt += f"{role}: {msg.content}\n"
            
        context_prompt += f"\nStudent: {message}\nTutor:"""
        
        try:
            response = model.generate_content(context_prompt)
            ai_response = response.text
            
            # Save AI response
            ChatMessage.objects.create(document=document, role='assistant', content=ai_response)
            
            return Response({"response": ai_response})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pdf_id = request.query_params.get('pdf_id')
        if not pdf_id:
            return Response({"error": "pdf_id required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            document = Document.objects.get(id=pdf_id, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
            
        note, created = Note.objects.get_or_create(document=document, user=request.user)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def post(self, request):
        pdf_id = request.data.get('pdf_id')
        content = request.data.get('content')
        
        try:
            document = Document.objects.get(id=pdf_id, user=request.user)
        except Document.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
            
        note, created = Note.objects.update_or_create(
            document=document, 
            user=request.user,
            defaults={'content': content}
        )
        
        return Response({"status": "saved", "updated_at": note.updated_at})

class DocumentDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            document = Document.objects.get(pk=pk, user=request.user)
            document.delete() # This will also delete the file from storage if configured correctly, or at least the DB record
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
class SubmitQuizView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        score = request.data.get('score')
        total_questions = request.data.get('total_questions')
        
        if score is None or total_questions is None:
            return Response({"error": "Missing score or total_questions"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate XP: 10 XP per correct answer
        xp_earned = score * 10
        
        QuizResult.objects.create(
            user=request.user,
            score=score,
            total_questions=total_questions,
            xp_earned=xp_earned
        )
        
        award_xp(request.user, xp_earned)
        
        return Response({
            "message": "Quiz submitted successfully",
            "xp_earned": xp_earned,
            "new_xp": request.user.profile.xp,
            "new_rank": request.user.profile.rank
        })
