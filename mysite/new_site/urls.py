from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^weather_symbol/$', views.weather_symbol, name='weather_symbol'),
    url(r'^city_weather/$', views.city_weather, name="city_weather"),
    url(r'^map_template/$', views.map_temp, name="map_temp"),
    url(r'^clock/$', views.clock, name="clock"),
    url(r'^home/$', views.front_page, name="front_page"),
    url(r'^country_info/$', views.country_info, name="country_info"),
    url(r'country_list/$', views.get_country_list, name='get_country_list'),
    url(r'city_list/$', views.get_city_list, name='get_city_list')
]