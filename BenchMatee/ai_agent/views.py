import os
import re
import pdfplumber
import json
from django.http import JsonResponse
from dotenv import load_dotenv
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
import os, json, math
from django.shortcuts import render
from .langgraph_agent import get_quiz


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PDF_FOLDER = "media/pdfs"  # folder where you keep PDFs


# Extract chapter by number
def extract_chapter_text(pdf_filename, chapter_num=1):
    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    chapters = text.split("Chapter ")
    if len(chapters) > chapter_num:
        return chapters[chapter_num]
    return text


# Extract chapter by title
def extract_chapter_by_title(pdf_filename, chapter_title):
    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    pattern = re.compile(r'(Chapter\s+\d+:\s+.*)', re.IGNORECASE)
    splits = pattern.split(text)
    for i in range(len(splits)-1):
        heading = splits[i].strip()
        content = splits[i+1].strip()
        if chapter_title.lower() in heading.lower():
            return content
    return text  # fallback if not found


# Gemini generation helper
def generate_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    text = response.text.strip()
    # remove markdown code blocks
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return text


# Main demo view
def study_and_quiz_view(request):
    subject = request.GET.get("subject", "Science")
    chapter_num = request.GET.get("chapter")
    chapter_title = request.GET.get("chapter_title")

    # map subjects to PDF files
    pdf_map = {
        "Science": "science.pdf",
        "Math": "math.pdf"
    }

    pdf_filename = pdf_map.get(subject)
    if not pdf_filename:
        return JsonResponse({"error": "Subject not found"}, status=400)

    # extract chapter text
    if chapter_title:
        chapter_text = extract_chapter_by_title(pdf_filename, chapter_title)
    elif chapter_num:
        chapter_text = extract_chapter_text(pdf_filename, int(chapter_num))
    else:
        chapter_text = extract_chapter_text(pdf_filename, 1)  # default to chapter 1

    # Generate study notes
    notes_prompt = f"Explain this chapter for Class 10 students in simple language:\n{chapter_text}"
    study_notes = generate_with_gemini(notes_prompt)

    # Generate 1 quiz
    quiz_prompt = f"Generate 1 multiple-choice question from this chapter. Return JSON only:\n{chapter_text}"
    quiz_json = generate_with_gemini(quiz_prompt)
    try:
        quiz = json.loads(quiz_json)
    except json.JSONDecodeError:
        quiz = {"error": "Invalid JSON from Gemini", "raw": quiz_json}

    return JsonResponse({
        "subject": subject,
        "chapter": chapter_title if chapter_title else chapter_num if chapter_num else 1,
        "study_notes": study_notes,
        "quiz": quiz
    })


@login_required
def quiz_page(request):
    MAX_QUIZ = 15
    if request.method == "POST":
        if "content" in request.POST:  # generate quiz
            content = request.POST.get("content", "").strip()
            if len(content.split()) < 50:
                return render(request, "ai_agent/quiz_page.html", {"error": "Content must be at least 50 words."})
            
            quizzes = []
            for i in range(MAX_QUIZ):
                result = get_quiz(content)
                if not result.get("question"):
                    break
                # Shuffle options
                options = [result["correct_answer"]] + result.get("distractors", [])
                import random; random.shuffle(options)
                
                quizzes.append({
                    "id": i+1,
                    "question": result["question"],
                    "options": options,
                    "correct_answer": result["correct_answer"]
                })

            # Save quizzes in session to keep track during submission
            request.session['quizzes'] = quizzes
            return render(request, "ai_agent/quiz_page.html", {"quizzes": quizzes, "content": content})

        elif "submit_quiz" in request.POST:  # submit answers
            quizzes = request.session.get("quizzes", [])
            score = 0
            results = []

            for quiz in quizzes:
                qid = str(quiz["id"])
                selected = request.POST.get(f"question_{qid}")
                correct = quiz["correct_answer"]
                is_correct = selected == correct
                if is_correct: score += 1
                results.append({
                    "question": quiz["question"],
                    "selected": selected,
                    "correct": correct,
                    "is_correct": is_correct
                })

            # Clear session
            request.session.pop("quizzes", None)
            return render(request, "ai_agent/quiz_page.html", {"results": results, "score": score, "total": len(quizzes)})

    return render(request, 'ai_agent/quiz_page.html')
