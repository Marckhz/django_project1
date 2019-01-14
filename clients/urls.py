from django.conf.urls import url
from . import views

from django.urls import path
from django.urls import re_path
from rest_framework import routers


app_name = 'clients'



urlpatterns = [
	


    re_path(r'show/(?P<username_url>\w+)/$', views.ShowView.as_view(), name= 'show'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('createUser/', views.Create.as_view(), name='registro'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('editPassword/', views.edit_password, name='editPassword'),
    path('edit_client/', views.edit_client, name='edit_client'),
    path('edit_social/', views.EditSocialClass.as_view(), name='edit_social'),
    path('apiClientView/', views.ApiClientView.as_view(), name='apiClientView'),
    path('hola', views.hola, name= 'hola'),
    re_path(r'ApiUserView/(?P<username>\w+)/$', views.ApiUserView.as_view(), name='ApiUserView')
]
