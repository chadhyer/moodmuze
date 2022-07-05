from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests 
from moodmuze.settings.common import BRIDGE_IP, BRIDGE_KEY

# Create your views here.
def say_hello(request):
	# do things
    return HttpResponse('Hello World')

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def room(request):
    """
    GET: Return list of all groups
    POST: Create new group
    PUT: Update existing group
    """

    if request.method == 'GET':
        print('GET')
        url=f'http://{BRIDGE_IP}/api/{BRIDGE_KEY}/groups/'
        response = requests.get(url=url)
        data = str(response.content, 'utf-8')
        print(data)
        return HttpResponse(data)

    if request.method == 'POST':
        print('POST')
        return HttpResponse('You post it')

    if request.method == 'PUT':
        print('PUT')
        return HttpResponse('You put it')

    if request.method == 'DELETE':
        print('DELETE')
        return HttpResponse('You delete it')