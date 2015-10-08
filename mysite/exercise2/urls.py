from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.rawsql, name='rawsql'),
    url(r'^orm/$', views.ormsql, name='ormsql'),
    url(r'^bootry/$', views.bootry, name='bootry'),
    url(r'^temp/$', views.temp_get, name='temp_get'),
    url(r'store/$', views.store_city_id, name='store_city_id'),
    url(r'remove/$', views.remove_city_id, name='remove_city_id'),
    url(r'retrieve/$', views.retrieve_city_ids, name='retrieve_city_ids'),
    url(r'info/$', views.retrieve_info_for_table, name='retrieve_info_for_table'),
    url(r'country_list/$', views.get_country_list, name='get_country_list'),
    url(r'city_list/$', views.get_city_list, name='get_city_list')
]
