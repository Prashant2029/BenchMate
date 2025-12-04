from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader
import io
from typing import List
from pydantic import BaseModel

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bench-mate.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded PDFs
pdf_storage = {}

class QuizRequest(BaseModel):
    pdf_id: str
    num_questions: int = 5

class FlashcardRequest(BaseModel):
    pdf_id: str
    num_cards: int = 10

@app.get("/")
def read_root():
    return {"message": "NotebookLM Clone API"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file and extract its text content"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read the PDF file
        contents = await file.read()
        pdf_reader = PdfReader(io.BytesIO(contents))
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Store the text with a simple ID
        pdf_id = str(len(pdf_storage) + 1)
        pdf_storage[pdf_id] = {
            "filename": file.filename,
            "text": text
        }
        
        return {
            "pdf_id": pdf_id,
            "filename": file.filename,
            "pages": len(pdf_reader.pages),
            "text_length": len(text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/generate/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate quiz questions from uploaded PDF"""
    if request.pdf_id not in pdf_storage:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    text = pdf_storage[request.pdf_id]["text"]
    
    prompt = f"""Based on the following text, generate {request.num_questions} multiple-choice quiz questions.
Each question should have 4 options (A, B, C, D) with only one correct answer.
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
{text[:4000]}"""  # Limit text to avoid token limits
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from markdown code blocks if present
        result_text = response.text
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        return {"quiz": result_text}
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@app.post("/generate/flashcards")
async def generate_flashcards(request: FlashcardRequest):
    """Generate flashcards from uploaded PDF"""
    if request.pdf_id not in pdf_storage:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    text = pdf_storage[request.pdf_id]["text"]
    
    prompt = f"""Based on the following text, generate {request.num_cards} flashcards for studying.
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
{text[:4000]}"""  # Limit text to avoid token limits
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from markdown code blocks if present
        result_text = response.text
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        return {"flashcards": result_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating flashcards: {str(e)}")
