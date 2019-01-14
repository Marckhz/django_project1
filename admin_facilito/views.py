from django.shortcuts import render


""""

Aqui se encuentran las vistas
que le pertenecen a la pagina.

"""




def home(request):

	context = {}

	return render(request, 'home.html', context)



def error_404(request):

	context = {}

	return render(request, 'error_404.html', context)