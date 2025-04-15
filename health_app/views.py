from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .models import Blog
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.db import IntegrityError

from .models import *
from .utils import Calendar
from .forms import EventForm

# The code below is to display the User Registration Page and capture the details in the database
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'features/register.html', context)

# The code below is to display the User Login Page and do validations as well
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'features/login.html', context)

# The code below is to allow the user to logout
def logoutUser(request):
    logout(request)
    return redirect('login')

def quiz(request):
    return render(request, 'features/quiz.html')


# @login_required(login_url='login')
# def main_page(request):
#     blog_rows = Blog.objects.all()
#
#     context = {'blog_data': blog_rows}
#     return render(request, 'travel/main_page.html', context)
#
# @login_required(login_url='login')
# def insert(request):
#     blog_record = Blog(name=request.POST['name'], topic=request.POST['topic'], description=request.POST['description'])
#     blog_record.save()
#     return redirect('/')


from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.

def home(request):
    forums = forum.objects.all()
    count = forums.count()
    discussions = []
    for i in forums:
        discussions.append(i.discussion_set.all())

    context = {'forums': forums,
               'count': count,
               'discussions': discussions}
    return render(request, 'features/home.html', context)

@login_required(login_url='login')
def addInForum(request):
    
    error_message = ""
    forum_form = CreateInForum(user_id=request.user.id)
    if request.method == 'POST':
        forum_form = CreateInForum(request.POST, user_id=request.user.id)
        try:
            if forum_form.is_valid():
                # forum_form.save()
                obj1 = forum_form.save(commit=False)
                obj1.user_id = User.objects.get(id=request.user.id)
                obj1.save()
                forum_form = CreateInForum(user_id=request.user.id)
                # forum_form.description = forms.CharField(widget=forms.Textarea)
                return redirect('/')
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                error_message = "This Event ID Is Already Used By You"
    context = {'forum_form': forum_form, 'error_message': error_message}
    return render(request, 'features/addInForum.html', context)

# def new(request):
#      return render(request,"features/addInForum.html", {
#         "create_forum": CreateInForum()
#      })

@login_required(login_url='login')
def addInDiscussion(request):
    error_message = ""
    discussion_form = CreateInDiscussion(user_id=request.user.id)
    if request.method == 'POST':
        discussion_form = CreateInDiscussion(request.POST, user_id=request.user.id)
        try:
            if discussion_form.is_valid():
                obj2 = discussion_form.save(commit=False)
                obj2.user_id = User.objects.get(id=request.user.id)
                obj2.save()
                discussion_form = CreateInDiscussion(user_id=request.user.id)
                return redirect('/')
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                error_message = "This Event ID Is Already Used By You"
    context = {'discussion_form': discussion_form, 'error_message': error_message}
    return render(request, 'features/addInDiscussion.html', context)


# @login_required(login_url='login')
# def addInDiscussion(request):
#     discussion_form = CreateInDiscussion()
#     if request.method == 'POST':
#         form = CreateInDiscussion(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context = {'discussion_form': form}
#     return render(request, 'features/addInDiscussion.html', context)

from django.shortcuts import render
from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie

@login_required(login_url='login')
def points(request):

    forums = forum.objects.all()
    count = forums.count()
    discussions = []

    context = {'forums': forums,
               'count': count,
               'discussions': discussions}
    return render(request, 'features/points.html', context)


def info(request):
    return render(request, 'features/information.html')


def about_us(request):
    return render(request, 'features/aboutUs.html')

def index(request):
    return HttpResponse('hello')


class CalendarView(generic.ListView):
    model = Event
    template_name = 'features/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user_id = self.request.user.id
        cal = Calendar(d.year, d.month, user_id)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# def event(request, event_id=None):
#     instance = Event()
#     if event_id:
#         # instance = get_object_or_404(Event, pk=event_id)
#         instance = event_update(request)
#     else:
#         # instance = Event()
#         instance = event_insert(request)

#     form = EventForm(request.POST or None, instance=instance)
#     if request.POST and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('calendar'))
#     return render(request, 'features/event.html', {'form': form})

@login_required(login_url='login')
def event_insert(request):
    eventlist = Event.objects.filter(user_id=request.user.id)
    error_message = ""
    form = EventForm(user_id=request.user.id)
    if request.method == "POST":
        form = EventForm(request.POST, user_id=request.user.id)
        try:
            if form.is_valid():
                #form.save()
                obj = form.save(commit=False)
                obj.user_id = User.objects.get(id=request.user.id)
                obj.save()
                form = EventForm(user_id=request.user.id)
                return HttpResponseRedirect(reverse('calendar'))
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                error_message = "This Event ID Is Already Used By You"

    context = {'event_form': form, 'eventlist': eventlist, 'error_message': error_message}
    return render(request, 'features/event.html', context)

@login_required(login_url='login')
def event_update(request, pk):

    event = Event.objects.get(id=pk,user_id=request.user.id)

    eventlist = Event.objects.filter(user_id=request.user.id)
    form = EventForm(instance=event, user_id=request.user.id)
    if request.method == "POST":
        print(f"pk: {pk}, Update Event: {event}")
        form = EventForm(request.POST, instance=event, user_id=request.user.id)
        if form.is_valid():
            form.save()
            form = EventForm(user_id=request.user.id)
            return HttpResponseRedirect(reverse('calendar'))

    context = {'event_form': form, 'eventlist': eventlist}
    return render(request, 'features/event.html', context)

# @login_required(login_url='login')
# def period_insert(request):
#     periodlist = Period.objects.filter(user_id=request.user.id)
#     error_message = ""
#     form = PeriodTrack(user_id=request.user.id)
#     if request.method == "POST":
#         form = PeriodTrack(request.POST, user_id=request.user.id)
#         try:
#             if form.is_valid():
#                 #form.save()
#                 obj = form.save(commit=False)
#                 obj.user_id = User.objects.get(id=request.user.id)
#                 obj.save()
#                 form = PeriodTrack(user_id=request.user.id)
#                 return HttpResponseRedirect(reverse('calendar'))
#         except IntegrityError as e:
#             if 'UNIQUE constraint' in str(e.args):
#                 error_message = "This Event ID Is Already Used By You"

#     context = {'period_form': form, 'eventlist': periodlist, 'error_message': error_message}
#     return render(request, 'features/event.html', context)

