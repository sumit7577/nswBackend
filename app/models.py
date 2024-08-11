from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.utils.translation import gettext_lazy as _
from app.manager import CustomManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from app.utils import *
import pyotp


totp = pyotp.TOTP('veryhardpass',interval=60)


# Create your models here.
class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True
    )
    image = models.ImageField(upload_to="people",null=True,blank=True)

    email = models.EmailField(_("email address"), blank=False,
                              unique=True,null=False)

    phone = models.CharField(max_length=10,blank=False,
                             null=False,
                             unique=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = CustomManager()

class Otp(models.Model):
    otp = models.CharField(blank=False,null=False,max_length=6,unique=True)
    email = models.EmailField(_('email address'))
    phone = models.CharField(max_length=20)
    password = models.CharField(_("password"), max_length=128)
    created_at = models.DateTimeField(default=timezone.now())

    class Meta:
        get_latest_by = "id"

    def __str__(self):
        return self.otp

class Sessions(models.Model):
    name = models.CharField(max_length=400,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now())
    gdrive_link = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self) -> str:
        return self.gdrive_link

BATCH_TYPE = (
    ("Regular","Regular"),
    ("Weekend","Weekend")
)

class Course(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False)
    batch_type = models.CharField(choices=BATCH_TYPE,max_length=30,null=False,blank=False)
    description = models.TextField(max_length=10000,blank=False,null=False)
    students = models.ManyToManyField(to=CustomUser,related_name="students",null=True,blank=True)
    starting_date = models.DateField(default=timezone.now())
    ending_date = models.DateField(blank=False,null=False)
    teaching_time_start = models.DateTimeField(null=True,blank=True)
    teaching_time_end = models.DateTimeField(null=True,blank=True)
    registration_fees = models.IntegerField(null=True,blank=True)
    image = models.ImageField(upload_to="course")
    recording_sessions= models.ManyToManyField(to=Sessions,null=True,blank=True)
    refunded = models.BooleanField(null=False,blank=False,default=False)

    def __str__(self) -> str:
        return self.name

INSTALLMENT_CHOICES = (
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("6","6"),
    ("7","7")
)

class Installment(models.Model):
    course = models.ForeignKey(to=Course,blank=False,null=False,on_delete=models.CASCADE)
    user  = models.ManyToManyField(to=CustomUser,blank=True,null=True)
    date = models.DateTimeField(default=timezone.now())
    price = models.IntegerField(null=True,blank=True)
    installment_number = models.CharField(choices=INSTALLMENT_CHOICES,null=False,blank=False,max_length=100)
    paid = models.BooleanField(default=False,null=False,blank=False)

    def __str__(self) -> str:
        return self.course.name
    

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
