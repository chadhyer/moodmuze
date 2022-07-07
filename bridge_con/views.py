from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from moodmuze.settings.common import BRIDGE_API
import requests 
import json

# Create your views here.
def say_hello(request):
	# do things
    return HttpResponse('Hello World')

@api_view(['GET', 'POST'])
def room(request):
    """
    GET: Return list of all groups
    POST: Create new group
    """

    context = {}
        
    if request.method == 'GET':

        url = f'{BRIDGE_API}/groups/'
        response = requests.get(url=url)
        context['group'] = json.loads(str(response.content, 'utf-8'))

        return render(request, "get_room.html", context)

    if request.method == 'POST':
        print('POST')
        return HttpResponse('You post it')

@api_view(['GET', 'POST'])
def light(request):
    """
    GET: Return list of lights
    POST: Create a new light
    """

    context = {}

    if request.method == 'GET':

        url = f'{BRIDGE_API}/lights'
        response = requests.get(url=url)
        context['light'] = json.loads(str(response.content, 'utf-8'))
        print(context)
        return render(request, "get_light.html", context)

    if request.method == 'POST':
        print('POST')
        return HttpResponse('You post it')

@api_view(['GET', 'PUT', 'DELETE'])
def light_id(request, id):
    """
    GET: Return info on light
    PUT: Update info about light
    DELETE: Delete light
    """

    context = {}

    if request.method == 'GET':

        url = f'{BRIDGE_API}/lights/{id}'
        response = requests.get(url=url)
        context['light'] = json.loads(str(response.content, 'utf-8'))
        context['light']['id'] = id
        print(context)
        return render(request, "get_light_id.html", context)

    if request.method == 'PUT':
        print('PUT')
        return HttpResponse('You PUT it')

    if request.method == 'DELETE':
        print('DELETE')
        return HttpResponse('You DELETE it')