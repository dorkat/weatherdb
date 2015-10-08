from django.shortcuts import render
from django.http import HttpResponse
import django.db 
from exercise2.models import Cities, Countries, City_Temperature_Table
from django.db import connection
from django.template import loader


def rawsql(request):
    template = loader.get_template('exercise2/test.html')
    return HttpResponse(template.render())

def ormsql(request):
    temp_stats = {}
    temp_stats['count_id'] = request.GET.get('c_id', '')
    temp_stats['country_code'] = Countries.objects.using('weather').get(country_id__exact = temp_stats['count_id']).country_name
    temp_stats['country_name'] = Countries.objects.using('weather').get(country_id__exact = temp_stats['count_id']).country_full_name
    temp_list = Cities.objects.using('weather').values_list('temperature').filter(country_id__exact = temp_stats['count_id'])
    temp_list = sorted(temp_list)
    temp_stats['max_temp'] = float(temp_list[len(temp_list)-1][0]) -273.15
    temp_stats['min_temp'] = float(temp_list[0][0]) -273.15
    if len(temp_list)%2 == 0:
        temp_stats['median'] = (float(temp_list[len(temp_list)/2][0]) + float(temp_list[len(temp_list)/2-1][0]))/2 - 273.15
    else:
        temp_stats['median'] = float(temp_list[(len(temp_list)-1)/2][0]) -273.15
    avg = 0.0
    for item in temp_list:
        avg += float(item[0])
    temp_stats['avg'] = '%.3f'%(avg/len(temp_list) - 273.15)
    template = loader.get_template('exercise2/country_temp.html')
    return HttpResponse(template.render(temp_stats))


def bootry(request):
    template = loader.get_template('exercise2/bootry.html')
    return HttpResponse(template.render())


def temp_get(request):
    count_name = request.GET.get('country', '')
    cit_name = request.GET.get('city', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact = count_name ).country_id
    temperature = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact = cit_name).temperature
    humidity = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact = cit_name).humidity
    return_list = ['%.1f'%(float(temperature)-273.15), humidity]
    return HttpResponse("%s" %return_list)


def store_city_id(request):
    name = request.GET.get('name', '')
    country = request.GET.get('country', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact = country ).country_id
    c_id = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact = name).city_id
    entry = City_Temperature_Table(city_id = c_id)
    entry.save()
    return HttpResponse()


def remove_city_id(request):
    name = request.GET.get('name', '')
    country = request.GET.get('country', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact = country ).country_id
    c_id = Cities.objects.using('weather').get(country_id__exact = country_id, city_name__exact = name).city_id
    entry = City_Temperature_Table(city_id = c_id)
    entry.delete()
    return HttpResponse()


def retrieve_city_ids(request):
    ct_list = City_Temperature_Table.objects.values_list('city_id', flat=True)
    ct_list = [int(item) for item in ct_list]
    return HttpResponse("%s" %ct_list)


def retrieve_info_for_table(request):
    ct_id = request.GET.get('id', '')
    return_list = ["", "", "", ""]
    return_list[1] = Cities.objects.using('weather').get(city_id__exact = ct_id, ).city_name
    temperature = Cities.objects.using('weather').get(city_id__exact = ct_id).temperature
    return_list[2] = '%.1f'%(float(temperature) - 273.15)
    return_list[3] = Cities.objects.using('weather').get(city_id__exact = ct_id, ).humidity
    country_id = Cities.objects.using('weather').get(city_id__exact = ct_id).country_id
    return_list[0] = Countries.objects.using('weather').get(country_id__exact = country_id).country_full_name
    return HttpResponse("%s" %return_list)


def get_country_list(request):
    country_list = list(Countries.objects.using('weather').values_list('country_full_name', flat=True).order_by('country_full_name'))
    return HttpResponse("%s" %country_list)


def get_city_list(request):
    country_name = request.GET.get('name', '')
    country_id = Countries.objects.using('weather').get(country_full_name__exact = country_name ).country_id
    city_list = list(Cities.objects.using('weather').filter(country_id__exact = country_id).values_list('city_name', flat=True).order_by('city_name'))
    return HttpResponse("%s" %city_list)