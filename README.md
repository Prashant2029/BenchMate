# Benchmate

A web application using **Gemini 2.0 Flash** for AI-powered quiz and flashcard generation from PDF documents.

## Features

- 📄 **PDF Upload**: Drag-and-drop or click to upload PDF files
- 🧠 **AI-Powered Quizzes**: Generate multiple-choice quizzes from PDF content
- 📚 **Flashcards**: Create interactive flashcards with flip animations
- ✨ **Modern UI**: Premium design with glassmorphism, gradients, and smooth animations

## Tech Stack

### Frontend
- React + Vite
- Tailwind CSS
- Framer Motion (animations)
- Axios (API calls)
- Lucide React (icons)

### Backend
- FastAPI
- Google Generative AI (Gemini 2.0 Flash)
- PyPDF (PDF parsing)

### Backend (Django)
- Django
- Django REST Framework

## Prerequisites

### Option 1: Local Development
- Node.js 18+ (v24.11.1 installed via NVM)
- Python 3.8+
- Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Option 2: Docker Deployment
- Docker Engine 20.10+
- Docker Compose 2.0+
- Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Prashant2029/BenchMate
```

### 2. FastAPI Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 3. Django Backend Setup

```bash
cd backend_django

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

### 4. Frontend Setup

```bash
cd ../frontend

# Make sure you're using Node 24 (if you have NVM)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 24

# Install dependencies
npm install
```

## Running the Application

### Start FastAPI Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### Start Django Backend Server

```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8001
```

The Django backend will be available at `http://localhost:8001` (Changed to 8001 to avoid conflict with FastAPI on 8000)

### Start Frontend Development Server

```bash
cd frontend
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 24
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Docker Deployment

For production deployment using Docker:

### 1. Setup Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

### 2. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### 3. Access the Application

- **Frontend**: http://localhost (port 80)
- **FastAPI Backend**: http://localhost:8000
- **Django Backend**: http://localhost:8001

> **Note**: For production deployment, you'll need to update the API URLs in the frontend to point to your production domain instead of localhost.

## Usage

1. **Upload PDF**: Drag and drop a PDF file or click to browse
2. **Generate Quiz**: Click the "Quiz" tab and generate questions
3. **Create Flashcards**: Click the "Flashcards" tab and generate study cards
4. **Study**: Interact with quizzes and flip through flashcards

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload a PDF file
- `POST /generate/quiz` - Generate quiz questions
- `POST /generate/flashcards` - Generate flashcards

## Environment Variables

Create a `.env` file in the `backend` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Project Structure

```
werter/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables (create this)
├── backend_django/       # Django application
│   ├── manage.py
│   └── ...
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Upload.jsx      # PDF upload component
    │   │   ├── Quiz.jsx        # Quiz component
    │   │   └── Flashcards.jsx  # Flashcard component
    │   ├── App.jsx       # Main application
    │   └── index.css     # Tailwind styles
    ├── package.json      # Node dependencies
    └── tailwind.config.js
```

## Notes

- PDFs are stored in memory and will be lost on server restart
- For production, consider implementing persistent storage (database)
- Gemini API has rate limits - adjust `num_questions` and `num_cards` as needed
