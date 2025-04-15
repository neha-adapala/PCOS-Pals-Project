from django.urls import path
from . import views
from django.urls import include, re_path
from django.conf import settings

# Added all of the URLs which are used in this application
urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('', views.about_us, name="about_us"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    # path('main_page/', views.main_page, name="main_page"),
    # re_path(r'^insert$', views.insert, name='insert')

    # path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('addInForum/', views.addInForum, name='addInForum'),
    path('addInDiscussion/', views.addInDiscussion, name='addInDiscussion'),
    path('addInDiscussion/', views.addInDiscussion, name='addInDiscussion'),
    path('points/', views.points, name='points'),
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event_insert/', views.event_insert, name='event_insert'),
    # path('period_insert/', views.period_insert, name='period_insert'),
    path('event_update/<str:pk>/', views.event_update, name="event_update"),
	#re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('quiz/', views.quiz, name='quiz'),
    path('info/', views.info, name='info'),
    path('about_us/', views.about_us, name='about_us'),

]
