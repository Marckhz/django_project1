from django.shortcuts import render
from .models import Evento
from status.models import Status as state

from .forms import CrearEventoForm
from status.forms import StatusChoiceForm
# Create your views here.



from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic  import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages


class CreateClass(CreateView, LoginRequiredMixin):
	
	login_url = 'client:login'
	template_name = 'eventos/crear_evento.html'
	model = Evento
	form_class = CrearEventoForm
	#success_url = reverse_lazy('clients:dashboard') 

	def form_valid(self, form):

		self.object = form.save( commit= False )
		self.object.user = self.request.user
		self.object.save()
		self.object.eventostatus_set.create( status = state.get_default_status() )


		return HttpResponseRedirect( self.get_url_project() )

	def get_url_project(self):
		return reverse_lazy( 'eventos:show', kwargs = {'slug':self.object.slug} )


class ClassList(ListView, LoginRequiredMixin):
	
	login_url = 'client:login'
	template_name = 'eventos/mis_proyectos.html'


	def get_queryset(self):

		return Evento.objects.filter(user = self.request.user).order_by('dead_line')


#Mostra a los usarios logeados o NO
class ShowClass(DetailView):

	model = Evento
	template_name = 'eventos/show_evento.html'


@login_required( login_url='client:login')
def edit(request, slug=''):

	evento = get_object_or_404(Evento, slug=slug)
	form = CrearEventoForm(request.POST or None, instance= evento)
	form_status = StatusChoiceForm(request.POST or None)


	if request.method == 'POST':
		if form.is_valid() and form_status.is_valid():
			selection_id = form_status.cleaned_data['status'].id

			form.save()
			evento.eventostatus_set.create( status_id = selection_id )
			message.success(request, 'datos actualizados correctamente')

	context = {
	'form':form,
	'form_status':form_status
	}

	return render(request, 'eventos/edit_evento.html', context)


