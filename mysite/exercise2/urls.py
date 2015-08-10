from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.rawsql, name='rawsql'),
	url(r'^orm/$', views.ormsql, name = 'ormsql'),
]
