from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User   #adding the user model auth table that django created for us using the admin login
from django.urls import reverse     #returns the full url to that route as a string and lets the view handle the redirect

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)  #, a ForeignKey is a field used to create a many-to-one relationship between two models in a database.
	likes = models.ManyToManyField(User, related_name='liked_posts')
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

	def __str__(self):   #dunder -> double underscore method (magic methods)
		return self.title


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user} likes {self.post.title}"


class Comment(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
	user = models.CharField(max_length=100)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)