from django.shortcuts import render
from rest_framework import generics
from admin.serializers import *
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from app.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Func, Value, F,Count
from django.db.models.functions import Cast
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

# Create your views here.
class AdminAnalyticsViews(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request):
        return self.createResponse()

    def createResponse(self):
        user_count= CustomUser.objects.filter(is_staff=False).count()
        course_count = Course.objects.count()
        total_revenue = (
            Order.objects.filter(status="SUCCESS")
            .annotate(amount=Cast(F('order_data__amount'), output_field=models.FloatField()))
            .aggregate(total_cash=Sum('amount'))['total_cash'] or 0
        )


        today = datetime.now()
        one_year_ago = today - timedelta(days=365)

        # Per-course data
        courses = Course.objects.all()
        course_data = []
        for course in courses:
            # Aggregate total orders, unique users, and revenue for this course
            course_orders = Order.objects.filter(course=course,status="SUCCESS",order_date__gte=one_year_ago)
            course_revenue = (course_orders
                              .annotate(amount = Cast(F('order_data__amount'),output_field=models.FloatField()))
                              .aggregate(total_cash= Sum("amount"))['total_cash'] or 0
                              )
            unique_users = course_orders.values("user").distinct().count()
            total_orders = course_orders.count()

            # Monthly data for this course
            monthly_data = (
                course_orders.annotate(month=TruncMonth("order_date"))
                .values("month")
                .annotate(
                    total_orders=Count("id"),
                    total_users=Count("user", distinct=True),
                    revenue=Sum(Cast(F('order_data__amount'),output_field=models.FloatField())),
                )
                .order_by("-month")
            )

            # Format monthly data
            monthly_graph_data = [
                {
                    "month": data["month"].strftime("%m %Y"),
                    "total_orders": data["total_orders"],
                    "total_users": data["total_users"],
                    "revenue": data["revenue"],
                }
                for data in monthly_data
            ]

            # Add data for this course
            course_data.append(
                {
                    "course_name": course.name,
                    "course_id": course.id,
                    "total_orders": total_orders,
                    "total_users": unique_users,
                    "total_revenue": course_revenue,
                    "monthly_data": monthly_graph_data,
                }
            )

        return Response({"total_student": user_count,
                         "total_course": course_count,
                         "total_revenue": total_revenue,
                         "graph_data":course_data
                         },status=status.HTTP_200_OK)