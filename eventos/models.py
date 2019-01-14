from django.db import models

# Create your models here.

from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError

from status.models import Status
from django.utils import timezone



class Evento(models.Model):


	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)
	description = models.TextField(max_length= 300)
	dead_line = models.DateField()
	create_date = models.DateField(default = datetime.date.today)
	slug = models.CharField(max_length=50, default='')


	def __str__(self):


		return self.title


	def validate_unique(self, exclude=None):
		if Evento.objects.filter(title=self.title).exists():
			raise ValidationError("el proyecto ya existe")



	def save(self, *args, **kwargs):

		self.validate_unique()
		self.slug = self.title.replace(' ', '_').lower()
		super(Evento, self).save(*args, **kwargs)


class EventoStatus(models.Model):


	eventos = models.ForeignKey(Evento, on_delete=models.CASCADE )
	status = models.ForeignKey(Status, on_delete=models.CASCADE)
	create_date = models.DateTimeField(default = timezone.now )