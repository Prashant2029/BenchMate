from django.shortcuts import render

# Create your views here.
def subject(request):
    username = request.user.username
    return render(request, "course/subject.html", {'username': username})