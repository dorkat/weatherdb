from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from new_site.models import Cities, Countries
from django.template import loader


def weather_symbol(request):
    template = loader.get_template('new_site/weather_symbol_template.html')
    return HttpResponse(template.render())


def city_weather(request):
    name = request.GET.get('name', '')
    country = request.GET.get('country', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact=country).country_id
    temperature = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact=name).temperature
    humidity = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact=name).humidity
    clouds = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact=name).clouds
    winds = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact=name).wind_speed
    weather = {'temp' : int(float(temperature) - 273.15), 'humidity' : int(humidity), 'clouds' : int(clouds), 'wind' : float(winds)}
    return JsonResponse(weather)