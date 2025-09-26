from django.shortcuts import render
from django.http import HttpResponse

# def home(request):
#   return HttpResponse("Hello, world. You're at the home page.")

def home(request):
  return render(request, 'index.html')
