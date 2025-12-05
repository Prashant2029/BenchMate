# Benchmate

A web application using **Gemini 2.0 Flash** for AI-powered quiz and flashcard generation from PDF documents.
=======


# 📘 Benchmate

A web application that uses **Gemini 2.0 Flash** for AI-powered **quiz and flashcard generation from PDF documents**.

---

## ✨ Features

* 📄 **PDF Upload** – Drag-and-drop or click to upload PDFs
* 🧠 **AI-Powered Quizzes** – Automatically generate MCQs from documents
* 📚 **Flashcards** – Interactive flashcards with flip animations
* ✨ **Modern UI** – Glassmorphism, gradients & smooth animations

---

## 🛠 Tech Stack

### Frontend

* React + Vite
* Tailwind CSS
* Framer Motion
* Axios
* Lucide React

### Backend (FastAPI)

* FastAPI
* Google Gemini 2.0 Flash
* PyPDF

### Backend (Django)

* Django
* Django REST Framework

---

## ✅ Prerequisites (All Operating Systems)

You must have the following installed:

* **Node.js 18+**
* **Python 3.8+**
* **Git**
* **Gemini API Key**
  👉 [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

# 🚀 Installation Guide (Linux, macOS & Windows)

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Prashant2029/BenchMate
<<<<<<< HEAD
=======
cd BenchMate
>>>>>>> 950369e (final touch)
```

---

# ⚙️ Backend Setup – FastAPI

## ✅ Linux & macOS

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

---

## ✅ Windows (PowerShell)

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
echo GEMINI_API_KEY=your_api_key_here > .env
```

---

# ⚙️ Backend Setup – Django

## ✅ Linux & macOS

```bash
cd backend_django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

---

## ✅ Windows

```powershell
cd backend_django
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

---

# 🎨 Frontend Setup (React + Vite)

```bash
cd frontend
npm install
```

---

# ▶️ Running the Application

---

## ✅ Start FastAPI Backend (Port 8000)

### Linux & macOS

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Windows

```powershell
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

✅ Backend runs at:
**[http://localhost:8000](http://localhost:8000)**

---

## ✅ Start Django Backend (Port 8001)

### Linux & macOS

```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8001
```

### Windows

```powershell
cd backend_django
venv\Scripts\activate
python manage.py runserver 8001
```

✅ Django runs at:
**[http://localhost:8001](http://localhost:8001)**

---

## ✅ Start Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend runs at:
**[http://localhost:5173](http://localhost:5173)**

---

# 🐳 Docker Deployment (All OS)

### 1️⃣ Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 2️⃣ Build & Run

```bash
docker-compose up -d --build
```

---

### 3️⃣ View Logs

```bash
docker-compose logs -f
```

---

### 4️⃣ Stop Containers

```bash
docker-compose down
```

---

### ✅ Docker Access URLs

| Service  | URL                                            |
| -------- | ---------------------------------------------- |
| Frontend | [http://localhost](http://localhost:5173)           |
| FastAPI  | [http://localhost:8000](http://localhost:8000) |
| Django   | [http://localhost:8001](http://localhost:8001) |

---

# 📌 Usage

1. Upload a **PDF document**
2. Click **Quiz** to generate AI-based questions
3. Click **Flashcards** to generate study cards
4. Flip flashcards and practice quizzes interactively

---

# 🔌 API Endpoints

| Method | Endpoint               | Description         |
| ------ | ---------------------- | ------------------- |
| GET    | `/`                    | Health check        |
| POST   | `/upload`              | Upload PDF          |
| POST   | `/generate/quiz`       | Generate quiz       |
| POST   | `/generate/flashcards` | Generate flashcards |

---

# ⚠️ Notes

* PDFs are stored **in memory only**
* Restarting backend will remove uploaded files
* Gemini API has **rate limits**
* Update frontend API URLs for production deployment

---

# 📂 Project Structure

```
BenchMate/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
├── backend_django/
│   ├── manage.py
│   └── ...
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Upload.jsx
    │   │   ├── Quiz.jsx
    │   │   └── Flashcards.jsx
    │   ├── App.jsx
    │   └── index.css
    ├── package.json
    └── tailwind.config.js
```
