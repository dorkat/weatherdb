from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from new_site.models import Cities, Countries
from django.template import loader


def weather_symbol(request):
    template = loader.get_template('new_site/weather_symbol_template.html')
    return HttpResponse(template.render())

def clock(request):
    template = loader.get_template('new_site/clock_template.html')
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


def map_temp(request):
    template = loader.get_template('new_site/google_map_template.html')
    return HttpResponse(template.render())


def front_page(request):
    template = loader.get_template('new_site/front_page.html')
    return HttpResponse(template.render())


def country_info(request):
    name = request.GET.get('name', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact=name).country_id
    temp_list = Cities.objects.using('weather').values_list('temperature').filter(country_id__exact = country_id)
    temp_list = sorted(temp_list)
    avg = 0.0
    for item in temp_list:
        avg += float(item[0])
    average = '%.2f'%(avg/len(temp_list) - 273.15)
    hot_city = Cities.objects.using('weather').filter(country_id__exact = country_id).order_by('temperature').last().city_name
    cold_city = Cities.objects.using('weather').filter(country_id__exact = country_id).order_by('temperature').first().city_name
    return_info = {'hottest' : hot_city, 'hottest_temp': '%.2f'%(float(temp_list[len(temp_list)-1][0]) -273.15), 'coldest' : cold_city,
                   'coldest_temp' :'%.2f'%(float(temp_list[0][0]) -273.15), 'average_temp' : average}
    return JsonResponse(return_info)


def get_country_list(request):
    country_list = list(Countries.objects.using('weather').values_list('country_full_name', flat=True).order_by('country_full_name'))
    return HttpResponse("%s" %country_list)


def get_city_list(request):
    country_name = request.GET.get('name', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact = country_name ).country_id
    city_list = list(Cities.objects.using('weather').filter(country_id__exact = country_id).values_list('city_name', flat=True).order_by('city_name'))
    return HttpResponse("%s" %city_list)