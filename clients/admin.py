from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import Client
from .models import SocialNetwork



# Register your models here.



class ClientAdmin(admin.ModelAdmin):
	exclude = ('user',)

class ClientInLine(admin.StackedInline):
	model = Client
	can_delete = False



class SocialInLine(admin.StackedInline):
	model = SocialNetwork
	can_delete = False



class UserAdmin(AuthUserAdmin):
	inlines = [ClientInLine, SocialInLine]



#admin.site.register(Client)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
