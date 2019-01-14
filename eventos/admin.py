from django.contrib import admin
from .models import Evento
from .models import EventoStatus
# Register your models here.




class EventoStatusInline(admin.TabularInline):
	model = EventoStatus
	extra = 0
	can_delete = False

class EventoAdmin(admin.ModelAdmin):

	inlines = [EventoStatusInline, ]


admin.site.register(Evento, EventoAdmin)