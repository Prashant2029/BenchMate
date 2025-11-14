from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subject, Chapter, UserChapterProgress, UserSubjectProgress
from django.contrib.staticfiles import finders
import os
from django.http import JsonResponse
from dotenv import load_dotenv
import google.generativeai as genai
from django.shortcuts import render, get_object_or_404
from .models import Subject, Chapter, UserChapterProgress
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from django.conf import settings
from ai_agent.langgraph_agent import get_quiz
import random
import re
from django.http import JsonResponse
import google.generativeai as genai

# Create your views here.
def subject(request):
    username = request.user.username
    return render(request, "course/subject.html", {'username': username})


@login_required
def dashboard(request):
    user = request.user
    pdf_path = "static/books/Mathematics.pdf"
    reader = PdfReader(pdf_path)

    # Extract text from pages 19–20 (0-indexed)
    pages_to_scan = [18, 19]
    extracted_text = ""
    for p in pages_to_scan:
        if p < len(reader.pages):
            extracted_text += reader.pages[p].extract_text() + "\n"

    if not extracted_text.strip():
        extracted_text = "No readable text found in pages 19–20."

    # Configure Gemini 2.5 flash
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt: explicitly ask for formulas, theorems, or definitions
    prompt = f"""
    You are an academic assistant. From the following mathematics textbook text, extract a **single key concept** suitable for a 'Topic of the Day'.
    The topic should be a **formula, theorem, definition, or named concept** found on the page.
    Respond **only in JSON**, no markdown, no explanation, in this format:
    {{
      "title": "<formula/theorem/definition name>",
      "description": "<1-2 sentence explanation or context>",
      "subject": "Mathematics"
    }}

    Text:
    {extracted_text[:5000]}
    """

    response = model.generate_content(prompt)
    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        topic_of_the_day = json.loads(text)
    except json.JSONDecodeError:
        topic_of_the_day = {
            "title": "Pythagoras Theorem",
            "description": "A squared plus B squared equals C squared for right-angled triangles.",
            "subject": "Mathematics"
        }

    # Subjects and progress
    subjects = Subject.objects.all()
    subject_progress_data = []
    for subject in subjects:
        user_subject_progress = UserSubjectProgress.objects.filter(user=user, subject=subject).first()
        progress_percentage = user_subject_progress.progress_percentage if user_subject_progress else 0
        subject_progress_data.append({
            'name': subject.name,
            'progress': progress_percentage
        })

    # Recent chapters
    user_chapter_progress_qs = UserChapterProgress.objects.filter(user=user).order_by('-last_accessed')[:2]
    recent_chapters = [
        {
            'title': progress.chapter.title,
            'description': f"You were learning {progress.chapter.title} in {progress.chapter.subject.name}",
            'progress': progress.progress_percentage
        } for progress in user_chapter_progress_qs
    ]

    # Fill with demo data if less than 2
    while len(recent_chapters) < 2:
        recent_chapters.append({
            'title': 'Algebra: Quadratic Equations',
            'description': 'You were learning about solving quadratic equations using different methods.',
            'progress': 65
        })

    context = {
        'username': user.username,
        'subjects': subjects,
        'subject_progress_data': subject_progress_data,
        'recent_chapters': recent_chapters,
        'topic_of_the_day': topic_of_the_day,
    }

    return render(request, 'course/dashboard.html', context)




load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@login_required
def subject_chat(request, subject_name):
    if request.method == "POST":
        user_input = request.POST.get("message")

        # Construct prompt for Gemini
        prompt = f"You are a helpful tutor for {subject_name.capitalize()}. Answer the student query clearly: {user_input}"

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return JsonResponse({"reply": response.text.strip()})



@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    chapters = Chapter.objects.filter(subject=subject).order_by('order')

    # Get user progress
    user_progress = UserChapterProgress.objects.filter(user=request.user, chapter__in=chapters)

    progress_dict = {p.chapter.id: p.progress_percentage for p in user_progress}

    # Prepare chapter data for template
    chapters_data = []
    for ch in chapters:
        chapters_data.append({
            'id': ch.id,
            'title': ch.title,
            'progress': progress_dict.get(ch.id, 0),
            'content_file': ch.content_file.url if ch.content_file else None
        })

    context = {
        'subject': subject,
        'chapters': chapters_data
    }
    return render(request, 'course/subject_detail.html', context)



genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@login_required
def subject_book(request, subject_name):
    return render(request, "course/subject_book.html", {
        'subject_name': subject_name,
        'pdf_path': f'books/{subject_name}.pdf'
    })

@csrf_exempt
@login_required
def ask_about_pdf(request, subject_name):
    if request.method != "POST":
        return JsonResponse({'error': 'POST request required'}, status=405)
    
    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()
        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        pdf_path = finders.find(f'books/{subject_name}.pdf')
        if not pdf_path:
            return JsonResponse({'error': f'PDF for {subject_name} not found'}, status=404)

        reader = PdfReader(pdf_path)
        full_text = "\n".join([page.extract_text() for page in reader.pages])

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        You are an educational assistant. The following is the text of a textbook.
        Answer the user's question using only that content. Be concise and factual.

        Textbook content:
        {full_text[:150000000]}

        Question: {question}
        """
        response = model.generate_content(prompt)
        answer = response.text.strip()

        # Save AI reply in session for quiz generation
        request.session['ai_reply'] = answer

        return JsonResponse({'answer': answer})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


@login_required
def quiz_page(request):
    MAX_QUIZ = 15
    ai_reply = request.session.get('last_ai_reply', '')
    original_question = request.session.get('last_question', '')

    # If user submits quiz
    if request.method == "POST" and "submit_quiz" in request.POST:
        quizzes = request.session.get("quizzes", [])
        score = 0
        results = []

        for quiz in quizzes:
            qid = str(quiz["id"])
            selected = request.POST.get(f"question_{qid}")
            correct = quiz["correct_answer"]
            is_correct = selected == correct
            if is_correct:
                score += 1
            results.append({
                "question": quiz["question"],
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct
            })

        request.session.pop("quizzes", None)
        request.session.pop("last_ai_reply", None)
        request.session.pop("last_question", None)
        return render(request, "course/quiz_page.html", {"results": results, "score": score, "total": len(quizzes)})

    # Automatically generate quizzes if AI reply exists and quizzes not yet in session
    if ai_reply and not request.session.get('quizzes'):
        content_for_quiz = f"Question: {original_question}\nAnswer: {ai_reply}"
        quizzes = []
        for i in range(MAX_QUIZ):
            result = get_quiz(content_for_quiz)
            if not result.get("question"):
                break
            options = [result["correct_answer"]] + result.get("distractors", [])
            import random
            random.shuffle(options)
            quizzes.append({
                "id": i+1,
                "question": result["question"],
                "options": options,
                "correct_answer": result["correct_answer"]
            })

        request.session['quizzes'] = quizzes
        # Render the page with quizzes immediately
        return render(request, "course/quiz_page.html", {"quizzes": quizzes, "ai_reply": ai_reply})

    # Fallback: no AI reply, show empty page
    return render(request, 'course/quiz_page.html')

@login_required
def generate_quiz_from_ai(request):
    MAX_QUIZ = 10
    import random

    # If submitting answers
    if request.method == "POST" and "submit_quiz" in request.POST:
        quizzes = request.session.get("quizzes", [])
        score = 0
        results = []

        for quiz in quizzes:
            qid = str(quiz["id"])
            selected = request.POST.get(f"question_{qid}")
            correct = quiz["correct_answer"]
            is_correct = selected == correct
            if is_correct:
                score += 1
            results.append({
                "question": quiz["question"],
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct
            })

        request.session.pop("quizzes", None)
        return render(request, 'course/quiz_page.html', {
            "results": results,
            "score": score,
            "total": len(quizzes)
        })

    # If generating quiz from content
    content_for_quiz = request.GET.get('content') or request.POST.get('content')
    if not content_for_quiz:
        return render(request, 'course/quiz_page.html', {"error": "No content provided."})

    quizzes = []
    for i in range(MAX_QUIZ):
        result = get_quiz(content_for_quiz)
        if not result.get("question"):
            break
        options = [result["correct_answer"]] + result.get("distractors", [])
        random.shuffle(options)
        quizzes.append({
            "id": i+1,
            "question": result["question"],
            "options": options,
            "correct_answer": result["correct_answer"]
        })

    request.session['quizzes'] = quizzes

    return render(request, 'course/quiz_page.html', {
        "quizzes": quizzes,
        "content": content_for_quiz
    })

