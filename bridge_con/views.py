from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):
	# do things
    return HttpResponse('Hello World')