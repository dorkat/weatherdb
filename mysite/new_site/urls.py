from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^weather_symbol/$', views.weather_symbol, name='weather_symbol'),
    url(r'^city_weather/$', views.city_weather, name="city_weather"),
    url(r'^map_template/$', views.mao_temp, name="map_temp")
]