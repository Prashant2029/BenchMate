"""
URL configuration for BenchMatee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from course import views

urlpatterns = [
    path('subject/', views.subject, name='subject'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('chat/<str:subject_name>/', views.subject_chat, name='subject_chat'),
    path('subject12/<str:subject_name>/book/', views.subject_book, name='subject_book'),
    path('subject12/<str:subject_name>/ask/', views.ask_about_pdf, name='ask_about_pdf'),
    path('ai_quiz/', views.quiz_page, name='generate_quiz'),
    path('generate-quiz-from-ai/', views.generate_quiz_from_ai, name='generate_quiz_from_ai'),


]
