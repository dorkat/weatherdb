from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import datetime
import json

def index(request):
	n = request.GET.get('name', '')
	template = loader.get_template('exercise1/index.html')
	return HttpResponse(template.render({'name': n}))	
#    return HttpResponse("hello %s" %(name)) 

def info(request):
	n = request.GET.get('name', '')
	t =str( datetime.datetime.now())
	data = {
		'name': n,
		'time': t 
		}
	return HttpResponse(json.dumps(data), content_type="application/json") 
