from django.contrib.auth.models import User
from .models import Client
from. models import SocialNetwork


from rest_framework import generics
from . import serializers

import requests

from django.shortcuts import render
from django.http import HttpResponse

from .formularios import LoginForm 
from .formularios import createUserForm 
from .formularios import EditUserForm 
from .formularios import EditPasswordForm
from .formularios import EditClientForm
from .formularios import EditSocialNetwork




from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as loginDjango
from django.contrib.auth import logout as logoutDjango
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response


from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . serializers import ClientSerializer, UserSerializer
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt



"""Create your views here."""



class ApiUserView(APIView):

  login_url = 'clients:login'
  def get(self, request,username):

    user = User.objects.get(username=self.request.user)
    user_json = UserSerializer(user)
    print(user_json)
    return Response(user_json.data)



class ApiClientView(APIView):
  def get(self, request):

    user = Client.objects.all()
    user_json = ClientSerializer(user, many=True)
    return Response(user_json.data)


class ShowView(DetailView):
  model = User
  template_name = 'client/show.html'
  slug_field = 'username' #Que campo de la base de datos
  slug_url_kwarg = 'username_url' #Que atributo de la url

class LoginView(View):
  form = LoginForm()
  message = None
  template = 'client/login.html'

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('clients:dashboard')
      
    return render(request, self.template, self.get_context() )


  def post(self, request, *args, **kwargs):

    #si envian el formulario
    username_post = request.POST.get('username')
    password_post = request.POST.get('password')


    print("tu usuario es: ", username_post)
    print("tu password es: ", password_post) 

    user = authenticate(username = username_post, password = password_post)

    

    if user is not None:
      loginDjango(request, user)
      print("welcome")
      return redirect('clients:dashboard')
      
    else:
      self.message = "Username or password incorrect"


    return render(request, self.template, self.get_context() )



  def get_context(self):
    return {'form': self.form, 'message':self.message}



class DashboardView(LoginRequiredMixin, View):

  
  login_url = 'clients:login'
  def get(self, request, *args, **kwargs):    

    context = {
    }
    

    return render(request, 'client/dashboard.html', context)

  
class Create(CreateView):
  
  template_name = 'client/createUser.html'
  model = User
  form_class = createUserForm
  success_url = reverse_lazy('clients:login')
    
  def form_valid(self, form):
    #encargado de guardar la entidad
    self.object = form.save( commit=False)
    self.object.set_password( self.object.password )
    self.object.save()

    return HttpResponseRedirect( self.get_success_url() )



def logout(request):
	logoutDjango(request)
	error = None
	if error == None:
		print("yay it works")
	else:
		print("found error")


	return redirect("clients:login")




class Edit(UpdateView):
  model = User
  template_name = 'client/edit.html'
  success_url = reverse_lazy('clients:dashboard')
  form_class= EditUserForm

  def get_object(self, queryset = None):
    return self.request.user


class EditSocialClass(UpdateView, LoginRequiredMixin):

  login_url = 'client:login'
  model = SocialNetwork
  template_name = 'client/edit_social.html'
  success_url = reverse_lazy('clients:edit_social')
  form_class = EditSocialNetwork
  succes_message = 'yay funciona'

  def get_object(self, queryset =None):
    return self.get_social_instance()

  def get_social_instance(self):
    try:
      return self.request.user.socialnetwork
    except:
      return SocialNetwork(user = self.request.user)






""" Funciones """

@login_required ( login_url = 'clients:login')
def hola(request):

  context = {}

  return render(request, 'client/hola.html', context)

@login_required ( login_url = 'clients:login')
def edit_social(request):

  form = EditSocialNetwork ( request.POST or None)
  
  if ( request.method == 'POST'):
    
    if ( form.is_valid() ):
      print("it works")

      form.save()
      messages.success(request, 'hi there it works')

  context =  {

    'form':form
  }

  return render( request, 'edit_social.html', context )

"""
@login_required ( login_url = 'clients:login' )
def create_evento(request):

    form = EventoForm( request.POST or None ) 

    if request.method =='POST':
      if form.is_valid():
        print('yay evento creado')
        form.save()
        messages.success(request, 'hi there it works')
        #return redirect("client:hola")

    context = {
      'form':form
    }

    return render(request, 'client/crear_evento.html', context)
"""

@login_required ( login_url = 'clients:login' )
def edit_password(request):

  form = EditPasswordForm(request.POST or None)


  if(request.method =='POST'):

    if (form.is_valid()):

      print("formulario valido")
      current_password = form.cleaned_data.get('password')
      new_password = form.cleaned_data.get('new_password')

      if authenticate(username = request.user.username,  password = current_password):
        request.user.set_password( new_password)
        request.user.save()

        update_session_auth_hash( request, request.user )
        message ='Password actualizado'

  context = {

    'form':form
   
  }  
  return render(request, 'client/editPassword.html', context)


@login_required ( login_url = 'clients:login' )
def edit_client(request):
  
  form_client = EditClientForm( request.POST or None,  instance = client_instance(request.user) )
  form_user = EditUserForm( request.POST or None, instance = request.user )
 
  if(request.method =='POST'):
    if( form_user.is_valid() and form_client.is_valid() ):
      print('formulario valido')
      form_user.save()
      form_client.save()
      messages.success(request, 'datos actualizados correctament')

  context = {
  'form_client':form_client,
  'form_user' : form_user
  }
  return render(request, 'client/edit_client.html', context)



@login_required( login_url = 'clients:login')
def edit_evento(request):
  pass

def client_instance(user):
  try:
    return user.client
  except:
    return Client(user = user)




