from django.shortcuts import render
from django.http import HttpResponse
import django.db 
from django.db import connection

def rawsql(request):
	name = request.GET.get('name', '')
	cursor = connection.cursor()
	cursor.execute("SELECT temperature FROM weather.cities WHERE city_name = %s", [name])
	p = cursor.fetchone()
	return HttpResponse("this is a raw request, %s" %p)

def ormsql(request):
	name = request.GET.get('name', '')
	Entry = django.db.weather.cities
	a = Entry.objects.filter(city_name = name)
	return HttpResponse("this is an orm request %s" %a)
