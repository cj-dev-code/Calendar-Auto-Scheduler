"""project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from . import views

app_name = 'calendarauto'
urlpatterns = [
    path('', views.CalendarView, name='temp_view'),
<<<<<<< HEAD
    path('<int:year>/<int:month>/<int:day>/', views.CalendarView, name='calendar_view'),
=======
    path('<int:year>/<int:month>/week/<int:week>/', views.CalendarView, name='calendar_view'),
>>>>>>> 83fb07511f767675616159fd872ed54bc1d62e6e
    path('', views.CalendarView, name='calendar'), # Assume right now aliu doesn't use a generic view
    path('Todo', views.TodoView, name='todo'),
    #path('Mystery', views.MysteryView, name='mystery'),
]
