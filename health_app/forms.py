from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django import forms
from django.forms import ModelForm, DateInput
from health_app.models import Event
from django.db import models
from django.urls import reverse

class UploadFileForm(forms.Form):
    file = forms.FileField()

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class CreateInForum(ModelForm, forms.Form):
	class Meta:
		model = forum
		
		exclude = ['user_id']
		description = forms.CharField(widget=forms.Textarea)
		widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
		# fields = ['title', 'description']
	def __init__(self, *args, **kwargs):
		user_id = kwargs.pop('user_id')
		super(CreateInForum, self).__init__(*args, **kwargs)
		self.fields["description"].widget.attrs.update(size="40")
	
# class EditForum(forms.Form):
#     title = forms.CharField(widget=forms.Textarea)
#     description = forms.CharField(widget=forms.Textarea)

# class CreateInDiscussion(ModelForm):
# 	class Meta:
# 		model = Discussion
# 		fields = "__all__"

class CreateInDiscussion(ModelForm):
	class Meta:
		model = Discussion
		exclude = ['user_id']
		discuss = forms.CharField(widget=forms.Textarea)
		widgets = {
            'discuss': forms.Textarea(attrs={'rows': 3}),
        }
		# fields = "__all__"
	def __init__(self, *args, **kwargs):
		user_id = kwargs.pop('user_id')
		super(CreateInDiscussion, self).__init__(*args, **kwargs)
		self.fields["discuss"].widget.attrs.update(size="40")

from django import forms

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['user_id']
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            # 'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
		
        #fields = '__all__'

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        # self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

# class PeriodTrack(ModelForm):
#     class Meta:
#         model = Period
#         exclude = ['user_id']
#         # datetime-local is a HTML5 input type, format to make date time show on fields
#         widgets = {
#             'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
#             'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
#         }
		
        #fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     user_id = kwargs.pop('user_id')
    #     super(EventForm, self).__init__(*args, **kwargs)
    #     # input_formats parses HTML5 datetime-local input to datetime field
    #     self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    #     self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

