from rest_framework import routers
from django.urls import include,path
from app.views import *

urlpatterns = [
    path("register/",RegisterUserView.as_view()),
    path("otp-verify/",OtpVerifyView.as_view()),
    path("update-profile/",UpdateOwnProfile.as_view()),
    path("login/",LoginView.as_view()),
    path("courses/",CourseView.as_view({"get":"list"})),
    path("courses/<pk>",SingleCourseView.as_view({"get":"retrieve"})),
    path("checkout/<pk>",Checkout.as_view()),
    path("checkout/success/",CheckoutSuccess.as_view(),name="success"),
    path("orders/",Orders.as_view({"get":"list"}),name="orders"),
    path("invoice/",InvoiceMail.as_view())
]