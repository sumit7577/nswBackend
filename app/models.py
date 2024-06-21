from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.utils.translation import gettext_lazy as _
from app.manager import CustomManager



# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to="people",null=True,blank=True)
    email = models.EmailField(_("email address"), blank=False,unique=True,null=False)
    phone = models.CharField(max_length=10,blank=False,null=False,unique=True)
    objects = CustomManager()


class Course(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False)
    description = models.TextField(max_length=10000,blank=False,null=False)
    students = models.ManyToManyField(to=CustomUser,related_name="students")
    starting_date = models.DateField(default=timezone.now())
    teaching_time_start = models.DateTimeField(null=True,blank=True)
    teaching_time_end = models.DateTimeField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    image = models.ImageField(upload_to="course")

    def __str__(self) -> str:
        return self.name



class Order(models.Model):
    keys = (("FAILED","FAILED"),
            ("PENDING","PENDING"),
            ("SUCCESS","SUCCESS"))
    course = models.ForeignKey(to=Course,blank=False,null=False,on_delete=models.CASCADE)
    user  = models.ForeignKey(to=CustomUser,blank=False,null=False,on_delete=models.CASCADE)
    order_data = models.JSONField(blank=False,null=False)
    status = models.CharField(choices=keys,null=False,blank=False,max_length=100,default="PENDING")
    payment_id = models.CharField(null=True,blank=True,max_length=200)
    order_id = models.CharField(null=True,blank=True,max_length=200)
    signature = models.CharField(null=True,blank=True,max_length=200)

    def __str__(self) -> str:
        return self.user.username
