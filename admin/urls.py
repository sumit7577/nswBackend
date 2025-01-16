from rest_framework import routers
from django.urls import include,path
from admin.views import *

urlpatterns = [
    path("home/",AdminAnalyticsViews.as_view()),
]