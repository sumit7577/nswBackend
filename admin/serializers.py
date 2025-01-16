from rest_framework import serializers


class AdminAnalyticsSerialzier(serializers.Serializer):
    course_count = serializers.IntegerField()
    student_count = serializers.IntegerField()
    course_count = serializers.IntegerField()
    total_revenue = serializers.IntegerField()