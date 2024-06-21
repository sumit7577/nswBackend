from rest_framework import routers
from django.urls import include,path
from app.views import *

urlpatterns = [
    path("register/",RegisterUserView.as_view({"post":"create"})),
    path("login/",LoginView.as_view()),
    path("checkout/<pk>",Checkout.as_view()),
    path("checkout/success/",CheckoutSuccess.as_view(),name="success")
]