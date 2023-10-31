from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User   #adding the user model auth table that django created for us using the admin login


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)  #, a ForeignKey is a field used to create a many-to-one relationship between two models in a database.

	def __str__(self):   #dunder -> double underscore method (magic methods)
		return self.title