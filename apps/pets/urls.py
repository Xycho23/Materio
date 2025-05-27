from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Make this the root URL
]
