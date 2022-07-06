from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from moodmuze.settings.common import BRIDGE_IP, BRIDGE_KEY
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

        url=f'http://{BRIDGE_IP}/api/{BRIDGE_KEY}/groups/'
        response = requests.get(url=url)
        context['group'] = json.loads(str(response.content, 'utf-8'))

        return render(request, "get_room.html", context)

    if request.method == 'POST':
        print('POST')
        return HttpResponse('You post it')
