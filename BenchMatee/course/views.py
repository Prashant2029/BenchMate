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

# Create your views here.
def subject(request):
    username = request.user.username
    return render(request, "course/subject.html", {'username': username})


@login_required
def dashboard(request):
    user = request.user

    # Subjects
    subjects = Subject.objects.all()

    # Fake progress data for demo
    subject_progress_data = []
    for subject in subjects:
        # Try to get actual progress
        user_subject_progress = UserSubjectProgress.objects.filter(user=user, subject=subject).first()

        if user_subject_progress:
            progress_percentage = user_subject_progress.progress_percentage
        else:
            # Fake data for demo
            if subject.name in ["Nepali", "English"]:
                progress_percentage = 30 if subject.name == "Nepali" else 50
            else:
                progress_percentage = 0

        subject_progress_data.append({
            'name': subject.name,
            'progress': progress_percentage
        })

    # Recent chapters progress (demo purposes)
    recent_chapters = []

    user_chapter_progress_qs = UserChapterProgress.objects.filter(user=user).order_by('-last_accessed')[:2]
    for progress in user_chapter_progress_qs:
        recent_chapters.append({
            'title': progress.chapter.title,
            'description': f"You were learning {progress.chapter.title} in {progress.chapter.subject.name}",
            'progress': progress.progress_percentage
        })

    # Add fake data if less than 2 recent chapters
    while len(recent_chapters) < 2:
        if len(recent_chapters) == 0:
            recent_chapters.append({
                'title': 'एक चिहान',
                'description': 'You were exploring a progressive Nepali novel.',
                'progress': 40
            })
        else:
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
        {full_text[:15000]}

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
