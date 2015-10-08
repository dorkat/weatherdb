from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import datetime
import json
from exercise1.models import greeting

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

def ormsql(request):
	n = request.GET.get('pk', '')
	a = greeting.objects.get(greet_text = n)
	b = greeting.objects.values_list('name')
	c = greeting.objects.filter(name='a')
	return HttpResponse("this is an orm request, %s - %s - %s" %(a, len(b), c)) 
