from .views import *
from . import views
from django.urls import path

app_name = "newsletter"

urlpatterns = [
    path('subscribe/', views.newsletter_subscribe, name='subscribe'),
    path('unsubscribe/' , views.newsletter_unsubscribe , name='unsubscribe') ,
   
]
