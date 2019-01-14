from django.conf.urls import url
from . import views
from django.urls import path, re_path


app_name = 'eventos'

urlpatterns = [
	
	re_path(r'^edit/(?P<slug>[\w]+)$', views.edit, name='edit'),
	re_path(r'^show/(?P<slug>[\w]+)$', views.ShowClass.as_view(), name='show'),
	path('crear_evento/', views.CreateClass.as_view(), name='crear_evento'),
	path('mis_eventos/', views.ClassList.as_view(), name='mis_eventos')
		
]