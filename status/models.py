from django.db import models

# Create your models here.

from django.utils import timezone
import datetime

class Status(models.Model):

	title = models.CharField(max_length=50)
	description = models.TextField()
	color = models.CharField(max_length= 10)
	create_date = models.DateTimeField(default=timezone.now )
	active = models.BooleanField(default=True)

	@classmethod
	def get_default_status(cls):
		return cls.objects.get(pk = 1)

	class Meta:
		verbose_name_plural = 'status'


	def __str__(self):

		return self.title