from django.conf.urls import patterns, url
from submission import views

urlpatterns = patterns('',
		url(r'^$', views.list, name='list'),
		url(r'^new$', views.create, name='create'),
		url(r'^delete$', views.delete, name='delete'),
	)
