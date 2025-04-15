
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from .models import *
from django.db import models
from django.urls import reverse

class Event(models.Model):
    CHOICE = (
        ('Diet', 'Diet'),
        ('Exercise', 'Exercise'),
        ('Period', 'Period'),
    )
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, default=1, null=False, choices=CHOICE)
    description = models.TextField()
    start_time = models.DateTimeField()
    # end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        if self.title!='Period':
            url = reverse('event_update', args=(self.id,))
            return f'<a href="{url}"> {self.title} </a>'
        else:
             url = reverse('event_update', args=(self.id,))
             return f'<a href="{url}" style="color: #AA336A;"> Period </a>'
    
# class Period(models.Model):
#     user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()

#     # @property
#     # def get_html_url(self):
#     #     url = reverse('event_update', args=(self.id,))
#     #     return f'<a href="{url}"> {self.title} </a>'

# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.user.username


# parent model
class forum(models.Model):
    # user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, default=1)
    description = models.CharField(max_length=1000000, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return str(self.user_id)


# child model
class Discussion(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    forum = models.ForeignKey(forum, blank=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.forum)







