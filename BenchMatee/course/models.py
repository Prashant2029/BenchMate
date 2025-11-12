from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200)
    content_file = models.FileField(upload_to="pdfs/", blank=True, null=True)  # PDF/Text files
    order = models.IntegerField(default=1)  # order in the subject

    def __str__(self):
        return f"{self.subject.name} - {self.title}"


class UserSubjectProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subject_progress")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="user_progress")
    progress_percentage = models.FloatField(default=0.0)  
    quizzes_taken = models.IntegerField(default=0)
    quizzes_passed = models.IntegerField(default=0) 
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'subject')

    def __str__(self):
        return f"{self.user.username} → {self.subject.name} ({self.progress_percentage}%)"



class UserChapterProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chapter_progress")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="progress")
    is_completed = models.BooleanField(default=False)
    progress_percentage = models.FloatField(default=0.0)  
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username} - {self.chapter.title} ({self.progress_percentage}%)"
